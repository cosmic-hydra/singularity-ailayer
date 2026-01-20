"""Tests for configuration management."""

import pytest
from pydantic import ValidationError


class TestSettings:
    """Tests for Settings class."""

    def test_settings_loads_from_env(self, monkeypatch):
        """Test that settings loads from environment variables."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
        monkeypatch.setenv("OPENAI_MODEL", "gpt-4")
        monkeypatch.setenv("LOW_DATA_MODE", "false")

        from core.config import Settings

        settings = Settings()

        assert settings.openai_api_key == "test-key-123"
        assert settings.openai_model == "gpt-4"
        assert settings.low_data_mode is False

    def test_settings_defaults(self, monkeypatch):
        """Test default values are applied."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        from core.config import Settings

        settings = Settings()

        assert settings.openai_model == "gpt-4-1106-preview"
        assert settings.assistant_name == "Ok Computer"
        assert settings.low_data_mode is True
        assert settings.enable_ocr is False

    def test_settings_requires_api_key(self, monkeypatch):
        """Test that API key is required."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        from core.config import Settings

        with pytest.raises(ValidationError):
            Settings()
