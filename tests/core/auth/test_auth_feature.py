"""Authentication middleware tests."""

# ruff: noqa: D103, SLF001

import asyncio
from typing import Any

import pytest
from fastapi import status
from fastapi.responses import JSONResponse
from pytest_bdd import given, scenarios, then, when

from src.ska_src_maltopuft_backend.core.auth import (
    AuthenticationError,
    BearerTokenAuthBackend,
)
from src.ska_src_maltopuft_backend.core.config import settings
from tests.extras import build_request

scenarios("./auth.feature")


@pytest.fixture()
def context() -> dict[str, Any]:
    """HTTP response fixture to share between 'given', 'when', 'then' steps."""
    return {"request": None}


@given("an authentication header with a valid bearer token")
def valid_auth_header(context: dict[str, Any]) -> None:
    context["request"] = build_request(
        headers={"authorization": f"Bearer {settings.TEST_SUPERUSER_TOKEN}"},
    )


@given("an authentication header with an invalid authentication scheme")
def invalid_auth_header(context: dict[str, Any]) -> None:
    context["request"] = build_request(
        headers={
            "authorization": f"Invalid-auth-scheme {settings.TEST_SUPERUSER_TOKEN}",
        },
    )


@given("no authorization header is present in the request")
def no_auth_header(context: dict[str, Any]) -> None:
    context["request"] = build_request()


@when("the authentication middleware is executed")
def unauthed_user_flow(
    context: dict[str, Any],
    auth_backend: BearerTokenAuthBackend,
) -> None:
    context["auth_result"] = asyncio.run(
        auth_backend.authenticate(
            context.get("request"),  #  type: ignore[arg-type]
        ),
    )


@then("the token is extracted and returned")
def check_valid_token_extraction(
    context: dict[str, Any],
    auth_backend: BearerTokenAuthBackend,
) -> None:
    request = context.get("request")

    if request is not None:
        headers = request.headers

    token = auth_backend._get_token_from_header(
        auth_header=headers.get("authorization"),
    )
    assert token == settings.TEST_SUPERUSER_TOKEN


@then(
    "an AuthenticationError is raised for invalid "
    "or unsupported authentication scheme",
)
def check_invalid_scheme_error(
    context: dict[str, Any],
    auth_backend: BearerTokenAuthBackend,
) -> None:
    request = context.get("request")

    if request is not None:
        headers = request.headers

    with pytest.raises(
        AuthenticationError,
        match="Invalid or unsupported authentication scheme used.",
    ):
        auth_backend._get_token_from_header(
            auth_header=headers.get("authorization"),
        )


@then("nothing is returned")
def no_user_data(context: dict[str, Any]) -> None:
    assert context.get("auth_result") is None


@then("authenticated user data is parsed")
def user_data(context: dict[str, Any]) -> None:
    groups, user = context.get("auth_result", (None, None))

    assert groups is not None
    assert user is not None

    assert groups.scopes == settings.TEST_SUPERUSER_DECODED_TOKEN.get("groups")
    assert user.name == settings.TEST_SUPERUSER_BASE_DECODED_TOKEN.get("name")
    assert user.preferred_username == (
        settings.TEST_SUPERUSER_BASE_DECODED_TOKEN.get("preferred_username")
    )
    assert user.is_authenticated


@then("on_auth_error returns a JSONResponse with HTTP 401 status code")
def auth_error_response(auth_backend: BearerTokenAuthBackend) -> None:
    exc = AuthenticationError("Test error")
    response = auth_backend.on_auth_error(exc)
    assert isinstance(response, JSONResponse)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
