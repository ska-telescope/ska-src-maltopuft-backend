"""TEAL-505: Define Beam model.

Revision ID: 02ca2e21748e
Revises: d1c23b8223bb
Create Date: 2024-07-09 10:17:25.534036

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "02ca2e21748e"
down_revision: str | None = "d1c23b8223bb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create Beam table."""
    op.create_table(
        "beam",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column("coherent", sa.Boolean(), nullable=False),
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
            name=op.f("beam_observation_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("beam_pkey")),
    )


def downgrade() -> None:
    """Drop Beam table."""
    op.drop_table("beam")
