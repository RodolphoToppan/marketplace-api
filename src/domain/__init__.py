"""Domain models and enums."""

from .automation_state import AutomationState
from .target import DetectionResult, BoundingBox

__all__ = ["AutomationState", "DetectionResult", "BoundingBox"]

