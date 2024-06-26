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
