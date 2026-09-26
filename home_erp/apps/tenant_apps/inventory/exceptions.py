"""Domain exceptions for inventory."""

from home_erp.shared.exceptions import BusinessLogicError

class InsufficientStockError(BusinessLogicError):
    """Exception raised when InsufficientStockError occurs."""
    pass

class BatchNotFoundError(BusinessLogicError):
    """Exception raised when BatchNotFoundError occurs."""
    pass

class ItemNotFoundError(BusinessLogicError):
    """Exception raised when ItemNotFoundError occurs."""
    pass

