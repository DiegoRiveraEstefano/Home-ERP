"""Service operations for BudgetService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class BudgetService:
    """Business operations and mutations for BudgetService."""

    @classmethod
    @transaction.atomic
    def set_budget(cls, household_id: str | UUID, **kwargs):
        """Execute set_budget mutation safely wrapped in transaction."""
        logger.info("set_budget_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def validate_headroom(cls, household_id: str | UUID, **kwargs):
        """Execute validate_headroom mutation safely wrapped in transaction."""
        logger.info("validate_headroom_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

