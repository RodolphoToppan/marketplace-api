"""Tests for detection result models."""

import pytest
from src.domain.target import DetectionResult, BoundingBox


class TestBoundingBox:
    """Tests for BoundingBox class."""

    def test_valid_bounding_box(self):
        """Test creating a valid bounding box."""
        bbox = BoundingBox(x=100, y=200, width=50, height=60)

        assert bbox.x == 100
        assert bbox.y == 200
        assert bbox.width == 50
        assert bbox.height == 60

    def test_center_calculation(self):
        """Test center point calculation."""
        bbox = BoundingBox(x=100, y=200, width=50, height=60)
        center_x, center_y = bbox.center()

        assert center_x == 125  # 100 + 50//2
        assert center_y == 230  # 200 + 60//2

    def test_contains_point(self):
        """Test point containment."""
        bbox = BoundingBox(x=100, y=200, width=50, height=60)

        # Inside
        assert bbox.contains(125, 230) is True
        assert bbox.contains(100, 200) is True  # Top-left
        assert bbox.contains(149, 259) is True  # Bottom-right (just inside)

        # Outside
        assert bbox.contains(99, 230) is False
        assert bbox.contains(150, 230) is False
        assert bbox.contains(125, 199) is False
        assert bbox.contains(125, 260) is False

    def test_immutable(self):
        """Test that bounding box is immutable."""
        bbox = BoundingBox(x=100, y=200, width=50, height=60)

        with pytest.raises(AttributeError):
            bbox.x = 200


class TestDetectionResult:
    """Tests for DetectionResult class."""

    def test_successful_detection(self):
        """Test creating a successful detection result."""
        bbox = BoundingBox(x=100, y=200, width=50, height=60)
        result = DetectionResult(
            found=True,
            confidence=0.95,
            center_x=125,
            center_y=230,
            bounding_box=bbox
        )

        assert result.found is True
        assert result.confidence == 0.95
        assert result.center_x == 125
        assert result.center_y == 230
        assert result.bounding_box == bbox

    def test_not_found_factory(self):
        """Test creating not-found result."""
        result = DetectionResult.not_found(confidence=0.42)

        assert result.found is False
        assert result.confidence == 0.42
        assert result.center_x is None
        assert result.center_y is None
        assert result.bounding_box is None

    def test_not_found_default_confidence(self):
        """Test not-found with default confidence."""
        result = DetectionResult.not_found()

        assert result.found is False
        assert result.confidence == 0.0

    def test_found_without_center_rejected(self):
        """Test that found=True without center is rejected."""
        bbox = BoundingBox(x=100, y=200, width=50, height=60)

        with pytest.raises(ValueError, match="Found target must have center"):
            DetectionResult(
                found=True,
                confidence=0.95,
                center_x=None,  # Missing
                center_y=230,
                bounding_box=bbox
            )

    def test_found_without_bbox_rejected(self):
        """Test that found=True without bounding box is rejected."""
        with pytest.raises(ValueError, match="Found target must have bounding box"):
            DetectionResult(
                found=True,
                confidence=0.95,
                center_x=125,
                center_y=230,
                bounding_box=None  # Missing
            )

    def test_invalid_confidence_rejected(self):
        """Test that confidence outside 0-1 range is rejected."""
        bbox = BoundingBox(x=100, y=200, width=50, height=60)

        with pytest.raises(ValueError, match="Confidence must be between 0 and 1"):
            DetectionResult(
                found=True,
                confidence=1.5,  # Invalid
                center_x=125,
                center_y=230,
                bounding_box=bbox
            )

    def test_negative_confidence_rejected(self):
        """Test that negative confidence is rejected."""
        with pytest.raises(ValueError, match="Confidence must be between 0 and 1"):
            DetectionResult.not_found(confidence=-0.1)

    def test_immutable(self):
        """Test that detection result is immutable."""
        result = DetectionResult.not_found()

        with pytest.raises(AttributeError):
            result.found = True

