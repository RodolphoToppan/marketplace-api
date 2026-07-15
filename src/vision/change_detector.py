"""Change detection for dynamic visual elements."""

import cv2
import numpy as np
from typing import Optional

from ..observability import get_logger

logger = get_logger(__name__)


class ChangeDetector:
    """
    Detects visual changes in a specific region of the screen.

    Useful for detecting bubbles, animations, or other dynamic elements.
    """

    def __init__(self, sensitivity: float = 0.3, min_change: int = 15):
        """
        Initialize change detector.

        Args:
            sensitivity: Sensitivity to changes (0.0 to 1.0)
            min_change: Minimum pixel value change to consider significant
        """
        self.sensitivity = max(0.0, min(1.0, sensitivity))
        self.min_change = max(1, min_change)
        self.previous_frame: Optional[np.ndarray] = None

        logger.debug(
            f"ChangeDetector initialized: sensitivity={self.sensitivity}, "
            f"min_change={self.min_change}"
        )

    def reset(self) -> None:
        """Reset the detector, clearing previous frame."""
        self.previous_frame = None
        logger.debug("ChangeDetector reset")

    def detect_change(
        self,
        current_frame: np.ndarray,
        region: Optional[tuple] = None
    ) -> tuple[bool, float]:
        """
        Detect if significant change occurred in the frame.

        Args:
            current_frame: Current frame in BGR format
            region: Optional (x, y, width, height) to analyze specific region

        Returns:
            Tuple of (change_detected: bool, change_percentage: float)
        """
        if current_frame is None or current_frame.size == 0:
            logger.warning("Empty frame provided to change detector")
            return False, 0.0

        # Extract region if specified
        if region is not None:
            x, y, w, h = region
            current_frame = current_frame[y:y+h, x:x+w]

        # Convert to grayscale
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise (3x3 kernel for faster processing)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # If this is the first frame, store it and return no change
        if self.previous_frame is None:
            self.previous_frame = gray
            return False, 0.0

        # Compute absolute difference
        frame_diff = cv2.absdiff(self.previous_frame, gray)

        # Threshold the difference
        _, thresh = cv2.threshold(
            frame_diff,
            self.min_change,
            255,
            cv2.THRESH_BINARY
        )

        # Calculate percentage of changed pixels
        changed_pixels = np.count_nonzero(thresh)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        change_percentage = (changed_pixels / total_pixels) * 100

        # Update previous frame
        self.previous_frame = gray

        # Determine if change is significant based on sensitivity.
        # Higher sensitivity = lower threshold for small bubble animations.
        threshold_percentage = max(0.2, (1.0 - self.sensitivity) * 5)
        change_detected = bool(change_percentage >= threshold_percentage)

        if change_detected:
            logger.debug(
                f"Change detected: {change_percentage:.2f}% "
                f"(threshold: {threshold_percentage:.2f}%)"
            )

        return change_detected, change_percentage

    def wait_for_change(
        self,
        frame_generator,
        region: Optional[tuple] = None,
        max_frames: int = 100,
        min_consecutive: int = 2
    ) -> bool:
        """
        Wait for a change to be detected across multiple frames.

        Args:
            frame_generator: Iterator that yields frames
            region: Optional region to monitor
            max_frames: Maximum frames to check before timeout
            min_consecutive: Minimum consecutive detections required

        Returns:
            True if change was detected, False if timeout
        """
        consecutive_detections = 0

        for frame_count, frame in enumerate(frame_generator):
            if frame_count >= max_frames:
                logger.debug(f"Change detection timeout after {max_frames} frames")
                return False

            change_detected, percentage = self.detect_change(frame, region)

            if change_detected:
                consecutive_detections += 1
                if consecutive_detections >= min_consecutive:
                    logger.info(
                        f"Change confirmed after {consecutive_detections} "
                        f"consecutive detections"
                    )
                    return True
            else:
                consecutive_detections = 0

        return False

