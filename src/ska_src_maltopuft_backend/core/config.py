"""Application configuration."""

from typing import Any

from pydantic import Field, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configures settings used throughout the application."""

    # pylint: disable=C0103

    model_config = SettingsConfigDict(env_file=".env")

    # Application settings
    APP_NAME: str = "ska-src-maltopuft-backend"
    RELEASE_VERSION: str = "0.1.0"
    DEBUG: int = 0

    # Database settings
    MALTOPUFT_POSTGRES_USER: str = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_POSTGRES_USER"},
    )
    MALTOPUFT_POSTGRES_PASSWORD: str = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_POSTGRES_PASSWORD"},
    )
    MALTOPUFT_POSTGRES_HOST: str = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_POSTGRES_HOST"},
    )
    MALTOPUFT_POSTGRES_PORT: int = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_POSTGRES_PORT"},
    )
    MALTOPUFT_POSTGRES_DB_NAME: str = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_POSTGRES_DB_NAME"},
    )

    @computed_field  # type: ignore[misc]
    @property
    def MALTOPUFT_POSTGRES_INFO(self) -> str:  # noqa: N802
        """Database connection info without credentials."""
        return (
            f"postgresql+psycopg://{self.MALTOPUFT_POSTGRES_HOST}:"
            f"{self.MALTOPUFT_POSTGRES_PORT}/{self.MALTOPUFT_POSTGRES_DB_NAME}"
        )

    @computed_field  # type: ignore[misc]
    @property
    def MALTOPUFT_POSTGRES_URI(self) -> PostgresDsn:  # noqa: N802
        """Build the database connection string from settings."""
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.MALTOPUFT_POSTGRES_USER,
            password=self.MALTOPUFT_POSTGRES_PASSWORD,
            host=self.MALTOPUFT_POSTGRES_HOST,
            port=self.MALTOPUFT_POSTGRES_PORT,
            path=self.MALTOPUFT_POSTGRES_DB_NAME,
        )

    MALTOPUFT_AUDIENCE: str = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_AUDIENCE"},
    )

    MALTOPUFT_SERVICE_GROUP: str = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_SERVICE_GROUP"},
    )

    MALTOPUFT_ROOT_GROUP: str = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_ROOT_GROUP"},
    )

    AUTH_ENABLED: int = Field(
        default=True,
        json_schema_extra={"env": "AUTH_ENABLED"},
    )
    AUTHN_API_URL: str = Field(
        ...,
        json_schema_extra={"env": "AUTHN_API_URL"},
    )

    MALTOPUFT_ENTITIES: list[dict[str, Any]] = Field(
        ...,
        json_schema_extra={"env": "MALTOPUFT_ENTITIES"},
    )

    TEST_UUID4: str = Field(
        ...,
        json_schema_extra={"env": "TEST_UUID4"},
    )
    TEST_SUPERUSER_BASE_DECODED_TOKEN: dict[str, Any] = Field(
        ...,
        json_schema_extra={"env": "TEST_SUPERUSER_BASE_DECODED_TOKEN"},
    )

    @computed_field  # type: ignore[misc]
    @property
    def TEST_SUPERUSER_DECODED_TOKEN(self) -> dict[str, Any]:  # noqa: N802
        """Add pre-generated UUID4 fields to test token."""
        token = dict(self.TEST_SUPERUSER_BASE_DECODED_TOKEN)

        # Add pre-generated test UUID4 to the token
        token["sub"] = self.TEST_UUID4
        token["client_id"] = self.TEST_UUID4
        token["jti"] = self.TEST_UUID4
        return token

    @computed_field  # type: ignore[misc]
    @property
    def TEST_SUPERUSER_TOKEN(self) -> str:  # noqa: N802
        """Encode the test token."""
        import jwt  # pylint: disable=C0415

        return jwt.encode(
            self.TEST_SUPERUSER_DECODED_TOKEN,
            "secret",
            algorithm="HS256",
        )


settings: Settings = Settings()
