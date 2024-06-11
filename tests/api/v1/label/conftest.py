"""BDD test steps shared between label features."""

from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given

from tests.api.v1.datagen import (
    candidate_data_generator,
    entity_data_generator,
    label_data_generator,
    user_data_generator,
)


@given("an 'RFI' entity")
def rfi_data(result: dict[str, Any]) -> None:
    """Generate fake RFI entity data."""
    result["entity"] = entity_data_generator(type_="RFI")


@given("a 'SINGLE_PULSE' entity")
def sp_data(result: dict[str, Any]) -> None:
    """Generate fake SINGLE_PULSE entity data."""
    result["entity"] = entity_data_generator(type_="SINGLE_PULSE")


@given("a 'PERIODIC_PULSE' entity")
def periodic_data(result: dict[str, Any]) -> None:
    """Generate fake PERIODIC_PULSE entity data."""
    result["entity"] = entity_data_generator(type_="PERIODIC_PULSE")


@given("the entity exists in the database")
def entity_exists(result: dict[str, Any], client: TestClient) -> None:
    """Take entity from the 'result' fixture and create it."""
    client.post(url="/v1/labels/entity", json=result.get("entity"))


@given("a label")
def label_and_parent_data(
    result: dict[str, Any],
    client: TestClient,
) -> None:
    """Generate fake label."""
    result["user"] = user_data_generator()
    result["candidate"] = candidate_data_generator()

    user = client.post(url="/v1/users", json=result.get("user")).json()
    cand = client.post(url="/v1/candle", json=result.get("candidate")).json()

    # Try to get an entity. If none exists, create one.
    entity = client.get(url="/v1/labels/entity/1").json()
    if entity.get("id") is None:
        result["entity"] = entity_data_generator()
        entity = client.post(
            url="/v1/labels/entity",
            json=result.get("entity"),
        ).json()

    result["label"] = label_data_generator(
        labeller_id=user.get("id"),
        candidate_id=cand.get("id"),
        entity_id=entity.get("id"),
    )


@given("the label exists in the database")
def label_exists(result: dict[str, Any], client: TestClient) -> None:
    """Take label from the 'result' fixture and create it."""
    client.post(url="/v1/labels", json=result.get("label"))
