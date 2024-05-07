"""Dependency to check user is authenticated."""

import logging

from fastapi import Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.ska_src_maltopuft_backend.core.exceptions import MaltopuftError

log = logging.getLogger(__name__)


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

        try:
            is_authenticated = request.user.is_authenticated
        except AttributeError as exc:
            log.exception(
                "Received request with valid token but missing user "
                "information.",
            )
            raise AuthenticationRequiredError from exc

        if not is_authenticated:
            raise AuthenticationRequiredError
