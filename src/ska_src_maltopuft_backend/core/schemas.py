"""Schemas used by src.ska_src_maltopuft_backend.core sub-package."""

from enum import Enum

from pydantic import UUID4, BaseModel, Field, HttpUrl
from pydantic.dataclasses import dataclass
from starlette.authentication import BaseUser


class AccessToken(BaseModel):
    """Decoded access token schema."""

    sub: UUID4
    iss: HttpUrl
    groups: list[str]
    preferred_username: str
    organisation_name: str
    client_id: UUID4
    aud: str
    scope: str
    name: str
    exp: int = Field(gt=0)
    iat: int = Field(gt=0)
    jti: UUID4


class UserGroups(str, Enum):
    """User group definitions."""

    SRC = "src"
    MALTOPUFT = "src/maltopuft"
    MALTOPUFT_USER = "src/maltopuft/user"
    MALTOPUFT_ADMIN = "src/maltopuft/admin"


@dataclass
class AuthenticatedUser(BaseUser):
    """Logged in (authenticated) user schema."""

    # pylint: disable=W0223

    sub: UUID4
    name: str
    preferred_username: str
    is_authenticated: bool = True


@dataclass
class UnauthenticatedUser(BaseUser):
    """Unauthenticated user schema."""

    # pylint: disable=W0223

    name: str = ""
    is_authenticated: bool = False
