"""Candidate request schemas."""

import datetime as dt
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field, StringConstraints

from .extras import DEC_PATTERN, RA_PATTERN


class GetCandidateQueryParams(BaseModel):
    """Query parameters for Candidate model HTTP GET requests."""

    id: list[Annotated[int, None]] = Field(Query(default=[]))
    dm: list[Annotated[float, None]] = Field(Query(default=[]))
    snr: list[Annotated[float, None]] = Field(Query(default=[]))
    width: list[Annotated[float, None]] = Field(Query(default=[]))
    ra: list[
        (
            Annotated[
                str,
                StringConstraints(
                    strip_whitespace=True,
                    min_length=10,
                    max_length=10,
                    pattern=RA_PATTERN,
                ),
            ]
            | None
        )
    ] = Field(Query(default=[]))
    dec: list[
        (
            Annotated[
                str,
                StringConstraints(
                    strip_whitespace=True,
                    min_length=10,
                    max_length=10,
                    pattern=DEC_PATTERN,
                ),
            ]
            | None
        )
    ] = Field(Query(default=[]))
    created_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))
    updated_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))


class CreateCandidate(BaseModel):
    """Schema for Candidate model HTTP POST requests."""

    dm: float = Field(gt=0)
    snr: float = Field(gt=0)
    width: float = Field(gt=0)
    ra: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=10,
            max_length=10,
            pattern=RA_PATTERN,
        ),
    ]
    dec: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=10,
            max_length=12,
            pattern=DEC_PATTERN,
        ),
    ]


class GetSPCandidateQueryParams(BaseModel):
    """Query parameters for SPCandidate model HTTP Get requests."""

    id: list[Annotated[int, None]] = Field(Query(default=[]))
    data_path: list[
        (Annotated[str, StringConstraints(strip_whitespace=True)] | None)
    ] = Field(Query(default=[]))
    observed_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))
    created_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))
    updated_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))

    candidate_id: list[Annotated[int, None]] = Field(Query(default=[]))


class CreateSPCandidate(BaseModel):
    """Schema for SPCandidate model HTTP POST requests."""

    data_path: Annotated[str, StringConstraints(strip_whitespace=True)]
    observed_at: dt.datetime

    candidate_id: int = Field(gt=0)
