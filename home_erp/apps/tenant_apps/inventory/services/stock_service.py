"""Service operations for StockService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class StockService:
    """Business operations and mutations for StockService."""

    @classmethod
    @transaction.atomic
    def add_batch(cls, household_id: str | UUID, **kwargs):
        """Execute add_batch mutation safely wrapped in transaction."""
        logger.info("add_batch_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def consume_batch(cls, household_id: str | UUID, **kwargs):
        """Execute consume_batch mutation safely wrapped in transaction."""
        logger.info("consume_batch_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def adjust_stock(cls, household_id: str | UUID, **kwargs):
        """Execute adjust_stock mutation safely wrapped in transaction."""
        logger.info("adjust_stock_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

