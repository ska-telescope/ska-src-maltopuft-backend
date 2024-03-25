"""User response models."""

from pydantic import BaseModel


class User(BaseModel):
    """Response containing information shared by all User responses."""

    name: str
