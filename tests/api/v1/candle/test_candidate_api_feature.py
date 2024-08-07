"""Candidate service API tests."""

# ruff: noqa: D103

import ast
from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when
from ska_src_maltopuft_backend.app.schemas.responses import Candidate

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


@given(parsers.parse("a candidate where {attributes} is {values}"))
def candidate_with_attributes(
    result: dict[str, Any],
    attributes: str,
    values: Any,
) -> None:
    """Create a candidate model with the given attributes."""
    cand_attributes = {}
    for att, val in zip(
        ast.literal_eval(attributes),
        ast.literal_eval(values),
        strict=False,
    ):
        cand_attributes[att] = val
    result["candidate"] = candidate_data_generator(**cand_attributes)


@when("candidates are retrieved from the database")
def do_get_candidates(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/candle", params=result.get("q"))


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


@then(parsers.parse("the response data should contain {num:d} candidates"))
def response_data_has_num_cand(result: dict[str, Any], num: int) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None

    if isinstance(data, dict):
        data = [data]

    assert len(data) == int(num)
    for d in data:
        cand = Candidate(**d)
        assert cand.id is not None
