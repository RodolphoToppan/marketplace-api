"""Tests for bubble change detection."""

import numpy as np

from src.vision.change_detector import ChangeDetector


def test_higher_sensitivity_detects_small_bubble_change():
    base = np.zeros((100, 100, 3), dtype=np.uint8)
    bubble = base.copy()
    bubble[44:55, 44:55] = 255

    slow = ChangeDetector(sensitivity=0.1, min_change=10)
    slow.detect_change(base)
    assert slow.detect_change(bubble)[0] is False

    fast = ChangeDetector(sensitivity=0.7, min_change=10)
    fast.detect_change(base)
    assert fast.detect_change(bubble)[0] is True
