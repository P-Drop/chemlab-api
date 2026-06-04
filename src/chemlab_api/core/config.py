"""Application settings, loaded from environment variables."""

from importlib.metadata import version

from pydantic_settings import BaseSettings, SettingsConfigDict


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


settings = Settings()
