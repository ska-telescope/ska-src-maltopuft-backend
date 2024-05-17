"""Label service request schemas."""

import datetime as dt
from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, Field, StringConstraints

from .entity import EntityNames


class GetLabelQueryParams(BaseModel):
    """Query parameters for Label model HTTP GET requests."""

    id: list[Annotated[int, None]] = Field(Query(default=[]))
    labeller_id: list[Annotated[int, None]] = Field(Query(default=[]))
    candidate_id: list[Annotated[int, None]] = Field(Query(default=[]))
    entity_id: list[Annotated[int, None]] = Field(Query(default=[]))

    created_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))
    updated_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))


class CreateLabel(BaseModel):
    """Schema for Label model HTTP POST requests."""

    labeller_id: int = Field(gt=0)
    candidate_id: int = Field(gt=0)
    entity_id: int = Field(gt=0)


class GetEntityQueryParams(BaseModel):
    """Query parameters for Entity model HTTP GET requests."""

    id: list[Annotated[int, None]] = Field(Query(default=[]))
    type: list[Annotated[EntityNames, None]] = Field(Query(default=[]))
    css_color: list[
        (
            Annotated[
                str,
                StringConstraints(
                    strip_whitespace=True,
                ),
            ]
            | None
        )
    ] = Field(Query(default=[]))

    created_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))
    updated_at: list[Annotated[dt.datetime, None]] = Field(Query(default=[]))


class CreateEntity(BaseModel):
    """Schema for Entity model HTTP POST requests."""

    type: EntityNames
    css_color: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
        ),
    ]
