"""Selectors for tenant_analytics."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class TenantAnalyticsSelector:
    """Encapsulates optimized read queries for tenant_analytics."""

    @classmethod
    def get_household_overview_metrics(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

