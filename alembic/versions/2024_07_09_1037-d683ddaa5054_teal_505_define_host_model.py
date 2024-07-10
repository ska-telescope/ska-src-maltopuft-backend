"""TEAL-505: Define Host model.

Revision ID: d683ddaa5054
Revises: 02ca2e21748e
Create Date: 2024-07-09 10:37:35.411885

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d683ddaa5054"
down_revision: str | None = "02ca2e21748e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create Host table."""
    op.create_table(
        "host",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ip_address", sa.String(), nullable=False),
        sa.Column("hostname", sa.String(), nullable=True),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("host_pkey")),
    )


def downgrade() -> None:
    """Drop Host table."""
    op.drop_table("host")
