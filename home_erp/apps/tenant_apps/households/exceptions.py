"""Domain exceptions for households."""

from home_erp.shared.exceptions import BusinessLogicError

class HouseholdNotFoundError(BusinessLogicError):
    """Exception raised when HouseholdNotFoundError occurs."""
    pass

class MemberAlreadyExistsError(BusinessLogicError):
    """Exception raised when MemberAlreadyExistsError occurs."""
    pass

class InvitationExpiredError(BusinessLogicError):
    """Exception raised when InvitationExpiredError occurs."""
    pass

