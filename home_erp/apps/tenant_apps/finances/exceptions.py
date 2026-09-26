"""Domain exceptions for finances."""

from home_erp.shared.exceptions import BusinessLogicError

class AccountNotFoundError(BusinessLogicError):
    """Exception raised when AccountNotFoundError occurs."""
    pass

class InsufficientFundsError(BusinessLogicError):
    """Exception raised when InsufficientFundsError occurs."""
    pass

class BudgetExceededError(BusinessLogicError):
    """Exception raised when BudgetExceededError occurs."""
    pass

