"""Template-based bubble detection."""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple

from ..observability import get_logger

logger = get_logger(__name__)


class TemplateBubbleDetector:
    """
    Detects bubbles using template matching.

    More accurate than change detection - looks for a specific image.
    """

    def __init__(self, template_path: str, threshold: float = 0.8):
        """
        Initialize template bubble detector.

        Args:
            template_path: Path to bubble template image
            threshold: Matching threshold (0.0 to 1.0)
        """
        self.threshold = threshold
        self.template = None
        self.template_path = Path(template_path)

        # Load template
        if self.template_path.exists():
            self.template = cv2.imread(str(self.template_path))
            if self.template is not None:
                logger.info(
                    f"✓ Bubble template loaded: {template_path} "
                    f"({self.template.shape[1]}x{self.template.shape[0]}px)"
                )
            else:
                logger.error(f"Failed to load template: {template_path}")
        else:
            logger.warning(
                f"Template file not found: {template_path}\n"
                f"Run 'python capture_bubble_template.py' to create one!"
            )

    def detect(
        self,
        image: np.ndarray,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> Tuple[bool, float, Optional[Tuple[int, int]]]:
        """
        Detect bubble in image using template matching.

        Args:
            image: Input image (BGR)
            region: Optional (x, y, width, height) to search within

        Returns:
            Tuple of (found, confidence, position)
            - found: True if bubble detected
            - confidence: Match confidence (0.0 to 1.0)
            - position: (x, y) center of bubble if found, else None
        """
        if self.template is None:
            logger.warning("No template loaded, cannot detect bubbles")
            return False, 0.0, None

        # Extract region if specified
        search_image = image
        offset_x, offset_y = 0, 0

        if region is not None:
            x, y, w, h = region
            # Ensure region is within image bounds
            x = max(0, min(x, image.shape[1] - 1))
            y = max(0, min(y, image.shape[0] - 1))
            w = min(w, image.shape[1] - x)
            h = min(h, image.shape[0] - y)

            search_image = image[y:y+h, x:x+w]
            offset_x, offset_y = x, y

        if search_image.size == 0:
            return False, 0.0, None

        # Ensure template is smaller than search area
        if (self.template.shape[0] > search_image.shape[0] or
            self.template.shape[1] > search_image.shape[1]):
            logger.warning(
                f"Template ({self.template.shape[1]}x{self.template.shape[0]}) "
                f"larger than search area ({search_image.shape[1]}x{search_image.shape[0]})"
            )
            return False, 0.0, None

        # Perform template matching
        try:
            result = cv2.matchTemplate(
                search_image,
                self.template,
                cv2.TM_CCOEFF_NORMED
            )

            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # max_val is the confidence (0 to 1)
            confidence = float(max_val)

            if confidence >= self.threshold:
                # Calculate center position
                template_h, template_w = self.template.shape[:2]
                center_x = max_loc[0] + template_w // 2 + offset_x
                center_y = max_loc[1] + template_h // 2 + offset_y

                return True, confidence, (center_x, center_y)
            else:
                return False, confidence, None

        except Exception as e:
            logger.error(f"Template matching failed: {e}")
            return False, 0.0, None

