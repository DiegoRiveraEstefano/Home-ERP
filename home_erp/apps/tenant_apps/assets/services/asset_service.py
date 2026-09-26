"""Service operations for AssetService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class AssetService:
    """Business operations and mutations for AssetService."""

    @classmethod
    @transaction.atomic
    def register_asset(cls, household_id: str | UUID, **kwargs):
        """Execute register_asset mutation safely wrapped in transaction."""
        logger.info("register_asset_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def update_asset(cls, household_id: str | UUID, **kwargs):
        """Execute update_asset mutation safely wrapped in transaction."""
        logger.info("update_asset_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

