"""Selectors for chores."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class ChoreSelector:
    """Encapsulates optimized read queries for chores."""

    @classmethod
    def get_pending_assignments(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def get_chore_leaderboard(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

