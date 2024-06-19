"""Test health check endpoints."""

# ruff: noqa: D103

import json

import fastapi
import pytest
from fastapi.testclient import TestClient
from httpx import Response
from pytest_bdd import given, scenarios, then, when
from ska_src_maltopuft_backend.app.schemas.responses import Status
from ska_src_maltopuft_backend.core.config import settings
from ska_src_maltopuft_backend.core.database.database import ping_db

scenarios("./health_api.feature")


##############################################################################
# Given steps ################################################################
##############################################################################


@given("a database is available")
def db_is_available() -> None:
    ping_db()


@given("a database is unavailable")
def db_is_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        settings,
        "MALTOPUFT_POSTGRES_HOST",
        "this-is-not-a-host",
    )


##############################################################################
# When steps #################################################################
##############################################################################


@when("the /ping endpoint is called")
def do_ping(
    client: TestClient,
    result: dict[str, Response | None],
) -> None:
    result["result"] = client.get("/v1/ping")


@when("the /health/app endpoint is called")
def do_health_app(
    client: TestClient,
    result: dict[str, Response | None],
) -> None:
    result["result"] = client.get("/v1/health/app")


@when("the /health/db endpoint is called")
def do_health_db_available(
    client: TestClient,
    result: dict[str, Response | None],
) -> None:
    result["result"] = client.get("/v1/health/db")


@when("the /health/db endpoint is called from client to unavailable DB")
def do_health_db_unavailable(
    one_off_test_client: TestClient,
    result: dict[str, Response | None],
) -> None:
    result["result"] = one_off_test_client.get("/v1/health/db")


##############################################################################
# Then steps #################################################################
##############################################################################


@then("an empty response with HTTP 204 status code is returned")
def ok_response(result: dict[str, Response | None]) -> None:
    response = result.get("result")
    assert isinstance(response, Response)
    assert response.status_code == fastapi.status.HTTP_204_NO_CONTENT

    # Attempting to parse empty response raises JSONDecode exception
    with pytest.raises(json.decoder.JSONDecodeError):
        response.json()


@then("a successful response with service information is returned")
def successful_health_app_response(result: dict[str, Response]) -> None:
    response = result.get("result")
    assert isinstance(response, Response)
    assert response.status_code == fastapi.status.HTTP_200_OK

    json_content = response.json()
    assert isinstance(json_content, dict)

    content = Status(**json_content)
    assert content.name == settings.APP_NAME
    assert content.status == "HEALTHY"


@then("a successful response with healthy status is returned")
def successful_health_db_response(result: dict[str, Response]) -> None:
    response = result.get("result")
    assert isinstance(response, Response)
    assert response.status_code == fastapi.status.HTTP_200_OK

    json_content = response.json()
    assert isinstance(json_content, dict)

    content = Status(**json_content)
    assert content.name == settings.MALTOPUFT_POSTGRES_HOST
    assert content.status == "HEALTHY"


@then("a successful response with unhealthy status is returned")
def successful_unhealthy_db_response(result: dict[str, Response]) -> None:
    response = result.get("result")
    assert isinstance(response, Response)
    assert response.status_code == fastapi.status.HTTP_200_OK

    json_content = response.json()
    assert isinstance(json_content, dict)

    content = Status(**json_content)
    assert content.name == settings.MALTOPUFT_POSTGRES_HOST
    assert content.status == "UNAVAILABLE"
