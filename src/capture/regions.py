"""Screen region management."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScreenRegion:
    """
    Represents a rectangular region on the screen.

    Attributes:
        x: Left coordinate
        y: Top coordinate
        width: Width in pixels
        height: Height in pixels
    """

    x: int
    y: int
    width: int
    height: int

    def __post_init__(self):
        """Validate region coordinates."""
        if self.x < 0:
            raise ValueError(f"x must be >= 0, got {self.x}")
        if self.y < 0:
            raise ValueError(f"y must be >= 0, got {self.y}")
        if self.width <= 0:
            raise ValueError(f"width must be > 0, got {self.width}")
        if self.height <= 0:
            raise ValueError(f"height must be > 0, got {self.height}")

    @property
    def right(self) -> int:
        """Right edge coordinate (x + width)."""
        return self.x + self.width

    @property
    def bottom(self) -> int:
        """Bottom edge coordinate (y + height)."""
        return self.y + self.height

    @property
    def area(self) -> int:
        """Total area in pixels."""
        return self.width * self.height

    def to_mss_monitor(self) -> dict:
        """
        Convert to MSS monitor dictionary format.

        Returns:
            Dictionary compatible with MSS library
        """
        return {
            "left": self.x,
            "top": self.y,
            "width": self.width,
            "height": self.height
        }

    def contains_point(self, x: int, y: int) -> bool:
        """
        Check if a point is within this region.

        Args:
            x: Point x coordinate
            y: Point y coordinate

        Returns:
            True if point is inside region
        """
        return (
            self.x <= x < self.right and
            self.y <= y < self.bottom
        )

    def intersects(self, other: "ScreenRegion") -> bool:
        """
        Check if this region intersects with another.

        Args:
            other: Another screen region

        Returns:
            True if regions overlap
        """
        return not (
            self.right <= other.x or
            other.right <= self.x or
            self.bottom <= other.y or
            other.bottom <= self.y
        )

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ScreenRegion(x={self.x}, y={self.y}, "
            f"width={self.width}, height={self.height})"
        )

