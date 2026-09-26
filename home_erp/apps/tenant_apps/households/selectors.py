"""Selectors for households."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class HouseholdSelector:
    """Encapsulates optimized read queries for households."""

    @classmethod
    def get_household_by_id(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_members(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_active_invitations(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

