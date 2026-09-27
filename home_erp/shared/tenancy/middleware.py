"""Django middleware for managing domestic tenancy context per request."""

import logging
import uuid
from typing import TYPE_CHECKING

from .context import tenant_context

if TYPE_CHECKING:
    from collections.abc import Callable

    from django.http import HttpRequest
    from django.http import HttpResponse

logger = logging.getLogger(__name__)


class HouseholdTenancyMiddleware:
    """
    Middleware establishing active household in ContextVar for request.

    Looks for an active household in:
    1. request.household
    2. request.session["active_household_id"]
    3. request.headers["X-Household-ID"]
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        household_id = self._resolve_household_id(request)
        with tenant_context(household_id):
            return self.get_response(request)

    @classmethod
    def _resolve_household_id(cls, request: HttpRequest) -> uuid.UUID | None:
        """Extract and validate household UUID from request."""
        # 1. Direct attribute on request
        if hasattr(request, "household") and getattr(request.household, "id", None):
            try:
                return uuid.UUID(str(request.household.id))
            except (ValueError, TypeError, AttributeError):
                pass

        # 2. Session state
        if hasattr(request, "session"):
            session_household = request.session.get("active_household_id")
            if session_household:
                try:
                    return uuid.UUID(str(session_household))
                except (ValueError, TypeError):
                    pass

        # 3. Header fallback
        header_household = request.headers.get("X-Household-ID")
        if header_household:
            try:
                return uuid.UUID(str(header_household))
            except (ValueError, TypeError):
                pass

        return None
