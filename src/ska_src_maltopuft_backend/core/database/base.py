"""SQLAlchemy declarative base object."""

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

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
