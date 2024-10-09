"""Initialise database records."""

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import delete, insert

from ska_src_maltopuft_backend.app.models import Entity
from ska_src_maltopuft_backend.core.config import settings


def init_db(db: Session) -> None:
    """Insert initial data into database.

    Inserts the default entity records into the database.
    """
    bulk_insert_stmt = insert(Entity).returning(Entity.id)
    db.execute(bulk_insert_stmt, params=settings.MALTOPUFT_ENTITIES).fetchall()
    db.commit()


def deinit_db(db: Session) -> None:
    """Delete initial data from database.

    Deletes the default entity records from the database.
    """
    # pylint: disable=not-an-iterable

    with db.begin():
        for entity in settings.MALTOPUFT_ENTITIES:
            db.execute(delete(Entity), params=entity)
