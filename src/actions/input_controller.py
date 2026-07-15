"""Unified input controller combining keyboard and mouse."""

from typing import Tuple, Optional

from .keyboard_controller import KeyboardController
from .mouse_controller import MouseController
from ..observability import get_logger

logger = get_logger(__name__)


class InputController:
    """
    Unified controller for all input operations.

    Combines keyboard and mouse control with coordinated actions.
    """

    def __init__(
        self,
        dry_run: bool = True,
        click_offset_range: Tuple[int, int] = (-3, 3),
        movement_duration_range: Tuple[float, float] = (0.1, 0.3)
    ):
        """
        Initialize input controller.

        Args:
            dry_run: If True, actions are logged but not executed
            click_offset_range: Random offset range for clicks
            movement_duration_range: Duration range for mouse movements
        """
        self.dry_run = dry_run
        self.keyboard = KeyboardController(dry_run=dry_run)
        self.mouse = MouseController(
            dry_run=dry_run,
            click_offset_range=click_offset_range,
            movement_duration_range=movement_duration_range
        )

        logger.info(f"InputController initialized (dry_run={dry_run})")

    def click_and_press(
        self,
        x: int,
        y: int,
        *keys: str,
        move_first: bool = True
    ) -> None:
        """
        Move to position, click, and press keys.

        Args:
            x: X coordinate
            y: Y coordinate
            keys: Keys to press after clicking
            move_first: Whether to move mouse before clicking
        """
        if move_first:
            self.mouse.move_to(x, y)

        self.mouse.click(x, y)

        if keys:
            self.keyboard.press_hotkey(*keys)

    def press_at_position(
        self,
        x: int,
        y: int,
        *keys: str,
        move_first: bool = True
    ) -> None:
        """
        Move to position and press keys without clicking.

        Args:
            x: X coordinate
            y: Y coordinate
            keys: Keys to press
            move_first: Whether to move mouse before pressing
        """
        if move_first:
            self.mouse.move_to(x, y)

        if keys:
            self.keyboard.press_hotkey(*keys)

    def set_dry_run(self, dry_run: bool) -> None:
        """
        Enable or disable dry-run mode for all controllers.

        Args:
            dry_run: New dry-run state
        """
        self.dry_run = dry_run
        self.keyboard.dry_run = dry_run
        self.mouse.dry_run = dry_run

        logger.info(f"Dry-run mode {'enabled' if dry_run else 'disabled'}")

