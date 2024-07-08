"""User service API tests."""

# ruff: noqa: D103

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, scenarios, then, when

from src.ska_src_maltopuft_backend.user.responses import User
from tests.api.v1.datagen import user_data_generator

scenarios("./user_api.feature")


@given("a user with username 'test_user'")
def user_data_with_username(result: dict[str, Any]) -> None:
    result["user"] = user_data_generator(
        username="test_user",  # type: ignore[arg-type]
    )


@given("a user with is_admin 'None'")
def user_data_with_null_is_admin(result: dict[str, Any]) -> None:
    result["user"] = user_data_generator(
        is_admin="",  # type: ignore[arg-type]
    )


@given("a user with is_admin 'True'")
def user_data_with_true_is_admin(result: dict[str, Any]) -> None:
    result["user"] = user_data_generator(
        is_admin=True,  # type: ignore[arg-type]
    )


@given("a user with email address 'test@example.com'")
def user_data_known_email_address(result: dict[str, Any]) -> None:
    result["user"] = user_data_generator(
        email="test@example.com",  # type: ignore[arg-type]
    )


@given("a user with uuid 'd9e414f3-2bee-48a1-8b4b-07ee5b50473d'")
def user_data_known_uuid(result: dict[str, Any]) -> None:
    result["user"] = user_data_generator(
        uuid="d9e414f3-2bee-48a1-8b4b-07ee5b50473d",  # type: ignore[arg-type]
    )


@given("a user with uuid is 'this is not a uuid'")
def user_data_invalid_uuid(result: dict[str, Any]) -> None:
    result["user"] = user_data_generator(
        uuid="this is not a uuid",  # type: ignore[arg-type]
    )


@given("a user with email address 'this is not an email address'")
def user_data_invalid_email_address(result: dict[str, Any]) -> None:
    result["user"] = user_data_generator(
        email="this is not an email address",  # type: ignore[arg-type]
    )


@when("users are retrieved from the database")
def do_get_users(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/users")


@when("an attempt is made to create the user")
def do_create_user(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.post(
        url="/v1/users",
        json=result.get("user"),
    )


@when("the user is retrieved from the database by id")
def do_get_user_by_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/users/1")


@then("the response data should contain a user")
def response_data_is_user(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    user = User(**data)
    assert user.id is not None


@then("the response data should contain three users")
def response_data_has_3_users(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    assert len(data) == 3  # noqa: PLR2004
    for d in data:
        User(**d)


@then("the value of is_admin should be False")
def is_admin_is_false(result: dict[str, Any]) -> None:
    data = result.get("response").json()  # type: ignore[union-attr]
    assert data.get("is_admin") is False


@then("the value of is_admin should be True")
def is_admin_is_true(result: dict[str, Any]) -> None:
    data = result.get("response").json()  # type: ignore[union-attr]
    assert data.get("is_admin") is True
