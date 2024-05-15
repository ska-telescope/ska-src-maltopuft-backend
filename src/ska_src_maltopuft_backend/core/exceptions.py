"""Custom MALTOPUFT exceptions."""

from fastapi import status


class MaltopuftError(Exception):
    """MALTOPUFT base HTTP exception from which all other custom exceptions
    inherit.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "Internal server error."

    def __init__(self, message: str | None = None) -> None:
        """Initialiser for the MaltopuftError base error."""
        if message:
            self.message = message


class InvalidAudienceError(MaltopuftError):
    """Raised when bearer token has an invalid audience."""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid audience."


class AuthenticationRequiredError(MaltopuftError):
    """Raised when an authenticated user makes a request that requires
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
