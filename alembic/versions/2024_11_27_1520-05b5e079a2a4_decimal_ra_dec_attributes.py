"""Decimal ra, dec attributes

Revision ID: 05b5e079a2a4
Revises: 8f80e6af6846
Create Date: 2024-11-27 15:20:14.368167

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "05b5e079a2a4"
down_revision: str | None = "8f80e6af6846"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Update the ra and dec column types from Unicode to REAL."""
    op.alter_column(
        "beam",
        "ra",
        existing_type=sa.VARCHAR(),
        type_=sa.REAL(precision=5),
        existing_nullable=False,
        postgresql_using="ra::text::real",
    )
    op.alter_column(
        "beam",
        "dec",
        existing_type=sa.VARCHAR(),
        type_=sa.REAL(precision=5),
        existing_nullable=False,
        postgresql_using="dec::text::real",
    )
    op.alter_column(
        "candidate",
        "ra",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.REAL(precision=5),
        existing_nullable=False,
        postgresql_using="ra::text::real",
    )
    op.alter_column(
        "candidate",
        "dec",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.REAL(precision=5),
        existing_nullable=False,
        postgresql_using="dec::text::real",
    )
    op.alter_column(
        "coherent_beam_config",
        "fraction_overlap",
        existing_type=sa.Numeric(),
        type_=sa.REAL(precision=5),
        existing_nullable=False,
        postgresql_using="fraction_overlap::text::real",
    )
    op.alter_column(
        "known_pulsar",
        "ra",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.REAL(precision=5),
        existing_nullable=True,
        postgresql_using="ra::text::real",
    )
    op.alter_column(
        "known_pulsar",
        "dec",
        existing_type=sa.VARCHAR(length=12),
        type_=sa.REAL(precision=5),
        existing_nullable=True,
        postgresql_using="dec::text::real",
    )
    op.alter_column(
        "observation",
        "s_ra",
        existing_type=sa.VARCHAR(),
        type_=sa.REAL(precision=5),
        nullable=False,
        postgresql_using="s_ra::text::real",
    )
    op.alter_column(
        "observation",
        "s_dec",
        existing_type=sa.VARCHAR(),
        type_=sa.REAL(precision=5),
        nullable=False,
        postgresql_using="s_dec::text::real",
    )
    op.alter_column(
        "tiling_config",
        "ra",
        existing_type=sa.VARCHAR(),
        type_=sa.REAL(precision=5),
        existing_nullable=False,
        postgresql_using="ra::text::real",
    )
    op.alter_column(
        "tiling_config",
        "dec",
        existing_type=sa.VARCHAR(),
        type_=sa.REAL(precision=5),
        existing_nullable=False,
        postgresql_using="dec::text::real",
    )


def downgrade() -> None:
    """Update the ra and dec column types from REAL to Unicode."""
    op.alter_column(
        "tiling_config",
        "dec",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "tiling_config",
        "ra",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "observation",
        "s_dec",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "observation",
        "s_ra",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "known_pulsar",
        "dec",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=True,
    )
    op.alter_column(
        "known_pulsar",
        "ra",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=True,
    )
    op.alter_column(
        "coherent_beam_config",
        "fraction_overlap",
        existing_type=sa.REAL(precision=5),
        type_=sa.Numeric(),
        existing_nullable=False,
    )
    op.alter_column(
        "candidate",
        "dec",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=False,
    )
    op.alter_column(
        "candidate",
        "ra",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(length=12),
        existing_nullable=False,
    )
    op.alter_column(
        "beam",
        "dec",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "beam",
        "ra",
        existing_type=sa.REAL(precision=5),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
