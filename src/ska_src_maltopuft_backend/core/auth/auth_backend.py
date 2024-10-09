"""Middleware to verify user authorisation."""

import logging
from typing import Any

import httpx
import jwt
import sqlalchemy as sa
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from ska_src_maltopuft_backend.app.schemas.requests import CreateUser
from ska_src_maltopuft_backend.core.config import settings
from ska_src_maltopuft_backend.core.exceptions import MaltopuftError
from ska_src_maltopuft_backend.core.factory import Factory

from .exceptions import InvalidAudienceError
from .schemas import AccessToken, AuthenticatedUser, UserGroups

logger = logging.getLogger(__name__)


class BearerTokenAuthBackend(AuthenticationBackend):
    """Injects authenticated user information into the HTTP request.

    Uses the ska-src-auth-api to request a token exchange for the maltopuft
    backend from a base64 encoded access token extracted from an authorization
    header of the form "Bearer <token>".

    If the AUTH_ENABLED environment variable is set to False, then a test
    admin user is created and injected into the request. This setting should
    not be used in production.
    """

    # pylint: disable=R0903

    def __init__(self, db: Session) -> None:
        """Initialises the transactional database connection and user
        controller.
        """
        self.db = db
        self.user_controller = Factory().get_user_controller()

    def _get_token_from_header(self, auth_header: str) -> str:
        """Extract bearer token from Authorization header.

        Looks for a string of the form "Bearer <token>" in a request's
        "Authorization" header where <token> is a base64 encoded string.

        Args:
            auth_header (str): The authorization header.

        Returns:
            str: A base64 encoded access token with "auth-api" audience
            ready for exchange. If no authorization header is present in the
            request then nothing is returned.

        """
        try:
            scheme, token = auth_header.split()
        except ValueError as exc:
            msg = "Invalid or unsupported authentication scheme used."
            raise AuthenticationError(msg) from exc

        if scheme.lower() != "bearer":
            msg = "Invalid or unsupported authentication scheme used."
            raise AuthenticationError(msg)
        return token

    def _do_exchange_token(self, token: str) -> str:
        """Exchange a token with authn-api audience for one with maltopuft-api
        audience.
        """
        exchange_uri = (
            f"{settings.AUTHN_API_URL}"
            "/token/exchange"
            f"/{settings.MALTOPUFT_AUDIENCE}"
        )
        response = httpx.get(
            exchange_uri,
            params={"access_token": token},
        )
        if response.status_code != status.HTTP_200_OK:
            msg = "Attempt to exchange auth token failed."
            raise AuthenticationError(msg)

        return response.json().get("access_token")

    def _decode_jwt(self, token: str) -> AccessToken:
        """Decodes a base64 encoded JWT.

        Args:
            token (string): The base64 encoded Access token.

        Returns:
            IDToken: A decoded Access token.

        """
        decoded = jwt.decode(token, options={"verify_signature": False})
        return AccessToken(**decoded)

    async def _get_or_create_test_admin_user(self) -> dict[str, Any]:
        """Get or create a test user."""
        user = await self.user_controller.repository.get_unique_by(
            db=self.db,
            field="username",
            value="admin",
        )
        if not user:
            user_data = {
                "username": "admin",
                "is_admin": True,
            }
            user = await self.user_controller.create(
                db=self.db,
                attributes=CreateUser(**user_data).model_dump(),
            )
        return {
            c.key: getattr(user, c.key)
            for c in sa.inspect(user).mapper.column_attrs
        }

    async def _get_or_create_token_user(
        self,
        token: AccessToken,
    ) -> dict[str, Any]:
        """Get the request user in the access token if it exists, otherwise
        create the request user.
        """
        user = await self.user_controller.repository.get_unique_by(
            db=self.db,
            field="uuid",
            value=token.sub,
        )
        if not user:
            user_data = {
                "uuid": token.sub,
                "username": token.preferred_username,
                "is_admin": UserGroups.MALTOPUFT_ADMIN in token.groups,
            }
            user = await self.user_controller.create(
                db=self.db,
                attributes=CreateUser(**user_data).model_dump(),
            )
        return {
            c.key: getattr(user, c.key)
            for c in sa.inspect(user).mapper.column_attrs
        }

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
            authorization and `AuthenticatedUser` is an object containing
            basic user information which inherits from starlette's
            `SimpleUser`.

            The returned tuple is injected into the request to enable
            accessing user auth information throughout the application. If
            None is returned, then a starlette UnauthenticatedUser object
            is injected into the request.

        """
        if not settings.AUTH_ENABLED:
            # Inject test admin user into request
            user = await self._get_or_create_test_admin_user()
            return (
                AuthCredentials(UserGroups.MALTOPUFT_ADMIN),
                AuthenticatedUser(**user),
            )

        auth_header = conn.headers.get("Authorization")

        if auth_header is None:
            # Inject UnauthenticatedUser into request
            return None

        # Exchange token
        token = self._get_token_from_header(auth_header=auth_header)
        token = self._do_exchange_token(token=token)

        # Verify exchanged token audience
        decoded_token = self._decode_jwt(token=token)
        if decoded_token.aud != settings.MALTOPUFT_AUDIENCE:
            raise InvalidAudienceError

        user = await self._get_or_create_token_user(token=decoded_token)
        # Inject authenticated user information into request
        return (
            AuthCredentials(decoded_token.groups),
            AuthenticatedUser(**user),
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
