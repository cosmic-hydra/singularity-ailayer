"""Pytest configuration and fixtures."""
import os

import pytest
from unittest.mock import MagicMock, patch

# Set test environment variables before importing modules
os.environ["OPENAI_API_KEY"] = "test-api-key"
os.environ["LOG_LEVEL"] = "DEBUG"


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing."""
    with patch("core.core_api.client") as mock_client:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
        mock_client.chat.completions.create.return_value = mock_response
        yield mock_client


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    from core.config import Settings

    return Settings(
        openai_api_key="test-key",
        openai_model="gpt-4-1106-preview",
        low_data_mode=True,
        enable_ocr=False,
    )


@pytest.fixture
def sample_action_json():
    """Sample action JSON for testing."""
    return {
        "actions": [
            {"act": "click_element", "step": "Click on the search button"},
            {"act": "text_entry", "step": "Hello World"},
            {"act": "press_key", "step": "Enter"},
        ]
    }
