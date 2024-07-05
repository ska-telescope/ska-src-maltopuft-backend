"""Observation metadata models."""

import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.mixins import TimestampMixin


class ScheduleBlock(Base, TimestampMixin):
    """Schedule block metadata."""

    __tablename__ = "schedule_block"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_at: Mapped[dt.datetime] = mapped_column(nullable=False)
    est_end_at: Mapped[dt.datetime] = mapped_column(nullable=False)

    __table_args__ = (sa.UniqueConstraint("start_at", "est_end_at"),)

    def __repr__(self) -> str:
        """ScheduleBlock repr."""
        return (
            "<ScheduleBlock: "
            f"id={self.id},"
            f"start_at={self.start_at},"
            f"est_end_at={self.est_end_at},"
        )
