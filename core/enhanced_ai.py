"""Enhanced AI capabilities for better task execution.

This module provides improved AI decision-making, context awareness,
and task optimization features.
"""

import json
from typing import Any, Dict, List, Optional

from .config import get_settings
from .core_api import api_call
from .logging_config import get_logger
from .performance import cached

logger = get_logger(__name__)
settings = get_settings()


class EnhancedAI:
    """Enhanced AI system for improved task execution."""

    def __init__(self):
        """Initialize the enhanced AI system."""
        self.context_history: List[Dict[str, Any]] = []
        self.max_context_length = 10
        logger.info("Enhanced AI system initialized")

    def analyze_goal_with_context(self, goal: str, app_name: Optional[str] = None) -> Dict[str, Any]:
        """Analyze a goal with enhanced context awareness.

        Args:
            goal: User's goal/intent
            app_name: Optional application name for context

        Returns:
            Enhanced goal analysis with confidence scores
        """
        logger.info("Analyzing goal with context", goal=goal, app=app_name)

        # Build context-aware prompt
        context_prompt = self._build_context_prompt(goal, app_name)

        # Get AI analysis
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an advanced Windows automation AI with deep understanding of user intents. "
                    "Analyze the goal and provide a structured response with confidence score."
                ),
            },
            {"role": "user", "content": context_prompt},
        ]

        response = api_call(messages, temperature=0.3, max_tokens=300)

        # Parse and enhance response
        analysis = {
            "original_goal": goal,
            "enhanced_goal": response,
            "app_context": app_name,
            "confidence": self._calculate_confidence(response),
        }

        # Add to context history
        self._add_to_context(analysis)

        logger.info("Goal analysis complete", confidence=analysis["confidence"])
        return analysis

    def generate_optimized_actions(self, goal: str, app_name: str, use_vision: bool = True) -> List[Dict[str, str]]:
        """Generate optimized action sequence for a goal.

        Args:
            goal: User's goal
            app_name: Target application
            use_vision: Whether to use vision analysis

        Returns:
            List of optimized actions
        """
        logger.info("Generating optimized actions", goal=goal, app=app_name, vision=use_vision)

        from .core_api import api_call

        # Check cache first for common patterns
        cache_key = f"actions:{app_name}:{goal}"
        cached_actions = self._check_action_cache(cache_key)
        if cached_actions:
            logger.info("Using cached actions", count=len(cached_actions))
            return cached_actions

        # Build enhanced prompt with past successful patterns
        prompt = self._build_action_generation_prompt(goal, app_name)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert Windows automation AI. Generate the most efficient "
                    "sequence of actions to achieve the goal. Prioritize speed and accuracy."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        response = api_call(messages, model_name=settings.openai_model, temperature=0.2, max_tokens=500)

        # Parse actions from response
        actions = self._parse_actions(response)

        # Optimize action sequence
        optimized_actions = self._optimize_action_sequence(actions)

        # Cache successful patterns
        self._cache_actions(cache_key, optimized_actions)

        logger.info("Actions generated and optimized", count=len(optimized_actions))
        return optimized_actions

    def suggest_improvements(self, action_sequence: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Suggest improvements to an action sequence.

        Args:
            action_sequence: Current action sequence

        Returns:
            Improved action sequence
        """
        logger.info("Analyzing action sequence for improvements", count=len(action_sequence))

        # Check for redundant actions
        improved = self._remove_redundant_actions(action_sequence)

        # Check for missing wait times
        improved = self._add_smart_waits(improved)

        # Check for keyboard shortcuts that could be faster
        improved = self._optimize_keyboard_shortcuts(improved)

        if len(improved) != len(action_sequence):
            logger.info("Action sequence optimized", original=len(action_sequence), optimized=len(improved))

        return improved

    def _build_context_prompt(self, goal: str, app_name: Optional[str]) -> str:
        """Build a context-aware prompt."""
        prompt_parts = [f"Goal: {goal}"]

        if app_name:
            prompt_parts.append(f"Application: {app_name}")

        if self.context_history:
            recent_context = self.context_history[-3:]
            prompt_parts.append("Recent context:")
            for ctx in recent_context:
                prompt_parts.append(f"- {ctx.get('original_goal', 'Unknown')}")

        return "\n".join(prompt_parts)

    def _build_action_generation_prompt(self, goal: str, app_name: str) -> str:
        """Build an action generation prompt."""
        prompt = f"""Generate a JSON action sequence for the following goal:

Application: {app_name}
Goal: {goal}

Requirements:
1. Use the most efficient path to achieve the goal
2. Minimize the number of actions
3. Use keyboard shortcuts when possible
4. Return ONLY valid JSON with this structure:
{{
  "actions": [
    {{"act": "action_type", "step": "description"}},
    ...
  ]
}}

Available action types: open_app, click_element, text_entry, press_key, move_window
"""
        return prompt

    def _parse_actions(self, response: str) -> List[Dict[str, str]]:
        """Parse actions from API response."""
        try:
            # Extract JSON from response
            json_match = response.find("{")
            if json_match != -1:
                json_end = response.rfind("}") + 1
                json_str = response[json_match:json_end]
                data = json.loads(json_str)
                return data.get("actions", [])
        except Exception as e:
            logger.error("Error parsing actions", error=str(e))

        return []

    def _optimize_action_sequence(self, actions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Optimize an action sequence."""
        if not actions:
            return actions

        optimized = []
        skip_next = False

        for i, action in enumerate(actions):
            if skip_next:
                skip_next = False
                continue

            # Combine consecutive text entries
            if action.get("act") == "text_entry" and i + 1 < len(actions):
                next_action = actions[i + 1]
                if next_action.get("act") == "text_entry":
                    combined_text = action["step"] + next_action["step"]
                    optimized.append({"act": "text_entry", "step": combined_text})
                    skip_next = True
                    continue

            optimized.append(action)

        return optimized

    def _remove_redundant_actions(self, actions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Remove redundant actions."""
        if len(actions) <= 1:
            return actions

        result = [actions[0]]
        for action in actions[1:]:
            # Don't add if it's identical to the previous action
            if action != result[-1]:
                result.append(action)

        return result

    def _add_smart_waits(self, actions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Add intelligent wait times where needed."""
        # For now, just return as-is
        # Future: Add wait actions after app launches, page loads, etc.
        return actions

    def _optimize_keyboard_shortcuts(self, actions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Optimize keyboard shortcuts in action sequence."""
        # Future: Replace click sequences with keyboard shortcuts
        return actions

    def _calculate_confidence(self, response: str) -> float:
        """Calculate confidence score for a response."""
        # Simple heuristic based on response length and completeness
        if not response:
            return 0.0

        confidence = 0.5  # Base confidence

        # Increase confidence for longer, more detailed responses
        if len(response) > 50:
            confidence += 0.2
        if len(response) > 100:
            confidence += 0.2

        # Cap at 0.9 (never 100% certain)
        return min(confidence, 0.9)

    def _add_to_context(self, analysis: Dict[str, Any]):
        """Add analysis to context history."""
        self.context_history.append(analysis)
        if len(self.context_history) > self.max_context_length:
            self.context_history.pop(0)

    @cached(ttl=1800)  # Cache for 30 minutes
    def _check_action_cache(self, cache_key: str) -> Optional[List[Dict[str, str]]]:
        """Check cache for common action patterns."""
        # Placeholder - actual caching handled by decorator
        return None

    def _cache_actions(self, cache_key: str, actions: List[Dict[str, str]]):
        """Cache successful action patterns."""
        from .performance import get_cache

        cache = get_cache()
        cache.set(cache_key, actions, ttl=1800)  # 30 minutes


# Global enhanced AI instance
_enhanced_ai: Optional[EnhancedAI] = None


def get_enhanced_ai() -> EnhancedAI:
    """Get or create the global enhanced AI instance."""
    global _enhanced_ai
    if _enhanced_ai is None:
        _enhanced_ai = EnhancedAI()
    return _enhanced_ai
