"""Meta-progression profile persistence model (Phase 3 Slice A, Task A01).

SUGGEST.md §9.4:
Cross-run persistence tracking permanently unlocked endings, total escapes,
and total deaths. Ensures that game over or victory purges single-run state
without wiping discovered endings.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

DEFAULT_PROFILE_PATH = Path("data/profile.json")


@dataclass
class PlayerProfile:
    """Persistent player profile tracking meta-progression across runs."""

    unlocked_endings: set[str] = field(default_factory=set)
    total_escapes: int = 0
    total_deaths: int = 0

    def is_ending_unlocked(self, ending_id: str) -> bool:
        """Return True if the specified ending ID has been unlocked."""
        return ending_id in self.unlocked_endings

    def unlock(self, ending_id: str) -> bool:
        """Unlock an ending. Returns True if newly added, False if already present."""
        if ending_id not in self.unlocked_endings:
            self.unlocked_endings.add(ending_id)
            return True
        return False

    def to_dict(self) -> dict[str, Any]:
        """Convert profile to serializable dictionary."""
        return {
            "unlocked_endings": sorted(self.unlocked_endings),
            "total_escapes": self.total_escapes,
            "total_deaths": self.total_deaths,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PlayerProfile:
        """Construct a PlayerProfile from a dictionary with safe fallbacks."""
        raw_endings = data.get("unlocked_endings", [])
        if isinstance(raw_endings, (list, set, tuple)):
            unlocked = {str(e).strip() for e in raw_endings if isinstance(e, str) and str(e).strip()}
        else:
            unlocked = set()

        try:
            escapes = max(0, int(data.get("total_escapes", 0)))
        except (ValueError, TypeError):
            escapes = 0

        try:
            deaths = max(0, int(data.get("total_deaths", 0)))
        except (ValueError, TypeError):
            deaths = 0

        return cls(
            unlocked_endings=unlocked,
            total_escapes=escapes,
            total_deaths=deaths,
        )


def get_profile_path(path: Path | str | None = None) -> Path:
    """Resolve the active profile path."""
    if path is None or path == "":
        return DEFAULT_PROFILE_PATH
    return Path(path)


def save_profile(profile: PlayerProfile, path: Path | str | None = None) -> bool:
    """Serialize PlayerProfile into JSON using atomic write-temp-and-rename.

    Returns True on success, False on error.
    """
    target_path = get_profile_path(path)
    tmp_path = target_path.with_suffix(f"{target_path.suffix}.tmp")

    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(profile.to_dict(), f, indent=2)
            f.flush()
        tmp_path.replace(target_path)
        return True
    except Exception:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except Exception:
                pass
        return False


def load_profile(path: Path | str | None = None) -> PlayerProfile:
    """Load PlayerProfile from disk with graceful fallback to clean default."""
    target_path = get_profile_path(path)
    if not target_path.exists() or not target_path.is_file():
        return PlayerProfile()

    try:
        if target_path.stat().st_size == 0:
            return PlayerProfile()
        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return PlayerProfile()
        return PlayerProfile.from_dict(data)
    except Exception:
        return PlayerProfile()


def unlock_ending(ending_id: str, path: Path | str | None = None) -> bool:
    """Idempotently unlock an ending in the profile and persist the update."""
    if not isinstance(ending_id, str) or not ending_id.strip():
        return False
    profile = load_profile(path)
    profile.unlock(ending_id.strip())
    return save_profile(profile, path)


def get_unlocked_endings(path: Path | str | None = None) -> set[str]:
    """Retrieve the set of unlocked ending IDs."""
    return set(load_profile(path).unlocked_endings)


def record_escape(path: Path | str | None = None) -> bool:
    """Increment total escapes tally and persist."""
    profile = load_profile(path)
    profile.total_escapes += 1
    return save_profile(profile, path)


def record_death(path: Path | str | None = None) -> bool:
    """Increment total deaths tally and persist."""
    profile = load_profile(path)
    profile.total_deaths += 1
    return save_profile(profile, path)


def delete_profile(path: Path | str | None = None) -> bool:
    """Delete the profile file if present. Returns True if deleted, False otherwise."""
    target_path = get_profile_path(path)
    if target_path.exists():
        try:
            target_path.unlink()
            return True
        except Exception:
            return False
    return False
