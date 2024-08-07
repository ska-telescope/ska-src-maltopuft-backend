"""Pulsar catalogue models

Revision ID: e84e368b1f23
Revises: 1ee0728a4b6f
Create Date: 2024-08-07 09:31:23.532320

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e84e368b1f23"
down_revision: str | None = "1ee0728a4b6f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create external pulsar catalogue models."""
    op.create_table(
        "catalogue",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
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
        sa.PrimaryKeyConstraint("id", name=op.f("catalogue_pkey")),
        sa.UniqueConstraint("url", name=op.f("catalogue_url_key")),
    )
    op.create_table(
        "catalogue_visit",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("visited_at", sa.DateTime(), nullable=False),
        sa.Column("catalogue_id", sa.Integer(), nullable=False),
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
            ["catalogue_id"],
            ["catalogue.id"],
            name=op.f("catalogue_visit_catalogue_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("catalogue_visit_pkey")),
    )
    op.create_table(
        "known_pulsar",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("dm", sa.Float(), nullable=True),
        sa.Column("width", sa.Float(), nullable=True),
        sa.Column("ra", sa.Unicode(length=12), nullable=True),
        sa.Column("dec", sa.Unicode(length=12), nullable=True),
        sa.Column("period", sa.Float(), nullable=True),
        sa.Column("catalogue_id", sa.Integer(), nullable=False),
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
            ["catalogue_id"],
            ["catalogue.id"],
            name=op.f("known_pulsar_catalogue_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("known_pulsar_pkey")),
        sa.UniqueConstraint("name", name=op.f("known_pulsar_name_key")),
    )


def downgrade() -> None:
    """Drop external pulsar catalogue models."""
    op.drop_table("known_pulsar")
    op.drop_table("catalogue_visit")
    op.drop_table("catalogue")
