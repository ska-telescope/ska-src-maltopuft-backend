"""TEAL-505: Add beam_id FK to Candidate model.

Revision ID: fc4d99bbdf16
Revises: d683ddaa5054
Create Date: 2024-07-09 16:13:27.113066

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "fc4d99bbdf16"
down_revision: str | None = "d683ddaa5054"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add Candidate.beam_id foreign key."""
    op.add_column(
        "candidate", sa.Column("beam_id", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        op.f("candidate_beam_id_fkey"),
        "candidate",
        "beam",
        ["beam_id"],
        ["id"],
    )


def downgrade() -> None:
    """Drop Candidate.beam_id foreign key."""
    op.drop_constraint(
        op.f("candidate_beam_id_fkey"), "candidate", type_="foreignkey",
    )
    op.drop_column("candidate", "beam_id")
