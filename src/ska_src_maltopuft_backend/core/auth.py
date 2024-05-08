"""Middleware to verify user authorisation."""

import logging

import jwt
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from src.ska_src_maltopuft_backend.core.exceptions import MaltopuftError
from src.ska_src_maltopuft_backend.core.schemas import (
    AccessToken,
    AuthenticatedUser,
)

logger = logging.getLogger(__name__)


class BearerTokenAuthBackend(AuthenticationBackend):
    """Injects authenticated user information into the HTTP request.

    Uses the ska-src-auth-api to request a token exchange for the maltopuft
    backend from a base64 encoded access token extracted from an authorization
    header of the form "Bearer <token>".
    """

    # pylint: disable=R0903

    def _get_token_from_header(self, auth_header: str) -> str:
        """Extract bearer token from Authorization header.

        Looks for a string of the form "Bearer <token>" in a request's
        "Authorization" header where <token> is a base64 encoded string.
        Successful token decoding is deferred to the src-ska-auth-api.

        Args:
            auth_header (str): The authorization header.

        Returns:
            str | None: A base64 encoded access token with "auth-api" audience
            ready for exchange. If no authorization header is present in the
            request then nothing is returned.

        """
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            msg = "Invalid or unsupported authentication scheme used."
            raise AuthenticationError(msg)
        return token

    def _decode_jwt(self, token: str) -> AccessToken:
        """Decodes a base64 encoded JWT.

        Args:
            token (string): The base64 encoded access token.

        Returns:
            AccessToken: A decoded access token.

        """
        return AccessToken(
            **jwt.decode(token, options={"verify_signature": False}),
        )

    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> tuple[AuthCredentials, AuthenticatedUser] | None:
        """User authentication dependency.

        Args:
            conn (HTTPConnection): The incoming HTTP request.

        Returns:
            tuple[AuthCredentials, AuthenticatedUser] | None:
            `AuthCredentials` is a list of user groups to be used in
            authorisation and `AuthenticatedUser` is an object containing
            basic user information. The returned tuple is injected into
            the request.

        """
        auth_header = conn.headers.get("Authorization")

        if auth_header is None:
            # Return UnauthenticatedUser
            return None

        token = self._get_token_from_header(
            auth_header=auth_header,
        )

        # For now, just return the decoded access_token with auth-api audience
        decoded_token = self._decode_jwt(token=token)

        return (
            AuthCredentials(decoded_token.groups),
            AuthenticatedUser(**decoded_token.model_dump()),
        )

    def on_auth_error(
        self,
        exc: AuthenticationError,
    ) -> JSONResponse:
        """Re-raises AuthBackend exceptions as HTTPExceptions."""
        status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse(
            status_code=status_code,
            content={
                "message": (
                    exc.message
                    if isinstance(exc, MaltopuftError)
                    else str(exc)
                ),
                "status_code": status_code,
            },
        )
