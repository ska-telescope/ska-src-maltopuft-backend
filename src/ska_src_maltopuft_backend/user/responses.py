"""User response schemas."""

from typing import Annotated

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    PastDatetime,
    StringConstraints,
)


class User(BaseModel):
    """Response model for HTTP GET/POST requests."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(gt=0)
    uuid: UUID4
    username: Annotated[str, StringConstraints(strip_whitespace=True)]
    is_admin: bool
    created_at: PastDatetime
    updated_at: PastDatetime
