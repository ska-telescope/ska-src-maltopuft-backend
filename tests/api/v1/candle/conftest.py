"""BDD test steps shared between candle features."""

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given

from tests.api.v1.datagen import (
    candidate_data_generator,
    sp_candidate_data_generator,
)


@given("a candidate")
def cand_data(result: dict[str, Any]) -> None:
    """Generate fake candidate data."""
    result["candidate"] = candidate_data_generator()


@given("the candidate exists in the database")
def candidate_exists(result: dict[str, Any], client: TestClient) -> None:
    """Take candidate from the 'result' fixture and create it."""
    client.post(url="/v1/candle", json=result.get("candidate"))


@given("a sp candidate")
def sp_candidate_and_parent_data(
    result: dict[str, Any],
    client: TestClient,
) -> None:
    """Generate fake candidate and sp candidates."""
    result["candidate"] = candidate_data_generator()
    cand = client.post(url="/v1/candle", json=result.get("candidate")).json()
    result["sp_candidate"] = sp_candidate_data_generator(
        candidate_id=cand.get("id"),
    )


@given("the sp candidate exists in the database")
def sp_candidate_exists(result: dict[str, Any], client: TestClient) -> None:
    """Take sp candidate from the 'result' fixture and create it."""
    client.post(url="/v1/candle/sp", json=result.get("sp_candidate"))
