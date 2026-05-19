"""Application configuration loaded from environment variables / .env."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Resume Screening AI"
    api_prefix: str = "/api"
    database_url: str = Field(default="sqlite:///./storage/app.db")
    upload_dir: str = Field(default="./uploads")
    storage_dir: str = Field(default="./storage")
    cors_origins: str = Field(default="http://localhost:3000")
    use_sentence_transformer: bool = Field(default=False)
    sentence_model: str = Field(default="all-MiniLM-L6-v2")

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    def ensure_dirs(self) -> None:
        Path(self.upload_dir).mkdir(parents=True, exist_ok=True)
        Path(self.storage_dir).mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    s = Settings()
    s.ensure_dirs()
    return s
