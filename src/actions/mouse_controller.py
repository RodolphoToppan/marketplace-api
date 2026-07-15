"""Mouse control implementation."""

import time
import random
from typing import Optional, Tuple
import pyautogui

from ..observability import get_logger

logger = get_logger(__name__)


class MouseController:
    """
    Controls mouse input for game automation.

    Supports dry-run mode and human-like movement variations.
    """

    def __init__(
        self,
        dry_run: bool = True,
        click_offset_range: Tuple[int, int] = (-3, 3),
        movement_duration_range: Tuple[float, float] = (0.1, 0.3)
    ):
        """
        Initialize mouse controller.

        Args:
            dry_run: If True, actions are logged but not executed
            click_offset_range: Random offset range (min, max) for click position
            movement_duration_range: Duration range for mouse movement
        """
        self.dry_run = dry_run
        self.click_offset_range = click_offset_range
        self.movement_duration_range = movement_duration_range

        # PyAutoGUI failsafe
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0

        logger.info(
            f"MouseController initialized (dry_run={dry_run}, "
            f"offset_range={click_offset_range})"
        )

    def _apply_offset(self, x: int, y: int) -> Tuple[int, int]:
        """Apply random offset to coordinates for human-like variation."""
        offset_x = random.randint(*self.click_offset_range)
        offset_y = random.randint(*self.click_offset_range)
        return (x + offset_x, y + offset_y)

    def _get_movement_duration(self) -> float:
        """Get random movement duration for human-like movement."""
        return random.uniform(*self.movement_duration_range)

    def move_to(self, x: int, y: int, apply_offset: bool = True) -> None:
        """
        Move mouse to specified position.

        Args:
            x: Target x coordinate
            y: Target y coordinate
            apply_offset: Whether to apply random offset
        """
        if apply_offset:
            x, y = self._apply_offset(x, y)

        if self.dry_run:
            logger.info(f"DRY_RUN - move_to(x={x}, y={y})")
            return

        try:
            duration = self._get_movement_duration()
            pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)
            logger.debug(f"Moved mouse to ({x}, {y})")
        except Exception as e:
            logger.error(f"Failed to move mouse to ({x}, {y}): {e}")
            raise

    def click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        button: str = 'left',
        clicks: int = 1,
        interval: float = 0.0,
        apply_offset: bool = True
    ) -> None:
        """
        Click at specified position or current position.

        Args:
            x: X coordinate (None for current position)
            y: Y coordinate (None for current position)
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks
            interval: Interval between clicks
            apply_offset: Whether to apply random offset
        """
        if x is not None and y is not None:
            if apply_offset:
                x, y = self._apply_offset(x, y)

            if self.dry_run:
                logger.info(
                    f"DRY_RUN - click(x={x}, y={y}, button='{button}', "
                    f"clicks={clicks})"
                )
                return

            try:
                pyautogui.click(x, y, clicks=clicks, interval=interval, button=button)
                logger.debug(f"Clicked at ({x}, {y}) with {button} button")
            except Exception as e:
                logger.error(f"Failed to click at ({x}, {y}): {e}")
                raise
        else:
            if self.dry_run:
                logger.info(
                    f"DRY_RUN - click(button='{button}', clicks={clicks})"
                )
                return

            try:
                pyautogui.click(clicks=clicks, interval=interval, button=button)
                logger.debug(f"Clicked with {button} button")
            except Exception as e:
                logger.error(f"Failed to click: {e}")
                raise

    def right_click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        apply_offset: bool = True
    ) -> None:
        """
        Right-click at specified position.

        Args:
            x: X coordinate
            y: Y coordinate
            apply_offset: Whether to apply random offset
        """
        self.click(x, y, button='right', apply_offset=apply_offset)

    def double_click(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        apply_offset: bool = True
    ) -> None:
        """
        Double-click at specified position.

        Args:
            x: X coordinate
            y: Y coordinate
            apply_offset: Whether to apply random offset
        """
        self.click(x, y, clicks=2, interval=0.1, apply_offset=apply_offset)

    def get_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.

        Returns:
            Tuple of (x, y) coordinates
        """
        x, y = pyautogui.position()
        return (x, y)

