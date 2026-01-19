"""Tests for security validation module."""
import pytest


class TestSecurityValidator:
    """Tests for SecurityValidator class."""

    def test_validator_initialization(self):
        """Test validator initializes correctly."""
        from core.security import SecurityValidator

        validator = SecurityValidator()
        assert len(validator.restricted_paths) > 0
        assert len(validator.restricted_extensions) > 0

    def test_validate_safe_file_path(self):
        """Test validation of safe file paths."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        # Safe paths should pass
        is_valid, error = validator.validate_file_path("C:\\Users\\test\\document.txt")
        assert is_valid is True
        assert error is None

    def test_validate_restricted_directory(self):
        """Test validation blocks restricted directories."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        # System32 should be blocked
        is_valid, error = validator.validate_file_path("C:\\Windows\\System32\\kernel32.dll")
        assert is_valid is False
        assert error is not None
        assert "restricted directory" in error.lower()

    def test_validate_restricted_extension(self):
        """Test validation blocks restricted file types."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        # .exe files should be blocked
        is_valid, error = validator.validate_file_path("C:\\Users\\test\\malware.exe")
        assert is_valid is False
        assert error is not None
        assert "restricted file type" in error.lower()

    def test_validate_safe_command(self):
        """Test validation of safe commands."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        # Safe commands should pass
        is_valid, error = validator.validate_command("dir")
        assert is_valid is True

        is_valid, error = validator.validate_command("echo Hello")
        assert is_valid is True

    def test_validate_dangerous_command(self):
        """Test validation blocks dangerous commands."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        dangerous_commands = [
            "format c:",
            "del /s /q C:\\",
            "shutdown /s",
            "regedit",
            "rd /s C:\\Users",
        ]

        for cmd in dangerous_commands:
            is_valid, error = validator.validate_command(cmd)
            assert is_valid is False, f"Command '{cmd}' should be blocked"
            assert error is not None

    def test_validate_text_entry(self):
        """Test text entry validation."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        # Safe text should pass
        is_valid, error = validator.validate_text_entry("Hello, this is normal text")
        assert is_valid is True

        # SQL injection attempts should be blocked
        sql_injections = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "UNION SELECT * FROM passwords",
        ]

        for injection in sql_injections:
            is_valid, error = validator.validate_text_entry(injection)
            assert is_valid is False, f"SQL injection '{injection}' should be blocked"

    def test_validate_action_open_app(self):
        """Test action validation for opening apps."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        # Safe app should pass
        action = {"act": "open_app", "step": "Firefox"}
        is_valid, error = validator.validate_action(action)
        assert is_valid is True

        # Restricted apps should be blocked
        restricted_apps = ["regedit", "cmd", "powershell"]
        for app in restricted_apps:
            action = {"act": "open_app", "step": app}
            is_valid, error = validator.validate_action(action)
            assert is_valid is False, f"Opening '{app}' should be blocked"

    def test_validate_action_text_entry(self):
        """Test action validation for text entry."""
        from core.security import SecurityValidator

        validator = SecurityValidator()

        # Safe text entry
        action = {"act": "text_entry", "step": "Hello World"}
        is_valid, error = validator.validate_action(action)
        assert is_valid is True

        # Malicious text entry
        action = {"act": "text_entry", "step": "<script>alert('xss')</script>"}
        is_valid, error = validator.validate_action(action)
        assert is_valid is False

    def test_get_validator_singleton(self):
        """Test get_validator returns singleton."""
        from core.security import get_validator

        validator1 = get_validator()
        validator2 = get_validator()

        assert validator1 is validator2
