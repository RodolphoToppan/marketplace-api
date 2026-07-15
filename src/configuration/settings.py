"""Application settings and configuration."""

import yaml
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class RangeConfig(BaseModel):
    """Configuration for a min-max range."""

    min: int
    max: int

    @model_validator(mode='after')
    def validate_range(self) -> 'RangeConfig':
        """Ensure min <= max."""
        if self.min > self.max:
            raise ValueError(f"min ({self.min}) must be <= max ({self.max})")
        return self


class ScreenRegion(BaseModel):
    """Screen region coordinates."""

    x: int = Field(ge=0, description="X coordinate")
    y: int = Field(ge=0, description="Y coordinate")
    width: int = Field(gt=0, description="Width in pixels")
    height: int = Field(gt=0, description="Height in pixels")


class ApplicationConfig(BaseModel):
    """Application metadata."""

    name: str
    debug: bool = False
    version: str = "0.1.0"


class ExecutionConfig(BaseModel):
    """Execution settings."""

    dry_run: bool = True
    random_seed: int = 42


class WindowConfig(BaseModel):
    """Game window configuration."""

    title: str


class RegionsConfig(BaseModel):
    """Screen regions configuration."""

    game_area: ScreenRegion


class CaptureConfig(BaseModel):
    """Screen capture settings."""

    interval_ms: int = Field(gt=0, le=10000)
    idle_interval_ms: int = Field(gt=0, le=10000)
    save_on_error: bool = True

    @model_validator(mode='after')
    def validate_intervals(self) -> 'CaptureConfig':
        """Ensure idle interval >= active interval."""
        if self.idle_interval_ms < self.interval_ms:
            raise ValueError(
                f"idle_interval_ms ({self.idle_interval_ms}) should be >= "
                f"interval_ms ({self.interval_ms})"
            )
        return self


class DetectionConfig(BaseModel):
    """Detection settings."""

    template: str
    threshold: float = Field(ge=0.0, le=1.0)
    required_confirmations: int = Field(ge=1, le=10)
    confirmation_interval_ms: int = Field(gt=0, le=5000)


class BehaviorConfig(BaseModel):
    """Human-like behavior settings."""

    reaction_time_ms: RangeConfig
    action_interval_ms: RangeConfig
    click_offset_pixels: RangeConfig


class SafetyConfig(BaseModel):
    """Safety limits configuration."""

    emergency_stop_key: str
    max_actions_per_run: int = Field(gt=0)
    max_runtime_seconds: int = Field(gt=0)
    max_consecutive_failures: int = Field(gt=0, le=100)


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = "INFO"
    format: str = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @field_validator('level')
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v_upper


class WaterDetectionConfig(BaseModel):
    """Water detection by color configuration."""

    hue_min: int = Field(ge=0, le=180)
    hue_max: int = Field(ge=0, le=180)
    saturation_min: int = Field(ge=0, le=255)
    value_min: int = Field(ge=0, le=255)
    min_area: int = Field(gt=0)


class BubbleDetectionConfig(BaseModel):
    """Bubble detection configuration."""

    method: str = Field(default='change', description="Detection method: 'change' or 'template'")
    sensitivity: float = Field(ge=0.0, le=1.0)
    min_change_threshold: int = Field(ge=1, le=255)
    region_size: int = Field(gt=0)
    template: Optional[str] = Field(default='bubble.png', description="Template filename for template matching")
    template_threshold: float = Field(default=0.8, ge=0.0, le=1.0, description="Confidence threshold for template matching")

    @field_validator('method')
    @classmethod
    def validate_method(cls, v: str) -> str:
        """Validate detection method."""
        valid_methods = {'change', 'template'}
        v_lower = v.lower()
        if v_lower not in valid_methods:
            raise ValueError(f"Invalid detection method: {v}. Must be one of {valid_methods}")
        return v_lower


class FishingTimingConfig(BaseModel):
    """Fishing timing configuration."""

    cast_wait_ms: int = Field(gt=0)
    bubble_wait_min_ms: int = Field(gt=0)
    bubble_wait_max_ms: int = Field(gt=0)
    bubble_check_interval_ms: int = Field(gt=0)
    pull_delay_ms: int = Field(ge=0)
    collect_wait_ms: int = Field(ge=0)
    recast_delay_ms: int = Field(ge=0, default=1000, description="Delay between pulling fish and recasting (fast mode)")
    cooldown_ms: int = Field(ge=0)

    @model_validator(mode='after')
    def validate_timing(self) -> 'FishingTimingConfig':
        """Ensure min <= max for bubble wait."""
        if self.bubble_wait_min_ms > self.bubble_wait_max_ms:
            raise ValueError(
                f"bubble_wait_min_ms ({self.bubble_wait_min_ms}) must be <= "
                f"bubble_wait_max_ms ({self.bubble_wait_max_ms})"
            )
        return self


class FishingHotkeysConfig(BaseModel):
    """Fishing hotkeys configuration."""

    fishing_action: str
    toggle_bot: str


class FishingConfig(BaseModel):
    """Complete fishing automation configuration."""

    water_detection: WaterDetectionConfig
    bubble_detection: BubbleDetectionConfig
    timing: FishingTimingConfig
    hotkeys: FishingHotkeysConfig


class Settings(BaseModel):
    """Complete application settings."""

    application: ApplicationConfig
    execution: ExecutionConfig
    window: WindowConfig
    regions: RegionsConfig
    capture: CaptureConfig
    detection: DetectionConfig
    behavior: BehaviorConfig
    safety: SafetyConfig
    logging: LoggingConfig
    fishing: FishingConfig

    def get_template_path(self, base_path: Optional[Path] = None) -> Path:
        """Get full path to template file."""
        if base_path is None:
            base_path = Path.cwd()

        template_path = base_path / "assets" / "templates" / self.detection.template
        return template_path

    def validate_template_exists(self, base_path: Optional[Path] = None) -> bool:
        """Check if template file exists."""
        template_path = self.get_template_path(base_path)
        return template_path.exists()


def load_settings(config_path: str | Path = "config.yaml") -> Settings:
    """
    Load settings from YAML configuration file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Validated Settings object

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If configuration is invalid
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)

    return Settings(**config_data)


