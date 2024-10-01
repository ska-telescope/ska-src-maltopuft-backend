"""Test login."""

# ruff: noqa: D103

import asyncio
from typing import Any

from pytest_bdd import given, scenarios, then, when
from ska_src_maltopuft_backend.app.schemas.responses import User
from ska_src_maltopuft_backend.core.auth import BearerTokenAuthBackend
from ska_src_maltopuft_backend.core.config import settings

scenarios("./login.feature")


@given("a valid auth token")
def valid_auth_token(
    result: dict[str, Any],
    auth_backend: BearerTokenAuthBackend,
) -> None:
    result["token"] = auth_backend._decode_jwt(  # noqa: SLF001
        settings.TEST_SUPERUSER_TOKEN,
    )


@when("the token user is retrieved from the database")
def unauthed_user_flow(
    result: dict[str, Any],
    auth_backend: BearerTokenAuthBackend,
) -> None:
    result["user"] = asyncio.run(
        auth_backend._get_or_create_token_user(  # noqa: SLF001
            result.get("token"),  #  type: ignore[arg-type]
        ),
    )


@when("the test user is retrieved from the database")
def test_user_flow(
    result: dict[str, Any],
    auth_backend: BearerTokenAuthBackend,
) -> None:
    result["user"] = asyncio.run(
        auth_backend._get_or_create_test_admin_user(),  # noqa: SLF001
    )


@then("a user should be returned")
def user_found(result: dict[str, Any]) -> None:
    user = result.get("user")
    assert user is not None
    User(**user)
