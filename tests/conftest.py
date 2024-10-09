"""Pytest configuration, fixtures and BDD test steps shared between test
cases.
"""

# ruff: noqa: ARG001 E402

import ast
import datetime as dt
import os
import uuid
from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock

import pytest
import sqlalchemy as sa
from fastapi import status
from fastapi.testclient import TestClient
from httpx import Response
from pytest_bdd import given, parsers, then, when
from pytest_mock import MockerFixture
from ska_src_maltopuft_backend.core.auth import (
    Authenticated,
    AuthenticatedUser,
    AuthorizationChecker,
    BearerTokenAuthBackend,
    UserGroups,
)
from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.database.database import (
    get_db,
    init_engine,
)
from ska_src_maltopuft_backend.core.server import app
from sqlalchemy.orm import Session, sessionmaker
from starlette.authentication import AuthCredentials

from tests.api.v1.datagen import user_data_generator
from tests.observation import datagen


def pytest_bdd_apply_tag(tag: str, function: pytest.Item) -> bool | None:
    """Custom handling of pytest_bdd tags."""
    if os.getenv("ENVIRONMENT") == "CI" and tag == "skip-ci":
        marker = pytest.mark.skip(reason="Not implemented in CI yet")
        marker(function)
        return True
    return None


@pytest.fixture()
def engine() -> Generator[sa.engine.base.Engine, None, None]:
    """Create a test database engine.

    After initialising a database engine a 'drop all' statement is issued to
    ensure that the test database instance doesn't contain any stale data from
    previous tests.

    After re-creating the database schema, an engine generator is provided
    for the duration of the test session. After the test session has completed
    all tables are dropped and the engine is terminated.
    """
    engine = init_engine()

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def db(
    engine: sa.engine.base.Engine,
) -> Generator[Session, None, None]:
    """Create a database session with transaction rollback.

    Yields a transactional database session bound to the single database
    connection used during a single test. Binding the session object to an
    individual database connection ensures that database operations are scoped
    to the connection.

    After database operations are completed (or an error occurs) the
    connection to the database is closed and the transaction is rolled back,
    leaving the database in it's original state.

    This is used to override the `get_db` method in the FastAPI client during
    testing to ensure that the database is returned to a "clean" state after
    each test.
    """
    with engine.connect() as conn:
        transaction = conn.begin()
        db = Session(bind=conn)

        try:
            yield db
        finally:
            db.close()
            transaction.rollback()


@pytest.fixture(scope="session")
def client_with_auth(db: Session) -> Generator[TestClient, None, None]:
    """Create a Fast API test client.

    Overrides `get_db` in the Fast API test client with the `db` fixture which
    rolls back test transactions. The auth middleware is enabled in the test client.
    """
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def auth_backend(db: Session) -> "BearerTokenAuthBackend":
    """Instantiate a BearerTokenAuthBackend object test fixture."""
    return BearerTokenAuthBackend(db=db)


@pytest.fixture(scope="session")
def authenticated_user() -> tuple[AuthCredentials, AuthenticatedUser]:
    """Return a mocked authenticated user with all groups."""
    return (
        AuthCredentials(
            [
                UserGroups.SRC,
                UserGroups.MALTOPUFT,
                UserGroups.MALTOPUFT_USER,
                UserGroups.MALTOPUFT_ADMIN,
            ],
        ),
        AuthenticatedUser(
            is_authenticated=True,
            id="1",
            name="test-user",
            is_admin=False,
            created_at=dt.datetime.now(tz=dt.timezone.utc),  # noqa: UP017
            updated_at=dt.datetime.now(tz=dt.timezone.utc),  # noqa: UP017
            uuid=uuid.uuid4(),
            username="test-user",
        ),
    )


@pytest.fixture()
def _mock_authenticate(
    mocker: MockerFixture,
    authenticated_user: tuple[AuthCredentials, AuthenticatedUser],
) -> None:
    """Mock BearerTokenAuthBackend.

    Mocks the BearerTokenAuthBackend.authenticate method to return an
    authenticated user (from the `authenticated_user` user fixture)
    with all available groups assigned.
    """
    async_mock = AsyncMock(return_value=authenticated_user)
    mocker.patch.object(
        BearerTokenAuthBackend,
        attribute="authenticate",
        side_effect=async_mock,
    )


@pytest.fixture()
def client(
    _mock_authenticate: MockerFixture,
    db: Session,
) -> Generator[TestClient, None, None]:
    """Create a Fast API test client with auth disabled.

    Overrides `get_db` in the Fast API test client with the `db` fixture which
    rolls back test transactions.

    The BearerTokenAuthMiddleware is overridden by passing the
    `_mock_authenticate` MockerFixture to the client. Additionally, the
    Authenticated and AuthorizationChecker dependencies are bypassed.
    """
    # Ignore the Authenticated and AuthorizationChecker dependencies in tests.
    app.dependency_overrides[Authenticated] = lambda: None
    app.dependency_overrides[AuthorizationChecker] = lambda: None

    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def one_off_test_client(
    _mock_authenticate: MockerFixture,
) -> Generator[TestClient, None, None]:
    """Creates a FastAPI test client scoped to the test function.

    This fixture should only be used when the test case is expected to raise
    an exception due to an invalid database connection.

    Because this fixture configures its own database session for the duration
    of the test, it can be used *after monkeypatching* environment variables
    inside a test to mock 'bad' database connections.

    As the database referenced by this fixture isn't expected to exist, there
    are a few key differences with the `db` fixture defined in conftest.py.

        1. There is no attempt to create the database schemas before the test.
        2. There is no attempt to clean up database schemas after a test.
    """
    test_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=init_engine(),
    )

    def override_get_db() -> Generator[Session, None, None]:
        try:
            db = test_session()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[Authenticated] = lambda: None
    app.dependency_overrides[AuthorizationChecker] = lambda: None

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def result() -> dict[str, Any]:
    """HTTP response fixture to share between 'given', 'when', 'then'
    steps.
    """
    return {}


# ----------------------------------------------------------------------------
# Shared BDD test steps ------------------------------------------------------
# ----------------------------------------------------------------------------


@given("an empty database")
def db_is_empty() -> None:
    """Nothing exists in the database."""
    return


@given("observation metadata exists in the database")
def observation_metadata(db: Session, result: dict[str, Any]) -> None:
    """Create observation metadata in the database."""
    args = {
        "id": 1,
        "schedule_block_id": 1,
        "observation_id": 1,
        "coherent_beam_config_id": 1,
        "host_id": 1,
        "beam_id": 1,
    }
    db.add(datagen.sb_data_generator(**args))
    db.add(datagen.obs_data_generator(**args))
    db.add(datagen.cb_config_data_generator(**args))
    db.add(datagen.host_data_generator(**args))
    beam_data = datagen.beam_data_generator(**args)
    db.add(beam_data)
    db.commit()
    result["beam_id"] = beam_data.id


@given(parsers.parse("a user where {attributes} is {values}"))
def user_with_attributes(
    result: dict[str, Any],
    attributes: str,
    values: Any,
) -> None:
    """Create a dictionary of query parameters."""
    user_attributes = {}
    for att, val in zip(
        ast.literal_eval(attributes),
        ast.literal_eval(values),
        strict=False,
    ):
        user_attributes[att] = val
    result["user"] = user_data_generator(**user_attributes)


@given("the user exists in the database")
def user_exists(result: dict[str, Any], client: TestClient) -> None:
    """Take user from the 'result' fixture and create it."""
    client.post(url="/v1/users", json=result.get("user"))


@when(parsers.parse("the query parameters {attributes} have values {values}"))
def prepare_query_params(
    result: dict[str, Any],
    attributes: str,
    values: Any,
) -> None:
    """Create a dictionary of query parameters."""
    q = {}
    for att, val in zip(
        ast.literal_eval(attributes),
        ast.literal_eval(values),
        strict=False,
    ):
        q[att] = val
    result["q"] = q


@then("a response should be returned")
def result_is_response(result: dict[str, Any]) -> None:
    """Verify API returned a Response object."""
    res = result.get("result")
    assert isinstance(res, Response)
    result["response"] = res


@then("an error response should be returned")
def result_is_error_response(result: dict[str, Any]) -> None:
    """Verify API returned an error response, which contains only 'message'
    and 'detail' fields.
    """
    response = result.get("result")
    assert response is not None
    response = response.json()
    assert response.get("message") is not None
    assert response.get("status_code") is not None
    result["response"] = response


@then("a validation error response should be returned")
def result_is_validation_error_response(result: dict[str, Any]) -> None:
    """Verify API returned a validation error response, which contains only a
    'detail' field.
    """
    response = result.get("result")
    assert response is not None
    response = response.json()
    assert response.get("detail") is not None
    result["response"] = response


@then("the response data should contain an empty list")
def response_data_is_empty_list(result: dict[str, Any]) -> None:
    """Verify the response data contains an empty list."""
    response = result.get("response")
    assert response is not None
    assert response.json() == []


@then("the response data should be empty")
def response_data_is_empty(result: dict[str, Any]) -> None:
    """Verify the response data is empty/null/None."""
    response = result.get("response")
    assert response is not None
    response = response.json()
    assert response.json() is None


@then("the response data should not be empty")
def response_data_is_not_empty(result: dict[str, Any]) -> None:
    """Verify the response data is not empty/null/None."""
    response = result.get("response")
    assert response is not None
    assert response.json() is not None


@then("the status code should be HTTP 200")
def response_status_code_200(result: dict[str, Any]) -> None:
    """Verify the API response has status code 200."""
    response = result.get("response")
    assert response is not None
    assert response.status_code == status.HTTP_200_OK


@then("the status code should be HTTP 201")
def response_status_code_201(result: dict[str, Any]) -> None:
    """Verify the API response has status code 201."""
    response = result.get("response")
    assert response is not None
    assert response.status_code == status.HTTP_201_CREATED


@then("the status code should be HTTP 204")
def response_status_code_204(result: dict[str, Any]) -> None:
    """Verify the API response has status code 204."""
    response = result.get("response")
    assert response is not None
    assert response.status_code == status.HTTP_204_NO_CONTENT


@then("the status code should be HTTP 404")
def response_status_code_404(result: dict[str, Any]) -> None:
    """Verify the API response has status code 404."""
    response = result.get("response")
    assert response is not None
    assert response.get("status_code") == status.HTTP_404_NOT_FOUND


@then("the status code should be HTTP 409")
def response_status_code_409(result: dict[str, Any]) -> None:
    """Verify the API response has status code 409."""
    response = result.get("response")
    assert response is not None
    assert response.get("status_code") == status.HTTP_409_CONFLICT


@then("the status code should be HTTP 422")
def response_status_code_422(result: dict[str, Any]) -> None:
    """Verify the API response has status code 422."""
    validation_error_response = result.get("result")
    assert validation_error_response is not None
    assert (
        validation_error_response.status_code
        == status.HTTP_422_UNPROCESSABLE_ENTITY
    )
