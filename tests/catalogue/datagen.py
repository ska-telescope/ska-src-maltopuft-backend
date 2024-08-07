"""Fake catalogue data generators."""

import json
from typing import Any

from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from ska_src_maltopuft_backend.app.schemas.requests import CreateKnownPulsar

fake = Faker()


def catalogue_data_generator(
    id_: int | None = None,
    name: str | None = None,
    url: str | None = None,
) -> dict[str, Any]:
    """Generate fake catalogue data."""
    return {
        "id": id_ or fake.random_number(),
        "name": name or fake.name(),
        "url": url or fake.url(),
    }


class KnownPulsarFactory(ModelFactory[CreateKnownPulsar]):
    """CreateKnownPulsar Pydantic model factory."""


def pulsar_data_generator(**kwargs: dict[str, Any]) -> dict[str, Any]:
    """Generate fake KnownPulsar data."""
    pulsar_model = KnownPulsarFactory.build()
    pulsar_data = json.loads(pulsar_model.model_dump_json())

    for arg, value in kwargs.items():
        if value is None:
            continue
        if value == "":
            pulsar_data[arg] = None
        else:
            pulsar_data[arg] = value

    pulsar_data["pos"] = f"({pulsar_data['ra']},{pulsar_data['dec']})"

    return pulsar_data
