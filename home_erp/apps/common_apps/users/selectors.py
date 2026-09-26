"""Selectors for users."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class UserSelector:
    """Encapsulates optimized read queries for users."""

    @classmethod
    def get_by_email(cls, *args, **kwargs):
        """Fetch data for users."""
        return None

    @classmethod
    def get_active_users(cls, *args, **kwargs):
        """Fetch data for users."""
        return None

