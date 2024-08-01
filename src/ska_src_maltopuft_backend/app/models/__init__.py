"""MALTOPUFT database models."""

from ska_src_maltopuft_backend.candle.models import Candidate, SPCandidate
from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.label.models import Entity, Label
from ska_src_maltopuft_backend.observation.models import (
    Beam,
    CoherentBeamConfig,
    Host,
    MeerkatScheduleBlock,
    Observation,
    ScheduleBlock,
    TilingConfig,
)
from ska_src_maltopuft_backend.user.models import User

__all__ = [
    "Base",
    "User",
    "Candidate",
    "SPCandidate",
    "Entity",
    "Label",
    "ScheduleBlock",
    "MeerkatScheduleBlock",
    "CoherentBeamConfig",
    "Observation",
    "TilingConfig",
    "Beam",
    "Host",
]
