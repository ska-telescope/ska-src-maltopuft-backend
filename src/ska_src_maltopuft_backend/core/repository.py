"""Base class for data repositories."""

import logging
from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import Row, Select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from ska_src_maltopuft_backend.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)
logger = logging.getLogger(__name__)


class BaseRepository(Generic[ModelT]):
    """Base class for data repositories."""

    def __init__(self, model: type[ModelT]) -> None:
        """Initialise a BaseRepository instance."""
        self.model_class: type[ModelT] = model

    async def create(
        self,
        db: Session,
        attributes: dict[str, Any],
    ) -> ModelT:
        """Creates the model instance.

        :param db: The database session.
        :param attributes: The attributes to create the model with.
        :return: The created model instance.
        """
        model = self.model_class(**attributes)
        db.add(model)
        return model

    async def get_all(
        self,
        db: Session,
        join_: set[str] | None = None,
        order_: dict[str, list[str]] | None = None,
        *,
        q: dict[str, Any] | None = None,
    ) -> Sequence[Row[ModelT]]:
        """Returns a list of model instances.

        :param db: The database session.
        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :param q: The query parameters.
        :return: A list of model instances.
        """
        query = self._query(join_=join_, order_=order_)
        if q is not None:
            query = self._where(query=query, q=q)
            query = self._paginate(query=query, q=q)
        return await self._all(db=db, query=query)

    async def get_by(  # pylint: disable=R0913 # noqa: PLR0913
        self,
        db: Session,
        field: str,
        value: Any,
        join_: set[str] | None = None,
        order_: dict[str, dict[str, str]] | None = None,
    ) -> Sequence[Row[ModelT]]:
        """Returns the model instance matching the field and value.

        :param db: The database session.
        :param field: The field to match.
        :param value: The value to match.
        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :return: The model instance.
        """
        query = self._query(join_=join_, order_=order_)
        query = self._get_by(query=query, field=field, value=value)
        return await self._all(db=db, query=query)

    async def get_unique_by(  # pylint: disable=R0913 # noqa: PLR0913
        self,
        db: Session,
        field: str,
        value: Any,
        join_: set[str] | None = None,
        order_: dict[str, dict[str, str]] | None = None,
    ) -> Row[ModelT] | None:
        """Returns the model instance matching the field and value.

        :param db: The database session.
        :param field: The field to match.
        :param value: The value to match.
        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :return: The model instance.
        """
        query = self._query(join_=join_, order_=order_)
        query = self._get_by(query=query, field=field, value=value)
        return await self._one(db=db, query=query)

    async def delete(self, db: Session, db_obj: ModelT) -> ModelT:
        """Deletes the model.

        :param db: The database session.
        :param id: The model id to delete.
        :return: The deleted model instance
        """
        db.delete(db_obj)
        return db_obj

    def _query(
        self,
        join_: set[str] | None = None,
        order_: dict | None = None,
    ) -> Select:
        """Returns a callable that can be used to query the model.

        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :return: A callable that can be used to query the model.
        """
        query = select(self.model_class)
        query = self._maybe_join(query=query, join_=join_)
        return self._maybe_ordered(query=query, order_=order_)

    async def _all(
        self,
        db: Session,
        query: Select,
    ) -> Sequence[Row[ModelT]]:
        """Returns all results from the query.

        :param db: The database session.
        :param query: The query to execute.
        :return: A list of model instances.
        """
        return db.execute(query).all()

    async def _one(self, db: Session, query: Select) -> Row[ModelT] | None:
        """Returns the first result from the query if it exists.

        :param query: The query to execute.
        :return: The first model instance.
        """
        return db.execute(query).first()

    def _get_by(
        self,
        query: Select,
        field: str,
        value: Any,
    ) -> Select:
        """Returns the query filtered by the given column.

        :param query: The query to filter.
        :param field: The column to filter by.
        :param value: The value to filter by.
        :return: The filtered query.
        """
        return query.where(getattr(self.model_class, field) == value)

    def _maybe_join(
        self,
        query: Select,
        join_: set[str] | None = None,
    ) -> Select:
        """Returns the query with the given joins.

        :param query: The query to join.
        :param join_: The joins to make.
        :return: The query with the given joins.
        """
        if not join_:
            return query

        if not isinstance(join_, set):
            msg = "join_ must be a set"
            raise TypeError(msg)

        return self._add_join_to_query(query=query, join_=join_)

    def _maybe_ordered(
        self,
        query: Select,
        order_: dict | None = None,
    ) -> Select:
        """Returns the query ordered by the given column.

        :param query: The query to order.
        :param order_: The order to make.
        :return: The query ordered by the given column.
        """
        if not order_:
            return query

        asc = order_.get("asc")
        desc = order_.get("desc")

        if asc is not None:
            for order in asc:
                query = query.order_by(
                    getattr(self.model_class, order).asc(),
                )
        if desc is not None:
            for order in desc:
                query = query.order_by(
                    getattr(self.model_class, order).desc(),
                )
        return query

    def _add_join_to_query(self, query: Select, join_: set[str]) -> Select:
        """Returns the query with the given join.

        :param query: The query to join.
        :param join_: The join to make.
        :return: The query with the given join.
        """
        table_names = {
            table.__tablename__: table for table in Base.__subclasses__()
        }
        for table_name in join_:
            query = query.join(
                table_names.get(table_name),  # type: ignore[arg-type]
            )
        return query

    def _where(self, query: Select, q: dict[str, Any] | None) -> Select:
        """Apply predicates from query parameters to query string.

        :param query: The query to predicate.
        :param q: The query parameters.
        :return: The query with predicate clauses.
        """
        if q is None or q == {}:
            return query

        for k, v in q.items():
            if k in ("skip", "limit"):
                # Skip pagination parameters
                continue
            if v is None:
                # Checking for v = None is not strictly required because
                # the QueryParam base model is passed to from the controller
                # with exclude_unset=True.
                #
                # However this condition is kept for safety in case of e.g.
                # https://github.com/tiangolo/fastapi/discussions/9595
                continue
            if isinstance(v, list):
                len_for_range = 2
                if v == []:
                    continue

                if len(v) == len_for_range and isinstance(v[0], float):
                    # Interpret element 0 min and element 1 as max
                    v.sort()
                    query = query.where(
                        getattr(self.model_class, k) >= v[0],
                        getattr(self.model_class, k) <= v[1],
                    )
                else:
                    query = query.where(getattr(self.model_class, k).in_(v))
            else:
                query = self._get_by(
                    query=query,
                    field=k,
                    value=v,
                )
        return query

    def _paginate(self, query: Select, q: dict[str, Any]) -> Select:
        try:
            skip, limit = q.pop("skip"), q.pop("limit")
        except KeyError:
            skip, limit = 0, 100

        return query.offset(skip).limit(limit)
