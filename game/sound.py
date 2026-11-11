"""Audio dispatch service for terminal system bell horror cues (Task H01).

SUGGEST.md §5.2:
The system bell is the terminal's horror channel:
- CUE_DOOR_OPEN: When a door silently swings open or unlatches.
- CUE_DOG_CHAIN: When the Hell Dog's iron chain rattles.
- CUE_SHADOW_WHISPER: When the Shadow delivers a direct whisper.
"""

from __future__ import annotations

import sys
from typing import Any

CUE_DOOR_OPEN = "door_open"
CUE_DOG_CHAIN = "dog_chain"
CUE_SHADOW_WHISPER = "shadow_whisper"

VALID_CUES = {CUE_DOOR_OPEN, CUE_DOG_CHAIN, CUE_SHADOW_WHISPER}


def is_sound_enabled(app: Any) -> bool:
    """Check if sound is enabled in application configuration."""
    if app is None:
        return False
    config = getattr(app, "config", None)
    if config is None:
        return False
    if hasattr(config, "get"):
        return bool(config.get("sound", True))
    if isinstance(config, dict):
        return bool(config.get("sound", True))
    return False


def play_cue(app: Any, cue_name: str) -> bool:
    """Trigger a terminal bell horror cue if sound is enabled.

    Returns True if the cue was played/emitted, False if suppressed or disabled.
    Handles headless or broken stdout gracefully without raising exceptions.
    """
    if cue_name not in VALID_CUES:
        raise ValueError(f"Unknown sound cue: '{cue_name}'")

    if not is_sound_enabled(app):
        return False

    try:
        if app is not None and hasattr(app, "bell"):
            app.bell()
            return True
        sys.stdout.write("\a")
        sys.stdout.flush()
        return True
    except (IOError, OSError):
        return False
