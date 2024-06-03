"""Create User table.

Revision ID: d3d424ed8f75
Revises: None
Create Date: 2024-05-13 16:26:55.067116

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d3d424ed8f75"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create User table."""
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("email", sa.Unicode(length=255), nullable=False),
        sa.Column("username", sa.Unicode(length=255), nullable=False),
        sa.Column(
            "is_admin", sa.Boolean(), server_default="false", nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("user_pkey")),
        sa.UniqueConstraint("email", name=op.f("user_email_key")),
        sa.UniqueConstraint("username", name=op.f("user_username_key")),
        sa.UniqueConstraint("uuid", name=op.f("user_uuid_key")),
    )


def downgrade() -> None:
    """Drop User table."""
    op.drop_table("user")
