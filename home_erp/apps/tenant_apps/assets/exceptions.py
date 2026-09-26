"""Domain exceptions for assets."""

from home_erp.shared.exceptions import BusinessLogicError

class AssetNotFoundError(BusinessLogicError):
    """Exception raised when AssetNotFoundError occurs."""
    pass

class MaintenanceScheduleNotFoundError(BusinessLogicError):
    """Exception raised when MaintenanceScheduleNotFoundError occurs."""
    pass

