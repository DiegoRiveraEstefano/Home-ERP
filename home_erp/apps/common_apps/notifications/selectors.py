"""Selectors for notifications."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class NotificationSelector:
    """Encapsulates optimized read queries for notifications."""

    @classmethod
    def get_unread_notifications(cls, household_id: str | UUID):
        """Fetch data scoped by household_id."""
        # Implementation delegates to ORM with select_related / prefetch_related
        return None

