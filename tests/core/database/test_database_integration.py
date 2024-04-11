"""Database connection integration 'smoke' tests."""

# ruff: noqa: D103

import fastapi
import pytest
import sqlalchemy
from _pytest.monkeypatch import MonkeyPatch
from pytest_bdd import given, scenarios, then

from src.ska_src_maltopuft_backend.core.config import settings
from src.ska_src_maltopuft_backend.core.database import (
    init_engine,
    ping_db,
)

scenarios("./database_integration.feature")

##############################################################################
# Given steps ################################################################
##############################################################################


@given("the application is configured with a valid connection string")
def valid_database_conn_string() -> None:
    pass


@given("an invalid database hostname in the connection string")
def invalid_database_hostname_in_conn_string(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        settings,
        "MALTOPUFT_POSTGRES_HOST",
        "this-is-not-a-host",
    )


@given("an invalid database port in the connection string")
def invalid_database_port_in_conn_string(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        settings,
        "MALTOPUFT_POSTGRES_PORT",
        1234,
    )


@given("an invalid database user in the connection string")
def invalid_database_user_in_conn_string(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        settings,
        "MALTOPUFT_POSTGRES_USER",
        "this-is-an-invalid-user",
    )


@given("an invalid database password in the connection string")
def invalid_database_password_in_conn_string(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        settings,
        "MALTOPUFT_POSTGRES_PASSWORD",
        "this-is-an-invalid-password",
    )


##############################################################################
# Then steps #################################################################
##############################################################################


@then("a minimal database operation should return a valid result")
def result_object_is_returned() -> None:
    result = ping_db()
    assert isinstance(result, sqlalchemy.engine.cursor.Result)


@then("a 'Database unavailable' error message is raised")
def error_is_raised() -> None:
    with pytest.raises(fastapi.HTTPException, match="Database unavailable"):
        ping_db(db_engine=init_engine())
