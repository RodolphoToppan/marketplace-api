"""Fishing automation bot."""

import time
import threading
from typing import Optional, Tuple
import cv2
import numpy as np
from pathlib import Path

from ..domain import AutomationState
from ..configuration import Settings
from ..capture import ScreenCapture, ScreenRegion
from ..vision import ColorDetector, ChangeDetector
from ..actions import InputController, HotkeyManager
from ..observability import get_logger

logger = get_logger(__name__)


class FishingBot:
    """
    Main fishing automation bot.

    Manages the complete fishing workflow:
    1. Detect water (blue area)
    2. Position mouse over water
    3. Cast rod (Shift+Z)
    4. Wait for bubbles
    5. Pull fish (Shift+Z)
    6. Collect loot
    7. Repeat
    """

    def __init__(self, settings: Settings):
        """
        Initialize fishing bot.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.state = AutomationState.IDLE
        self.running = False
        self._state_lock = threading.Lock()

        # Initialize components
        self.screen_capture = ScreenCapture()
        self.input_controller = InputController(
            dry_run=settings.execution.dry_run,
            click_offset_range=(
                settings.behavior.click_offset_pixels.min,
                settings.behavior.click_offset_pixels.max
            ),
            movement_duration_range=(
                settings.behavior.reaction_time_ms.min / 1000,
                settings.behavior.reaction_time_ms.max / 1000
            )
        )

        # Initialize detectors
        self.water_detector = ColorDetector(
            hue_min=settings.fishing.water_detection.hue_min,
            hue_max=settings.fishing.water_detection.hue_max,
            saturation_min=settings.fishing.water_detection.saturation_min,
            value_min=settings.fishing.water_detection.value_min
        )

        # Initialize bubble detector based on method
        detection_method = settings.fishing.bubble_detection.method

        if detection_method == 'template':
            from ..vision import TemplateBubbleDetector
            from pathlib import Path

            template_path = Path('assets/templates') / settings.fishing.bubble_detection.template
            self.bubble_detector = TemplateBubbleDetector(
                template_path=str(template_path),
                threshold=settings.fishing.bubble_detection.template_threshold
            )
            self.bubble_detection_method = 'template'
            logger.info(f"Using TEMPLATE bubble detection (threshold={settings.fishing.bubble_detection.template_threshold})")
        else:
            from ..vision import ChangeDetector

            self.bubble_detector = ChangeDetector(
                sensitivity=settings.fishing.bubble_detection.sensitivity,
                min_change=settings.fishing.bubble_detection.min_change_threshold
            )
            self.bubble_detection_method = 'change'
            logger.info(f"Using CHANGE bubble detection (sensitivity={settings.fishing.bubble_detection.sensitivity})")

        # Hotkey manager
        self.hotkey_manager = HotkeyManager()

        # Statistics
        self.stats = {
            "casts": 0,
            "successful_catches": 0,
            "failed_catches": 0,
            "total_runtime": 0.0,
            "start_time": None
        }

        # Game region
        config_region = settings.regions.game_area
        self.game_region = ScreenRegion(
            x=config_region.x,
            y=config_region.y,
            width=config_region.width,
            height=config_region.height
        )

        # Last water position
        self._last_water_pos: Optional[Tuple[int, int]] = None
        self._rod_already_cast = False
        self._challenge_fish_templates = self._load_challenge_fish_templates()

        logger.info("FishingBot initialized")

    def _load_challenge_fish_templates(self) -> list[np.ndarray]:
        """Load color-agnostic fish templates for the optional challenge."""
        templates = []
        template_dir = Path("assets/templates")
        for path in sorted(template_dir.glob("fishing_challenge_fish_*.png")):
            image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if image is not None and image.size:
                templates.append(cv2.Canny(image, 50, 150))

        if templates:
            logger.info(f"Loaded {len(templates)} fishing challenge fish templates")

        return templates

    def _change_state(self, new_state: AutomationState) -> None:
        """Change bot state with logging."""
        with self._state_lock:
            old_state = self.state
            self.state = new_state
            logger.info(f"State transition: {old_state} → {new_state}")

    def toggle(self) -> None:
        """Toggle bot on/off."""
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self) -> None:
        """Start the fishing bot."""
        if self.running:
            logger.warning("Bot is already running")
            return

        self.running = True
        self.stats["start_time"] = time.time()
        self._change_state(AutomationState.STARTING)

        logger.info("🎣 Fishing bot started!")
        logger.info(f"Hotkey: {self.settings.fishing.hotkeys.toggle_bot} to stop")

        # Start fishing loop in a separate thread
        self._fishing_thread = threading.Thread(target=self._fishing_loop, daemon=True)
        self._fishing_thread.start()

    def stop(self) -> None:
        """Stop the fishing bot."""
        if not self.running:
            logger.warning("Bot is not running")
            return

        self.running = False
        self._change_state(AutomationState.STOPPING)

        # Calculate stats
        if self.stats["start_time"]:
            self.stats["total_runtime"] = time.time() - self.stats["start_time"]

        logger.info("🛑 Fishing bot stopped")
        logger.info(f"Statistics:")
        logger.info(f"  - Total casts: {self.stats['casts']}")
        logger.info(f"  - Successful: {self.stats['successful_catches']}")
        logger.info(f"  - Failed: {self.stats['failed_catches']}")
        logger.info(f"  - Runtime: {self.stats['total_runtime']:.1f}s")

        self._change_state(AutomationState.IDLE)

    def _fishing_loop(self) -> None:
        """Main fishing loop."""
        try:
            while self.running:
                try:
                    self._execute_fishing_cycle()
                except Exception as e:
                    logger.error(f"Error in fishing cycle: {e}", exc_info=True)
                    self.stats["failed_catches"] += 1

                    # Cooldown after error
                    time.sleep(self.settings.fishing.timing.cooldown_ms / 1000)
        except Exception as e:
            logger.critical(f"Fatal error in fishing loop: {e}", exc_info=True)
            self.stop()

    def _execute_fishing_cycle(self) -> None:
        """Execute one complete fishing cycle - MODO ULTRA-RÁPIDO."""
        if self._rod_already_cast:
            self._rod_already_cast = False
        else:
            # Step 1: Detect water
            water_pos = self._detect_water()
            if water_pos is None:
                logger.warning("Could not detect water, retrying...")
                time.sleep(0.5)  # Reduzido de 1.0 para 0.5
                return

            # Step 2: Position mouse
            self._position_mouse(water_pos)

            # Step 3: Cast rod
            self._cast_rod()

        # Step 4: Wait for bubble
        bubble_detected = self._wait_for_bubble()

        # Step 5: Pull fish and IMMEDIATELY recast (modo jogador focado!)
        if bubble_detected:
            self._pull_fish()

            self._handle_fishing_challenge()
            self._recast_rod()

            self.stats["successful_catches"] += 1
        else:
            logger.warning("Bubble detection timeout")
            self.stats["failed_catches"] += 1
            # Cooldown reduzido em caso de falha
            time.sleep(self.settings.fishing.timing.cooldown_ms / 1000)

        # Step 6: Cooldown final mínimo (já lançou acima se sucesso)
        if not bubble_detected:
            self._cooldown()

    def _recast_rod(self) -> None:
        """Recast without re-detecting water after a successful catch."""
        total_wait = self.settings.fishing.timing.collect_wait_ms + self.settings.fishing.timing.recast_delay_ms
        if total_wait > 0:
            time.sleep(total_wait / 1000)

        if self.running:
            self._cast_rod()
            self._rod_already_cast = True

    def _handle_fishing_challenge(self) -> bool:
        """Solve the optional fishing challenge when it appears."""
        with self.screen_capture:
            challenge = self._wait_for_challenge(self.screen_capture)
            if challenge is None:
                return False

            logger.info("🎯 Fishing challenge detected")
            missing_frames = 0
            deadline = time.time() + 30

            while self.running and time.time() < deadline:
                frame = self.screen_capture.capture(self.game_region)
                challenge = self._locate_challenge(frame)

                if challenge is None:
                    missing_frames += 1
                    if missing_frames >= 5:
                        logger.info("✅ Fishing challenge finished")
                        return True
                    time.sleep(0.05)
                    continue

                missing_frames = 0
                fish_y, bar_y = challenge

                if bar_y > fish_y + 8:
                    self.input_controller.keyboard.press_key("space", duration=0.04)
                else:
                    time.sleep(0.03)

        logger.warning("Fishing challenge timed out")
        return False

    def _wait_for_challenge(self, screen_capture: ScreenCapture) -> Optional[Tuple[float, float]]:
        """Wait briefly for the fishing challenge UI after pulling."""
        deadline = time.time() + 0.35
        while self.running and time.time() < deadline:
            frame = screen_capture.capture(self.game_region)
            challenge = self._locate_challenge(frame)
            if challenge is not None:
                return challenge
            time.sleep(0.05)
        return None

    def _locate_challenge(self, frame: np.ndarray) -> Optional[Tuple[float, float]]:
        """Return (fish_y, bar_y) for the fishing challenge, if visible."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dark = cv2.inRange(hsv, np.array([0, 0, 0]), np.array([180, 255, 55]))
        count, labels, stats, _ = cv2.connectedComponentsWithStats(dark)

        candidates = []
        for label in range(1, count):
            x, y, w, h, area = stats[label]
            if 8 <= w <= 40 and h >= frame.shape[0] * 0.22 and area >= 500:
                candidates.append((h, area, x, y, w))

        if not candidates:
            return None

        _, _, rail_x, _, rail_w = max(candidates)
        rail_center_x = rail_x + rail_w // 2
        x0 = max(0, rail_center_x - 35)
        x1 = min(frame.shape[1], rail_center_x + 35)

        rail_dark = dark[:, max(0, rail_center_x - 10):min(frame.shape[1], rail_center_x + 10)]
        ys = np.where(rail_dark > 0)[0]
        if ys.size == 0:
            return None

        y0 = max(0, int(ys.min()) - 10)
        y1 = min(frame.shape[0], int(ys.max()) + 10)
        roi = hsv[y0:y1, x0:x1]
        gray_roi = cv2.cvtColor(frame[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)

        purple = cv2.inRange(roi, np.array([135, 70, 70]), np.array([175, 255, 255]))
        blue_x0 = max(0, rail_center_x - 12 - x0)
        blue_x1 = min(roi.shape[1], rail_center_x + 12 - x0)
        blue = cv2.inRange(roi[:, blue_x0:blue_x1], np.array([85, 80, 120]), np.array([115, 255, 255]))

        fish_y = self._fish_template_center_y(gray_roi, y0)
        if fish_y is None:
            fish_y = self._mask_center_y(purple, y0, min_area=40)
        bar_y = self._mask_center_y(blue, y0, min_area=25)
        if fish_y is None or bar_y is None:
            return None

        return fish_y, bar_y

    def _fish_template_center_y(self, gray_roi: np.ndarray, offset_y: int) -> Optional[float]:
        if not self._challenge_fish_templates:
            return None

        edges = cv2.Canny(gray_roi, 50, 150)
        best_score = 0.0
        best_y = None

        for template in self._challenge_fish_templates:
            if template.shape[0] > edges.shape[0] or template.shape[1] > edges.shape[1]:
                continue

            result = cv2.matchTemplate(edges, template, cv2.TM_CCOEFF_NORMED)
            _, score, _, location = cv2.minMaxLoc(result)
            if score > best_score:
                best_score = score
                best_y = location[1] + template.shape[0] / 2 + offset_y

        if best_score < 0.18:
            return None

        return float(best_y)

    def _mask_center_y(self, mask: np.ndarray, offset_y: int, min_area: int) -> Optional[float]:
        count, labels, stats, centers = cv2.connectedComponentsWithStats(mask)
        best = None
        for label in range(1, count):
            area = stats[label, cv2.CC_STAT_AREA]
            if area >= min_area and (best is None or area > stats[best, cv2.CC_STAT_AREA]):
                best = label

        if best is None:
            return None

        return float(centers[best][1] + offset_y)

    def _detect_water(self) -> Optional[Tuple[int, int]]:
        """Detect water and return center position."""
        self._change_state(AutomationState.DETECTING_WATER)

        with self.screen_capture:
            image = self.screen_capture.capture(self.game_region)
            center = self.water_detector.get_center_of_largest(
                image,
                min_area=self.settings.fishing.water_detection.min_area
            )

        if center:
            # Convert relative to absolute coordinates
            abs_x = self.game_region.x + center[0]
            abs_y = self.game_region.y + center[1]
            self._last_water_pos = (abs_x, abs_y)
            logger.debug(f"Water detected at ({abs_x}, {abs_y})")
            return (abs_x, abs_y)

        return self._last_water_pos  # Use last known position

    def _position_mouse(self, position: Tuple[int, int]) -> None:
        """Position mouse over water."""
        self._change_state(AutomationState.POSITIONING_MOUSE)

        x, y = position
        self.input_controller.mouse.move_to(x, y, apply_offset=True)

        # No delay needed - movement is already handled by input_controller

    def _cast_rod(self) -> None:
        """Cast the fishing rod."""
        self._change_state(AutomationState.CASTING_ROD)

        # Parse hotkey (e.g., "shift+z" -> ["shift", "z"])
        keys = self.settings.fishing.hotkeys.fishing_action.split('+')
        self.input_controller.keyboard.press_hotkey(*keys)

        self.stats["casts"] += 1
        logger.debug("Rod cast")

        # Wait after casting
        time.sleep(self.settings.fishing.timing.cast_wait_ms / 1000)

    def _wait_for_bubble(self) -> bool:
        """Wait for bubble to appear."""
        self._change_state(AutomationState.WAITING_FOR_BUBBLE)

        # Wait minimum time before checking
        time.sleep(self.settings.fishing.timing.bubble_wait_min_ms / 1000)

        self._change_state(AutomationState.DETECTING_BUBBLE)

        # Different logic for different detection methods
        if self.bubble_detection_method == 'template':
            return self._wait_for_bubble_template()
        else:
            return self._wait_for_bubble_change()

    def _wait_for_bubble_template(self) -> bool:
        """Wait for bubble using template matching."""
        # Define region around bobber
        mouse_x, mouse_y = self.input_controller.mouse.get_position()
        region_size = self.settings.fishing.bubble_detection.region_size
        half_size = region_size // 2

        rel_x = mouse_x - self.game_region.x - half_size
        rel_y = mouse_y - self.game_region.y - half_size
        rel_x = max(0, min(rel_x, self.game_region.width - region_size))
        rel_y = max(0, min(rel_y, self.game_region.height - region_size))

        bubble_region = ScreenRegion(
            x=self.game_region.x + rel_x,
            y=self.game_region.y + rel_y,
            width=region_size,
            height=region_size
        )

        logger.info(
            f"🔍 [TEMPLATE] Monitoring for bubble template at "
            f"region: x={rel_x}, y={rel_y}, size={region_size}x{region_size}"
        )

        max_wait = self.settings.fishing.timing.bubble_wait_max_ms
        check_interval = self.settings.fishing.timing.bubble_check_interval_ms
        max_checks = max_wait // check_interval

        start_time = time.time()
        check_count = 0

        with self.screen_capture:
            for check in range(max_checks):
                if not self.running:
                    return False

                check_count += 1
                frame = self.screen_capture.capture(bubble_region)

                # Use template matching
                found, confidence, position = self.bubble_detector.detect(frame)

                # Log less frequently to improve performance (every 20 checks instead of 10)
                if check_count % 20 == 0:
                    logger.debug(
                        f"Check #{check_count}: confidence={confidence:.3f} "
                        f"(threshold={self.settings.fishing.bubble_detection.template_threshold})"
                    )

                if found:
                    elapsed = (time.time() - start_time) * 1000
                    logger.info(
                        f"💧 Bubble template FOUND! "
                        f"time={elapsed:.0f}ms, confidence={confidence:.3f}, "
                        f"position={position}"
                    )
                    return True

                time.sleep(check_interval / 1000)

        elapsed_total = (time.time() - start_time) * 1000
        logger.warning(
            f"⏱️ Bubble template detection timeout after {elapsed_total:.0f}ms "
            f"({check_count} checks)"
        )
        return False

    def _wait_for_bubble_change(self) -> bool:
        """Wait for bubble using change detection (original method) - ULTRA-RÁPIDO."""
        # Reset bubble detector
        self.bubble_detector.reset()

        # Define region around bobber (use last mouse position)
        mouse_x, mouse_y = self.input_controller.mouse.get_position()
        region_size = self.settings.fishing.bubble_detection.region_size
        half_size = region_size // 2

        # Convert to game region relative coordinates
        rel_x = mouse_x - self.game_region.x - half_size
        rel_y = mouse_y - self.game_region.y - half_size

        # Clamp to game region bounds
        rel_x = max(0, min(rel_x, self.game_region.width - region_size))
        rel_y = max(0, min(rel_y, self.game_region.height - region_size))

        bubble_region = ScreenRegion(
            x=self.game_region.x + rel_x,
            y=self.game_region.y + rel_y,
            width=region_size,
            height=region_size
        )

        logger.info(
            f"🔍 [CHANGE] Monitoring region: x={rel_x}, y={rel_y}, size={region_size}x{region_size} "
            f"(sensitivity={self.settings.fishing.bubble_detection.sensitivity})"
        )

        # Monitor for changes
        max_wait = self.settings.fishing.timing.bubble_wait_max_ms
        check_interval = self.settings.fishing.timing.bubble_check_interval_ms
        max_checks = max_wait // check_interval

        start_time = time.time()
        check_count = 0
        consecutive_detections = 0
        stable_frames = 0
        detector_armed = False
        arming_timeout_ms = 700
        change_threshold = max(0.2, (1.0 - self.settings.fishing.bubble_detection.sensitivity) * 5)

        with self.screen_capture:
            for _ in range(max_checks):
                if not self.running:
                    return False

                check_count += 1

                # Capture frame
                frame = self.screen_capture.capture(bubble_region)

                # Check for change
                change_detected, percentage = self.bubble_detector.detect_change(frame)

                # Log a cada 10 verificações para debug
                if check_count % 10 == 0:
                    logger.debug(f"Check #{check_count}: change={percentage:.2f}%")

                elapsed = (time.time() - start_time) * 1000
                if not detector_armed:
                    if percentage < change_threshold:
                        stable_frames += 1
                    else:
                        stable_frames = 0

                    if stable_frames >= 2 or elapsed >= arming_timeout_ms:
                        detector_armed = True
                    else:
                        time.sleep(check_interval / 1000)
                        continue

                if change_detected:
                    consecutive_detections += 1
                else:
                    consecutive_detections = 0

                if consecutive_detections >= 3:
                    logger.info(f"💧 Bubble DETECTED! time={elapsed:.0f}ms, change={percentage:.2f}%")
                    return True

                # Wait before next check
                time.sleep(check_interval / 1000)

        elapsed_total = (time.time() - start_time) * 1000
        logger.warning(f"⏱️ Bubble timeout after {elapsed_total:.0f}ms ({check_count} checks)")
        return False

    def _pull_fish(self) -> None:
        """Pull the fish."""
        self._change_state(AutomationState.PULLING_FISH)

        # Small reaction delay
        time.sleep(self.settings.fishing.timing.pull_delay_ms / 1000)

        # Press fishing action key
        keys = self.settings.fishing.hotkeys.fishing_action.split('+')

        logger.info(f"🐟 Pulling fish with hotkey: {'+'.join(keys)}")
        self.input_controller.keyboard.press_hotkey(*keys)

        logger.debug("Fish pulled")

    def _wait_for_collection(self) -> None:
        """Wait for loot to be collected."""
        self._change_state(AutomationState.COLLECTING_LOOT)

        time.sleep(self.settings.fishing.timing.collect_wait_ms / 1000)

    def _cooldown(self) -> None:
        """Brief cooldown between casts."""
        self._change_state(AutomationState.COOLDOWN)

        time.sleep(self.settings.fishing.timing.cooldown_ms / 1000)

    def register_hotkeys(self) -> None:
        """Register global hotkeys."""
        toggle_key = self.settings.fishing.hotkeys.toggle_bot
        self.hotkey_manager.register_hotkey(toggle_key, self.toggle)
        logger.info(f"Registered toggle hotkey: {toggle_key}")

    def unregister_hotkeys(self) -> None:
        """Unregister all hotkeys."""
        self.hotkey_manager.unregister_all()

    def __enter__(self):
        """Context manager entry."""
        self.register_hotkeys()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        if self.running:
            self.stop()
        self.unregister_hotkeys()
