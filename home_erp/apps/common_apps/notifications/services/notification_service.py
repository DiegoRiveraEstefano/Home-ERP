"""Service operations for NotificationService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class NotificationService:
    """Business operations and mutations for NotificationService."""

    @classmethod
    @transaction.atomic
    def send_notification(cls, household_id: str | UUID, **kwargs):
        """Execute send_notification mutation safely wrapped in transaction."""
        logger.info("send_notification_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def mark_as_read(cls, household_id: str | UUID, **kwargs):
        """Execute mark_as_read mutation safely wrapped in transaction."""
        logger.info("mark_as_read_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

