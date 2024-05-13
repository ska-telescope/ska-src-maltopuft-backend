"""Candidate handler database models."""

import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class SPCandidate(Base, TimestampMixin):
    """Single-pulse candidate database model."""

    __tablename__ = "sp_candidate"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_path: Mapped[str] = mapped_column(nullable=False)
    observed_at: Mapped[dt.datetime] = mapped_column(nullable=False)

    # Foreign keys
    candidate_id: Mapped[int] = mapped_column(sa.ForeignKey("candidate.id"))

    # Relationships
    candidate: Mapped["Candidate"] = relationship(single_parent=True)
