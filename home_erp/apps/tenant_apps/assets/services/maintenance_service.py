"""Service operations for MaintenanceService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class MaintenanceService:
    """Business operations and mutations for MaintenanceService."""

    @classmethod
    @transaction.atomic
    def schedule_maintenance(cls, household_id: str | UUID, **kwargs):
        """Execute schedule_maintenance mutation safely wrapped in transaction."""
        logger.info("schedule_maintenance_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def log_maintenance(cls, household_id: str | UUID, **kwargs):
        """Execute log_maintenance mutation safely wrapped in transaction."""
        logger.info("log_maintenance_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

