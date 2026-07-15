"""
Local Game Automation - Fishing Bot

Academic project for learning computer vision, automation, and decision-making.
For use only with local educational game environments.
"""

import sys
from pathlib import Path
import time

from .configuration import load_settings
from .observability import setup_logging, get_logger
from .application import FishingBot

logger = get_logger(__name__)


def validate_environment(settings) -> bool:
    """
    Validate the execution environment.

    Args:
        settings: Application settings

    Returns:
        True if environment is valid
    """
    errors = []

    # Check dry-run mode
    if not settings.execution.dry_run:
        logger.warning(
            "⚠️  dry_run is DISABLED. Real actions WILL be executed!"
        )
        response = input("Continue in REAL mode? (type 'yes' to confirm): ")
        if response.lower() != 'yes':
            logger.info("Aborting - staying in safe mode")
            return False

    # Validate artifacts directory
    artifacts_dir = Path("artifacts/errors")
    if not artifacts_dir.exists():
        logger.info(f"Creating artifacts directory: {artifacts_dir}")
        artifacts_dir.mkdir(parents=True, exist_ok=True)

    if errors:
        logger.error("Environment validation failed:")
        for error in errors:
            logger.error(f"  - {error}")
        return False

    return True


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    try:
        # Load configuration
        logger.info("Loading configuration...")
        settings = load_settings("config.yaml")

        # Setup logging with configuration
        setup_logging(
            level=settings.logging.level,
            log_format=settings.logging.format,
            date_format=settings.logging.date_format
        )

        logger.info("=" * 70)
        logger.info(f"🎣 {settings.application.name} v{settings.application.version}")
        logger.info("Academic Computer Vision Project - Fishing Automation")
        logger.info("=" * 70)

        # Log execution mode
        if settings.execution.dry_run:
            logger.info("🔒 Running in DRY-RUN mode (safe, no real actions)")
        else:
            logger.warning("⚠️  Running in REAL mode (actions WILL be executed)")

        # Validate environment
        if not validate_environment(settings):
            logger.error("Environment validation failed. Exiting.")
            return 1

        logger.info("Configuration loaded successfully")
        logger.info(f"  - Game window: {settings.window.title}")
        logger.info(f"  - Game region: {settings.regions.game_area}")
        logger.info(f"  - Fishing hotkey: {settings.fishing.hotkeys.fishing_action}")
        logger.info(f"  - Toggle hotkey: {settings.fishing.hotkeys.toggle_bot}")

        logger.info("\n" + "=" * 70)
        logger.info("🎣 FISHING BOT - Instructions")
        logger.info("=" * 70)
        logger.info(f"1. Position your game window within the configured region")
        logger.info(f"2. Make sure water (blue area) is visible on screen")
        logger.info(f"3. Press {settings.fishing.hotkeys.toggle_bot} to START the bot")
        logger.info(f"4. Press {settings.fishing.hotkeys.toggle_bot} again to STOP")
        logger.info(f"5. Bot will automatically:")
        logger.info(f"   - Detect water")
        logger.info(f"   - Cast rod ({settings.fishing.hotkeys.fishing_action})")
        logger.info(f"   - Wait for bubbles")
        logger.info(f"   - Pull fish automatically")
        logger.info(f"   - Repeat the process")
        logger.info("=" * 70)

        # Create and run fishing bot
        with FishingBot(settings) as bot:
            logger.info(f"\n✅ Bot ready! Press {settings.fishing.hotkeys.toggle_bot} to start fishing...")
            logger.info("Press Ctrl+C to exit the application")

            # Keep running until interrupted
            try:
                while True:
                    time.sleep(0.5)
            except KeyboardInterrupt:
                logger.info("\n\n🛑 Shutting down...")

        logger.info("=" * 70)
        logger.info("✅ Application exited successfully")
        logger.info("=" * 70)

        return 0

    except FileNotFoundError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Application interrupted by user")
        return 0
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())




