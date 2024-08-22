"""User database model."""

from typing import TYPE_CHECKING
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.mixins import TimestampMixin

if TYPE_CHECKING:
    from ska_src_maltopuft_backend.app.models import Label


class User(Base, TimestampMixin):
    """User database model."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        sa.Unicode(255),
        nullable=False,
        unique=True,
    )
    is_admin: Mapped[bool] = mapped_column(server_default="false")

    # Relationships
    labels: Mapped[list["Label"]] = relationship(back_populates="labeller")

    def __repr__(self) -> str:
        """User repr."""
        return (
            f"<User: id={self.id},"
            f"uuid={self.uuid},"
            f"username={self.username},"
            f"is_admin={self.is_admin}"
        )
