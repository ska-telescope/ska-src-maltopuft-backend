"""Database initialisation tests."""

# ruff: noqa: D103

from pytest_bdd import scenarios, then, when
from ska_src_maltopuft_backend.app.models import Entity
from ska_src_maltopuft_backend.core.config import settings
from ska_src_maltopuft_backend.core.database.init_db import deinit_db, init_db
from sqlalchemy.orm import Session

scenarios("./init_db.feature")


@when("the database is initialised")
def database_initialised(db: Session) -> None:
    init_db(db=db)


@when("the database is deinitialised")
def database_deinitialised(db: Session) -> None:
    deinit_db(db=db)


@then("the label entities should be created")
def check_label_entities_created(db: Session) -> None:
    entities = db.query(Entity).all()
    assert len(entities) == len(settings.MALTOPUFT_ENTITIES)


@then("there should be no label entities in the database")
def check_label_entities_removed(db: Session) -> None:
    entities = db.query(Entity).all()
    assert len(entities) == 0
