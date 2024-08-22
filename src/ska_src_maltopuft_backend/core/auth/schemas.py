"""Schemas used by auth sub-package."""

from enum import Enum

from pydantic import UUID4, BaseModel, HttpUrl, PositiveInt
from starlette.authentication import SimpleUser

from ska_src_maltopuft_backend.app.schemas.responses import User


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
    exp: PositiveInt
    iat: PositiveInt
    jti: UUID4


class UserGroups(str, Enum):
    """User group definitions."""

    SRC = "src"
    MALTOPUFT = "src/maltopuft"
    MALTOPUFT_USER = "src/maltopuft/user"
    MALTOPUFT_ADMIN = "src/maltopuft/admin"


class AuthenticatedUser(User, SimpleUser):
    """Logged in (authenticated) user schema."""

    # pylint: disable=W0223

    is_authenticated: bool = True
