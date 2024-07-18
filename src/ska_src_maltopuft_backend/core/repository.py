"""Base class for data repositories."""

import logging
from collections.abc import Sequence
from typing import Any, ClassVar, Generic

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Row, Select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func, insert, select

from .database.base import Base
from .extras import ModelT

logger = logging.getLogger(__name__)


class BaseRepository(Generic[ModelT]):
    """Base class for data repositories."""

    table_name_class_map: ClassVar = {
        table.__tablename__: table for table in Base.__subclasses__()
    }

    foreign_key_map: ClassVar = {
        f"{table_name}_id": (table_class, "id")
        for table_name, table_class in table_name_class_map.items()
    }

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

    async def create_many(
        self,
        db: Session,
        objects: list[ModelT],
    ) -> Sequence[Row[tuple[int]]]:
        """Create multiple model instances.

        :param db: The database session.
        :param objects: The models to create.
        :return: The created model instance ids.
        """
        bulk_insert_stmt = insert(self.model_class).returning(
            self.model_class.id,
        )
        return db.execute(bulk_insert_stmt, params=objects).fetchall()

    async def count(
        self,
        db: Session,
        join_: list[str] | None = None,
        *,
        q: dict[str, Any] | None = None,
    ) -> int | None:
        """Returns the count of model instances.

        :param db: The database session.
        :param join_: The joins to make.
        :param q: The query parameters.
        :return: The count of model instances.
        """
        query = select(
            func.count(self.model_class.id),  # pylint: disable=E1102
        )

        if q is not None:
            query = self._apply_filters(query=query, q=q)

        query = query.select_from(self.model_class)
        query = self._apply_joins(query=query, join_=join_)
        return db.execute(query).scalar()

    async def get_all(
        self,
        db: Session,
        join_: list[str] | None = None,
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
        query = self._build_query(join_=join_, order_=order_)
        if q is not None:
            query = self._apply_filters(query=query, q=q)
            query = self._apply_pagination(query=query, q=q)
        return await self._execute_all(db=db, query=query)

    async def get_by(  # pylint: disable=R0913 # noqa: PLR0913
        self,
        db: Session,
        field: str,
        value: Any,
        join_: list[str] | None = None,
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
        query = self._build_query(join_=join_, order_=order_)
        query = self._filter_by(query=query, field=field, value=value)
        return await self._execute_all(db=db, query=query)

    async def get_unique_by(  # pylint: disable=R0913 # noqa: PLR0913
        self,
        db: Session,
        field: str,
        value: Any,
        join_: list[str] | None = None,
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
        query = self._build_query(join_=join_, order_=order_)
        query = self._filter_by(query=query, field=field, value=value)
        return await self._execute_one(db=db, query=query)

    async def delete(self, db: Session, db_obj: ModelT) -> ModelT:
        """Deletes the model.

        :param db: The database session.
        :param id: The model id to delete.
        :return: The deleted model instance
        """
        db.delete(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelT,
        update_obj: dict[str, Any],
    ) -> ModelT:
        """Updates the model.

        :param db: The database session.
        :param db_obj: The existing database object.
        :param update_obj: The attributes to update the object with.
        :return: The updated object.
        """
        obj_data = jsonable_encoder(db_obj)
        for field in obj_data:
            if field in update_obj:
                setattr(db_obj, field, update_obj[field])
        db.add(db_obj)
        return db_obj

    def _add_joins_to_query(self, query: Select, join_: list[str]) -> Select:
        """Add the given joins to a query.

        :param query: The query that joins are added to.
        :param join_: The list of table names to join.
        :return: The query with the given joins applied.
        """
        for table_name in join_:
            table_class = self.table_name_class_map.get(table_name)
            if table_class is not None:
                query = query.join(table_class)
        return query

    def _validate_joins(self, join_: list[str]) -> None:
        """Validate the join_ parameter to ensure it's a list of unique, valid
        table names.

        :param join_: The list of table names to validate.
        :raises TypeError: If join_ is not a list.
        :raises ValueError: If there are duplicate or invalid table names in
            join_.
        """
        if not isinstance(join_, list):
            msg = f"join_ parameter should be a list, found {type(join_)}"
            raise TypeError(msg)

        if len(join_) != len(set(join_)):
            msg = "Duplicate table found in list of joins"
            raise ValueError(msg)

        for join in join_:
            if join not in self.table_name_class_map:
                msg = f"Invalid table name '{join}' provided"
                raise ValueError(msg)

    def _apply_joins(
        self,
        query: Select,
        join_: list[str] | None = None,
    ) -> Select:
        """Returns the query with the given joins.

        :param query: The query to join.
        :param join_: The joins to make.
        :return: The query with the given joins.
        """
        if not join_:
            return query

        self._validate_joins(join_=join_)

        return self._add_joins_to_query(query=query, join_=join_)

    def _apply_ordering(
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

    def _filter_by(
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

    def _apply_filters(
        self,
        query: Select,
        q: dict[str, Any] | None,
    ) -> Select:
        """Apply predicates from query parameters to query string.

        :param query: The query to predicate.
        :param q: The query parameters.
        :return: The query with predicate clauses.
        """
        if q is None or not q:
            return query

        for k, v in q.items():
            if self._is_pagination_param(k):
                continue
            if self._is_invalid_filter(v):
                continue
            if self._is_foreign_key_filter(k):
                query = self._apply_foreign_key_filter(query, k, v)
            elif isinstance(v, list):
                query = self._apply_list_filter(query, k, v)
            else:
                query = self._filter_by(query, k, v)
        return query

    def _apply_pagination(self, query: Select, q: dict[str, Any]) -> Select:
        skip = q.pop("skip", 0)
        limit = q.pop("limit", 100)
        return query.offset(skip).limit(limit)

    def _build_query(
        self,
        join_: list[str] | None = None,
        order_: dict | None = None,
    ) -> Select:
        """Returns a callable that can be used to query the model.

        :param join_: The joins to make.
        :param order_: The order of the results. (e.g desc, asc)
        :return: A callable that can be used to query the model.
        """
        query = select(self.model_class)
        query = self._apply_joins(query=query, join_=join_)
        return self._apply_ordering(query=query, order_=order_)

    async def _execute_all(
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

    async def _execute_one(
        self,
        db: Session,
        query: Select,
    ) -> Row[ModelT] | None:
        """Returns the first result from the query if it exists.

        :param query: The query to execute.
        :return: The first model instance.
        """
        return db.execute(query).first()

    def _is_pagination_param(self, key: str) -> bool:
        """Check if the key is a pagination parameter."""
        return key in {"skip", "limit"}

    def _is_invalid_filter(self, value: Any) -> bool:
        """Check if the filter value is invalid (None or empty list)."""
        return value is None or (isinstance(value, list) and not value)

    def _is_foreign_key_filter(self, key: str) -> bool:
        """Check if the key is a foreign key filter."""
        return key in self.foreign_key_map

    def _apply_foreign_key_filter(
        self,
        query: Select,
        key: str,
        value: Any,
    ) -> Select:
        """Apply a foreign key filter to the query."""
        related_table_class, related_attr = self.foreign_key_map[key]
        return query.where(
            getattr(related_table_class, related_attr).in_(value),
        )

    def _apply_list_filter(
        self,
        query: Select,
        key: str,
        value: list,
    ) -> Select:
        """Apply a list filter to the query."""
        len_for_range = 2
        if len(value) == len_for_range and all(
            isinstance(item, int | float) for item in value
        ):
            # Interpret list as a range of continuous values to search between
            value.sort()
            return query.where(
                getattr(self.model_class, key) >= value[0],
                getattr(self.model_class, key) <= value[1],
            )

        # Treat list as discrete values
        return query.where(getattr(self.model_class, key).in_(value))
