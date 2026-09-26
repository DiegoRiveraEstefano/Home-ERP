"""Service operations for PantryService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class PantryService:
    """Business operations and mutations for PantryService."""

    @classmethod
    @transaction.atomic
    def register_item(cls, household_id: str | UUID, **kwargs):
        """Execute register_item mutation safely wrapped in transaction."""
        logger.info("register_item_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def archive_item(cls, household_id: str | UUID, **kwargs):
        """Execute archive_item mutation safely wrapped in transaction."""
        logger.info("archive_item_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

