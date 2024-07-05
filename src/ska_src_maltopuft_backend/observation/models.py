"""Observation metadata models."""

import datetime as dt
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.mixins import TimestampMixin


class ScheduleBlock(Base, TimestampMixin):
    """Schedule block metadata."""

    __tablename__ = "schedule_block"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_at: Mapped[dt.datetime] = mapped_column(nullable=False)
    est_end_at: Mapped[dt.datetime] = mapped_column(nullable=False)

    # Relationships
    meerkat_schedule_block: Mapped["MeerkatScheduleBlock"] = relationship(
        back_populates="schedule_block",
    )
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="schedule_block",
    )

    __table_args__ = (sa.UniqueConstraint("start_at", "est_end_at"),)

    def __repr__(self) -> str:
        """ScheduleBlock repr."""
        return (
            "<ScheduleBlock: "
            f"id={self.id},"
            f"start_at={self.start_at},"
            f"est_end_at={self.est_end_at},"
        )


class MeerkatScheduleBlock(Base, TimestampMixin):
    """Meerkat telescope schedule block metadata."""

    __tablename__ = "meerkat_schedule_block"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meerkat_id: Mapped[int] = mapped_column(nullable=False)
    meerkat_id_code: Mapped[str] = mapped_column(nullable=False)
    proposal_id: Mapped[str] = mapped_column(nullable=False)

    # Foreign keys
    schedule_block_id: Mapped[int] = mapped_column(
        sa.ForeignKey("schedule_block.id"),
        nullable=False,
    )

    # Relationships
    schedule_block: Mapped["ScheduleBlock"] = relationship(
        back_populates="meerkat_schedule_block",
    )

    __table_args__ = (
        sa.UniqueConstraint("meerkat_id"),
        sa.UniqueConstraint("meerkat_id_code"),
    )

    def __repr__(self) -> str:
        """MeerkatScheduleBlock repr."""
        return (
            "<MeerkatScheduleBlock: "
            f"id={self.id},"
            f"meerkat_id={self.meerkat_id},"
            f"meerkat_id_code={self.meerkat_id_code},"
            f"proposal_id={self.proposal_id},"
            f"schedule_block_id={self.schedule_block_id},"
        )


class CoherentBeamConfig(Base, TimestampMixin):
    """Meerkat telescope observation coherent beam configuration."""

    __tablename__ = "coherent_beam_config"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    angle: Mapped[float] = mapped_column(nullable=False)
    fraction_overlap: Mapped[Decimal] = mapped_column(nullable=False)
    x: Mapped[float] = mapped_column(nullable=False)
    y: Mapped[float] = mapped_column(nullable=False)

    __table_args__ = (
        sa.UniqueConstraint("angle", "fraction_overlap", "x", "y"),
    )

    def __repr__(self) -> str:
        """CoherentBeamConfig repr."""
        return (
            "<CoherentBeamConfig: "
            f"id={self.id},"
            f"angle={self.angle},"
            f"fraction_overlap={self.fraction_overlap},"
            f"x={self.x},"
            f"y={self.y},"
        )

