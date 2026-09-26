"""Domain exceptions for users."""

from home_erp.shared.exceptions import BusinessLogicError

class UserNotFoundError(BusinessLogicError):
    """Exception raised when UserNotFoundError occurs."""
    pass

class InvalidProfileError(BusinessLogicError):
    """Exception raised when InvalidProfileError occurs."""
    pass

