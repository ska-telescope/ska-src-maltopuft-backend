"""Candidate handler database models."""

import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.ska_src_maltopuft_backend.candle.entity import (
    EntityNames,
    EntityNamesDBEnum,
)
from src.ska_src_maltopuft_backend.core.database import Base
from src.ska_src_maltopuft_backend.core.mixins import TimestampMixin


class Candidate(Base, TimestampMixin):
    """Base candidate database model."""

    __tablename__ = "candidate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dm: Mapped[float] = mapped_column(nullable=False)
    snr: Mapped[float] = mapped_column(nullable=False)
    width: Mapped[float] = mapped_column(nullable=False)
    ra: Mapped[str] = mapped_column(sa.Unicode(12), nullable=False)
    dec: Mapped[str] = mapped_column(sa.Unicode(12), nullable=False)

    # Relationships
    sp_candidate: Mapped["SPCandidate"] = relationship()
    labels: Mapped[list["Label"]] = relationship()


class SPCandidate(Base, TimestampMixin):
    """Single-pulse candidate database model."""

    __tablename__ = "sp_candidate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_path: Mapped[str] = mapped_column(nullable=False)
    observed_at: Mapped[dt.datetime] = mapped_column(nullable=False)

    # Foreign keys
    candidate_id: Mapped[int] = mapped_column(
        sa.ForeignKey("candidate.id"),
        nullable=False,
    )

    # Relationships
    candidate: Mapped["Candidate"] = relationship(single_parent=True)


class Label(Base, TimestampMixin):
    """Candidate label database model."""

    __tablename__ = "label"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Foreign keys
    labeller_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id"),
        nullable=False,
    )
    candidate_id: Mapped[int] = mapped_column(
        sa.ForeignKey("candidate.id"),
        nullable=False,
    )
    entity_id: Mapped[int] = mapped_column(
        sa.ForeignKey("entity.id"),
        nullable=False,
    )

    # Relationships
    candidate: Mapped["Candidate"] = relationship()


class Entity(Base, TimestampMixin):
    """Label entity database model."""

    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(EntityNamesDBEnum, nullable=False)
    css_color: Mapped[EntityNames] = mapped_column(
        sa.Unicode(7),
        nullable=False,
    )

    # Relationships
    labels: Mapped[list["Label"]] = relationship()
