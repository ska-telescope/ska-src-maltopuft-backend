"""TEAL-505: Define MeerkatScheduleBlock model.

Revision ID: b54b8dd660e0
Revises: 442b90f93f12
Create Date: 2024-07-05 13:46:54.654035

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b54b8dd660e0"
down_revision: str | None = "442b90f93f12"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create MeerkatScheduleBlock table."""
    op.create_table(
        "meerkat_schedule_block",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("meerkat_id", sa.Integer(), nullable=False),
        sa.Column("meerkat_id_code", sa.String(), nullable=False),
        sa.Column("proposal_id", sa.String(), nullable=False),
        sa.Column("schedule_block_id", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["schedule_block_id"],
            ["schedule_block.id"],
            name=op.f("meerkat_schedule_block_schedule_block_id_fkey"),
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("meerkat_schedule_block_pkey"),
        ),
        sa.UniqueConstraint(
            "meerkat_id", name=op.f("meerkat_schedule_block_meerkat_id_key"),
        ),
        sa.UniqueConstraint(
            "meerkat_id_code",
            name=op.f("meerkat_schedule_block_meerkat_id_code_key"),
        ),
    )


def downgrade() -> None:
    """Drop MeerkatScheduleBlock table."""
    op.drop_table("meerkat_schedule_block")
