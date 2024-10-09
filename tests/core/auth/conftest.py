"""Shared authentication test steps."""

import pytest
from pytest_bdd import given
from ska_src_maltopuft_backend.core.config import settings


@given("authentication is enabled")
def auth_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    """Enable authentication for a test."""
    monkeypatch.setattr(
        settings,
        "AUTH_ENABLED",
        "1",
    )
