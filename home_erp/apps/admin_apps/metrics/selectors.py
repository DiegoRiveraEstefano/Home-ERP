"""Selectors for admin_metrics."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class MetricSelector:
    """Encapsulates optimized read queries for admin_metrics."""

    @classmethod
    def get_performance_snapshots(cls, *args, **kwargs):
        """Fetch data for admin_metrics."""
        return None

