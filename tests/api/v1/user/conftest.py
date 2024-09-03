"""BDD test steps shared between user features."""

from typing import Any

from pytest_bdd import given

from tests.api.v1.datagen import user_data_generator


@given("a user")
def user_data(result: dict[str, Any]) -> None:
    """Generate fake user data."""
    result["user"] = user_data_generator()
