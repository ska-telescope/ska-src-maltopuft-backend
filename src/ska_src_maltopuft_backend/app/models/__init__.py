"""MALTOPUFT database models."""

from ska_src_maltopuft_backend.candle.models import Candidate, SPCandidate
from ska_src_maltopuft_backend.core.database import Base
from ska_src_maltopuft_backend.label.models import Entity, Label
from ska_src_maltopuft_backend.user.models import User

__all__ = ["Base", "User", "Candidate", "SPCandidate", "Entity", "Label"]
