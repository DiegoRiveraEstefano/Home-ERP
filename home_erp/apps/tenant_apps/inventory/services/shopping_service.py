"""Service operations for ShoppingService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class ShoppingService:
    """Business operations and mutations for ShoppingService."""

    @classmethod
    @transaction.atomic
    def add_to_list(cls, household_id: str | UUID, **kwargs):
        """Execute add_to_list mutation safely wrapped in transaction."""
        logger.info("add_to_list_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def mark_as_purchased(cls, household_id: str | UUID, **kwargs):
        """Execute mark_as_purchased mutation safely wrapped in transaction."""
        logger.info("mark_as_purchased_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

