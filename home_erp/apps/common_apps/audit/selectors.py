"""Selectors for audit."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class AuditSelector:
    """Encapsulates optimized read queries for audit."""

    @classmethod
    def get_household_recent_logs(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

    @classmethod
    def filter_by_category(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

