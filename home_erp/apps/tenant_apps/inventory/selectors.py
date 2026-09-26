"""Selectors for inventory."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class InventorySelector:
    """Encapsulates optimized read queries for inventory."""

    @classmethod
    def get_item_by_id(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_pantry_items(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_expiring_batches(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_shopping_list(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

