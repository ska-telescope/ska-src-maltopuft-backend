"""Candidate handler database models."""

import datetime as dt
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.ska_src_maltopuft_backend.core.database import Base
from src.ska_src_maltopuft_backend.core.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.ska_src_maltopuft_backend.app.models import Label


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
        unique=True,
        nullable=False,
    )

    # Relationships
    candidate: Mapped["Candidate"] = relationship(
        back_populates="sp_candidate",
    )

    def __repr__(self) -> str:
        """SPCandidate repr."""
        return (
            f"<SPCandidate: id={self.id},"
            f"data_path={self.data_path},"
            f"observed_at={self.observed_at},"
            f"candidate_id={self.candidate_id}"
        )
