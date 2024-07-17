"""Single pulse candidate service API tests."""

# ruff: noqa: D103, PLR2004

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, scenarios, then, when
from ska_src_maltopuft_backend.app.schemas.responses import SPCandidate

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


@when("an attempt is made to count the sp candidates")
def do_count_sp_candidate(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle/sp/count")


@when(
    "an attempt is made to count the sp candidates with non-existent query parameters",
)
def do_count_sp_candidate_with_missing_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle/sp/count/?id=2")


@when("an attempt is made to count the sp candidates by observation id")
def do_count_sp_by_obs_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(
        url="/v1/candle/sp/count/?observation_id=1",
    )


@when(
    "an attempt is made to count the sp candidates by invalid observation id",
)
def do_count_sp_by_invalid_obs_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(
        url="/v1/candle/sp/count/?observation_id=2",
    )


@when("sp candidates are retrieved from the database by observation id")
def do_get_sp_by_obs_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle/sp/?observation_id=1")


@when(
    "sp candidates are retrieved from the database by invalid observation id",
)
def do_get_sp_by_invalid_obs_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle/sp/?observation_id=2")


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
    assert len(data) == 3
    for d in data:
        SPCandidate(**d)


@then("the response should equal 0")
def response_data_is_0(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data == 0


@then("the response should equal 1")
def response_data_is_1(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data == 1


@then("the response should equal 2")
def response_data_is_2(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data == 2
