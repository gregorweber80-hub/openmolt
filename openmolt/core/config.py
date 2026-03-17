from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecurityConfig(BaseModel):
    mode: str = "secure"
    require_explicit_send_approval: bool = True
    allowed_domains: list[str] = Field(default_factory=lambda: ["google.com", "github.com"])


class OllamaConfig(BaseModel):
    host: str = "http://127.0.0.1:11434"
    model: str = "llama3.1"


class TelegramConfig(BaseModel):
    enabled: bool = False
    bot_token: str | None = None
    allowed_chat_ids: list[int] = Field(default_factory=list)


class AppConfig(BaseModel):
    name: str = "OpenMolt"
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    telegram: TelegramConfig = Field(default_factory=TelegramConfig)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OPENMOLT_", env_file=".env", extra="ignore")
    config_path: str = "config/openmolt.yaml"


def load_app_config(path: str | Path) -> AppConfig:
    p = Path(path)
    if not p.exists():
        return AppConfig()

    with p.open("r", encoding="utf-8") as f:
        payload: dict[str, Any] = yaml.safe_load(f) or {}

    return AppConfig.model_validate(payload)
