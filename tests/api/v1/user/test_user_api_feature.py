"""User service API tests."""

# ruff: noqa: D103

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import parsers, scenarios, then, when
from ska_src_maltopuft_backend.user.responses import User

scenarios("./user_api.feature")


@when("users are retrieved from the database")
def do_get_users(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/users", params=result.get("q"))


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


@then(parsers.parse("the response data should contain {num:d} users"))
def response_data_has_num_user(result: dict[str, Any], num: int) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None

    if isinstance(data, dict):
        data = [data]

    assert len(data) == int(num)
    for d in data:
        user = User(**d)
        assert user.id is not None


@then("the value of is_admin should be False")
def is_admin_is_false(result: dict[str, Any]) -> None:
    data = result.get("response").json()  # type: ignore[union-attr]
    assert data.get("is_admin") is False


@then("the value of is_admin should be True")
def is_admin_is_true(result: dict[str, Any]) -> None:
    data = result.get("response").json()  # type: ignore[union-attr]
    assert data.get("is_admin") is True
