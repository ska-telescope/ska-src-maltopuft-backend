"""Add TimestampMixin to User table.

Revision ID: 87e2e3f6be9c
Revises: d3d424ed8f75
Create Date: 2024-05-13 16:37:52.561945

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "87e2e3f6be9c"
down_revision: str | None = "d3d424ed8f75"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add TimestampMixin to User table."""
    op.add_column(
        "user",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Drop TimestampMixin from User table."""
    op.drop_column("user", "updated_at")
    op.drop_column("user", "created_at")
