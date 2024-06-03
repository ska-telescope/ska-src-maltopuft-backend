"""Dependency to check user authorization."""

from fastapi import Depends, Request, status

from src.ska_src_maltopuft_backend.core.exceptions import MaltopuftError


def user_permissions(request: Request) -> set[str]:
    """Extract user permissions from the incoming request."""
    return set(request.auth.scopes)


class PermissionDeniedError(MaltopuftError):
    """Raised when an user has insufficient permissions to fulfil a
    request.
    """

    status_code = status.HTTP_403_FORBIDDEN
    message = "Permission denied."


class AuthorizationChecker:
    """Check user request is authorized."""

    def __init__(self, required_permissions: list[str]) -> None:
        """AuthorizationChecker initialiser."""
        self.required_permissions = set(required_permissions)

    def __call__(
        self,
        permissions: set[str] = Depends(user_permissions),
    ) -> None:
        """Check user request is authorized by checking the user's
        permissions.

        If required permissions is a subset of user's permissions, then the
        user is authorized to make the request.
        """
        if not self.required_permissions.issubset(permissions):
            raise PermissionDeniedError
