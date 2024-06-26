"""Base class for data controllers."""

import logging
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from psycopg import errors as psycopgexc
from pydantic import BaseModel
from sqlalchemy import Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.exceptions import (
    AlreadyExistsError,
    NotFoundError,
    ParentNotFoundError,
)
from ska_src_maltopuft_backend.core.repository import BaseRepository

ModelT = TypeVar("ModelT", bound=Base)
CreateModelT = TypeVar("CreateModelT", bound=Base)
logger = logging.getLogger(__name__)


class BaseController(Generic[ModelT, CreateModelT]):
    """Base class for data controllers."""

    def __init__(
        self,
        model: type[ModelT],
        repository: BaseRepository,
    ) -> None:
        """Initialises a data controller instance."""
        self.model_class = model
        self.repository = repository
        self._type = self.model_class.__tablename__.title()

    def _flatten_ids(
        self,
        returned_ids: Sequence[Row[tuple[int]]],
    ) -> list[int]:
        return [id_[0] for id_ in returned_ids]

    async def get_by_id(
        self,
        db: Session,
        id_: int,
        join_: set[str] | None = None,
    ) -> ModelT:
        """Returns the model instance matching the id.

        :param id_: The id to match.
        :param join_: The joins to make.
        :return: The model instance.
        """
        db_obj: Row[ModelT] | None = await self.repository.get_unique_by(
            db=db,
            field="id",
            value=id_,
            join_=join_,
        )
        logger.debug(f"Database returned object: {db_obj}")

        if not db_obj:
            msg = f"{self._type} with id={id_} does not exist"
            raise NotFoundError(msg)

        return db_obj[0]

    async def get_all(
        self,
        db: Session,
        join_: set[str] | None = None,
        order_: dict[str, list[str]] | None = None,
        *,
        q: BaseModel,
    ) -> Sequence[ModelT]:
        """Returns a list of records based on pagination params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.
        :param order_: Dict whose keys are sort order and values are lists of
            fields
        :param q: The query parameters.
        :return: A list of records.
        """
        rows: Sequence[Row[ModelT]] = await self.repository.get_all(
            db=db,
            join_=join_,
            order_=order_,
            q=q.model_dump(exclude_unset=True),
        )
        logger.info(
            f"Database returned {len(rows)} {self.model_class} objects.",
        )
        return [row[0] for row in rows]

    async def create(
        self,
        db: Session,
        attributes: dict[str, Any],
    ) -> ModelT:
        """Creates a new Object in the DB.

        :param attributes: The attributes to create the object with.
        :return: The created object.
        """
        created_object = await self.repository.create(
            db=db,
            attributes=attributes,
        )

        try:
            db.commit()
        except IntegrityError as exc:
            logger.exception("Error encountered:")
            if isinstance(exc.orig, psycopgexc.ForeignKeyViolation):
                msg = (
                    f"Can't create object {self._type} with non-existent"
                    "parent."
                )
                raise ParentNotFoundError(msg) from exc
            if isinstance(exc.orig, psycopgexc.UniqueViolation):
                msg = (
                    f"Can't create object {self._type} with duplicate"
                    "attribute."
                )
                raise AlreadyExistsError(msg) from exc
        return created_object

    async def create_many(
        self,
        db: Session,
        objects: list[CreateModelT],
    ) -> list[int]:
        """Create a list of objects."""
        objects = [jsonable_encoder(obj) for obj in objects]
        try:
            created_ids = await self.repository.create_many(
                db=db,
                objects=objects,
            )
            db.commit()
        except IntegrityError as exc:
            logger.exception("Error encountered:")
            if isinstance(exc.orig, psycopgexc.ForeignKeyViolation):
                msg = (
                    f"Can't create object {self._type} with non-existent"
                    "parent."
                )
                raise ParentNotFoundError(msg) from exc
            if isinstance(exc.orig, psycopgexc.UniqueViolation):
                msg = (
                    f"Can't create object {self._type} with duplicate"
                    "attribute."
                )
                raise AlreadyExistsError(msg) from exc
        logger.info(f"Created {len(created_ids)} {self.model_class} objects")
        return self._flatten_ids(created_ids)

    async def delete(self, db: Session, id_: int) -> None:
        """Deletes the Object from the DB.

        :param model: The model to delete.
        :return: True if the object was deleted, False otherwise.
        """
        db_obj: ModelT = await self.get_by_id(db=db, id_=id_)
        await self.repository.delete(db=db, db_obj=db_obj)
        db.commit()
