"""Add Candidate model.

Revision ID: b25703735700
Revises: 87e2e3f6be9c
Create Date: 2024-05-13 17:38:58.788019

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b25703735700"
down_revision: str | None = "87e2e3f6be9c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create Candidate table."""
    op.create_table(
        "candidate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("dm", sa.Float(), nullable=False),
        sa.Column("snr", sa.Float(), nullable=False),
        sa.Column("width", sa.Float(), nullable=False),
        sa.Column("ra", sa.Unicode(length=12), nullable=False),
        sa.Column("dec", sa.Unicode(length=12), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("candidate_pkey")),
    )


def downgrade() -> None:
    """Drop Candidate table."""
    op.drop_table("candidate")
