"""Add pos attribute to Candidate model

Revision ID: 572423489f3f
Revises: e84e368b1f23
Create Date: 2024-08-07 10:56:38.558543
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "572423489f3f"
down_revision: str | None = "e84e368b1f23"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add pos attribute to Candidate model."""
    op.add_column("candidate", sa.Column("pos", sa.String(), nullable=False))


def downgrade() -> None:
    """Drop pos attribute from Candidate model."""
    op.drop_column("candidate", "pos")
