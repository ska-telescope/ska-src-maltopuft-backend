"""Candidate request schemas."""

from typing import Annotated

from fastapi import Query
from pydantic import (
    BaseModel,
    Field,
    PastDatetime,
    PositiveInt,
    StringConstraints,
)

from ska_src_maltopuft_backend.core.extras import PositiveList
from ska_src_maltopuft_backend.core.schemas import CommonQueryParams

from .extras import DecStr, RaStr


class GetCandidateQueryParams(CommonQueryParams):
    """Query parameters for Candidate model HTTP GET requests."""

    dm: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    snr: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    width: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    ra: list[RaStr | None] = Field(Query(default=[]))
    dec: list[DecStr | None] = Field(Query(default=[]))
    beam_id: Annotated[PositiveList[int], None] = Field(Query(default=[]))


class CreateCandidate(BaseModel):
    """Schema for Candidate model HTTP POST requests."""

    dm: float = Field(gt=0)
    snr: float = Field(gt=0)
    width: float = Field(gt=0)
    ra: RaStr
    dec: DecStr
    beam_id: PositiveInt


class GetSPCandidateQueryParams(CommonQueryParams):
    """Query parameters for SPCandidate model HTTP Get requests."""

    plot_path: list[
        (Annotated[str, StringConstraints(strip_whitespace=True)] | None)
    ] = Field(Query(default=[]))
    observed_at: list[Annotated[PastDatetime, None]] = Field(Query(default=[]))

    candidate_id: Annotated[PositiveList[int], None] = Field(Query(default=[]))


class CreateSPCandidate(BaseModel):
    """Schema for SPCandidate model HTTP POST requests."""

    plot_path: Annotated[str, StringConstraints(strip_whitespace=True)]
    observed_at: PastDatetime

    candidate_id: int = Field(gt=0)
