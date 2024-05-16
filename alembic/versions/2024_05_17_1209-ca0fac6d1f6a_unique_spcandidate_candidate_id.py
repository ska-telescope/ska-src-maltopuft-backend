"""Unique SPCandidate.candidate_id.

Revision ID: ca0fac6d1f6a
Revises: 3954336bed7e
Create Date: 2024-05-17 12:09:32.541695

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ca0fac6d1f6a"
down_revision: str | None = "3954336bed7e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add sp_candidate.candidate_id unique constraint."""
    op.create_unique_constraint(
        op.f("sp_candidate_candidate_id_key"), "sp_candidate", ["candidate_id"],
    )


def downgrade() -> None:
    """Remove sp_candidate.candidate_id unique constraint."""
    op.drop_constraint(
        op.f("sp_candidate_candidate_id_key"), "sp_candidate", type_="unique",
    )
