"""Rename SPCandidate.data_path to SPCandidate.plot_path.

Revision ID: eef6ab50c536
Revises: 4cdc5297d69a
Create Date: 2024-07-01 09:17:40.114992

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eef6ab50c536"
down_revision: str | None = "4cdc5297d69a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Rename SPCandidate.data_path to SPCandidate.plot_path."""
    op.alter_column(
        "sp_candidate",
        "data_path",
        nullable=False,
        new_column_name="plot_path",
    )


def downgrade() -> None:
    """Revert rename SPCandidate.data_path to SPCandidate.plot_path."""
    op.alter_column(
        "sp_candidate",
        "plot_path",
        nullable=False,
        new_column_name="data_path",
    )
