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
    """Base candidate database model.

    A model which records observation metadata 'shared' between single pulse
    and period candidates. It has relationships the child sp_candidate and
    periodic_candidate tables.

    Allowing single pulse and period candidates to have a relationship to the
    same parent table facilitates identifying potential repeat candidates
    (e.g. by cross-matching dm, ra and dec between candidates, labels and
    known sources).
    """

    __tablename__ = "candidate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dm: Mapped[float] = mapped_column(nullable=False)
    snr: Mapped[float] = mapped_column(nullable=False)
    width: Mapped[float] = mapped_column(nullable=False)
    ra: Mapped[str] = mapped_column(sa.Unicode(12), nullable=False)
    dec: Mapped[str] = mapped_column(sa.Unicode(12), nullable=False)

    # Relationships
    sp_candidate: Mapped["SPCandidate"] = relationship(
        back_populates="candidate",
    )
    labels: Mapped[list["Label"]] = relationship(back_populates="candidate")


class SPCandidate(Base, TimestampMixin):
    """Single-pulse candidate database model.

    Records the observation metadata unique to a single pulse candidate
    observations. The sp_candidate model must have exactly one parent
    candidate which records the observation metadata attributes shared
    with periodic candidates.
    """

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
    candidate: Mapped["Candidate"] = relationship(
        back_populates="sp_candidate",
        single_parent=True,
    )


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
    labeller: Mapped["User"] = relationship(  # noqa: F821
        back_populates="labels",
    )
    candidate: Mapped["Candidate"] = relationship(back_populates="labels")


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
