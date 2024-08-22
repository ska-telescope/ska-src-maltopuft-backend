"""Authentication package."""

from .auth_backend import BearerTokenAuthBackend
from .authenticated import Authenticated
from .authorization_checker import AuthorizationChecker
from .exceptions import (
    AuthenticationRequiredError,
    InvalidAudienceError,
    PermissionDeniedError,
)
from .schemas import AccessToken, AuthenticatedUser, UserGroups

__all__ = [
    "BearerTokenAuthBackend",
    "Authenticated",
    "AuthorizationChecker",
    "PermissionDeniedError",
    "InvalidAudienceError",
    "AuthenticationRequiredError",
    "AccessToken",
    "UserGroups",
    "AuthenticatedUser",
]
