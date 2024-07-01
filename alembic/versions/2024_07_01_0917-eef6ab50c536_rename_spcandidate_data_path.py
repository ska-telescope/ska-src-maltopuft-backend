"""Rename SPCandidate.data_path to SPCandidate.plot_path.

Revision ID: eef6ab50c536
Revises: 4cdc5297d69a
Create Date: 2024-07-01 09:17:40.114992

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eef6ab50c536"
down_revision: str | None = "4cdc5297d69a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Rename SPCandidate.data_path to SPCandidate.plot_path."""
    op.add_column(
        "sp_candidate", sa.Column("plot_path", sa.String(), nullable=False),
    )
    op.drop_column("sp_candidate", "data_path")


def downgrade() -> None:
    """Revert rename SPCandidate.data_path to SPCandidate.plot_path."""
    op.add_column(
        "sp_candidate",
        sa.Column(
            "data_path", sa.VARCHAR(), autoincrement=False, nullable=False,
        ),
    )
    op.drop_column("sp_candidate", "plot_path")
