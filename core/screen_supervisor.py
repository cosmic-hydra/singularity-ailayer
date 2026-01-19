"""Screen supervision and monitoring service.

This module provides continuous screen monitoring capabilities for
proactive assistance and faster task execution.
"""
import threading
import time
from typing import Callable, Optional

from .config import get_settings
from .logging_config import get_logger

logger = get_logger(__name__)
settings = get_settings()


class ScreenSupervisor:
    """Continuous screen monitoring service for proactive assistance."""

    def __init__(self, callback: Optional[Callable] = None):
        """Initialize the screen supervisor.

        Args:
            callback: Optional callback function to handle screen changes
        """
        self.callback = callback
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.monitor_interval = 2.0  # Check every 2 seconds
        self.last_screenshot_hash: Optional[str] = None
        logger.info("Screen supervisor initialized", interval=self.monitor_interval)

    def start(self):
        """Start the screen supervision service."""
        if self.running:
            logger.warning("Screen supervisor already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        logger.info("Screen supervisor started")

    def stop(self):
        """Stop the screen supervision service."""
        if not self.running:
            return

        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Screen supervisor stopped")

    def _monitor_loop(self):
        """Main monitoring loop that runs in background thread."""
        while self.running:
            try:
                self._check_screen_changes()
                time.sleep(self.monitor_interval)
            except Exception as e:
                logger.error("Error in screen monitoring loop", error=str(e))
                time.sleep(self.monitor_interval)

    def _check_screen_changes(self):
        """Check for significant screen changes."""
        try:
            import pyautogui
            import hashlib

            # Take a low-res screenshot for comparison
            screenshot = pyautogui.screenshot(region=(0, 0, 400, 300))
            screenshot_bytes = screenshot.tobytes()
            current_hash = hashlib.md5(screenshot_bytes).hexdigest()

            if self.last_screenshot_hash and self.last_screenshot_hash != current_hash:
                logger.debug("Screen change detected")
                if self.callback:
                    self.callback()

            self.last_screenshot_hash = current_hash
        except Exception as e:
            logger.error("Error checking screen changes", error=str(e))


# Global supervisor instance
_supervisor: Optional[ScreenSupervisor] = None


def get_supervisor() -> ScreenSupervisor:
    """Get or create the global screen supervisor instance."""
    global _supervisor
    if _supervisor is None:
        _supervisor = ScreenSupervisor()
    return _supervisor


def start_supervision(callback: Optional[Callable] = None):
    """Start screen supervision with optional callback.

    Args:
        callback: Function to call when screen changes are detected
    """
    supervisor = get_supervisor()
    if callback:
        supervisor.callback = callback
    supervisor.start()


def stop_supervision():
    """Stop screen supervision."""
    supervisor = get_supervisor()
    supervisor.stop()
