"""Domain exceptions for admin_monitor."""

from home_erp.shared.exceptions import BusinessLogicError

class HealthCheckFailureError(BusinessLogicError):
    """Exception raised when HealthCheckFailureError occurs."""
    pass

