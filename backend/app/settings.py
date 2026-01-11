from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Matches docker-compose.yml
    database_url: str = Field(
        "postgresql+asyncpg://bus-tracker:bus-tracker_password_change_me@db:5432/bus-tracker",
        alias="DATABASE_URL",
    )

    app_env: str = Field("development", alias="APP_ENV")
    api_host: str = Field("0.0.0.0", alias="API_HOST")
    api_port: int = Field(8000, alias="API_PORT")
    app_tz: str = Field("Asia/Hong_Kong", alias="APP_TZ")

    redis_url: str = Field("redis://redis:6379/0", alias="REDIS_URL")

    # Worker defaults
    poll_interval_seconds: int = Field(60, alias="POLL_INTERVAL_SECONDS")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
