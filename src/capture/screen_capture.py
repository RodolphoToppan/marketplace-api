"""Screen capture implementation."""

import numpy as np
import mss
from pathlib import Path
from datetime import datetime
from typing import Optional

from .regions import ScreenRegion
from ..observability import get_logger

logger = get_logger(__name__)


class ScreenCapture:
    """
    Captures screenshots of specific screen regions.

    Uses MSS library for efficient screen capture without dependencies on
    PIL or other heavy libraries.
    """

    def __init__(self):
        """Initialize screen capture."""
        self._sct: Optional[mss.mss] = None
        logger.debug("ScreenCapture initialized")

    def __enter__(self):
        """Context manager entry."""
        self._sct = mss.mss()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self._sct:
            self._sct.close()
            self._sct = None

    def capture(self, region: ScreenRegion) -> np.ndarray:
        """
        Capture a specific screen region.

        Args:
            region: Screen region to capture

        Returns:
            Captured image as numpy array (BGR format, compatible with OpenCV)

        Raises:
            RuntimeError: If capture fails
        """
        if self._sct is None:
            raise RuntimeError(
                "ScreenCapture must be used as context manager: "
                "with ScreenCapture() as capture: ..."
            )

        try:
            monitor = region.to_mss_monitor()
            screenshot = self._sct.grab(monitor)

            # Convert to numpy array
            # MSS returns BGRA, we convert to BGR for OpenCV compatibility
            img = np.array(screenshot)
            img_bgr = img[:, :, :3]  # Remove alpha channel

            logger.debug(
                f"Captured region x={region.x} y={region.y} "
                f"w={region.width} h={region.height} "
                f"shape={img_bgr.shape}"
            )

            return img_bgr

        except Exception as e:
            logger.error(f"Failed to capture screen region: {e}")
            raise RuntimeError(f"Screen capture failed: {e}") from e

    def save_capture(
        self,
        image: np.ndarray,
        filepath: Path,
        create_dirs: bool = True
    ) -> None:
        """
        Save a captured image to disk.

        Args:
            image: Image array (BGR format)
            filepath: Destination file path
            create_dirs: Create parent directories if they don't exist

        Raises:
            ValueError: If image is invalid
            IOError: If save fails
        """
        if image is None or image.size == 0:
            raise ValueError("Cannot save empty image")

        if create_dirs:
            filepath.parent.mkdir(parents=True, exist_ok=True)

        try:
            import cv2
            success = cv2.imwrite(str(filepath), image)

            if not success:
                raise IOError(f"cv2.imwrite failed for {filepath}")

            logger.info(f"Saved capture to {filepath}")

        except Exception as e:
            logger.error(f"Failed to save capture: {e}")
            raise IOError(f"Failed to save capture: {e}") from e

    def save_error_capture(
        self,
        image: np.ndarray,
        error_context: str,
        output_dir: Path = Path("artifacts/errors")
    ) -> Path:
        """
        Save a capture with automatic timestamped filename.

        Useful for debugging failed detections or unexpected states.

        Args:
            image: Image array to save
            error_context: Context description (e.g., "detection_failed")
            output_dir: Directory to save error captures

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_{error_context}.png"
        filepath = output_dir / filename

        self.save_capture(image, filepath, create_dirs=True)
        return filepath

