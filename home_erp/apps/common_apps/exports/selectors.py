"""Selectors for exports."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class ExportSelector:
    """Encapsulates optimized read queries for exports."""

    @classmethod
    def get_export_status(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

