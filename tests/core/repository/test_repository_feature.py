"""Base CRUD repository tests."""

#  ruff: noqa: SLF001, PLR2004


from typing import Any

import pytest
import pytest_asyncio
import sqlalchemy as sa
from ska_src_maltopuft_backend.app.models import User
from ska_src_maltopuft_backend.app.schemas.requests import CreateUser
from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.repository import BaseRepository
from sqlalchemy import Select
from sqlalchemy.orm import Mapped, Session, mapped_column
from sqlalchemy.orm.exc import ObjectDeletedError

from tests.api.v1.datagen import user_data_generator


@pytest_asyncio.fixture(scope="module")
async def repository() -> BaseRepository:
    """User repository fixture."""
    return BaseRepository(model=User)


@pytest.mark.asyncio()
async def test_create(db: Session, repository: BaseRepository) -> None:
    """Given that valid input data is provided
    When the user is created with the base repository
    Then a non-null integer id should be present in the result.
    """
    user = await repository.create(
        db=db,
        attributes=user_data_generator(),
    )
    db.commit()
    assert user.id is not None


@pytest.mark.asyncio()
async def test_get_all(
    db: Session,
    repository: BaseRepository,
) -> None:
    """Given two users are created in the database,
    When all users are retrieved from the database,
    Then the result should have two records.
    """
    await repository.create(db=db, attributes=user_data_generator())
    await repository.create(db=db, attributes=user_data_generator())

    users = await repository.get_all(db=db)
    assert len(users) == 2


@pytest.mark.asyncio()
async def test_get_by(db: Session, repository: BaseRepository) -> None:
    """Given a user exists in the database,
    When user table is queried for the existing user's attributes,
    Then the user should be retrieved.
    """
    fake_user_data = user_data_generator()
    fake_user = await repository.create(db=db, attributes=fake_user_data)
    db.commit()

    for field in ("id", "uuid", "username", "is_admin"):
        value = getattr(fake_user, field)
        user = await repository.get_by(db=db, field=field, value=value)
        user = user[0][0]
        assert getattr(user, field) == value


@pytest.mark.asyncio()
async def test_get_by_with_predicate(
    db: Session,
    repository: BaseRepository,
) -> None:
    """Given a user exists in the database,
    And 5 records exist in the database,
    When the first record's username is used as a query predicate,
    Then the record should be returned.
    """
    user_data = user_data_generator()
    username = user_data.get("username")
    await repository.create(
        db=db,
        attributes=user_data,
    )

    for _ in range(5):
        await repository.create(
            db=db,
            attributes=user_data_generator(),
        )

    retrieved_user = await repository.get_by(
        db=db,
        field="username",
        value=username,
    )
    assert len(retrieved_user) == 1
    assert retrieved_user[0][0].username == username


@pytest.mark.asyncio()
async def test_get_unique_by_with_unique_field(
    db: Session,
    repository: BaseRepository,
) -> None:
    """Given a user exists in the database,
    When unique records are queried for with the existing record's (unique) primary key,
    Then the user should be retrieved.
    """
    fake_user_data = user_data_generator()
    fake_user = await repository.create(db=db, attributes=fake_user_data)
    db.commit()
    id_ = fake_user.id

    user = await repository.get_unique_by(db=db, field="id", value=id_)
    assert user is not None
    assert user.id == id_


@pytest.mark.asyncio()
async def test_get_unique_by_with_non_unique_field(
    db: Session,
    repository: BaseRepository,
) -> None:
    """Given two users exist in the database with the same value of `is_admin`,
    When unique records are queried for with the existing record's
        (non-unique) `is_admin` attribute,
    Then only one of the users should be retrieved.
    """
    is_admin = True
    user_1_data = user_data_generator(is_admin=is_admin)
    user_1 = await repository.create(db=db, attributes=user_1_data)
    db.commit()
    user_1_id = user_1.id

    user_2_data = user_data_generator(is_admin=is_admin)
    user_2 = await repository.create(db=db, attributes=user_2_data)
    db.commit()
    user_2_id = user_2.id

    # Check that only one of them is returned
    user = await repository.get_unique_by(
        db=db,
        field="is_admin",
        value=user_1_data["is_admin"],
    )
    assert user is not None
    assert user.id == (user_1_id or user_2_id)


@pytest.mark.asyncio()
async def test_delete(db: Session, repository: BaseRepository) -> None:
    """Given a user exists in the database,
    When the user is deleted,
    Then attempting to retrieve the user should raise an ObjectDeletedError.
    """
    fake_user_data = user_data_generator()
    fake_user = await repository.create(db=db, attributes=fake_user_data)
    db.commit()

    await repository.delete(db=db, db_obj=fake_user)
    with pytest.raises(ObjectDeletedError):
        await repository.get_unique_by(db=db, field="id", value=fake_user.id)


@pytest.mark.asyncio()
async def test_apply_pagination_with_default_values(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When skip and limit are not present in the query parameters,
    Then the `LIMIT` and `OFFSET` should be set to the default values.
    """
    query: Select = Select(User)
    query = repository._apply_pagination(query=query, q={})
    assert query._limit == 100
    assert query._offset == 0


@pytest.mark.asyncio()
async def test_apply_pagination_with_non_default_values(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When skip and limit are present in the query parameters,
    Then the `LIMIT` and `OFFSET` should be set.
    """
    query: Select = Select(User)

    skip = 3
    limit = 4
    query = repository._apply_pagination(
        query=query,
        q={
            "skip": skip,
            "limit": limit,
        },
    )

    assert query._offset is skip
    assert query._limit is limit


@pytest.mark.asyncio()
async def test_apply_pagination(
    db: Session,
    repository: BaseRepository,
) -> None:
    """Given 5 records exist in the database,
    When all records are retrieved with skip=3 and limit=2,
    Then two records should be returned
    And the record IDs to be first_id+skip and first_id+(skip+1).
    """
    for trial in range(5):
        user = await repository.create(
            db=db,
            attributes=user_data_generator(),
        )
        db.commit()

        if trial == 0:
            first_id = user.id

    skip = 3
    limit = 2
    users = await repository.get_all(
        db=db,
        q={"skip": skip, "limit": limit},
    )

    assert len(users) == limit
    assert users[0][0].id == first_id + skip
    assert users[1][0].id == first_id + (skip + 1)


@pytest.mark.asyncio()
async def test_sort_by_desc(db: Session, repository: BaseRepository) -> None:
    """Given 5 records exist in the database,
    When all records are retrieved ordered by descending id,
    Then the adjacent ID should be less than the current ID for each record.
    """
    for _ in range(5):
        await repository.create(
            db=db,
            attributes=user_data_generator(),
        )
    db.commit()

    users = await repository.get_all(
        db=db,
        order_={
            "desc": ["id"],
        },
    )

    for idx in range(len(users) - 1):
        current_user = users[idx][0]
        next_user = users[idx + 1][0]
        assert current_user.id > next_user.id


@pytest.mark.skip()
@pytest.mark.asyncio()
async def test_sort_by_asc(db: Session, repository: BaseRepository) -> None:
    """Given 5 records exist in the database,
    When all records are retrieved ordered by ascending username,
    Then the adjacent username should be after the current username in
    alphabetical order.
    """
    for _ in range(5):
        await repository.create(
            db=db,
            attributes=user_data_generator(),
        )
    db.commit()

    users = await repository.get_all(
        db=db,
        order_={
            "asc": ["username"],
        },
    )

    for idx in range(len(users) - 1):
        current_user = users[idx][0]
        next_user = users[idx + 1][0]
        assert current_user.username.lower() < next_user.username.lower()


@pytest.mark.asyncio()
async def test_add_joins_to_query(repository: BaseRepository) -> None:
    """Given a query,
    When an attempt is made to add valid joins to the query,
    Then the joins should be present in the query.
    """
    query: Select = Select(User)
    join_ = ["label", "entity"]

    query = repository._apply_joins(query=query, join_=join_)
    query_joins = [j[0].description for j in query._setup_joins]  # type: ignore[attr-defined]
    for j in join_:
        assert j in query_joins


@pytest.mark.asyncio()
async def test_add_no_join_to_query(repository: BaseRepository) -> None:
    """Given a query,
    When no joins are made on the query,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_join = repository._apply_joins(query=query)
    assert query == query_after_join


@pytest.mark.asyncio()
async def test_add_empty_join_to_query(repository: BaseRepository) -> None:
    """Given a query,
    When empty joins are made on the query,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_join = repository._apply_joins(query=query, join_=[])
    assert query == query_after_join


@pytest.mark.asyncio()
async def test_add_invalid_table_to_join(repository: BaseRepository) -> None:
    """Given a query,
    When list of joins contains an invalid table,
    Then a ValueError should be raised.
    """
    query: Select = Select(User)
    invalid_table_name = "this_table_doesnt_exist"
    join_ = [invalid_table_name]
    with pytest.raises(
        ValueError,
        match=f"Invalid table name '{invalid_table_name}' provided",
    ):
        repository._apply_joins(query=query, join_=join_)  # type: ignore[arg-type]


@pytest.mark.asyncio()
async def test_add_invalid_join_type_to_query(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When joins are specified in a set rather than a list,
    Then a TypeError should be raised.
    """
    query: Select = Select(User)
    join_ = {"label"}
    join_type = type(join_)
    with pytest.raises(
        TypeError,
        match=f"join_ parameter should be a list, found {join_type}",
    ):
        repository._apply_joins(query=query, join_=join_)  # type: ignore[arg-type]


@pytest.mark.asyncio()
async def test_add_duplicate_join_to_query(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When the joins contain a duplicated table,
    Then a TypeError should be raised.
    """
    query: Select = Select(User)
    join_ = ["label", "label"]
    with pytest.raises(
        ValueError,
        match="Duplicate table found in list of joins",
    ):
        repository._apply_joins(query=query, join_=join_)  # type: ignore[arg-type]


@pytest.mark.asyncio()
async def test_single_apply_filters(repository: BaseRepository) -> None:
    """Given a query,
    When a single value of ID is provided as a predicate,
    Then a user.id should be added to the where clause.
    """
    query: Select = Select(User)
    filters = {"id": 1}
    filtered_query = repository._apply_filters(query=query, q=filters)
    expected_query = query.where(User.id == filters.get("id"))
    assert str(filtered_query) == str(expected_query)


@pytest.mark.asyncio()
async def test_apply_filters_with_no_predicates(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When no predicates are given to the query,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_predicate = repository._apply_filters(query=query, q={})
    assert query == query_after_predicate


@pytest.mark.asyncio()
async def test_apply_filters_with_skip_and_limit(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When skip and limits are present in the query parameters,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_predicate = repository._apply_filters(
        query=query,
        q={
            "skip": 123,
            "limit": 123,
        },
    )

    assert query == query_after_predicate


@pytest.mark.asyncio()
async def test_apply_filters_with_null_predicate(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When a predicate with value `None` is provided,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_predicate = repository._apply_filters(
        query=query,
        q={"predicate": None},
    )
    assert query == query_after_predicate


@pytest.mark.asyncio()
async def test_apply_filters_with_empty_param_list(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When an empty list is provided as a query parameter,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after = repository._apply_filters(query=query, q={"id": []})
    assert query == query_after


@pytest.mark.asyncio()
async def test_apply_filters_with_id_param_list(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When a list of ids is provided as a query parameter,
    Then an user.id IN clause should be added to the query.
    """
    query: Select = Select(User)
    filters = {"id": [1, 2, 3]}
    filtered_query = repository._apply_filters(query=query, q=filters)
    expected_query = query.where(User.id.in_(filters["id"]))
    assert str(filtered_query) == str(expected_query)


@pytest.mark.asyncio()
async def test_apply_filters_with_str_param_list(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When a list of username strings is provided as a query parameter,
    Then an user.username IN clause should be added to the query.
    """
    query: Select = Select(User)
    filters = {"username": ["a", "b", "c"]}
    filtered_query = repository._apply_filters(
        query=query,
        q=filters,
    )
    expected_query = query.where(User.username.in_(filters["username"]))
    assert str(filtered_query) == str(expected_query)


@pytest.mark.asyncio()
def test_apply_foreign_key_filter(repository: BaseRepository) -> None:
    """Given a query,
    When a list of user_id foreign keys is provided as a query parameter,
    Then an user.user_id IN clause should be added to the query.
    """
    query: Select = Select(User)
    filters = {"user_id": [1, 2, 3]}
    filtered_query = repository._apply_filters(
        query=query,
        q=filters,
    )
    expected_query = query.where(User.id.in_([1, 2, 3]))
    assert str(filtered_query) == str(expected_query)


@pytest.mark.asyncio()
def test_ignore_invalid_filters(repository: BaseRepository) -> None:
    """Given a query,
    When invalid (None or empty list) query parameters are given,
    The the query should not be changed.
    """
    query: Select = Select(User)
    filters: dict[str, Any] = {"username": None, "is_admin": []}
    filtered_query = repository._apply_filters(query=query, q=filters)
    assert str(filtered_query) == str(query)


@pytest.mark.asyncio()
def test_combined_filters(engine: sa.Engine) -> None:
    """Given a database table with a string and float value,
    And a query,
    When a string is provided as a query parameter,
    And a list of two floats are provided as a query parameter,
    Then an model.string IN clause and a model.float range clause
        should be added to the query,
    """

    # Create a model with string and float values for this test.
    class FloatStringModel(Base):
        __tablename__ = "float_string_model"
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        string_value: Mapped[str] = mapped_column(
            sa.String(255),
            nullable=True,
        )
        float_value: Mapped[float] = mapped_column(sa.Integer, nullable=True)

    Base.metadata.tables["float_string_model"].create(bind=engine)
    float_repository = BaseRepository(model=FloatStringModel)

    # Actual test starts here
    query: Select = Select(FloatStringModel)
    filters = {"string_value": "hello", "float_value": [0.1, 0.5]}
    filtered_query = float_repository._apply_filters(query=query, q=filters)
    expected_query = query.where(
        FloatStringModel.string_value == filters.get("string_value"),
    ).where(
        (FloatStringModel.float_value >= filters["float_value"][0])
        & (FloatStringModel.float_value <= filters["float_value"][1]),
    )
    assert str(filtered_query) == str(expected_query)


@pytest.mark.asyncio()
def test_unsorted_continuous_range_filter(engine: sa.Engine) -> None:
    """Given a database table with a float value.
    And a query,
    When a list of two reverse sorted floats are provided as a query parameter,
    Then a model.float range clause should be added to the query in sorted order,
    """

    # Create a model with string and float values for this test.
    class FloatModel(Base):
        __tablename__ = "float_model"
        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        float_value: Mapped[float] = mapped_column(sa.Integer, nullable=True)

    Base.metadata.tables["float_model"].create(bind=engine)
    float_repository = BaseRepository(model=FloatModel)

    # Actual test starts here
    query: Select = Select(FloatModel)
    filters = {"float_value": [0.5, 0.1]}
    filtered_query = float_repository._apply_filters(query=query, q=filters)
    expected_query = query.where(
        (FloatModel.float_value >= filters["float_value"][1])
        & (FloatModel.float_value <= filters["float_value"][0]),
    )
    assert str(filtered_query) == str(expected_query)


@pytest.mark.asyncio()
async def test_update(db: Session, repository: BaseRepository) -> None:
    """Given an object exists in the database,
    When the object is updated,
    Then the object should contain the updated data.
    """
    # Create an object
    obj = await repository.create(
        db=db,
        attributes=user_data_generator(is_admin=True),
    )

    db.commit()
    id_ = obj.id

    # Generate updated data
    update_data = user_data_generator(is_admin=False)
    updated_model = CreateUser(**update_data)

    # Do the update
    updated_obj = await repository.update(
        db=db,
        db_obj=obj,
        update_obj=updated_model.model_dump(exclude_unset=True),
    )

    assert updated_obj.id == id_
    for k, v in updated_model.model_dump().items():
        assert getattr(updated_obj, k) == v


def test_has_pos_filter_with_no_params(repository: BaseRepository) -> None:
    """No pos filter params present returns False."""
    q: dict[str, Any] = {}
    assert not repository._has_pos_filter_params(q=q)


def test_has_pos_filter_with_invalid_params(
    repository: BaseRepository,
) -> None:
    """Present pos filter params returns True, even if they are invalid."""
    q: dict[str, Any] = {
        "ra": None,
        "dec": [],
        "pos": "(None,[])",
        "radius": None,
    }
    assert repository._has_pos_filter_params(q=q)


def test_has_pos_filter_with_missing_param(repository: BaseRepository) -> None:
    """Missing pos filter param returns False."""
    q: dict[str, Any] = {
        "ra": "6h03m00.65s",
        "dec": "-40d03m23.2s",
        "pos": "(6h03m00.65s,-40d03m23.2s)",
    }
    assert not repository._has_pos_filter_params(q=q)


def test_has_pos_filter_with_valid_params(repository: BaseRepository) -> None:
    """Present and valid pos filter params returns True."""
    q: dict[str, Any] = {
        "ra": "6h03m00.65s",
        "dec": "-40d03m23.2s",
        "pos": "(6h03m00.65s,-40d03m23.2s)",
        "radius": 1,
    }
    assert repository._has_pos_filter_params(q=q)
