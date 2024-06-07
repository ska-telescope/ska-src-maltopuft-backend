"""Tests for AuthorizationChecker dependency."""

# ruff: noqa: D103

from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src.ska_src_maltopuft_backend.core.auth import (
    AuthorizationChecker,
    PermissionDeniedError,
)

scenarios("./authorization_dependency.feature")


@pytest.fixture()
def context() -> dict[str, Any]:
    return {
        "user_scopes": Any,
        "auth_checker": Any,
    }


@given(parsers.parse("a request object containing valid {user_scopes}"))
def valid_scopes(context: dict[str, Any], user_scopes: str) -> None:
    context["user_scopes"] = user_scopes.split(",")


@given(parsers.parse("a request object containing invalid {user_scopes}"))
def invalid_scopes(context: dict[str, Any], user_scopes: str) -> None:
    context["user_scopes"] = user_scopes.split(",")


@when(
    parsers.parse(
        "the AuthorizationChecker checks for valid {required_scopes}",
    ),
)
def auth_checker_valid_scopes(
    context: dict[str, Any],
    required_scopes: str,
) -> None:
    context["auth_checker"] = AuthorizationChecker(
        required_permissions=required_scopes.split(","),
    )


@when(
    parsers.parse(
        "the AuthorizationChecker checks for invalid {required_scopes}",
    ),
)
def auth_checker_invalid_scopes(
    context: dict[str, Any],
    required_scopes: str,
) -> None:
    context["auth_checker"] = AuthorizationChecker(
        required_permissions=required_scopes.split(","),
    )


@then(
    parsers.parse(
        "the AuthorizationChecker dependency should be called without errors",
    ),
)
def auth_checker_returns(context: dict[str, Any]) -> None:
    auth_checker = context["auth_checker"]
    auth_checker(permissions=context.get("user_scopes"))


@then(
    parsers.parse(
        "the AuthorizationChecker dependency should raise a PermissionDeniedError",
    ),
)
def auth_checker_raises(context: dict[str, Any]) -> None:
    auth_checker = context["auth_checker"]
    with pytest.raises(PermissionDeniedError):
        auth_checker(permissions=context.get("user_scopes"))
