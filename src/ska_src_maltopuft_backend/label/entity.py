"""Types of entity which can be used as candidate labels."""

from enum import Enum

import sqlalchemy as sa

from src.ska_src_maltopuft_backend.core.database import Base


class EntityNames(str, Enum):
    """Names of entities which can be assigned as candidate labels."""

    RFI = "RFI"
    SINGLE_PULSE = "SINGLE_PULSE"
    PERIODIC_PULSE = "PERIODIC_PULSE"


EntityNamesDBEnum: sa.Enum = sa.Enum(
    EntityNames,
    # Ensure SQLAlchemy persists Enum values, rather than Enum keys
    values_callable=lambda obj: [o.value for o in obj],
    name="type",
    create_constraint=True,
    metadata=Base.metadata,
    validate_strings=True,
)
