"""TEAL-505: Define CoherentBeamConfig model.

Revision ID: aaceda90f7de
Revises: b54b8dd660e0
Create Date: 2024-07-05 14:18:18.229210

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aaceda90f7de"
down_revision: str | None = "b54b8dd660e0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create CoherentBeamConfig table."""
    op.create_table(
        "coherent_beam_config",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("angle", sa.Float(), nullable=False),
        sa.Column("fraction_overlap", sa.Numeric(), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("coherent_beam_config_pkey")),
        sa.UniqueConstraint(
            "angle",
            "fraction_overlap",
            "x",
            "y",
            name=op.f("coherent_beam_config_angle_key"),
        ),
    )


def downgrade() -> None:
    """Drop CoherentBeamConfig table."""
    op.drop_table("coherent_beam_config")
