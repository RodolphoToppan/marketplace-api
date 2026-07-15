"""Color-based detection for game elements."""

import cv2
import numpy as np
from typing import Optional, List, Tuple

from ..observability import get_logger

logger = get_logger(__name__)


class ColorDetector:
    """
    Detects regions in an image based on color ranges in HSV color space.

    Useful for detecting water, specific game elements, or areas by color.
    """

    def __init__(
        self,
        hue_min: int,
        hue_max: int,
        saturation_min: int = 0,
        saturation_max: int = 255,
        value_min: int = 0,
        value_max: int = 255
    ):
        """
        Initialize color detector with HSV range.

        Args:
            hue_min: Minimum hue value (0-180 in OpenCV)
            hue_max: Maximum hue value (0-180 in OpenCV)
            saturation_min: Minimum saturation (0-255)
            saturation_max: Maximum saturation (0-255)
            value_min: Minimum value/brightness (0-255)
            value_max: Maximum value/brightness (0-255)
        """
        self.lower_bound = np.array([hue_min, saturation_min, value_min])
        self.upper_bound = np.array([hue_max, saturation_max, value_max])

        logger.debug(
            f"ColorDetector initialized: H=[{hue_min},{hue_max}] "
            f"S=[{saturation_min},{saturation_max}] V=[{value_min},{value_max}]"
        )

    def detect(
        self,
        image: np.ndarray,
        min_area: int = 100
    ) -> List[Tuple[int, int, int, int]]:
        """
        Detect regions matching the color range.

        Args:
            image: Input image in BGR format (OpenCV default)
            min_area: Minimum area in pixels to consider a valid region

        Returns:
            List of bounding boxes (x, y, width, height) for detected regions
        """
        if image is None or image.size == 0:
            logger.warning("Empty image provided to color detector")
            return []

        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create mask for color range
        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)

        # Apply morphological operations to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # Filter by area and get bounding boxes
        regions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_area:
                x, y, w, h = cv2.boundingRect(contour)
                regions.append((x, y, w, h))

        logger.debug(f"Detected {len(regions)} color regions (min_area={min_area})")

        return regions

    def find_largest_region(
        self,
        image: np.ndarray,
        min_area: int = 100
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Find the largest region matching the color range.

        Args:
            image: Input image in BGR format
            min_area: Minimum area threshold

        Returns:
            Bounding box (x, y, width, height) of largest region, or None
        """
        regions = self.detect(image, min_area)

        if not regions:
            return None

        # Find region with largest area
        largest = max(regions, key=lambda r: r[2] * r[3])

        logger.debug(
            f"Largest region: x={largest[0]} y={largest[1]} "
            f"w={largest[2]} h={largest[3]} area={largest[2]*largest[3]}"
        )

        return largest

    def get_center_of_largest(
        self,
        image: np.ndarray,
        min_area: int = 100
    ) -> Optional[Tuple[int, int]]:
        """
        Get the center point of the largest detected region.

        Args:
            image: Input image in BGR format
            min_area: Minimum area threshold

        Returns:
            (x, y) coordinates of center, or None if no region found
        """
        region = self.find_largest_region(image, min_area)

        if region is None:
            return None

        x, y, w, h = region
        center_x = x + w // 2
        center_y = y + h // 2

        return (center_x, center_y)

