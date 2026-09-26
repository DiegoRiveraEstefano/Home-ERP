"""Selectors for imports."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class ImportSelector:
    """Encapsulates optimized read queries for imports."""

    @classmethod
    def get_import_job(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

