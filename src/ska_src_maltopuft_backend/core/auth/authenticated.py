"""Dependency to check user is authenticated."""

import logging

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ska_src_maltopuft_backend.core.config import settings

from .exceptions import AuthenticationRequiredError

log = logging.getLogger(__name__)


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
        if not settings.AUTH_ENABLED:
            return

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
