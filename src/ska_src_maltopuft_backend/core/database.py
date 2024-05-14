"""Initialises the database connection pool."""

import logging
from collections.abc import Generator

import sqlalchemy as sa
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from src.ska_src_maltopuft_backend.core.config import settings

logger = logging.getLogger(__name__)


def init_engine() -> sa.engine.base.Engine:
    """Initialise the database engine."""
    logger.info(
        f"Initialising database engine for {settings.MALTOPUFT_POSTGRES_INFO}",
    )

    engine_ = create_engine(str(settings.MALTOPUFT_POSTGRES_URI))

    logger.info(
        "Successfully initialised engine for "
        f"{settings.MALTOPUFT_POSTGRES_INFO}",
    )
    return engine_


engine = init_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Initialise a database session."""
    db = SessionLocal()
    try:
        yield db
    except sa.exc.OperationalError as e:
        logger.exception(
            f"Failed to connect to {settings.MALTOPUFT_POSTGRES_INFO}. ",
        )
        raise HTTPException(
            status_code=503,
            detail="Database unavailable.",
        ) from e
    finally:
        db.close()


def ping_db(
    db_engine: sa.engine.base.Engine = engine,
) -> sa.engine.cursor.Result:
    """Database readiness check."""
    try:
        with db_engine.connect() as conn:
            return conn.execute(sa.text("SELECT 1"))
    except sa.exc.OperationalError as e:
        logger.exception(
            f"Failed to connect to {settings.MALTOPUFT_POSTGRES_INFO}. ",
        )
        raise HTTPException(
            status_code=503,
            detail="Database unavailable.",
        ) from e


def ping_db_from_pool(db: Session) -> sa.engine.cursor.Result:
    """Database readiness check."""
    try:
        return db.execute(sa.text("SELECT 1"))
    except sa.exc.SQLAlchemyError as e:
        logger.exception(
            f"Failed to connect to {settings.MALTOPUFT_POSTGRES_INFO}. ",
        )
        raise HTTPException(
            status_code=503,
            detail="Database unavailable.",
        ) from e


POSTGRES_NAMING_CONVENTION = {
    "pk": "%(table_name)s_pkey",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "ix": "%(column_0_label)s_idx",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "uq": "%(table_name)s_%(column_0_name)s_key",
}

Base = declarative_base(
    metadata=sa.MetaData(naming_convention=POSTGRES_NAMING_CONVENTION),
)
