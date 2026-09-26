"""Domain exceptions for admin_backups."""

from home_erp.shared.exceptions import BusinessLogicError

class BackupExecutionError(BusinessLogicError):
    """Exception raised when BackupExecutionError occurs."""
    pass

