"""Security restrictions and validation module.

This module implements security controls to protect the system
from potentially harmful actions.
"""
import os
import re
from pathlib import Path
from typing import List, Optional, Set

from .config import get_settings
from .logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


class SecurityValidator:
    """Validates actions and inputs for security compliance."""

    def __init__(self):
        """Initialize the security validator."""
        # Restricted system directories
        self.restricted_paths: Set[Path] = {
            Path("C:\\Windows\\System32"),
            Path("C:\\Windows\\SysWOW64"),
            Path("C:\\Program Files"),
            Path("C:\\Program Files (x86)"),
        }

        # Restricted file extensions
        self.restricted_extensions: Set[str] = {
            ".exe",
            ".dll",
            ".sys",
            ".bat",
            ".cmd",
            ".ps1",
            ".vbs",
            ".scr",
        }

        # Suspicious command patterns
        self.suspicious_patterns: List[re.Pattern] = [
            re.compile(r"format\s+[a-z]:", re.IGNORECASE),
            re.compile(r"del\s+/[sqf]", re.IGNORECASE),
            re.compile(r"rd\s+/s", re.IGNORECASE),
            re.compile(r"rmdir\s+/s", re.IGNORECASE),
            re.compile(r"shutdown\s+", re.IGNORECASE),
            re.compile(r"taskkill\s+/f", re.IGNORECASE),
            re.compile(r"reg\s+delete", re.IGNORECASE),
            re.compile(r"regedit", re.IGNORECASE),
        ]

        logger.info("Security validator initialized")

    def validate_file_path(self, file_path: str) -> tuple[bool, Optional[str]]:
        """Validate if a file path is safe to access.

        Args:
            file_path: Path to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            path = Path(file_path).resolve()

            # Check if path is in restricted directories FIRST
            for restricted_path in self.restricted_paths:
                try:
                    if path.is_relative_to(restricted_path):
                        error = f"Access to restricted directory denied: {restricted_path}"
                        logger.warning("Security violation", path=str(path), reason=error)
                        return False, error
                except (ValueError, AttributeError):
                    # is_relative_to not available or path comparison failed
                    if str(restricted_path).lower() in str(path).lower():
                        error = f"Access to restricted directory denied: {restricted_path}"
                        logger.warning("Security violation", path=str(path), reason=error)
                        return False, error

            # Check file extension
            if path.suffix.lower() in self.restricted_extensions:
                error = f"Access to restricted file type denied: {path.suffix}"
                logger.warning("Security violation", path=str(path), reason=error)
                return False, error

            logger.debug("File path validated", path=str(path))
            return True, None

        except Exception as e:
            error = f"Invalid path: {str(e)}"
            logger.error("Path validation error", path=file_path, error=str(e))
            return False, error

    def validate_command(self, command: str) -> tuple[bool, Optional[str]]:
        """Validate if a command is safe to execute.

        Args:
            command: Command to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for suspicious patterns
        for pattern in self.suspicious_patterns:
            if pattern.search(command):
                error = f"Potentially dangerous command detected: {pattern.pattern}"
                logger.warning("Security violation", command=command, reason=error)
                return False, error

        logger.debug("Command validated", command=command)
        return True, None

    def validate_text_entry(self, text: str) -> tuple[bool, Optional[str]]:
        """Validate text entry for potentially harmful content.

        Args:
            text: Text to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check for SQL injection patterns
        sql_patterns = [
            re.compile(r";\s*drop\s+table", re.IGNORECASE),
            re.compile(r";\s*delete\s+from", re.IGNORECASE),
            re.compile(r"union\s+select", re.IGNORECASE),
            re.compile(r"'\s*or\s+'1'\s*=\s*'1", re.IGNORECASE),
        ]

        for pattern in sql_patterns:
            if pattern.search(text):
                error = "Potential SQL injection detected"
                logger.warning("Security violation", text_sample=text[:50], reason=error)
                return False, error

        # Check for script injection patterns
        script_patterns = [
            re.compile(r"<script", re.IGNORECASE),
            re.compile(r"javascript:", re.IGNORECASE),
            re.compile(r"onerror\s*=", re.IGNORECASE),
        ]

        for pattern in script_patterns:
            if pattern.search(text):
                error = "Potential script injection detected"
                logger.warning("Security violation", text_sample=text[:50], reason=error)
                return False, error

        logger.debug("Text entry validated")
        return True, None

    def validate_action(self, action: dict) -> tuple[bool, Optional[str]]:
        """Validate an action before execution.

        Args:
            action: Action dictionary with 'act' and 'step' keys

        Returns:
            Tuple of (is_valid, error_message)
        """
        action_type = action.get("act", "")
        step = action.get("step", "")

        # Validate based on action type
        if action_type == "open_app":
            # Validate application name
            if step.lower() in ["regedit", "cmd", "powershell", "command prompt"]:
                error = f"Opening restricted application denied: {step}"
                logger.warning("Security violation", action=action, reason=error)
                return False, error

        elif action_type == "text_entry":
            # Validate text content
            return self.validate_text_entry(step)

        elif action_type == "press_key":
            # Validate keyboard shortcuts (e.g., prevent Alt+F4 spam)
            if "Alt" in step and "F4" in step:
                logger.info("Potentially disruptive key combination detected", keys=step)
                # Allow but log for monitoring

        logger.debug("Action validated", action=action)
        return True, None


# Global validator instance
_validator: Optional[SecurityValidator] = None


def get_validator() -> SecurityValidator:
    """Get or create the global security validator instance."""
    global _validator
    if _validator is None:
        _validator = SecurityValidator()
    return _validator


def validate_action(action: dict) -> tuple[bool, Optional[str]]:
    """Validate an action for security compliance.

    Args:
        action: Action dictionary to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = get_validator()
    return validator.validate_action(action)


def validate_file_path(path: str) -> tuple[bool, Optional[str]]:
    """Validate a file path for security compliance.

    Args:
        path: File path to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = get_validator()
    return validator.validate_file_path(path)


def validate_command(command: str) -> tuple[bool, Optional[str]]:
    """Validate a command for security compliance.

    Args:
        command: Command to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = get_validator()
    return validator.validate_command(command)
