"""Tests for Authenticated dependency."""

# ruff: noqa: D103

from typing import Any

import pytest
from pytest_bdd import given, scenarios, then
from ska_src_maltopuft_backend.core.auth import (
    Authenticated,
    AuthenticatedUser,
    AuthenticationRequiredError,
)
from ska_src_maltopuft_backend.core.config import settings
from starlette.authentication import AuthCredentials, UnauthenticatedUser

from tests.extras import build_request

scenarios("./authentication_dependency.feature")


class TokenMock:
    """Mock interface for the BearerToken dependency.

    Args:
        verified (bool): Dependency passes if True.

    """

    def __init__(self, *, verified: bool) -> None:
        """Initialises the mock token."""
        self._verified = verified

    def __bool__(self) -> bool:
        """Mocks a passed (True) or failed (False) dependency."""
        return self._verified


@pytest.fixture()
def context() -> dict[str, Any]:
    """Fixture to share state between test steps."""
    return {
        "request": None,
        "token": None,
    }


@given("authentication is enabled")
def auth_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    # Enable auth
    monkeypatch.setattr(
        settings,
        "AUTH_ENABLED",
        "1",
    )


@given("an authenticated token")
def authenticated_token(context: dict[str, Any]) -> None:
    context["token"] = TokenMock(verified=True)


@given("an unauthenticated token")
def unauthenticated_token(context: dict[str, Any]) -> None:
    context["token"] = TokenMock(verified=False)


@given("a missing token")
def missing_token() -> None:
    pass


@given("a request object containing an authenticated user")
def authd_request(
    context: dict[str, Any],
    authenticated_user: tuple[AuthCredentials, AuthenticatedUser],
) -> None:
    _, user = authenticated_user
    context["request"] = build_request(user=user)


@given("a request object containing an unauthenticated user")
def unauthd_request(context: dict[str, Any]) -> None:
    context["request"] = build_request(user=UnauthenticatedUser())


@given("a request object contains no user information")
def missing_user_request(context: dict[str, Any]) -> None:
    context["request"] = build_request()


@then("the Authenticated dependency should be created without errors")
def success(context: dict[str, Any]) -> None:
    assert Authenticated(
        context.get("request"),  # type: ignore[arg-type]
        context.get("token"),  # type: ignore[arg-type]
    )


@then(
    "creating an Authenticated dependency instance should raise an "
    "AuthenticationRequiredError",
)
def error(context: dict[str, Any]) -> None:
    with pytest.raises(AuthenticationRequiredError):
        assert Authenticated(
            context.get("request"),  # type: ignore[arg-type]
            context.get("token"),  # type: ignore[arg-type]
        )
