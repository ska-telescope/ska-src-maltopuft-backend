"""TEAL-505: Define initial Observation model.

Revision ID: 6fed15bc581a
Revises: aaceda90f7de
Create Date: 2024-07-05 17:19:43.915963

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6fed15bc581a"
down_revision: str | None = "aaceda90f7de"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create Observsation table."""
    op.create_table(
        "observation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("coherent_beam_config_id", sa.Integer(), nullable=False),
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
            ["coherent_beam_config_id"],
            ["coherent_beam_config.id"],
            name=op.f("observation_coherent_beam_config_id_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["schedule_block_id"],
            ["schedule_block.id"],
            name=op.f("observation_schedule_block_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("observation_pkey")),
    )


def downgrade() -> None:
    """Drop Observsation table."""
    op.drop_table("observation")
