"""Pytest configuration and fixtures."""

from collections.abc import Generator

import pytest
import sqlalchemy
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.ska_src_maltopuft_backend.core.database.database import (
    Base,
    get_db,
    init_engine,
)
from src.ska_src_maltopuft_backend.core.server import app


@pytest.fixture(scope="session", autouse=True)
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


@pytest.fixture(scope="session")
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
def client(db: Session) -> Generator[TestClient, None, None]:
    """Create a Fast API test client.

    Overrides `get_db` in the Fast API test client with the `db` fixture which
    rolls back test transactions.
    """
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
