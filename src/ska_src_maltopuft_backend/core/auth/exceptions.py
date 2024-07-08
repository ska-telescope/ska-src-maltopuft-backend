"""Exception classes used in Authentication backend."""

from fastapi import status

from ska_src_maltopuft_backend.core.exceptions import MaltopuftError


class InvalidAudienceError(MaltopuftError):
    """Raised when bearer token has an invalid audience."""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid audience."


class AuthenticationRequiredError(MaltopuftError):
    """Raised when an unauthenticated user makes a request that requires
    authentication.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication required"


class PermissionDeniedError(MaltopuftError):
    """Raised when an user has insufficient permissions to fulfil a
    request.
    """

    status_code = status.HTTP_403_FORBIDDEN
    message = "Permission denied."
