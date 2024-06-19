"""Label service request schemas."""

from fastapi import Query
from pydantic import BaseModel, Field

from ska_src_maltopuft_backend.core.extras import PositiveList
from ska_src_maltopuft_backend.core.schemas import CommonQueryParams

from .css_color import CssColorStr
from .entity import EntityNames


class GetLabelQueryParams(CommonQueryParams):
    """Query parameters for Label model HTTP GET requests."""

    labeller_id: PositiveList[int] = Field(Query(default=[]))
    candidate_id: PositiveList[int] = Field(Query(default=[]))
    entity_id: PositiveList[int] = Field(Query(default=[]))


class CreateLabel(BaseModel):
    """Schema for Label model HTTP POST requests."""

    labeller_id: int = Field(gt=0)
    candidate_id: int = Field(gt=0)
    entity_id: int = Field(gt=0)


class GetEntityQueryParams(CommonQueryParams):
    """Query parameters for Entity model HTTP GET requests."""

    type: list[EntityNames | None] = Field(Query(default=[]))
    css_color: list[CssColorStr | None] = Field(Query(default=[]))


class CreateEntity(BaseModel):
    """Schema for Entity model HTTP POST requests."""

    type: EntityNames
    css_color: CssColorStr
