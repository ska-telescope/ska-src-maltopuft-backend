"""Fake data generators."""

import json
import random
from typing import Any

from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from ska_src_maltopuft_backend.app.schemas.requests import (
    CreateCandidate,
    CreateLabel,
    CreateSPCandidate,
    CreateUser,
)

fake = Faker()


def entity_data_generator(
    type_: str | None = None,
    css_color: str | None = None,
) -> dict[str, Any]:
    """Generate fake entity data."""
    return {
        "type": (
            type_
            or random.choice(  # noqa: S311
                ["RFI", "SINGLE_PULSE", "PERIODIC_PULSE"],
            )
        ),
        "css_color": css_color or fake.hex_color(),
    }


class CandidateFactory(ModelFactory[CreateCandidate]):
    """CreateCandidate Pydantic model factory."""


def candidate_data_generator(**kwargs: dict[str, Any]) -> dict[str, Any]:
    """Generate fake candidate data."""
    candidate_model = CandidateFactory.build()
    candidate_data = json.loads(candidate_model.model_dump_json())

    for arg, value in kwargs.items():
        if value is None:
            continue
        if value == "":
            candidate_data[arg] = None
        else:
            candidate_data[arg] = value

    candidate_data["beam_id"] = 1
    return candidate_data


class SPCandidateFactory(ModelFactory[CreateSPCandidate]):
    """CreateSPCandidate Pydantic model factory."""


def sp_candidate_data_generator(**kwargs: Any) -> dict[str, Any]:
    """Generate fake single pulse candidate data."""
    sp_candidate_model = SPCandidateFactory.build()
    sp_candidate_data = json.loads(sp_candidate_model.model_dump_json())

    for arg, value in kwargs.items():
        if value is None:
            continue
        if value == "":
            sp_candidate_data[arg] = None
        else:
            sp_candidate_data[arg] = value

    return sp_candidate_data


class UserFactory(ModelFactory[CreateUser]):
    """CreateUser Pydantic model factory."""


def user_data_generator(**kwargs: Any) -> dict[str, Any]:
    """Generate fake user data."""
    user_model = UserFactory.build()
    user_data = json.loads(user_model.model_dump_json())
    for arg, value in kwargs.items():
        if value is None:
            continue
        if value == "":
            user_data[arg] = None
        else:
            user_data[arg] = value

    return user_data


class LabelFactory(ModelFactory[CreateLabel]):
    """CreateLabel Pydantic model factory."""


def label_data_generator(**kwargs: Any) -> dict[str, Any]:
    """Generate fake label data."""
    label_model = LabelFactory.build()
    label_data = json.loads(label_model.model_dump_json())
    for arg, value in kwargs.items():
        if value is None:
            continue
        if value == "":
            label_data[arg] = None
        else:
            label_data[arg] = value

    return label_data
