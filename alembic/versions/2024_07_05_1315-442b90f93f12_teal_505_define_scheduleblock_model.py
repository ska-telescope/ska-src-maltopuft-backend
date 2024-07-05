"""TEAL-505: Define ScheduleBlock model.

Revision ID: 442b90f93f12
Revises: eef6ab50c536
Create Date: 2024-07-05 13:15:53.245072

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "442b90f93f12"
down_revision: str | None = "eef6ab50c536"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create ScheduleBlock table."""
    op.create_table(
        "schedule_block",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("start_at", sa.DateTime(), nullable=False),
        sa.Column("est_end_at", sa.DateTime(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("schedule_block_pkey")),
        sa.UniqueConstraint(
            "start_at", "est_end_at", name=op.f("schedule_block_start_at_key"),
        ),
    )


def downgrade() -> None:
    """Drop ScheduleBlock table."""
    op.drop_table("schedule_block")
