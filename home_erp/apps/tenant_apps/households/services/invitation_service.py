"""Service operations for InvitationService."""

import logging
from uuid import UUID
from django.db import transaction

logger = logging.getLogger(__name__)


class InvitationService:
    """Business operations and mutations for InvitationService."""

    @classmethod
    @transaction.atomic
    def invite_member(cls, household_id: str | UUID, **kwargs):
        """Execute invite_member mutation safely wrapped in transaction."""
        logger.info("invite_member_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def accept_invitation(cls, household_id: str | UUID, **kwargs):
        """Execute accept_invitation mutation safely wrapped in transaction."""
        logger.info("accept_invitation_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

    @classmethod
    @transaction.atomic
    def revoke_invitation(cls, household_id: str | UUID, **kwargs):
        """Execute revoke_invitation mutation safely wrapped in transaction."""
        logger.info("revoke_invitation_started", extra={"household_id": str(household_id)})
        # Implementation logic
        return None

