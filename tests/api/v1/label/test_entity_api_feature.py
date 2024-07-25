"""Entity service API tests."""

# ruff: noqa: D103

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, scenarios, then, when
from ska_src_maltopuft_backend.app.schemas.responses import (
    Entity,
    EntityNames,
)

from tests.api.v1.datagen import entity_data_generator

scenarios("./entity_api.feature")


@given("an entity with css_color 'cccccc'")
def known_css_color(result: dict[str, Any]) -> None:
    result["entity"] = entity_data_generator(css_color="cccccc")


@given("an entity with invalid type")
def entity_data_invalid_type(result: dict[str, Any]) -> None:
    result["entity"] = entity_data_generator(type_="invalid type")


@given("an entity with invalid css_color")
def entity_data_invalid_css_color(result: dict[str, Any]) -> None:
    result["entity"] = entity_data_generator(css_color="invalid css_color")


@when("entities are retrieved from the database")
def do_get_entities(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(
        url="/v1/labels/entity",
        params=result.get("q"),
    )


@when("an attempt is made to create the entity")
def do_create_entity(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.post(
        url="/v1/labels/entity",
        json=result.get("entity"),
    )


@when("the entity is retrieved from the database by id")
def do_get_entity_by_id(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(url="/v1/labels/entity/1")


##############################################################################
# Then steps #################################################################
##############################################################################


@then("the response data should contain an 'RFI' entity")
def response_data_is_rfi_entity(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    entity = Entity(**data)
    assert entity.type == EntityNames.RFI


@then("the response data should contain a 'SINGLE_PULSE' entity")
def response_data_is_sp_entity(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    entity = Entity(**data)
    assert entity.type == EntityNames.SINGLE_PULSE


@then("the response data should contain a 'PERIODIC_PULSE' entity")
def response_data_is_periodic_entity(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    entity = Entity(**data)
    assert entity.type == EntityNames.PERIODIC_PULSE


@then("the response data should contain three entities")
def response_data_has_3_entities(result: dict[str, Any]) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None
    assert len(data) == 3  # noqa: PLR2004
    for d in data:
        Entity(**d)
