"""Candidate service API tests."""

# ruff: noqa: D103

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, scenarios, then, when

from src.ska_src_maltopuft_backend.app.schemas.responses import Candidate
from tests.api.v1.datagen import candidate_data_generator

scenarios("./candidate_api.feature")


@given("a candidate with DM string")
def candidate_data_invalid_dm_string(result: dict[str, Any]) -> None:
    result["candidate"] = candidate_data_generator(
        dm="dm should be a float!",  # type: ignore[arg-type]
    )


@given("a candidate with negative DM")
def candidate_data_invalid_dm_negative_float(result: dict[str, Any]) -> None:
    result["candidate"] = candidate_data_generator(
        dm=-1,  # type: ignore[arg-type]
    )


@when("candidates are retrieved from the database")
def do_get_candidates(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle")


@when("an attempt is made to create the candidate")
def do_create_candidate(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.post(
        url="/v1/candle",
        json=result.get("candidate"),
    )


@when("the candidate is retrieved from the database by id")
def do_get_candidate_by_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle/1")


@when("an attempt is made to delete the candidate from the database")
def do_delete_candidate(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.delete(url="/v1/candle/1")


@then("the response data should contain a candidate")
def response_data_is_candidate(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    cand = Candidate(**data)
    assert cand.id is not None


@then("the response data should contain three candidates")
def response_data_has_3_candidates(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    assert len(data) == 3  # noqa: PLR2004
    for d in data:
        Candidate(**d)
