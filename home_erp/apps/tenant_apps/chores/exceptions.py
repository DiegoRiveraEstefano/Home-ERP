"""Domain exceptions for chores."""

from home_erp.shared.exceptions import BusinessLogicError

class ChoreNotFoundError(BusinessLogicError):
    """Exception raised when ChoreNotFoundError occurs."""
    pass

class AssignmentNotFoundError(BusinessLogicError):
    """Exception raised when AssignmentNotFoundError occurs."""
    pass

