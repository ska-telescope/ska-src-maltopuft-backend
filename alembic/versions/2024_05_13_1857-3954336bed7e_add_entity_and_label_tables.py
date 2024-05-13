"""Add Entity and Label tables.

Revision ID: 3954336bed7e
Revises: 5f542c987eb8
Create Date: 2024-05-13 18:57:13.638194

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from src.ska_src_maltopuft_backend.candle.entity import EntityNamesDBEnum

# revision identifiers, used by Alembic.
revision: str = "3954336bed7e"
down_revision: str | None = "5f542c987eb8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add Entity and Label tables."""
    EntityNamesDBEnum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "entity",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type", EntityNamesDBEnum, autoincrement=False, nullable=False),
        sa.Column("css_color", sa.Unicode(length=7), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("entity_pkey")),
    )
    op.create_table(
        "label",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("labeller_id", sa.Integer(), nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
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
            name=op.f("label_candidate_id_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["entity_id"], ["entity.id"], name=op.f("label_entity_id_fkey"),
        ),
        sa.ForeignKeyConstraint(
            ["labeller_id"], ["user.id"], name=op.f("label_labeller_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("label_pkey")),
    )


def downgrade() -> None:
    """Add Entity and Label tables."""
    op.drop_table("label")
    op.drop_table("entity")
    EntityNamesDBEnum.drop(op.get_bind(), checkfirst=True)
