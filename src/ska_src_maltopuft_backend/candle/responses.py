"""Candidate response schemas."""

import datetime as dt
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from .extras import DEC_PATTERN, RA_PATTERN


class Candidate(BaseModel):
    """Response model for Candidate HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
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
    created_at: dt.datetime
    updated_at: dt.datetime


class SPCandidate(BaseModel):
    """Response model for SPCandidate HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    data_path: str
    observed_at: dt.datetime
    candidate_id: int = Field(gt=0)
    created_at: dt.datetime
    updated_at: dt.datetime


class CandidateNested(Candidate):
    """Nest single pulse candidate under candidate if it exists."""

    sp_candidate: SPCandidate | None


class SPCandidateNested(SPCandidate):
    """Nest candidate under single pulse candidate."""

    candidate: Candidate
