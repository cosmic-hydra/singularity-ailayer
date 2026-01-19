"""Configuration management with environment variable support."""
import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # API Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-1106-preview", env="OPENAI_MODEL")

    # Assistant Configuration
    assistant_name: str = Field(default="Ok Computer", env="ASSISTANT_NAME")
    assistant_voice_enabled: bool = Field(default=True, env="ASSISTANT_VOICE_ENABLED")
    assistant_animations_enabled: bool = Field(default=True, env="ASSISTANT_ANIMATIONS_ENABLED")
    assistant_subtitles_enabled: bool = Field(default=True, env="ASSISTANT_SUBTITLES_ENABLED")
    assistant_voice_recognition_enabled: bool = Field(default=True, env="ASSISTANT_VOICE_RECOGNITION_ENABLED")

    # Operational Modes
    low_data_mode: bool = Field(default=True, env="LOW_DATA_MODE")
    enable_semantic_router_map: bool = Field(default=True, env="ENABLE_SEMANTIC_ROUTER_MAP")
    enable_ocr: bool = Field(default=False, env="ENABLE_OCR")

    # Database Configuration
    database_path: Path = Field(default=Path("history.db"), env="DATABASE_PATH")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
