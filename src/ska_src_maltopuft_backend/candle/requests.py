"""Candidate request schemas."""

from typing import Annotated

from fastapi import Query
from pydantic import (
    BaseModel,
    Field,
    PastDatetime,
    PositiveFloat,
    PositiveInt,
    StringConstraints,
)

from ska_src_maltopuft_backend.core.schemas import (
    CommonQueryParams,
    RaDecPositionBase,
    RaDecPositionQueryParameters,
)
from ska_src_maltopuft_backend.core.types import PositiveList


class GetCandidateQueryParams(CommonQueryParams, RaDecPositionQueryParameters):
    """Query parameters for Candidate model HTTP GET requests."""

    dm: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    snr: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    width: Annotated[PositiveList[float], None] = Field(Query(default=[]))
    observed_at: list[Annotated[PastDatetime, None]] = Field(Query(default=[]))
    beam_id: Annotated[PositiveList[int], None] = Field(Query(default=[]))


class CreateCandidate(RaDecPositionBase):
    """Schema for Candidate model HTTP POST requests."""

    dm: PositiveFloat
    snr: PositiveFloat
    width: PositiveFloat
    observed_at: PastDatetime
    beam_id: PositiveInt


class GetSPCandidateQueryParams(CommonQueryParams):
    """Query parameters for SPCandidate model HTTP Get requests."""

    plot_path: list[
        (Annotated[str, StringConstraints(strip_whitespace=True)] | None)
    ] = Field(Query(default=[]))

    candidate_id: Annotated[PositiveList[int], None] = Field(Query(default=[]))

    latest: bool | None = False


class CreateSPCandidate(BaseModel):
    """Schema for SPCandidate model HTTP POST requests."""

    plot_path: Annotated[str, StringConstraints(strip_whitespace=True)]

    candidate_id: PositiveInt
