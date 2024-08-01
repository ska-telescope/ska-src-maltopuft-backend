"""BDD test steps shared between observation features."""

import ast
from typing import Any

from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, when
from sqlalchemy.orm import Session

from tests.observation import datagen


@given("an observation")
def obs_data(db: Session, result: dict[str, Any]) -> None:
    """Generate fake observation data."""
    sb = datagen.sb_data_generator()
    cb = datagen.cb_config_data_generator()
    db.add(sb)
    db.add(cb)
    db.commit()

    result["obs"] = datagen.obs_data_generator(
        schedule_block_id=sb.id,
        coherent_beam_config_id=cb.id,
    )


@given(parsers.parse("an observation where {attributes} is {values}"))
def obs_data_with_attr(
    db: Session,
    result: dict[str, Any],
    attributes: str,
    values: Any,
) -> None:
    """Generate fake observation data with given attribute."""
    sb = datagen.sb_data_generator()
    cb = datagen.cb_config_data_generator()
    db.add(sb)
    db.add(cb)
    db.commit()

    result["sb"] = sb
    result["cb_config"] = cb
    obs_args = {}

    for att, val in zip(
        ast.literal_eval(attributes),
        ast.literal_eval(values),
        strict=False,
    ):
        obs_args[att] = val

    obs_args["schedule_block_id"] = result["sb"].id
    obs_args["coherent_beam_config_id"] = result["cb_config"].id
    result["obs"] = datagen.obs_data_generator(**obs_args)


@given("the observation exists in the database")
def observation_metadata(db: Session, result: dict[str, Any]) -> None:
    """Create observation metadata in the database."""
    obs = result["obs"]
    db.add(obs)
    db.commit()
    result["obs"] = obs


@when("observations are retrieved from the database")
def do_get_obs(
    client: TestClient,
    result: dict[str, Any],
) -> None:
    """Retrieve observations from the database."""
    result["result"] = client.get(url="/v1/obs", params=result.get("q"))
