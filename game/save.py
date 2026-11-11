"""Single-slot save file serialization and lifecycle management (Task I01, I02).

SUGGEST.md §9.1 & §9.2:
Single-slot JSON persistence storing full RunState snapshot, version, timestamp,
and supporting atomic writes and clean deletion on run termination.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from game.state import RunState

DEFAULT_SAVE_PATH = Path("savegame.json")
SAVE_VERSION = 1


def get_save_path(path: Path | str | None = None) -> Path:
    if path is None:
        return DEFAULT_SAVE_PATH
    return Path(path)


def has_saved_game(path: Path | str | None = None) -> bool:
    """True if a valid, readable save file exists at path."""
    save_path = get_save_path(path)
    if not save_path.exists() or not save_path.is_file():
        return False
    try:
        if save_path.stat().st_size == 0:
            return False
        with open(save_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return isinstance(data, dict) and "state" in data and isinstance(data["state"], dict)
    except Exception:
        return False


def save_to_disk(state: RunState, path: Path | str | None = None) -> bool:
    """Serialize RunState into a JSON file using atomic write-temp-and-rename.

    Returns True on success, False on error.
    """
    save_path = get_save_path(path)
    tmp_path = save_path.with_suffix(f"{save_path.suffix}.tmp")

    envelope = {
        "save_version": SAVE_VERSION,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "current_room": state.current_room,
        "state": state.snapshot(),
    }

    try:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(envelope, f, indent=2)
            f.flush()
        tmp_path.replace(save_path)
        return True
    except Exception:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        return False


def load_from_disk(path: Path | str | None = None) -> Optional[RunState]:
    """Reconstitute RunState from saved file, or return None if missing/invalid."""
    save_path = get_save_path(path)
    if not has_saved_game(save_path):
        return None

    try:
        with open(save_path, "r", encoding="utf-8") as f:
            envelope = json.load(f)
        raw_state = envelope.get("state", {})
        state = RunState.fresh_run()
        state.restore(raw_state)
        return state
    except Exception:
        return None


def delete_saved_game(path: Path | str | None = None) -> bool:
    """Delete the saved game file if present. Returns True if deleted, False if absent."""
    save_path = get_save_path(path)
    if save_path.exists():
        try:
            save_path.unlink()
            return True
        except Exception:
            return False
    return False
