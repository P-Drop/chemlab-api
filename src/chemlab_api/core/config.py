"""Application settings, loaded from environment variables."""

from importlib.metadata import version

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    """
    Centralised application settings.

    Values can be overridden via environment variables or an `.env` file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API metadata
    api_title: str = "ChemLab API"
    api_description: str = (
        "Open-source REST API powering ChemLab, a virtual chemistry "
        "laboratory for Spanish Secondary Education students."
    )
    api_version: str = version("chemlab-api")

    # Database (PostgreSQL)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "chemlab"
    postgres_password: SecretStr = SecretStr("chemlab")
    postgres_db: str = "chemlab"

    @property
    def database_url(self) -> URL:
        """Assemble the async SQLAlchemy connection URL from the DB settings."""
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        )


settings = Settings()
