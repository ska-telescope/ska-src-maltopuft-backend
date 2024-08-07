"""Label service response schemas."""

from pydantic import BaseModel, ConfigDict, Field, PastDatetime

from ska_src_maltopuft_backend.candle.responses import CandidateNested
from ska_src_maltopuft_backend.core.types import PositiveList
from ska_src_maltopuft_backend.user.responses import User

from .css_color import CssColorStr
from .entity import EntityNames


class Entity(BaseModel):
    """Response model for Entity HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., gt=0)
    type: EntityNames
    css_color: CssColorStr
    created_at: PastDatetime
    updated_at: PastDatetime


class Label(BaseModel):
    """Response model for Label HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    labeller_id: int = Field(gt=0)
    candidate_id: int = Field(gt=0)
    entity_id: int = Field(gt=0)
    created_at: PastDatetime
    updated_at: PastDatetime

    candidate: CandidateNested
    entity: Entity
    labeller: User


class LabelBulk(BaseModel):
    """Response model for bulk create Label requests."""

    model_config = ConfigDict(from_attributes=True)

    ids: PositiveList[int]
