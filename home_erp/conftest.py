from __future__ import annotations

import pytest

from home_erp.apps.common_apps.users.models import User


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123",  # noqa: S106
    )
