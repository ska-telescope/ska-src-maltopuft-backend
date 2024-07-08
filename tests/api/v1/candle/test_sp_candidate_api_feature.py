"""Single pulse candidate service API tests."""

# ruff: noqa: D103

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, scenarios, then, when

from src.ska_src_maltopuft_backend.app.schemas.responses import SPCandidate
from tests.api.v1.datagen import sp_candidate_data_generator

scenarios("./sp_candidate_api.feature")


@given("a sp candidate with null parent candidate attribute")
def sp_candidate_null_parent_data(result: dict[str, Any]) -> None:
    """Generate fake sp candidate data with null parent."""
    result["sp_candidate"] = sp_candidate_data_generator(candidate_id="")


@given("a sp candidate with non-existent parent candidate attribute")
def sp_candidate_invalid_parent_data(result: dict[str, Any]) -> None:
    """Generate fake sp candidate data with invalid parent."""
    result["sp_candidate"] = sp_candidate_data_generator(candidate_id=999)


@when("sp candidates are retrieved from the database")
def do_get_sp_candidates(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle/sp")


@when("an attempt is made to create the sp candidate")
def do_create_sp_candidate(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.post(
        url="/v1/candle/sp",
        json=result.get("sp_candidate"),
    )


@when("the sp candidate is retrieved from the database by id")
def do_get_sp_candidate_by_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle/sp/1")


@when("an attempt is made to delete the sp candidate from the database")
def do_delete_sp_candidate(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.delete(url="/v1/candle/sp/1")


@then("the response data should contain a sp candidate")
def response_data_is_sp_scandidate(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    cand = SPCandidate(**data)
    assert cand.id is not None


@then("the response data should contain three sp candidates")
def response_data_has_3_sp_candidates(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    assert len(data) == 3  # noqa: PLR2004
    for d in data:
        SPCandidate(**d)
