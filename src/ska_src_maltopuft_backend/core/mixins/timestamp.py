"""Timestamp database columns for auditing."""

# pylint: skip-file

import datetime as dt

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """A class which creates timestamp database columns for auditing."""

    @declared_attr
    def created_at(cls) -> Mapped[dt.datetime]:  # noqa: N805
        """An attribute whose value is generated on the database server
        by the PostgreSQL now() function, which returns the current timestamp
        in the UTC timezone. It is computed once when a row is first appended
        to a table.
        """
        return mapped_column(
            sa.DateTime,
            server_default=sa.func.now(),
            nullable=False,
        )

    @declared_attr
    def updated_at(cls) -> Mapped[dt.datetime]:  # noqa: N805
        """An attribute whose value is generated on the database server
        by the PostgreSQL now() function, which returns the current timestamp
        in the UTC timezone. It is computed and updated every time a row is
        updated.
        """
        return mapped_column(
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        )
