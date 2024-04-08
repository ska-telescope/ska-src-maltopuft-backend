"""Application configuration."""

from pydantic import Field, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configures settings used throughout the application."""

    # pylint: disable=C0103

    model_config = SettingsConfigDict(env_file=".env")

    # Application settings
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


settings: Settings = Settings()
