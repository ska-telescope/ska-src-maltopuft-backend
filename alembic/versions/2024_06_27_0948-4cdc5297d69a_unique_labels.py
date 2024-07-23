"""Unique labels.

Revision ID: 4cdc5297d69a
Revises: 5f2f21c8df0c
Create Date: 2024-06-27 09:48:33.963956

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4cdc5297d69a"
down_revision: str | None = "5f2f21c8df0c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create unique constraint for Label candidate_id and labeller_id."""
    op.create_unique_constraint(
        op.f("label_labeller_id_key"),
        "label",
        ["labeller_id", "candidate_id"],
    )


def downgrade() -> None:
    """Drop unique constraint for Label candidate_id and labeller_id."""
    op.drop_constraint(
        op.f("label_labeller_id_key"), "label", type_="unique",
    )
