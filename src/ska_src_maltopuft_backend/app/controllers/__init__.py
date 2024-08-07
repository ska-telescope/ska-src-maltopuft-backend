"""MALTOPUFT data controllers."""

from ska_src_maltopuft_backend.candle.controller import (
    CandidateController,
    SPCandidateController,
)
from ska_src_maltopuft_backend.catalogue.controller import (
    KnownPulsarController,
)
from ska_src_maltopuft_backend.label.controller import (
    EntityController,
    LabelController,
)
from ska_src_maltopuft_backend.observation.controller import (
    ObservationController,
)
from ska_src_maltopuft_backend.user.controller import UserController

__all__ = [
    "CandidateController",
    "SPCandidateController",
    "EntityController",
    "LabelController",
    "ObservationController",
    "UserController",
    "KnownPulsarController",
]
