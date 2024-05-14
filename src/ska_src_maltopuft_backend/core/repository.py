"""Base class for data repositories."""

from collections.abc import Mapping, Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import Row, Select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from src.ska_src_maltopuft_backend.core.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    """Base class for data repositories."""

    def __init__(self, model: type[ModelT]) -> None:
        """Initialise a BaseRepository instance."""
        self.model_class: type[ModelT] = model

    async def create(
        self,
        db: Session,
        attributes: dict[str, Any] | None = None,
    ) -> ModelT:
        """Creates the model instance.

        :param db: The database session.
        :param attributes: The attributes to create the model with.
        :return: The created model instance.
        """
        if attributes is None:
            attributes = {}

        model = self.model_class(**attributes)
        db.add(model)
        return model

    async def get_all(  # noqa: PLR0913
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        join_: set[str] | None = None,
        order_: dict[str, dict[str, str]] | None = None,
        *,
        q: Mapping[str, Any],
    ) -> Sequence[Row[ModelT]]:
        """Returns a list of model instances.

        :param db: The database session.
        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :param q: The query parameters.
        :return: A list of model instances.
        """
        query = self._query(join_=join_, order_=order_)
        query = self._where(query=query, q=q)
        query = query.offset(skip).limit(limit)
        return await self._all(db=db, query=query)

    async def get_by(
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
        query = await self._get_by(query=query, field=field, value=value)
        return await self._all(db=db, query=query)

    async def get_unique_by(
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
        query = self._query(join_=join_, order=order_)
        query = await self._get_by(query=query, field=field, value=value)
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

    async def _all_unique(
        self,
        db: Session,
        query: Select,
    ) -> Sequence[Row[ModelT]]:
        """Returns all unique results from the query.

        :param db: The database session.
        :param query: The query to execute.
        :return: A list of unique model instances.
        """
        result = db.execute(query)
        return result.unique().scalars().all()

    async def _one(self, db: Session, query: Select) -> Row[ModelT] | None:
        """Returns the first result from the query if it exists.

        :param query: The query to execute.
        :return: The first model instance.
        """
        return db.execute(query).first()

    async def _sort_by(
        self,
        query: Select,
        sort_by: str,
        order: str | None = "asc",
        model: type[ModelT] | None = None,
    ) -> Select:
        """Returns the query sorted by the given column.

        :param db: The database session.
        :param query: The query to sort.
        :param sort_by: The column to sort by.
        :param order: The order to sort by.
        :param model: The model to sort.
        :return: The sorted query.
        """
        model = model or self.model_class
        order_column = getattr(model, sort_by)

        if order == "desc":
            return query.order_by(order_column.desc())

        return query.order_by(order_column.asc())

    async def _get_by(
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
        if order_:
            asc = order_.get("asc")
            if asc is not None:
                for order in asc:
                    query = query.order_by(
                        getattr(self.model_class, order).asc(),
                    )

            desc = order_.get("desc")
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
            query = query.join(table_names.get(table_name))
        return query

    def _where(self, query: Select, q: Mapping[str, Any]) -> Select:
        """Apply predicates from query parameters to query string.

        :param query: The query to predicate.
        :param q: The query parameters.
        :return: The query with predicate clauses.
        """
        for k, v in q.items():
            if v is None:
                # Checking for v = None is not strictly required because
                # the QueryParam base model is passed to from the controller
                # with exclude_unset=True.
                #
                # However this condition is kept for safety in case of e.g.
                # https://github.com/tiangolo/fastapi/discussions/9595
                continue
            if isinstance(v, list):
                LEN_FOR_RANGE = 2  # noqa: N806
                if len(v) == LEN_FOR_RANGE and k != "id":
                    # Interpret element 0 min and element 1 as max
                    v.sort()
                    query = query.where(
                        getattr(self.model_class, k) >= v[0],
                        getattr(self.model_class, k) <= v[1],
                    )
                elif v != []:
                    query = query.where(getattr(self.model_class, k).in_(v))
            else:
                query = query.where(getattr(self.model_class, k) == v)
        return query
