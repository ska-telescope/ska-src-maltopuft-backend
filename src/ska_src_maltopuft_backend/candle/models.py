"""Candidate handler database models."""

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

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
