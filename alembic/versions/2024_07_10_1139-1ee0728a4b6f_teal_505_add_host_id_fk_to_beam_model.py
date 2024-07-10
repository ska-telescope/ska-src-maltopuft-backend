"""TEAL-505: Add host_id FK to Beam model.

Revision ID: 1ee0728a4b6f
Revises: fc4d99bbdf16
Create Date: 2024-07-10 11:39:28.436747

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "1ee0728a4b6f"
down_revision: str | None = "fc4d99bbdf16"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add Beam.host_id foreign key."""
    op.add_column("beam", sa.Column("host_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        op.f("beam_host_id_fkey"), "beam", "host", ["host_id"], ["id"],
    )


def downgrade() -> None:
    """Drop Beam.host_id foreign key."""
    op.drop_constraint(op.f("beam_host_id_fkey"), "beam", type_="foreignkey")
    op.drop_column("beam", "host_id")
