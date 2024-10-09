"""Create entities.

Revision ID: 234732fe6c09
Revises: abac0168c671
Create Date: 2024-10-03 11:44:43.215376

"""

from collections.abc import Sequence

import sqlalchemy as sa
from ska_src_maltopuft_backend.core.database.init_db import deinit_db, init_db

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "234732fe6c09"
down_revision: str | None = "abac0168c671"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Insert initial data."""
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    init_db(db=session)


def downgrade() -> None:
    """Remove initial data."""
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    deinit_db(db=session)
