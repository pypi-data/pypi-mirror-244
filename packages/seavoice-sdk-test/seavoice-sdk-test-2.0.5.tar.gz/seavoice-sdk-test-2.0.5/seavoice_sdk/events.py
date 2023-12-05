from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar, List

from seavoice_sdk.exceptions import InvalidEvent


class SpeechEvent(str, Enum):
    INFO = "info"
    RECOGNIZING = "recognizing"
    RECOGNIZED = "recognized"


class SpeechStatus(str, Enum):
    BEGIN = "begin"
    END = "end"
    ERROR = "error"


@dataclass
class BaseEvent:
    event: SpeechEvent
    payload: Any


@dataclass
class InfoEventPayload:
    status: SpeechStatus


@dataclass
class InfoEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.INFO
    payload: InfoEventPayload

    def __post_init__(self):
        self.payload = InfoEventPayload(**self.payload)  # type: ignore


@dataclass
class InfoErrorEventPayload(InfoEventPayload):
    status: SpeechStatus
    error: dict


@dataclass
class InfoErrorEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.INFO
    payload: InfoErrorEventPayload

    def __post_init__(self):
        self.payload = InfoErrorEventPayload(**self.payload)  # type: ignore


@dataclass
class WordAlignment:
    word: str
    start: float


@dataclass
class RecognizingEventPayload:
    segment_id: int
    text: str
    voice_start_time: float
    word_alignments: List[WordAlignment]

    def __post_init__(self):
        self.word_alignments = [WordAlignment(**word_alignment) for word_alignment in self.word_alignments]  # type: ignore


@dataclass
class RecognizingEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.RECOGNIZING
    payload: RecognizingEventPayload

    def __post_init__(self):
        self.payload = RecognizingEventPayload(**self.payload)  # type: ignore


@dataclass
class RecognizedEventPayload(RecognizingEventPayload):
    duration: float


@dataclass
class RecognizedEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.RECOGNIZED
    payload: RecognizedEventPayload

    def __post_init__(self):
        self.payload = RecognizedEventPayload(**self.payload)  # type: ignore


def raw_data_to_event(event: str, payload: Any) -> BaseEvent:
    try:
        if event == SpeechEvent.INFO:
            return InfoErrorEvent(payload=payload) if "error" in payload else InfoEvent(payload=payload)
        elif event == SpeechEvent.RECOGNIZING:
            return RecognizingEvent(payload=payload)
        elif event == SpeechEvent.RECOGNIZED:
            return RecognizedEvent(payload=payload)
        raise InvalidEvent(message=f"event: {event} is invalid.")
    except BaseException as e:
        raise InvalidEvent(message=f"event: {event} with payload: {payload} is invalid due to {e}.")
