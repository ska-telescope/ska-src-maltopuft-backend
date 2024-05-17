"""Label service response schemas."""

import datetime as dt

from pydantic import BaseModel, ConfigDict, Field

from src.ska_src_maltopuft_backend.candle.responses import CandidateNested
from src.ska_src_maltopuft_backend.user.responses import User

from .entity import EntityNames


class Entity(BaseModel):
    """Response model for Entity HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    type: EntityNames
    css_color: str
    created_at: dt.datetime
    updated_at: dt.datetime


class Label(BaseModel):
    """Response model for Label HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    labeller_id: int = Field(gt=0)
    candidate_id: int = Field(gt=0)
    entity_id: int = Field(gt=0)
    created_at: dt.datetime
    updated_at: dt.datetime

    candidate: CandidateNested
    entity: Entity
    labeller: User
