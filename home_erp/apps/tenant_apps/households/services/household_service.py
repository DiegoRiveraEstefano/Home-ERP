"""Service operations for HouseholdService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class HouseholdService:
    """Business operations and mutations for HouseholdService."""

    @classmethod
    @transaction.atomic
    def create_household(cls, household_id: str | UUID, **kwargs):
        """Execute create_household mutation safely wrapped in transaction."""
        logger.info("create_household_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def update_settings(cls, household_id: str | UUID, **kwargs):
        """Execute update_settings mutation safely wrapped in transaction."""
        logger.info("update_settings_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

