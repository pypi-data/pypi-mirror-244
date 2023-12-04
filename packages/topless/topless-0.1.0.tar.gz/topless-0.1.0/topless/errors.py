from enum import Enum, unique

from marshmallow.exceptions import ValidationError


class ErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    FORBIDDEN = "FORBIDDEN"
    BAD_REQUEST = "BAD_REQUEST"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    UNHANDLED_SOURCE = "UNHANDLED_SOURCE"
    INVALID_INTERCEPTOR = "INVALID_INTERCEPTOR"
    INVALID_EVENT_BUS = "INVALID_EVENT_BUS"
    INVALID_FIELD = "INVALID_FIELD"


class ToplessError(Exception):
    def __init__(self, code, message, attributes=None):
        if type(code) is Enum:
            code = code.value()

        self.code = code
        self.message = message
        self.attributes = attributes

        super().__init__(self.message)


class EventProcessingAllowedError(ToplessError):
    """Base exception class for errors that allow continued event processing."""

    pass


class NotFoundError(ToplessError):
    def __init__(self, attributes=None):
        code = ErrorCode.NOT_FOUND
        message = "Could not find the resource specified in the request."

        super().__init__(code, message, attributes)


class BadRequestError(ToplessError):
    pass


class UnhandledSourceError(ToplessError):
    def __init__(self, source=None):
        code = ErrorCode.UNHANDLED_SOURCE
        message = f"Cannot handle {source} event source"

        super().__init__(code, message)


class EventBusNotSetError(ToplessError):
    def __init__(self):
        code = ErrorCode.INVALID_EVENT_BUS
        message = f"The event-bus must be set"

        super().__init__(code, message)


class ForbiddenError(ToplessError):
    def __init__(self, message=None):
        code = ErrorCode.FORBIDDEN
        message = message or f"You shall not pass"

        super().__init__(code, message)
