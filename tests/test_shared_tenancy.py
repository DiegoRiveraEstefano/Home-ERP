"""Tests for tenancy ContextVar, tenant_context manager, and middleware."""

import uuid
from unittest.mock import MagicMock

import pytest

from home_erp.shared.tenancy import HouseholdTenancyMiddleware
from home_erp.shared.tenancy import get_current_household_id
from home_erp.shared.tenancy import reset_current_household_id
from home_erp.shared.tenancy import set_current_household_id
from home_erp.shared.tenancy import tenant_context


def test_tenancy_contextvar_set_get_reset():
    """Verify set_current_household_id, get_current_household_id, and reset."""
    assert get_current_household_id() is None

    test_id = uuid.uuid4()
    token = set_current_household_id(test_id)
    assert get_current_household_id() == test_id

    reset_current_household_id(token)
    assert get_current_household_id() is None


def test_tenancy_contextvar_accepts_string_uuid():
    """Verify string UUID is parsed to uuid.UUID."""
    test_id = uuid.uuid4()
    token = set_current_household_id(str(test_id))
    assert get_current_household_id() == test_id

    reset_current_household_id(token)
    assert get_current_household_id() is None


def test_tenant_context_context_manager():
    """Verify tenant_context sets and safely restores active household."""
    assert get_current_household_id() is None
    h1 = uuid.uuid4()
    h2 = uuid.uuid4()

    with tenant_context(h1):
        assert get_current_household_id() == h1

        # Nested context
        with tenant_context(h2):
            assert get_current_household_id() == h2

        # Restored to outer context
        assert get_current_household_id() == h1

    # Restored to original
    assert get_current_household_id() is None


def test_tenant_context_restores_on_exception():
    """Verify tenant_context cleans up even if an exception occurs."""
    assert get_current_household_id() is None
    h1 = uuid.uuid4()

    with pytest.raises(RuntimeError), tenant_context(h1):
        assert get_current_household_id() == h1
        raise RuntimeError("Boom")

    assert get_current_household_id() is None


def test_household_tenancy_middleware_from_request_household():
    """Verify middleware resolves household from request.household."""
    h_id = uuid.uuid4()
    request = MagicMock()
    request.household.id = h_id

    captured_tenant = None

    def dummy_view(req):
        nonlocal captured_tenant
        captured_tenant = get_current_household_id()
        return MagicMock()

    middleware = HouseholdTenancyMiddleware(dummy_view)
    middleware(request)

    assert captured_tenant == h_id
    assert get_current_household_id() is None


def test_household_tenancy_middleware_from_session():
    """Verify middleware resolves household from request.session."""
    h_id = uuid.uuid4()
    request = MagicMock(spec=["session", "headers"])
    request.session = {"active_household_id": str(h_id)}
    request.headers = {}

    captured_tenant = None

    def dummy_view(req):
        nonlocal captured_tenant
        captured_tenant = get_current_household_id()
        return MagicMock()

    middleware = HouseholdTenancyMiddleware(dummy_view)
    middleware(request)

    assert captured_tenant == h_id
    assert get_current_household_id() is None


def test_household_tenancy_middleware_from_header():
    """Verify middleware resolves household from X-Household-ID header."""
    h_id = uuid.uuid4()
    request = MagicMock(spec=["session", "headers"])
    request.session = {}
    request.headers = {"X-Household-ID": str(h_id)}

    captured_tenant = None

    def dummy_view(req):
        nonlocal captured_tenant
        captured_tenant = get_current_household_id()
        return MagicMock()

    middleware = HouseholdTenancyMiddleware(dummy_view)
    middleware(request)

    assert captured_tenant == h_id
    assert get_current_household_id() is None
