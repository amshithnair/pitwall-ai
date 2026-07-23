"""PitWall AI Configuration Utilities."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class PitWallBaseSettings(BaseSettings):
    """Base settings for all PitWall services."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"
    log_level: str = "INFO"
