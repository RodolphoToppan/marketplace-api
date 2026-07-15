"""Automation state machine states."""

from enum import Enum, auto


class AutomationState(Enum):
    """States of the fishing automation workflow."""

    # General states
    IDLE = auto()                   # Bot is stopped, waiting for activation
    STARTING = auto()               # Bot is initializing
    STOPPING = auto()               # Bot is shutting down
    PAUSED = auto()                 # Bot is temporarily paused
    FAILED = auto()                 # Bot encountered an error

    # Fishing-specific states
    DETECTING_WATER = auto()        # Looking for water (blue area)
    POSITIONING_MOUSE = auto()      # Moving mouse to water position
    CASTING_ROD = auto()            # Pressing Shift+Z to cast
    WAITING_FOR_BUBBLE = auto()     # Waiting minimum time before checking
    DETECTING_BUBBLE = auto()       # Actively watching for bubbles
    PULLING_FISH = auto()           # Pressing Shift+Z to pull
    COLLECTING_LOOT = auto()        # Waiting for loot collection
    COOLDOWN = auto()               # Brief pause before next cast

    def __str__(self) -> str:
        """Return string representation of the state."""
        return self.name

