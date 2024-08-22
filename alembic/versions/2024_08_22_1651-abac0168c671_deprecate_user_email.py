"""Deprecate User.email

Revision ID: abac0168c671
Revises: 572423489f3f
Create Date: 2024-08-22 16:51:27.938032

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "abac0168c671"
down_revision: str | None = "572423489f3f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Deprecate User.email attriute."""
    op.drop_constraint("user_email_key", "user", type_="unique")
    op.drop_column("user", "email")


def downgrade() -> None:
    """Add User.email attriute."""
    op.add_column(
        "user",
        sa.Column(
            "email",
            sa.VARCHAR(length=255),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.create_unique_constraint("user_email_key", "user", ["email"])
