"""Add SPCandidate table.

Revision ID: 5f542c987eb8
Revises: b25703735700
Create Date: 2024-05-13 18:15:14.422522

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5f542c987eb8"
down_revision: str | None = "b25703735700"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create SPCandidate table."""
    op.create_table(
        "sp_candidate",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("data_path", sa.String(), nullable=False),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
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
        sa.ForeignKeyConstraint(
            ["candidate_id"],
            ["candidate.id"],
            name=op.f("sp_candidate_candidate_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("sp_candidate_pkey")),
    )


def downgrade() -> None:
    """Drop SPCandidate table."""
    op.drop_table("sp_candidate")
