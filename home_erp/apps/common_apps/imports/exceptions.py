"""Domain exceptions for imports."""

from home_erp.shared.exceptions import BusinessLogicError

class ImportValidationError(BusinessLogicError):
    """Exception raised when ImportValidationError occurs."""
    pass

