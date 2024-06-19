"""Base CRUD repository tests."""

#  ruff: noqa: SLF001, PLR2004


import pytest
import pytest_asyncio
from ska_src_maltopuft_backend.app.models import User
from ska_src_maltopuft_backend.core.repository import BaseRepository
from sqlalchemy import Select
from sqlalchemy.orm import Session
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
async def test_get_all(db: Session, repository: BaseRepository) -> None:
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

    for field in ("id", "uuid", "email", "username", "is_admin"):
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
    assert len(user) == 1
    assert user[0].id == id_


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
    assert len(user) == 1
    assert user[0].id == (user_1_id or user_2_id)


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
async def test_paginate_with_default_values(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When skip and limit are not present in the query parameters,
    Then the `LIMIT` and `OFFSET` should be set to the default values.
    """
    query: Select = Select(User)
    query = repository._paginate(query=query, q={})
    assert query._limit == 100
    assert query._offset == 0


@pytest.mark.asyncio()
async def test_paginate_with_non_default_values(
    repository: BaseRepository,
) -> None:
    """Given a query,
    When skip and limit are present in the query parameters,
    Then the `LIMIT` and `OFFSET` should be set.
    """
    query: Select = Select(User)

    skip = 3
    limit = 4
    query = repository._paginate(
        query=query,
        q={
            "skip": skip,
            "limit": limit,
        },
    )

    assert query._offset is skip
    assert query._limit is limit


@pytest.mark.asyncio()
async def test_paginate(db: Session, repository: BaseRepository) -> None:
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
        assert current_user.username < next_user.username


@pytest.mark.asyncio()
async def test_add_join_to_query(repository: BaseRepository) -> None:
    """Given a query,
    When joins are given to the query,
    Then the joins should be present in the query.
    """
    query: Select = Select(User)
    join_ = {"label", "entity"}

    query = repository._maybe_join(query=query, join_=join_)
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
    query_after_join = repository._maybe_join(query=query)
    assert query == query_after_join


@pytest.mark.asyncio()
async def test_add_invalid_join_to_query(repository: BaseRepository) -> None:
    """Given a query,
    When joins are specified in a list rather than a set,
    Then a TypeError should be raised.
    """
    query: Select = Select(User)
    join_ = ["label"]
    with pytest.raises(TypeError):
        repository._maybe_join(query=query, join_=join_)  # type: ignore[arg-type]


@pytest.mark.asyncio()
async def test_where(repository: BaseRepository) -> None:
    """Given a query,
    When a single value of ID is provided as a predicate,
    Then a user.id should be added to the where clause.
    """
    query: Select = Select(User)
    query = repository._where(query=query, q={"id": 1})
    assert '"user".id' in str(query._whereclause)


@pytest.mark.asyncio()
async def test_where_with_no_predicates(repository: BaseRepository) -> None:
    """Given a query,
    When no predicates are given to the query,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_predicate = repository._where(query=query, q={})
    assert query == query_after_predicate


@pytest.mark.asyncio()
async def test_where_with_skip_and_limit(repository: BaseRepository) -> None:
    """Given a query,
    When skip and limits are present in the query parameters,
    Then the query should not have a row limiting clause
    And the query should not have a skip clause
    And the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_predicate = repository._where(
        query=query,
        q={
            "skip": 100,
            "limit": 100,
        },
    )

    assert query == query_after_predicate


@pytest.mark.asyncio()
async def test_where_with_null_predicate(repository: BaseRepository) -> None:
    """Given a query,
    When a predicate with value `None` is provided,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after_predicate = repository._where(
        query=query,
        q={"predicate": None},
    )
    assert query == query_after_predicate


@pytest.mark.asyncio()
async def test_where_with_empty_param_list(repository: BaseRepository) -> None:
    """Given a query,
    When an empty list is provided as a query parameter,
    Then the original query should not be changed.
    """
    query: Select = Select(User)
    query_after = repository._where(query=query, q={"id": []})
    assert query == query_after


@pytest.mark.asyncio()
async def test_where_with_id_param_list(repository: BaseRepository) -> None:
    """Given a query,
    When a list of ids is provided as a query parameter,
    Then an user.id IN clause should be added to the query.
    """
    query: Select = Select(User)
    query = repository._where(query=query, q={"id": [1, 2, 3]})
    assert 'WHERE "user".id IN' in str(query)


@pytest.mark.asyncio()
async def test_where_with_str_param_list(repository: BaseRepository) -> None:
    """Given a query,
    When a list of username strings is provided as a query parameter,
    Then an user.username IN clause should be added to the query.
    """
    query: Select = Select(User)
    query = repository._where(query=query, q={"username": ["a", "b", "c"]})
    assert 'WHERE "user".username IN' in str(query)
