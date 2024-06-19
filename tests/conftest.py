"""Pytest configuration and fixtures."""

# ruff: noqa: ARG001 E402

import uuid
from collections.abc import Generator
from unittest.mock import AsyncMock

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from ska_src_maltopuft_backend.core.auth import (
    Authenticated,
    AuthenticatedUser,
    AuthorizationChecker,
    BearerTokenAuthBackend,
    UserGroups,
)
from ska_src_maltopuft_backend.core.database import (
    Base,
    get_db,
    init_engine,
)
from ska_src_maltopuft_backend.core.server import app
from sqlalchemy.orm import Session, sessionmaker
from starlette.authentication import AuthCredentials


@pytest.fixture()
def engine() -> Generator[sqlalchemy.engine.base.Engine, None, None]:
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
    engine: sqlalchemy.engine.base.Engine,
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


@pytest.fixture(scope="module")
def auth_backend() -> "BearerTokenAuthBackend":
    """Instantiate a BearerTokenAuthBackend object test fixture."""
    return BearerTokenAuthBackend()


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
            name="test-user",
            is_authenticated=True,
            sub=uuid.uuid4(),
            preferred_username="test-user",
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
