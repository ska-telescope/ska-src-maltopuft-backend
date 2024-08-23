"""Add pos attribute to Candidate and KnownPulsar models

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
    """Add pos attribute to Candidate and KnownPulsar models."""
    op.add_column("candidate", sa.Column("pos", sa.String(), nullable=False))
    op.add_column("known_pulsar", sa.Column("pos", sa.String(), nullable=True))


def downgrade() -> None:
    """Drop pos attribute from Candidate and KnownPulsar models."""
    op.drop_column("known_pulsar", "pos")
    op.drop_column("candidate", "pos")
