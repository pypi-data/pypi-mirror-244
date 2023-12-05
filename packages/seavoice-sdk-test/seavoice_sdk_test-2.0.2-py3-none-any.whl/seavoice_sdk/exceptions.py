from typing import Optional


class SpeechRecognitionException(Exception):
    def __init__(self, exception: Optional[Exception] = None, message: Optional[str] = None) -> None:
        self._exception = exception
        self._message = message

    def __str__(self) -> str:
        return f"{type(self)}: {self._message if self._message else self._exception}"


class ClosedException(SpeechRecognitionException):
    pass


class UnExpectedClosedException(SpeechRecognitionException):
    pass


class InternalError(SpeechRecognitionException):
    pass


class InvalidURI(SpeechRecognitionException):
    pass


class AuthenticationFail(SpeechRecognitionException):
    pass


class InvalidEvent(SpeechRecognitionException):
    pass
