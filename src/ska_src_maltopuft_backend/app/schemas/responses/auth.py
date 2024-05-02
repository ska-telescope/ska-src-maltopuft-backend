"""Auth endpoint response models."""

from pydantic import BaseModel, HttpUrl


class LoginRedirect(BaseModel):
    """SKA IAM login URL schema."""

    login_url: HttpUrl
