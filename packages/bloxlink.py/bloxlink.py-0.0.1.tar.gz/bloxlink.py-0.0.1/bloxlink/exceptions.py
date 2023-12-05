"""

Contains exceptions used by bloxlink.py

"""


class BloxlinkException(Exception):
    """
    Base exception used by all of bloxlink.py
    """
    pass


class UserNotFound(BloxlinkException):
    """
    Exception that's raised when the user cannot be found.
    """
    pass


class Unauthorized(BloxlinkException):
    """HTTP exception raised for status code 401. This usually means you aren't properly authenticated."""


class TooManyRequests(BloxlinkException):
    """
    HTTP exception raised for status code 429.
    This means that Bloxlink has rate limited you.
    """
    pass


class InternalServerError(BloxlinkException):
    """
    HTTP exception raised for status code 500.
    This usually means that there was an issue on Bloxlink's end.
    """
    pass


class BadRequest(BloxlinkException):
    """HTTP exception raised for status code 400."""
    pass
