"""
SeaVoice Speech SDK v2

Descriptions:
To connect to SeaVoice STT server to finish speech recognizing and synthesizing work.
"""

import asyncio
import base64
import contextlib
import functools
import json
import logging
from types import TracebackType
from typing import Any, AsyncIterator, Callable, Coroutine, Optional, Type, TypeVar, Union

from typing_extensions import Awaitable, ParamSpec
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK, InvalidURI, WebSocketException
from websockets.legacy.client import WebSocketClientProtocol, connect

from seavoice_sdk.events import BaseEvent, InfoEvent, RecognizedEvent, RecognizingEvent, SpeechStatus, raw_data_to_event
from seavoice_sdk.exceptions import *
from seavoice_sdk.logger import get_logger

RT = TypeVar("RT")
Param = ParamSpec("Param")


class SpeechRecognizer:
    def __init__(
        self,
        token: str,
        language: str,
        sample_rate: int,
        enable_itn: bool,
        enable_punctuation: bool,
        contexts: dict,
        context_score: int,
        stt_endpoint_url: str,
        logger: Optional[logging.Logger] = None,
        stt_server_id: Optional[str] = None,
        send_chunk_interval: float = 0.05,
        retry_max: int = 3,
    ) -> None:
        self.token = token
        self.language = language
        self.sample_rate = sample_rate
        self.bytes_per_sample = 2
        self.channel = 1
        self.enable_itn = enable_itn
        self.enable_punctuation = enable_punctuation
        self.contexts = contexts
        self.context_score = context_score
        self.stt_endpoint_url = stt_endpoint_url
        self.stt_server_id = stt_server_id
        self.send_chunk_interval = send_chunk_interval
        self.websocket: WebSocketClientProtocol
        self.logger = logger or get_logger()
        self.retry_max = retry_max
        self.retry_count = 0

        self.send_chunk_interval = 0.02
        self._last_exec: BaseException
        self._error_raised = asyncio.Event()

        self._lock = asyncio.Lock()
        self._send_task: asyncio.Task
        self._send_queue = asyncio.Queue()
        self._recv_task: asyncio.Task
        self._recv_queue = asyncio.Queue()
        self._retry_bg_tasks: asyncio.Task
        self._segment_id_offset: int = 0
        self._recv_segment_id: int = 0
        self._sent_bytes_total: int = 0
        self._sent_bytes: int = 0
        self._voice_start_offset: float = 0
        self._base_sleep_time = 2

    @property
    def chunk_size(self) -> int:
        return int(self.sample_rate * self.bytes_per_sample * self.channel * self.send_chunk_interval)

    def update_recognition_status(self) -> None:
        self._voice_start_offset = self._sent_bytes / (self.sample_rate * self.bytes_per_sample * self.channel)
        self._sent_bytes = 0
        self._segment_id_offset = self._recv_segment_id + 1
        self._recv_segment_id = 0

    async def __aenter__(self) -> "SpeechRecognizer":
        await self._init_connection()
        if self._error_raised.is_set():
            raise self._last_exec
        self._send_task = asyncio.create_task(self._send_from_queue())
        self._recv_task = asyncio.create_task(self._recv_to_queue())
        self._retry_bg_tasks = asyncio.create_task(self._retry_bg_send_and_recv())
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        self._send_task.cancel()
        self._recv_task.cancel()
        self._retry_bg_tasks.cancel()
        with contextlib.suppress(BaseException):
            await self.websocket.close()
        return exc_type == ClosedException

    async def _init_connection(self):
        async with self._lock:
            if self._error_raised.is_set():
                self.logger.error(f"speech-to-text: {id(self)}-{self.retry_count} has error raised")
                return

            base_sleep_time = self._base_sleep_time
            while self.retry_count <= self.retry_max:
                try:
                    self.websocket = await _get_wrapped_ws(self.stt_endpoint_url)
                    return await self._authentication()
                except UnExpectedClosedException as error:
                    self._last_exec = error
                    self.retry_count += 1
                    await asyncio.sleep(base_sleep_time)
                    base_sleep_time = base_sleep_time**2
                except BaseException as error:
                    self._last_exec = error
                    self.logger.error(f"speech-to-text: {id(self)}-{self.retry_count} raise {error}")
                    self._error_raised.set()
                    return

            self.logger.error(f"speech-to-text: {id(self)}-{self.retry_count} has too many UnExpectedClosedException")
            self._error_raised.set()

    async def _retry_bg_send_and_recv(self):
        while True:
            await asyncio.wait([self._send_task, self._recv_task], return_when=asyncio.FIRST_COMPLETED)
            # maybe is soft closing
            if self._send_task.cancelled():
                self.logger.info(f"speech-to-text: {id(self)}-{self.retry_count} send_task is canceled due to _soft_close")
                return

            send_exec = _get_task_result(self._send_task)
            recv_exec = _get_task_result(self._recv_task)

            self.logger.info(
                f"speech-to-text: {id(self)}-{self.retry_count} got "
                f"send_task exception: {send_exec} recv_task exception: {recv_exec}"
            )
            # stop if there is an non unexpected exception
            if not (isinstance(recv_exec, UnExpectedClosedException) or isinstance(send_exec, UnExpectedClosedException)):
                last_exec = recv_exec or send_exec
                assert last_exec is not None
                self._last_exec = last_exec
                self.logger.info(f"speech-to-text: {id(self)}-{self.retry_count} close due to {self._last_exec}")
                self._error_raised.set()
                return

            self.logger.info(
                f"speech-to-text: {id(self)}-{self.retry_count} start create new connection"
                " because UnExpectedClosedException happened"
            )
            if not self._recv_task.done():
                self.logger.info(
                    f"speech-to-text: {id(self)}-{self.retry_count} wait recv_task done because UnExpectedClosedException "
                    "means recv_task is going to stop"
                )
                recv_exec = await _wait_task_result(self._recv_task)
            if not self._send_task.done():
                self.logger.info(
                    f"speech-to-text: {id(self)}-{self.retry_count} wait send_task done because UnExpectedClosedException "
                    "means send_task is going to stop"
                )
                send_exec = await _wait_task_result(self._send_task)

            self.update_recognition_status()
            last_exec = recv_exec or send_exec
            assert last_exec is not None
            self._last_exec = last_exec
            await self._init_connection()
            if self._error_raised.is_set():
                self.logger.error(f"speech-to-text: {id(self)}-{self.retry_count} close because error_raised is set")
                return

            self.logger.info(f"speech-to-text: {id(self)}-{self.retry_count} new connection created")
            self._send_task = asyncio.create_task(self._send_from_queue())
            self._recv_task = asyncio.create_task(self._recv_to_queue())

    async def change_language(self, language: str) -> None:
        self.logger.info(f"speech-to-text: {id(self)}-{self.retry_count} start change_language")
        if self._error_raised.is_set():
            raise self._last_exec
        if self.language == language:
            self.logger.info(f"speech-to-text: {id(self)}-{self.retry_count} passed if the language is the same")
            return

        await self._soft_close()
        self.language = language
        await self._init_connection()
        if self._error_raised.is_set():
            self.logger.error(f"speech-to-text: {id(self)}-{self.retry_count} error raised after _init_connection")
            raise self._last_exec

        self.logger.info(f"speech-to-text: {id(self)}-{self.retry_count} create new connection successfully")
        self._send_task = asyncio.create_task(self._send_from_queue())
        self._recv_task = asyncio.create_task(self._recv_to_queue())
        self._retry_bg_tasks = asyncio.create_task(self._retry_bg_send_and_recv())

    async def _soft_close(self):
        self.logger.info("wait until all data sent")
        queue_done = asyncio.create_task(self._send_queue.join())
        await asyncio.wait([queue_done, self._send_task], return_when=asyncio.FIRST_COMPLETED)
        if queue_done.done():
            self.logger.info("all data sent")
            self._send_task.cancel()
        else:
            self.logger.info("some error raised during waiting")
            queue_done.cancel()

        with contextlib.suppress(BaseException):
            await self.websocket.send(self._send_handler({"command": "stop"}))
        with contextlib.suppress(BaseException):
            await asyncio.wait_for(self._recv_task, 5)
        self.update_recognition_status()
        with contextlib.suppress(BaseException):
            await self.websocket.close()

    async def _authentication(self):
        try:
            await self.websocket.send(
                self._send_handler(
                    {
                        "command": "authentication",
                        "payload": {
                            "token": self.token,
                            "settings": {
                                "language": self.language,
                                "sample_rate": self.sample_rate,
                                "itn": self.enable_itn,
                                "punctuation": self.enable_punctuation,
                                "contexts": self.contexts,
                                "context_score": self.context_score,
                                "stt_server_id": self.stt_server_id,
                            },
                        },
                    }
                )
            )
        except BaseException as e:
            raise AuthenticationFail(message=f"send auth command fails, error: {e}")

        try:
            event = self._recv_handler(await self.websocket.recv())
        except BaseException as e:
            raise AuthenticationFail(message=f"receive and parse event fails, error: {e}")

        if not isinstance(event, InfoEvent) or event.payload.status != SpeechStatus.BEGIN:
            raise AuthenticationFail(message=f"receive unexpected event: {event}")

        self._recv_queue.put_nowait(event)

    async def recv(self) -> BaseEvent:
        recv = asyncio.create_task(self._recv_queue.get())
        error = asyncio.create_task(self._error_raised.wait())
        await asyncio.wait([recv, error], return_when=asyncio.FIRST_COMPLETED)

        if recv.done():
            error.cancel()
            return recv.result()

        raise self._last_exec

    def send(self, audio_data) -> None:
        if self._error_raised.is_set():
            raise self._last_exec
        for i in range(0, len(audio_data), self.chunk_size):
            self._send_queue.put_nowait(audio_data[i : i + self.chunk_size])

    def finish(self) -> None:
        self._send_queue.put_nowait({"command": "stop"})

    async def stream(self) -> AsyncIterator[BaseEvent]:
        while True:
            try:
                yield (await self.recv())
            except ClosedException:
                return
            except BaseException as e:
                raise e

    async def _send_from_queue(self) -> None:
        while True:
            data = await self._send_queue.get()
            try:
                await self.websocket.send(self._send_handler(data))
            finally:
                self._send_queue.task_done()
            await asyncio.sleep(self.send_chunk_interval)

    async def _recv_to_queue(self) -> None:
        while True:
            self._recv_queue.put_nowait(self._recv_handler(await self.websocket.recv()))

    def _recv_handler(self, data: Union[str, bytes]) -> BaseEvent:
        event = raw_data_to_event(**json.loads(data))
        if isinstance(event, RecognizingEvent) or isinstance(event, RecognizedEvent):
            self._recv_segment_id = event.payload.segment_id
            event.payload.segment_id += self._segment_id_offset
            event.payload.voice_start_time += self._voice_start_offset
            for word_aliment in event.payload.word_alignments:
                word_aliment.start += self._voice_start_offset
        return event

    def _send_handler(self, data):
        if isinstance(data, bytes):
            self._sent_bytes += len(data)
            return json.dumps(
                {
                    "command": "audio_data",
                    "payload": base64.b64encode(data).decode(),
                }
            )
        return json.dumps(data)


def _get_task_result(task: asyncio.Task) -> Optional[BaseException]:
    try:
        return task.result() if task.done() else None
    except BaseException as e:
        return e


async def _wait_task_result(task: Awaitable[RT]) -> Union[BaseException, RT]:
    try:
        return await task
    except BaseException as e:
        return e


def _ws_wrapper(func: Callable[Param, Coroutine[Any, Any, RT]]) -> Callable[Param, Coroutine[Any, Any, RT]]:
    @functools.wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> RT:
        try:
            return await func(*args, **kwargs)
        except InvalidURI as e:
            raise InvalidURI(exception=e)
        except ConnectionClosedOK as e:
            raise ClosedException(exception=e)
        except ConnectionClosed as e:
            raise UnExpectedClosedException(exception=e)
        except WebSocketException as e:
            raise InternalError(exception=e)
        except BaseException as e:
            raise e

    return wrapped


_connect = _ws_wrapper(connect)  # type: ignore


async def _get_wrapped_ws(url: str) -> WebSocketClientProtocol:
    websocket: WebSocketClientProtocol = await _connect(url)
    websocket.send = _ws_wrapper(websocket.send)
    websocket.recv = _ws_wrapper(websocket.recv)
    websocket.close = _ws_wrapper(websocket.close)

    return websocket
