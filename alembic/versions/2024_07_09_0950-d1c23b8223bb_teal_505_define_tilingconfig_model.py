"""TEAL-505: Define TilingConfig model.

Revision ID: d1c23b8223bb
Revises: 473ad72b94ee
Create Date: 2024-07-09 09:50:48.719623

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "d1c23b8223bb"
down_revision: str | None = "473ad72b94ee"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create Observation table."""
    op.create_table(
        "tiling_config",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("coordinate_type", sa.String(), nullable=False),
        sa.Column("epoch", sa.Float(), nullable=False),
        sa.Column("epoch_offset", sa.Float(), nullable=False),
        sa.Column("method", sa.String(), nullable=False),
        sa.Column("nbeams", sa.Integer(), nullable=False),
        sa.Column("overlap", sa.Float(), nullable=False),
        sa.Column("reference_frequency", sa.Float(), nullable=False),
        sa.Column("shape", sa.String(), nullable=False),
        sa.Column("target", sa.String(), nullable=False),
        sa.Column("ra", sa.String(), nullable=False),
        sa.Column("dec", sa.String(), nullable=False),
        sa.Column("observation_id", sa.Integer(), nullable=False),
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
            ["observation_id"],
            ["observation.id"],
            name=op.f("tiling_config_observation_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("tiling_config_pkey")),
    )


def downgrade() -> None:
    """Drop Observation table."""
    op.drop_table("tiling_config")
