"""User database model."""

from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.ska_src_maltopuft_backend.core.database import Base


class User(Base):
    """User database model."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        SA_UUID(as_uuid=True),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        sa.Unicode(255),
        nullable=False,
        unique=True,
    )
    username: Mapped[str] = mapped_column(
        sa.Unicode(255),
        nullable=False,
        unique=True,
    )
    is_admin: Mapped[bool] = mapped_column(server_default="false")
