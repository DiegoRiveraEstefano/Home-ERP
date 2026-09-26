"""Selectors for admin_monitor."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class HealthSelector:
    """Encapsulates optimized read queries for admin_monitor."""

    @classmethod
    def get_latest_service_statuses(cls, *args, **kwargs):
        """Fetch data for admin_monitor."""
        return None

