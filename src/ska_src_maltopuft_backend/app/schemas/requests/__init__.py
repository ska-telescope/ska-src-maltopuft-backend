"""API request models and associated types."""

from src.ska_src_maltopuft_backend.candle.requests import (
    CreateCandidate,
    CreateSPCandidate,
    GetCandidateQueryParams,
    GetSPCandidateQueryParams,
)
from src.ska_src_maltopuft_backend.label.requests import (
    CreateEntity,
    CreateLabel,
    GetEntityQueryParams,
    GetLabelQueryParams,
)
from src.ska_src_maltopuft_backend.user.requests import (
    CreateUser,
    GetUserQueryParams,
)

__all__ = [
    "GetCandidateQueryParams",
    "CreateCandidate",
    "GetSPCandidateQueryParams",
    "CreateSPCandidate",
    "GetEntityQueryParams",
    "CreateEntity",
    "GetLabelQueryParams",
    "CreateLabel",
    "GetUserQueryParams",
    "CreateUser",
]
