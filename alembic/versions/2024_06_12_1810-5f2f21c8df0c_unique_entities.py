"""Unique entities.

Revision ID: 5f2f21c8df0c
Revises: ca0fac6d1f6a
Create Date: 2024-06-12 18:10:44.085339

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5f2f21c8df0c"
down_revision: str | None = "ca0fac6d1f6a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add unique constraint to entity.type and entity.css_color."""
    op.create_unique_constraint(
        op.f("entity_css_color_key"), "entity", ["css_color"],
    )
    op.create_unique_constraint(op.f("entity_type_key"), "entity", ["type"])


def downgrade() -> None:
    """Remove unique constraint to entity.type and entity.css_color."""
    op.drop_constraint(op.f("entity_type_key"), "entity", type_="unique")
    op.drop_constraint(op.f("entity_css_color_key"), "entity", type_="unique")
