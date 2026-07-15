"""Global hotkey management for bot control."""

import keyboard
from typing import Callable, Optional
import threading

from ..observability import get_logger

logger = get_logger(__name__)


class HotkeyManager:
    """
    Manages global hotkeys for bot control.

    Allows starting/stopping the bot with a global hotkey (e.g., F12)
    that works even when the game window is focused.
    """

    def __init__(self):
        """Initialize hotkey manager."""
        self._hotkeys = {}
        self._lock = threading.Lock()
        logger.info("HotkeyManager initialized")

    def register_hotkey(
        self,
        hotkey: str,
        callback: Callable[[], None],
        suppress: bool = True
    ) -> None:
        """
        Register a global hotkey.

        Args:
            hotkey: Hotkey string (e.g., 'f12', 'ctrl+shift+a')
            callback: Function to call when hotkey is pressed
            suppress: Whether to suppress the key event from other applications
        """
        with self._lock:
            if hotkey in self._hotkeys:
                logger.warning(f"Hotkey '{hotkey}' already registered, removing old")
                self.unregister_hotkey(hotkey)

            try:
                keyboard.add_hotkey(hotkey, callback, suppress=suppress)
                self._hotkeys[hotkey] = callback
                logger.info(f"Registered hotkey: {hotkey}")
            except Exception as e:
                logger.error(f"Failed to register hotkey '{hotkey}': {e}")
                raise

    def unregister_hotkey(self, hotkey: str) -> None:
        """
        Unregister a global hotkey.

        Args:
            hotkey: Hotkey to unregister
        """
        with self._lock:
            if hotkey in self._hotkeys:
                try:
                    keyboard.remove_hotkey(hotkey)
                    del self._hotkeys[hotkey]
                    logger.info(f"Unregistered hotkey: {hotkey}")
                except Exception as e:
                    logger.error(f"Failed to unregister hotkey '{hotkey}': {e}")
            else:
                logger.warning(f"Hotkey '{hotkey}' not registered")

    def unregister_all(self) -> None:
        """Unregister all hotkeys."""
        with self._lock:
            hotkeys_to_remove = list(self._hotkeys.keys())
            for hotkey in hotkeys_to_remove:
                self.unregister_hotkey(hotkey)
            logger.info("All hotkeys unregistered")

    def is_registered(self, hotkey: str) -> bool:
        """
        Check if a hotkey is registered.

        Args:
            hotkey: Hotkey to check

        Returns:
            True if registered
        """
        with self._lock:
            return hotkey in self._hotkeys

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - unregister all hotkeys."""
        self.unregister_all()

