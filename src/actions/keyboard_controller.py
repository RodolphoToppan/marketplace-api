"""Keyboard control implementation."""

import time
from typing import Optional
import keyboard

from ..observability import get_logger

logger = get_logger(__name__)


class KeyboardController:
    """
    Controls keyboard input for game automation.

    Uses the 'keyboard' library which works better with games than pyautogui.
    Supports dry-run mode where actions are logged but not executed.
    """

    def __init__(self, dry_run: bool = True):
        """
        Initialize keyboard controller.

        Args:
            dry_run: If True, actions are logged but not executed
        """
        self.dry_run = dry_run

        logger.info(f"KeyboardController initialized (dry_run={dry_run})")

    def press_key(self, key: str, duration: float = 0.1) -> None:
        """
        Press and release a key.

        Args:
            key: Key to press (e.g., 'a', 'space', 'shift')
            duration: How long to hold the key in seconds
        """
        if self.dry_run:
            logger.info(f"DRY_RUN - press_key(key='{key}', duration={duration})")
            return

        try:
            keyboard.press_and_release(key)
            logger.info(f"✓ Pressed key: {key}")
        except Exception as e:
            logger.error(f"Failed to press key '{key}': {e}")
            raise

    def press_hotkey(self, *keys: str, interval: float = 0.05) -> None:
        """
        Press a combination of keys (hotkey).

        Args:
            keys: Keys to press together (e.g., 'shift', 'z')
            interval: Delay between key presses in seconds
        """
        if self.dry_run:
            hotkey_str = '+'.join(keys)
            logger.info(f"DRY_RUN - press_hotkey('{hotkey_str}')")
            return

        try:
            # Use keyboard library hotkey format
            hotkey_str = '+'.join(keys)
            keyboard.press_and_release(hotkey_str)
            logger.info(f"✓ Pressed hotkey: {hotkey_str}")
        except Exception as e:
            logger.error(f"Failed to press hotkey {keys}: {e}")
            raise

    def hold_key(self, key: str, duration: float) -> None:
        """
        Hold a key down for a specified duration.

        Args:
            key: Key to hold
            duration: Duration to hold in seconds
        """
        if self.dry_run:
            logger.info(f"DRY_RUN - hold_key(key='{key}', duration={duration})")
            return

        try:
            pyautogui.keyDown(key)
            time.sleep(duration)
            pyautogui.keyUp(key)
            logger.debug(f"Held key '{key}' for {duration}s")
        except Exception as e:
            logger.error(f"Failed to hold key '{key}': {e}")
            raise

    def type_text(self, text: str, interval: float = 0.1) -> None:
        """
        Type text character by character.

        Args:
            text: Text to type
            interval: Delay between characters in seconds
        """
        if self.dry_run:
            logger.info(f"DRY_RUN - type_text('{text}')")
            return

        try:
            pyautogui.write(text, interval=interval)
            logger.debug(f"Typed text: {text}")
        except Exception as e:
            logger.error(f"Failed to type text: {e}")
            raise

