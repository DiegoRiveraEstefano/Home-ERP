"""Thread-safe and async-safe tenancy context management using ContextVar."""

import uuid
from contextlib import contextmanager
from contextvars import ContextVar
from contextvars import Token
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator

_current_household_id: ContextVar[uuid.UUID | None] = ContextVar(
    "current_household_id",
    default=None,
)


def get_current_household_id() -> uuid.UUID | None:
    """Retrieve active domestic household UUID from execution context."""
    return _current_household_id.get()


def set_current_household_id(
    household_id: uuid.UUID | str | None,
) -> Token[uuid.UUID | None]:
    """
    Set active household UUID in execution context.

    Args:
        household_id: UUID or string UUID of household, or None to clear.

    Returns:
        Token that can be passed to reset_current_household_id.
    """
    parsed_uuid: uuid.UUID | None = None
    if household_id is not None:
        if isinstance(household_id, uuid.UUID):
            parsed_uuid = household_id
        else:
            parsed_uuid = uuid.UUID(str(household_id))
    return _current_household_id.set(parsed_uuid)


def reset_current_household_id(token: Token[uuid.UUID | None]) -> None:
    """
    Reset active household UUID to previous state.

    Args:
        token: Token returned by set_current_household_id.
    """
    _current_household_id.reset(token)


@contextmanager
def tenant_context(
    household_id: uuid.UUID | str | None,
) -> Generator[uuid.UUID | None]:
    """
    Context manager to scope execution to a specific household.

    Usage:
        with tenant_context(household_id):
            ...
    """
    token = set_current_household_id(household_id)
    try:
        yield get_current_household_id()
    finally:
        reset_current_household_id(token)
