"""MALTOPUFT CRUD repositories."""

from ska_src_maltopuft_backend.candle.repository import (
    CandidateRepository,
    SPCandidateRepository,
)
from ska_src_maltopuft_backend.catalogue.repository import (
    KnownPulsarRepository,
)
from ska_src_maltopuft_backend.label.repository import (
    EntityRepository,
    LabelRepository,
)
from ska_src_maltopuft_backend.observation.repository import (
    ObservationRepository,
)
from ska_src_maltopuft_backend.user.repository import UserRepository

__all__ = [
    "CandidateRepository",
    "SPCandidateRepository",
    "EntityRepository",
    "LabelRepository",
    "ObservationRepository",
    "UserRepository",
    "KnownPulsarRepository",
]
