"""Tests for enhanced AI module."""
import pytest
from unittest.mock import MagicMock, patch


class TestEnhancedAI:
    """Tests for EnhancedAI class."""

    def test_enhanced_ai_initialization(self):
        """Test enhanced AI initializes correctly."""
        from core.enhanced_ai import EnhancedAI

        ai = EnhancedAI()
        assert len(ai.context_history) == 0
        assert ai.max_context_length == 10

    @patch("core.enhanced_ai.api_call")
    def test_analyze_goal_with_context(self, mock_api_call):
        """Test goal analysis with context."""
        from core.enhanced_ai import EnhancedAI

        mock_api_call.return_value = "Enhanced goal description"

        ai = EnhancedAI()
        result = ai.analyze_goal_with_context("Open browser", "Firefox")

        assert result["original_goal"] == "Open browser"
        assert result["app_context"] == "Firefox"
        assert "confidence" in result
        assert isinstance(result["confidence"], float)

    def test_remove_redundant_actions(self):
        """Test removing redundant actions."""
        from core.enhanced_ai import EnhancedAI

        ai = EnhancedAI()

        actions = [
            {"act": "click", "step": "Button"},
            {"act": "click", "step": "Button"},  # Duplicate
            {"act": "text_entry", "step": "Hello"},
        ]

        result = ai._remove_redundant_actions(actions)

        assert len(result) == 2
        assert result[0] == {"act": "click", "step": "Button"}
        assert result[1] == {"act": "text_entry", "step": "Hello"}

    def test_optimize_action_sequence(self):
        """Test action sequence optimization."""
        from core.enhanced_ai import EnhancedAI

        ai = EnhancedAI()

        actions = [
            {"act": "text_entry", "step": "Hello"},
            {"act": "text_entry", "step": " World"},
            {"act": "click", "step": "Submit"},
        ]

        result = ai._optimize_action_sequence(actions)

        # Text entries should be combined
        assert len(result) == 2
        assert result[0]["step"] == "Hello World"

    def test_calculate_confidence(self):
        """Test confidence calculation."""
        from core.enhanced_ai import EnhancedAI

        ai = EnhancedAI()

        # Short response - low confidence
        confidence1 = ai._calculate_confidence("OK")
        assert 0 <= confidence1 <= 1

        # Longer response - higher confidence
        long_response = "This is a detailed response with comprehensive information about the task."
        confidence2 = ai._calculate_confidence(long_response)
        assert confidence2 > confidence1

    def test_context_history_limit(self):
        """Test context history size limit."""
        from core.enhanced_ai import EnhancedAI

        ai = EnhancedAI()
        ai.max_context_length = 3

        # Add more items than limit
        for i in range(5):
            analysis = {
                "original_goal": f"Goal {i}",
                "confidence": 0.8,
            }
            ai._add_to_context(analysis)

        # Should only keep last 3
        assert len(ai.context_history) == 3
        assert ai.context_history[-1]["original_goal"] == "Goal 4"

    def test_get_enhanced_ai_singleton(self):
        """Test get_enhanced_ai returns singleton."""
        from core.enhanced_ai import get_enhanced_ai

        ai1 = get_enhanced_ai()
        ai2 = get_enhanced_ai()

        assert ai1 is ai2
