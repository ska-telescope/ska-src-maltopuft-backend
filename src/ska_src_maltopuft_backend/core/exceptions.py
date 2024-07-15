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


class AlreadyExistsError(MaltopuftError):
    """HTTP 409 (conflict) error."""

    status_code = status.HTTP_409_CONFLICT
    message = "Can't create duplicate object."


class MissingRequiredAttributeError(MaltopuftError):
    """Mising required attribute error."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = "Can't create object with missing required attributes."


class ParentNotFoundError(MaltopuftError):
    """Parent record id not found."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Parent id not found."


class NotFoundError(MaltopuftError):
    """HTTP 404 (not found) error."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Not found."


class DeleteError(MaltopuftError):
    """HTTP 405 (method not allowed) error."""

    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    message = "Item can't be deleted."


class InvalidAudienceError(MaltopuftError):
    """Raised when bearer token has an invalid audience."""

    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid audience."
