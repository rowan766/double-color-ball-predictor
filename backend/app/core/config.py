from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Double Color Ball Predictor"
    app_version: str = "0.1.0"
    database_url: str = "postgresql+psycopg://dcb_user:dcb_password@localhost:5432/dcb_predictor"
    backend_cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value:
            raise ValueError("DATABASE_URL must not be empty")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
