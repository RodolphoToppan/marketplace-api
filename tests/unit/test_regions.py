"""Tests for screen regions."""

import pytest
from src.capture.regions import ScreenRegion


class TestScreenRegion:
    """Tests for ScreenRegion class."""

    def test_valid_region(self):
        """Test creating a valid screen region."""
        region = ScreenRegion(x=100, y=200, width=800, height=600)

        assert region.x == 100
        assert region.y == 200
        assert region.width == 800
        assert region.height == 600

    def test_negative_x_rejected(self):
        """Test that negative x coordinate is rejected."""
        with pytest.raises(ValueError, match="x must be >= 0"):
            ScreenRegion(x=-10, y=0, width=100, height=100)

    def test_negative_y_rejected(self):
        """Test that negative y coordinate is rejected."""
        with pytest.raises(ValueError, match="y must be >= 0"):
            ScreenRegion(x=0, y=-10, width=100, height=100)

    def test_zero_width_rejected(self):
        """Test that zero width is rejected."""
        with pytest.raises(ValueError, match="width must be > 0"):
            ScreenRegion(x=0, y=0, width=0, height=100)

    def test_negative_width_rejected(self):
        """Test that negative width is rejected."""
        with pytest.raises(ValueError, match="width must be > 0"):
            ScreenRegion(x=0, y=0, width=-100, height=100)

    def test_zero_height_rejected(self):
        """Test that zero height is rejected."""
        with pytest.raises(ValueError, match="height must be > 0"):
            ScreenRegion(x=0, y=0, width=100, height=0)

    def test_right_property(self):
        """Test right edge calculation."""
        region = ScreenRegion(x=100, y=200, width=800, height=600)
        assert region.right == 900  # 100 + 800

    def test_bottom_property(self):
        """Test bottom edge calculation."""
        region = ScreenRegion(x=100, y=200, width=800, height=600)
        assert region.bottom == 800  # 200 + 600

    def test_area_property(self):
        """Test area calculation."""
        region = ScreenRegion(x=0, y=0, width=800, height=600)
        assert region.area == 480000  # 800 * 600

    def test_contains_point(self):
        """Test point containment check."""
        region = ScreenRegion(x=100, y=100, width=200, height=200)

        # Inside
        assert region.contains_point(150, 150) is True
        assert region.contains_point(100, 100) is True  # Top-left corner
        assert region.contains_point(299, 299) is True  # Bottom-right (just inside)

        # Outside
        assert region.contains_point(99, 150) is False  # Left of region
        assert region.contains_point(150, 99) is False  # Above region
        assert region.contains_point(300, 150) is False  # Right of region
        assert region.contains_point(150, 300) is False  # Below region

    def test_intersects(self):
        """Test region intersection check."""
        region1 = ScreenRegion(x=100, y=100, width=200, height=200)

        # Overlapping
        region2 = ScreenRegion(x=200, y=200, width=200, height=200)
        assert region1.intersects(region2) is True
        assert region2.intersects(region1) is True

        # Non-overlapping
        region3 = ScreenRegion(x=400, y=400, width=100, height=100)
        assert region1.intersects(region3) is False
        assert region3.intersects(region1) is False

        # Touching edges (not intersecting)
        region4 = ScreenRegion(x=300, y=100, width=100, height=100)
        assert region1.intersects(region4) is False

    def test_to_mss_monitor(self):
        """Test conversion to MSS monitor format."""
        region = ScreenRegion(x=100, y=200, width=800, height=600)
        monitor = region.to_mss_monitor()

        assert monitor == {
            "left": 100,
            "top": 200,
            "width": 800,
            "height": 600
        }

    def test_repr(self):
        """Test string representation."""
        region = ScreenRegion(x=100, y=200, width=800, height=600)
        repr_str = repr(region)

        assert "ScreenRegion" in repr_str
        assert "x=100" in repr_str
        assert "y=200" in repr_str
        assert "width=800" in repr_str
        assert "height=600" in repr_str

    def test_immutable(self):
        """Test that region is immutable (frozen dataclass)."""
        region = ScreenRegion(x=100, y=100, width=200, height=200)

        with pytest.raises(AttributeError):
            region.x = 200

