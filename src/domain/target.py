"""Target detection models."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BoundingBox:
    """Bounding box coordinates."""

    x: int
    y: int
    width: int
    height: int

    def center(self) -> tuple[int, int]:
        """Calculate the center point of the bounding box."""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return center_x, center_y

    def contains(self, x: int, y: int) -> bool:
        """Check if a point is inside the bounding box."""
        return (
            self.x <= x < self.x + self.width and
            self.y <= y < self.y + self.height
        )


@dataclass(frozen=True)
class DetectionResult:
    """Result of a target detection operation."""

    found: bool
    confidence: float
    center_x: Optional[int] = None
    center_y: Optional[int] = None
    bounding_box: Optional[BoundingBox] = None

    def __post_init__(self):
        """Validate detection result consistency."""
        if self.found:
            if self.center_x is None or self.center_y is None:
                raise ValueError("Found target must have center coordinates")
            if self.bounding_box is None:
                raise ValueError("Found target must have bounding box")
            if not (0.0 <= self.confidence <= 1.0):
                raise ValueError(f"Confidence must be between 0 and 1, got {self.confidence}")
        else:
            if self.confidence > 0.0:
                # Allow confidence > 0 even when not found (below threshold)
                if not (0.0 <= self.confidence <= 1.0):
                    raise ValueError(f"Confidence must be between 0 and 1, got {self.confidence}")

    @classmethod
    def not_found(cls, confidence: float = 0.0) -> "DetectionResult":
        """Create a not-found result."""
        if confidence < 0.0 or confidence > 1.0:
            raise ValueError(f"Confidence must be between 0 and 1, got {confidence}")
        return cls(
            found=False,
            confidence=confidence,
            center_x=None,
            center_y=None,
            bounding_box=None
        )


