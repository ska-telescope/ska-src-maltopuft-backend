"""BDD test steps shared between user features."""

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given

from tests.api.v1.datagen import user_data_generator


@given("a user")
def user_data(result: dict[str, Any]) -> None:
    """Generate fake user data."""
    result["user"] = user_data_generator()


@given("the user exists in the database")
def user_exists(result: dict[str, Any], client: TestClient) -> None:
    """Take user from the 'result' fixture and create it."""
    client.post(url="/v1/users", json=result.get("user"))
