"""Catalogue service API tests."""

# ruff: noqa: D103

import ast
from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when
from ska_src_maltopuft_backend.app.models import (
    Catalogue as CatalogueSA,
)
from ska_src_maltopuft_backend.app.models import (
    KnownPulsar as KnownPulsarSA,
)
from ska_src_maltopuft_backend.app.schemas.responses import KnownPulsar
from sqlalchemy.orm import Session

from tests.catalogue.datagen import (
    catalogue_data_generator,
    pulsar_data_generator,
)

scenarios("./pulsar_catalogue_api.feature")


@given("a catalogue")
def catalogue(db: Session, result: dict[str, Any]) -> None:
    """Generate fake Catalogue data."""
    result["catalogue"] = catalogue_data_generator()
    cat = result["catalogue"]
    db.add(CatalogueSA(**cat))
    db.commit()
    result["catalogue"] = cat


@given("a pulsar")
def pulsar_data(result: dict[str, Any]) -> None:
    """Generate fake KnownPulsar data."""
    cat = result.get("catalogue")
    assert isinstance(cat, dict)
    result["pulsar"] = pulsar_data_generator(
        catalogue_id=cat.get("id"),  # type: ignore[arg-type]
    )


@given(parsers.parse("a pulsar where {attributes} is {values}"))
def pulsar_with_attributes(
    result: dict[str, Any],
    attributes: str,
    values: Any,
) -> None:
    """Create a KnownPulsar model with the given attributes."""
    pulsar_attributes = {}
    for att, val in zip(
        ast.literal_eval(attributes),
        ast.literal_eval(values),
        strict=False,
    ):
        pulsar_attributes[att] = val

    cat = result.get("catalogue")
    assert isinstance(cat, dict)
    result["pulsar"] = pulsar_data_generator(
        **pulsar_attributes,
        catalogue_id=cat.get("id"),  # type: ignore[arg-type]
    )


@given("the pulsar exists in the database")
def pulsar(db: Session, result: dict[str, Any]) -> None:
    """Create pulsar in the database."""
    pulsar = result["pulsar"]
    db.add(KnownPulsarSA(**pulsar))
    db.commit()
    result["pulsar"] = pulsar


@when("pulsars are retrieved from the database")
def do_get_pulsars(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    result["result"] = client.get(
        url="/v1/catalogues/pulsars",
        params=result.get("q"),
    )


@then(parsers.parse("the response data should contain {num:d} pulsars"))
def response_data_has_num_pulsars(result: dict[str, Any], num: int) -> None:
    response = result.get("response")
    assert response is not None
    data = response.json()
    assert data is not None

    if isinstance(data, dict):
        data = [data]

    assert len(data) == int(num)
    for d in data:
        cand = KnownPulsar(**d)
        assert cand.id is not None
