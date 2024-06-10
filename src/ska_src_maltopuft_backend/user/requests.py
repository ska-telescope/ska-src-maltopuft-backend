"""User request schemas."""

from typing import Annotated
from uuid import uuid4

from fastapi import Query
from pydantic import UUID4, BaseModel, EmailStr, Field, StringConstraints

from src.ska_src_maltopuft_backend.core.schemas import CommonQueryParams


class GetUser(BaseModel):
    """Attributes for User model GET requests."""

    id: int | None = Field(default=None, gt=0)
    uuid: UUID4 | None = None
    email: EmailStr | None = None
    username: (
        Annotated[str, StringConstraints(strip_whitespace=True)] | None
    ) = None
    is_admin: bool | None = None


class CreateUser(BaseModel):
    """Attributes for User model POST requests."""

    uuid: UUID4 = Field(default_factory=uuid4)
    email: EmailStr
    username: Annotated[str, StringConstraints(strip_whitespace=True)]
    is_admin: bool = False


class GetUserQueryParams(CommonQueryParams):
    """Query parameters for User model GET requests."""

    uuid: list[Annotated[UUID4, None]] = Field(Query(default=[]))
    email: list[Annotated[EmailStr, None]] = Field(Query(default=[]))
    username: list[
        (Annotated[str, StringConstraints(strip_whitespace=True)] | None)
    ] = Field(Query(default=[]))
    is_admin: bool | None = Field(Query(default=None))
