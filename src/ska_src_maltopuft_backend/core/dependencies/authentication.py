"""Dependency to check user is authenticated."""

from fastapi import Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.ska_src_maltopuft_backend.core.exceptions import MaltopuftError


class AuthenticationRequiredError(MaltopuftError):
    """Raised when an authenticated user makes a request that requires
    authentication.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication required"


class Authenticated:
    """Dependency which checks user is authenticated."""

    def __init__(
        self,
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(
            HTTPBearer(auto_error=False),
        ),
    ) -> None:
        """Initialisation only succeeds if a user is authenticated."""
        if not token:
            raise AuthenticationRequiredError

        if not request.user.is_authenticated:
            raise AuthenticationRequiredError
