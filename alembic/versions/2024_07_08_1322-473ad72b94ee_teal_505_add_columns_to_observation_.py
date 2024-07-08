"""TEAL-505: Add columns to Observation model.

Revision ID: 473ad72b94ee
Revises: 6fed15bc581a
Create Date: 2024-07-08 13:22:51.479524

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "473ad72b94ee"
down_revision: str | None = "6fed15bc581a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add more columns to Observation table."""
    op.add_column(
        "observation",
        sa.Column("dataproduct_type", sa.String(), nullable=True),
    )
    op.add_column(
        "observation",
        sa.Column("dataproduct_subtype", sa.String(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("calib_level", sa.Integer(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("obs_id", sa.String(), nullable=True),
    )
    op.add_column("observation", sa.Column("s_ra", sa.String(), nullable=True))
    op.add_column(
        "observation", sa.Column("s_dec", sa.String(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("t_min", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("t_max", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("t_exptime", sa.Interval(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("t_resolution", sa.Float(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("em_min", sa.Float(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("em_max", sa.Float(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("em_resolution", sa.Float(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("em_xel", sa.Integer(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("pol_states", sa.String(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("pol_xel", sa.Integer(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("facility_name", sa.String(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("instrument_name", sa.String(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("target_name", sa.String(), nullable=True),
    )
    op.add_column(
        "observation", sa.Column("target_class", sa.String(), nullable=True),
    )


def downgrade() -> None:
    """Drop additional tables from Observation table."""
    op.drop_column("observation", "target_class")
    op.drop_column("observation", "target_name")
    op.drop_column("observation", "instrument_name")
    op.drop_column("observation", "facility_name")
    op.drop_column("observation", "pol_xel")
    op.drop_column("observation", "pol_states")
    op.drop_column("observation", "em_xel")
    op.drop_column("observation", "em_resolution")
    op.drop_column("observation", "em_max")
    op.drop_column("observation", "em_min")
    op.drop_column("observation", "t_resolution")
    op.drop_column("observation", "t_exptime")
    op.drop_column("observation", "t_max")
    op.drop_column("observation", "t_min")
    op.drop_column("observation", "s_dec")
    op.drop_column("observation", "s_ra")
    op.drop_column("observation", "obs_id")
    op.drop_column("observation", "calib_level")
    op.drop_column("observation", "dataproduct_subtype")
    op.drop_column("observation", "dataproduct_type")
    # ### end Alembic commands ###
