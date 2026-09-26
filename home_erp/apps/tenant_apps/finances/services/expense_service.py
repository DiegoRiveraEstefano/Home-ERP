"""Service operations for ExpenseService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class ExpenseService:
    """Business operations and mutations for ExpenseService."""

    @classmethod
    @transaction.atomic
    def record_expense(cls, household_id: str | UUID, **kwargs):
        """Execute record_expense mutation safely wrapped in transaction."""
        logger.info("record_expense_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def record_income(cls, household_id: str | UUID, **kwargs):
        """Execute record_income mutation safely wrapped in transaction."""
        logger.info("record_income_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

