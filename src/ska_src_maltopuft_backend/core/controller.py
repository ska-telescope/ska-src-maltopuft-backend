"""Base class for data controllers."""

import logging
from collections.abc import Sequence
from typing import Any, Generic

from psycopg import errors as psycopgexc
from pydantic import BaseModel
from sqlalchemy import Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.core.exceptions import (
    AlreadyExistsError,
    MissingRequiredAttributeError,
    NotFoundError,
    ParentNotFoundError,
)
from ska_src_maltopuft_backend.core.repository import BaseRepository
from ska_src_maltopuft_backend.core.types import (
    CreateModelT,
    ModelT,
    UpdateModelT,
)

logger = logging.getLogger(__name__)


class BaseController(Generic[ModelT, CreateModelT, UpdateModelT]):
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

    def _merge_query_parameters(
        self,
        params: list[BaseModel] | None = None,
    ) -> dict[str, Any]:
        if params is None:
            return {}
        if not isinstance(params, list):
            msg = (
                "Parameter 'params' expected type list[BaseModel], "
                f"received {type(params)}"
            )
            raise TypeError(msg)

        if len(params) == 1:
            return params[0].model_dump(exclude_unset=True)

        params_ = [q.model_dump(exclude_unset=True) for q in params]
        merged_params: dict[str, Any] = {}
        for obj in params_:
            merged_params.update(obj)
        return merged_params

    async def get_by_id(
        self,
        db: Session,
        id_: int,
        join_: list[str] | None = None,
    ) -> ModelT:
        """Returns the model instance matching the id.

        :param id_: The id to match.
        :param join_: The joins to make.
        :return: The model instance.
        """
        db_obj: ModelT | None = await self.repository.get_unique_by(
            db=db,
            field="id",
            value=id_,
            join_=join_,
        )
        logger.debug(f"Database returned object: {db_obj}")

        if not db_obj:
            msg = f"{self._type} with id={id_} does not exist"
            raise NotFoundError(msg)

        return db_obj

    async def get_by_id_multi(
        self,
        db: Session,
        ids_: list[int],
    ) -> Sequence[Row[ModelT]]:
        """Returns the model instances matching the ids.

        :param id_: The ids to match.
        :return: The model instances.
        """
        db_obj = await self.repository.get_by_value_multi(
            db=db,
            field="id",
            values=ids_,
        )
        return [row[0] for row in db_obj]

    async def count(
        self,
        db: Session,
        join_: list[str] | None = None,
        q: list[BaseModel] | None = None,
    ) -> int:
        """Return count of objects matching given query parameters."""
        return (
            await self.repository.count(
                db=db,
                join_=join_,
                q=self._merge_query_parameters(params=q),
            )
            or 0
        )

    async def get_all(
        self,
        db: Session,
        join_: list[str] | None = None,
        order_: dict[str, list[str]] | None = None,
        q: list[BaseModel] | None = None,
    ) -> Sequence[ModelT]:
        """Returns a list of records based on query params.

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
            q=self._merge_query_parameters(params=q),
        )
        logger.info(
            f"Database returned {len(rows)} {self.model_class} objects.",
        )
        return [row[0] for row in rows]

    async def create(
        self,  # pylint: disable=unused-argument
        db: Session,
        attributes: dict[str, Any],
        *args: Any,  # noqa: ARG002
        **kwargs: Any,  # noqa: ARG002
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
                    f"Can't create object {self._type} with non-existent "
                    "parent."
                )
                raise ParentNotFoundError(msg) from exc
            if isinstance(exc.orig, psycopgexc.UniqueViolation):
                msg = (
                    f"Can't create object {self._type} with duplicate "
                    "attribute."
                )
                raise AlreadyExistsError(msg) from exc
            if isinstance(exc.orig, psycopgexc.NotNullViolation):
                msg = (
                    f"Can't create object {self._type} with missing "
                    "required attributes."
                )
                raise MissingRequiredAttributeError(msg) from exc
        return created_object

    async def create_many(
        self,  # pylint: disable=unused-argument
        db: Session,
        objects: list[dict[str, Any]],
        *args: Any,  # noqa: ARG002
        **kwargs: Any,  # noqa: ARG002
    ) -> list[int]:
        """Create a list of objects."""
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
                    f"Can't create object {self._type} with non-existent "
                    "parent."
                )
                raise ParentNotFoundError(msg) from exc
            if isinstance(exc.orig, psycopgexc.UniqueViolation):
                msg = (
                    f"Can't create object {self._type} with duplicate "
                    "attribute."
                )
                raise AlreadyExistsError(msg) from exc
            if isinstance(exc.orig, psycopgexc.NotNullViolation):
                msg = (
                    f"Can't create object {self._type} with missing "
                    "required attributes."
                )
                raise MissingRequiredAttributeError(msg) from exc
        logger.info(f"Created {len(created_ids)} {self.model_class} objects")
        return self._flatten_ids(created_ids)

    async def delete(self, db: Session, id_: int) -> None:
        """Deletes the Object from the DB.

        :param db: The database session.
        :param id_: The id of the object to delete from the database.
        :return: True if the object was deleted, False otherwise.
        """
        db_obj: ModelT = await self.get_by_id(db=db, id_=id_)
        await self.repository.delete(db=db, db_obj=db_obj)
        db.commit()

    async def update(
        self,
        db: Session,
        db_obj: ModelT,
        update_obj: UpdateModelT,
    ) -> ModelT:
        """Updates the db_obj with the update_obj attributes.

        The update method is only implemented for controllers that have been
        bound to an update (Pydantic) model type var.

        :param db: The database session.
        :param db_obj: The existing database object.
        :param update_obj: The attributes to update the object with.
        :return: The updated object.
        """
        if not isinstance(update_obj, BaseModel):
            raise NotImplementedError

        updated_object = await self.repository.update(
            db=db,
            db_obj=db_obj,
            update_obj=update_obj.model_dump(exclude_unset=True),
        )
        db.commit()
        db.refresh(db_obj)
        return updated_object
