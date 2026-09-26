"""Selectors for admin_backups."""

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class BackupSelector:
    """Encapsulates optimized read queries for admin_backups."""

    @classmethod
    def get_recent_backups(cls, *args, **kwargs):
        """Fetch data for admin_backups."""
        return None

