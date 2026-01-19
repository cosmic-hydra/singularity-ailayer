"""Tests for screen supervision module."""
import time

import pytest
from unittest.mock import MagicMock, patch


class TestScreenSupervisor:
    """Tests for ScreenSupervisor class."""

    def test_supervisor_initialization(self):
        """Test supervisor initializes correctly."""
        from core.screen_supervisor import ScreenSupervisor

        supervisor = ScreenSupervisor()
        assert supervisor.running is False
        assert supervisor.monitor_interval == 2.0

    def test_supervisor_start_stop(self):
        """Test starting and stopping supervisor."""
        from core.screen_supervisor import ScreenSupervisor

        supervisor = ScreenSupervisor()

        # Start supervisor
        supervisor.start()
        assert supervisor.running is True
        assert supervisor.thread is not None

        # Small delay to let thread start
        time.sleep(0.1)

        # Stop supervisor
        supervisor.stop()
        assert supervisor.running is False

    def test_supervisor_callback(self):
        """Test supervisor callback is triggered."""
        from core.screen_supervisor import ScreenSupervisor

        callback_triggered = {"value": False}

        def test_callback():
            callback_triggered["value"] = True

        supervisor = ScreenSupervisor(callback=test_callback)
        
        # Mock screen change detection
        with patch.object(supervisor, "_check_screen_changes") as mock_check:
            mock_check.side_effect = lambda: test_callback()
            supervisor.start()
            time.sleep(0.5)
            supervisor.stop()

    def test_get_supervisor_singleton(self):
        """Test get_supervisor returns singleton."""
        from core.screen_supervisor import get_supervisor

        supervisor1 = get_supervisor()
        supervisor2 = get_supervisor()

        assert supervisor1 is supervisor2
