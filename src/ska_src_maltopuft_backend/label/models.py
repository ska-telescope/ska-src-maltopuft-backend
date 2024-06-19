"""Label database models."""

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.mixins import TimestampMixin

from .entity import EntityNames, EntityNamesDBEnum

if TYPE_CHECKING:
    from ska_src_maltopuft_backend.app.models import Candidate, User


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
    labeller: Mapped["User"] = relationship(back_populates="labels")
    candidate: Mapped["Candidate"] = relationship(back_populates="labels")
    entity: Mapped["Entity"] = relationship(back_populates="labels")


class Entity(Base, TimestampMixin):
    """Label entity database model."""

    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(
        EntityNamesDBEnum,
        nullable=False,
        unique=True,
    )
    css_color: Mapped[EntityNames] = mapped_column(
        sa.Unicode(7),
        nullable=False,
        unique=True,
    )

    # Relationships
    labels: Mapped[list["Label"]] = relationship()
