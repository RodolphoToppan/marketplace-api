"""Tests for configuration and settings."""

import pytest
from pathlib import Path
import tempfile
import yaml

from src.configuration.settings import (
    Settings,
    RangeConfig,
    ScreenRegion,
    load_settings
)


class TestRangeConfig:
    """Tests for RangeConfig validation."""

    def test_valid_range(self):
        """Test valid min-max range."""
        config = RangeConfig(min=100, max=200)
        assert config.min == 100
        assert config.max == 200

    def test_equal_min_max(self):
        """Test equal min and max values."""
        config = RangeConfig(min=150, max=150)
        assert config.min == config.max

    def test_invalid_range(self):
        """Test that min > max raises error."""
        with pytest.raises(ValueError, match="min .* must be <= max"):
            RangeConfig(min=200, max=100)


class TestScreenRegion:
    """Tests for ScreenRegion configuration."""

    def test_valid_region(self):
        """Test valid screen region."""
        region = ScreenRegion(x=100, y=100, width=800, height=600)
        assert region.x == 100
        assert region.y == 100
        assert region.width == 800
        assert region.height == 600

    def test_zero_width_rejected(self):
        """Test that zero width is rejected."""
        with pytest.raises(ValueError):
            ScreenRegion(x=0, y=0, width=0, height=100)

    def test_negative_coordinates_rejected(self):
        """Test that negative coordinates are rejected."""
        with pytest.raises(ValueError):
            ScreenRegion(x=-10, y=0, width=100, height=100)


class TestSettingsValidation:
    """Tests for complete settings validation."""

    def test_load_default_config(self, tmp_path):
        """Test loading valid configuration."""
        config_data = {
            "application": {
                "name": "test-automation",
                "debug": False,
                "version": "0.1.0"
            },
            "execution": {
                "dry_run": True,
                "random_seed": 42
            },
            "window": {
                "title": "Test Game"
            },
            "regions": {
                "game_area": {
                    "x": 100,
                    "y": 100,
                    "width": 800,
                    "height": 600
                }
            },
            "capture": {
                "interval_ms": 100,
                "idle_interval_ms": 500,
                "save_on_error": True
            },
            "detection": {
                "template": "target.png",
                "threshold": 0.85,
                "required_confirmations": 2,
                "confirmation_interval_ms": 100
            },
            "behavior": {
                "reaction_time_ms": {"min": 180, "max": 350},
                "action_interval_ms": {"min": 250, "max": 600},
                "click_offset_pixels": {"min": -3, "max": 3}
            },
            "safety": {
                "emergency_stop_key": "f12",
                "max_actions_per_run": 10,
                "max_runtime_seconds": 120,
                "max_consecutive_failures": 3
            },
            "logging": {
                "level": "INFO",
                "format": "%(message)s",
                "date_format": "%Y-%m-%d"
            }
        }

        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        settings = load_settings(config_file)

        assert settings.application.name == "test-automation"
        assert settings.execution.dry_run is True
        assert settings.detection.threshold == 0.85

    def test_invalid_threshold_rejected(self):
        """Test that threshold outside 0-1 range is rejected."""
        with pytest.raises(ValueError):
            Settings(
                detection={"threshold": 1.5}  # Invalid
            )

    def test_invalid_log_level_rejected(self, tmp_path):
        """Test that invalid log level is rejected."""
        config_data = {
            "application": {"name": "test", "debug": False},
            "execution": {"dry_run": True, "random_seed": 42},
            "window": {"title": "Test"},
            "regions": {"game_area": {"x": 0, "y": 0, "width": 100, "height": 100}},
            "capture": {"interval_ms": 100, "idle_interval_ms": 500, "save_on_error": True},
            "detection": {
                "template": "test.png",
                "threshold": 0.8,
                "required_confirmations": 2,
                "confirmation_interval_ms": 100
            },
            "behavior": {
                "reaction_time_ms": {"min": 100, "max": 200},
                "action_interval_ms": {"min": 100, "max": 200},
                "click_offset_pixels": {"min": 0, "max": 5}
            },
            "safety": {
                "emergency_stop_key": "f12",
                "max_actions_per_run": 10,
                "max_runtime_seconds": 60,
                "max_consecutive_failures": 3
            },
            "logging": {
                "level": "INVALID",  # Invalid level
                "format": "%(message)s",
                "date_format": "%Y-%m-%d"
            }
        }

        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        with pytest.raises(ValueError, match="Invalid log level"):
            load_settings(config_file)

    def test_config_file_not_found(self):
        """Test error when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            load_settings("nonexistent.yaml")

    def test_idle_interval_less_than_active(self, tmp_path):
        """Test that idle_interval < interval is caught."""
        config_data = {
            "application": {"name": "test", "debug": False},
            "execution": {"dry_run": True, "random_seed": 42},
            "window": {"title": "Test"},
            "regions": {"game_area": {"x": 0, "y": 0, "width": 100, "height": 100}},
            "capture": {
                "interval_ms": 500,  # Active interval
                "idle_interval_ms": 100,  # Idle < Active (invalid)
                "save_on_error": True
            },
            "detection": {
                "template": "test.png",
                "threshold": 0.8,
                "required_confirmations": 2,
                "confirmation_interval_ms": 100
            },
            "behavior": {
                "reaction_time_ms": {"min": 100, "max": 200},
                "action_interval_ms": {"min": 100, "max": 200},
                "click_offset_pixels": {"min": 0, "max": 5}
            },
            "safety": {
                "emergency_stop_key": "f12",
                "max_actions_per_run": 10,
                "max_runtime_seconds": 60,
                "max_consecutive_failures": 3
            },
            "logging": {
                "level": "INFO",
                "format": "%(message)s",
                "date_format": "%Y-%m-%d"
            }
        }

        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        with pytest.raises(ValueError, match="idle_interval_ms .* should be >="):
            load_settings(config_file)


class TestTemplatePathHandling:
    """Tests for template path resolution."""

    def test_get_template_path(self, tmp_path):
        """Test template path resolution."""
        config_data = {
            "application": {"name": "test", "debug": False},
            "execution": {"dry_run": True, "random_seed": 42},
            "window": {"title": "Test"},
            "regions": {"game_area": {"x": 0, "y": 0, "width": 100, "height": 100}},
            "capture": {"interval_ms": 100, "idle_interval_ms": 500, "save_on_error": True},
            "detection": {
                "template": "my_target.png",
                "threshold": 0.8,
                "required_confirmations": 2,
                "confirmation_interval_ms": 100
            },
            "behavior": {
                "reaction_time_ms": {"min": 100, "max": 200},
                "action_interval_ms": {"min": 100, "max": 200},
                "click_offset_pixels": {"min": 0, "max": 5}
            },
            "safety": {
                "emergency_stop_key": "f12",
                "max_actions_per_run": 10,
                "max_runtime_seconds": 60,
                "max_consecutive_failures": 3
            },
            "logging": {"level": "INFO", "format": "%(message)s", "date_format": "%Y-%m-%d"}
        }

        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        settings = load_settings(config_file)
        template_path = settings.get_template_path(tmp_path)

        expected = tmp_path / "assets" / "templates" / "my_target.png"
        assert template_path == expected

    def test_validate_template_exists(self, tmp_path):
        """Test template existence validation."""
        # Create template file
        template_dir = tmp_path / "assets" / "templates"
        template_dir.mkdir(parents=True)
        template_file = template_dir / "test_template.png"
        template_file.write_bytes(b"fake image data")

        config_data = {
            "application": {"name": "test", "debug": False},
            "execution": {"dry_run": True, "random_seed": 42},
            "window": {"title": "Test"},
            "regions": {"game_area": {"x": 0, "y": 0, "width": 100, "height": 100}},
            "capture": {"interval_ms": 100, "idle_interval_ms": 500, "save_on_error": True},
            "detection": {
                "template": "test_template.png",
                "threshold": 0.8,
                "required_confirmations": 2,
                "confirmation_interval_ms": 100
            },
            "behavior": {
                "reaction_time_ms": {"min": 100, "max": 200},
                "action_interval_ms": {"min": 100, "max": 200},
                "click_offset_pixels": {"min": 0, "max": 5}
            },
            "safety": {
                "emergency_stop_key": "f12",
                "max_actions_per_run": 10,
                "max_runtime_seconds": 60,
                "max_consecutive_failures": 3
            },
            "logging": {"level": "INFO", "format": "%(message)s", "date_format": "%Y-%m-%d"}
        }

        config_file = tmp_path / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        settings = load_settings(config_file)

        # Should return True when file exists
        assert settings.validate_template_exists(tmp_path) is True

        # Should return False when file doesn't exist
        settings.detection.template = "nonexistent.png"
        assert settings.validate_template_exists(tmp_path) is False


