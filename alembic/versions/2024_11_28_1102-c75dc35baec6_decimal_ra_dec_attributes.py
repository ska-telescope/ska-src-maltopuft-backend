"""Decimal ra, dec attributes

Revision ID: c75dc35baec6
Revises: 8f80e6af6846
Create Date: 2024-11-28 11:02:19.699549

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c75dc35baec6"
down_revision: str | None = "8f80e6af6846"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Migrate to decimal ra and dec attributes."""
    op.alter_column(
        "beam",
        "ra",
        existing_type=sa.VARCHAR(),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=False,
        postgresql_using="ra::text::numeric",
    )
    op.alter_column(
        "beam",
        "dec",
        existing_type=sa.VARCHAR(),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=False,
        postgresql_using="dec::text::numeric",
    )
    op.alter_column(
        "candidate",
        "ra",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=False,
        postgresql_using="ra::text::numeric",
    )
    op.alter_column(
        "candidate",
        "dec",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=False,
        postgresql_using="dec::text::numeric",
    )
    op.alter_column(
        "known_pulsar",
        "ra",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=True,
        postgresql_using="ra::text::numeric",
    )
    op.alter_column(
        "known_pulsar",
        "dec",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=True,
        postgresql_using="dec::text::numeric",
    )
    op.alter_column(
        "observation",
        "s_ra",
        existing_type=sa.VARCHAR(),
        type_=sa.Numeric(precision=8, scale=5),
        nullable=False,
        postgresql_using="s_ra::text::numeric",
    )
    op.alter_column(
        "observation",
        "s_dec",
        existing_type=sa.VARCHAR(),
        type_=sa.Numeric(precision=8, scale=5),
        nullable=False,
        postgresql_using="s_dec::text::numeric",
    )
    op.alter_column(
        "tiling_config",
        "ra",
        existing_type=sa.VARCHAR(),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=False,
        postgresql_using="ra::text::numeric",
    )
    op.alter_column(
        "tiling_config",
        "dec",
        existing_type=sa.VARCHAR(),
        type_=sa.Numeric(precision=8, scale=5),
        existing_nullable=False,
        postgresql_using="dec::text::numeric",
    )


def downgrade() -> None:
    """Revert decimal ra, dec attributes."""
    op.alter_column(
        "tiling_config",
        "dec",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "tiling_config",
        "ra",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "observation",
        "s_dec",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "observation",
        "s_ra",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "known_pulsar",
        "dec",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=True,
    )
    op.alter_column(
        "known_pulsar",
        "ra",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=True,
    )
    op.alter_column(
        "candidate",
        "dec",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=False,
    )
    op.alter_column(
        "candidate",
        "ra",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=False,
    )
    op.alter_column(
        "beam",
        "dec",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "beam",
        "ra",
        existing_type=sa.Numeric(precision=8, scale=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
