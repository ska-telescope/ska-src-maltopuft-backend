"""Move observed_at to candidate table

Revision ID: 6d975c10c6ce
Revises: 234732fe6c09
Create Date: 2024-10-25 14:02:48.951584

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "6d975c10c6ce"
down_revision: str | None = "234732fe6c09"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Move observed_at from sp_candidate to candidate."""
    op.add_column(
        "candidate", sa.Column("observed_at", sa.DateTime(), nullable=False),
    )
    op.create_unique_constraint(
        op.f("candidate_observed_at_beam_id_key"),
        "candidate",
        ["observed_at", "beam_id"],
    )
    op.create_unique_constraint(
        op.f("sp_candidate_plot_path_key"), "sp_candidate", ["plot_path"],
    )
    op.drop_column("sp_candidate", "observed_at")


def downgrade() -> None:
    """Move observed_at from candidate to sp_candidate."""
    op.add_column(
        "sp_candidate",
        sa.Column(
            "observed_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_constraint(
        op.f("sp_candidate_plot_path_key"), "sp_candidate", type_="unique",
    )
    op.drop_constraint(
        op.f("candidate_observed_at_beam_id_key"), "candidate", type_="unique",
    )
    op.drop_column("candidate", "observed_at")
