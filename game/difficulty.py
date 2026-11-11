"""Difficulty configuration and parameter seam.

Rule (§5.1):
"Difficulty changes information and mercy, never story. No difficulty locks a
room, an item, or a solution. HARD removes safety nets, never fairness."

All consumers must read parameters from DifficultyConfig, never branching on
the raw difficulty string directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DifficultyName = Literal["EASY", "MEDIUM", "HARD"]


@dataclass(frozen=True)
class DifficultyConfig:
    """Carries generosity, information, mercy, and pressure parameters.

    Every field is named for what it does, never for the setting it attaches to.
    No field may carry a room id, item id, or solution identifier (ASM-14).
    """

    # --- Generosity (the two bars) ---
    # GP-6: unconfirmed; pre-slice baseline for lantern is 100 on MEDIUM.
    initial_lantern: int = 100
    # GP-6: unconfirmed; pre-slice baseline for composure will be 100 on MEDIUM.
    initial_composure: int = 100

    # --- Information (hints & guidance) ---
    # GP-6: unconfirmed; EASY enables Shadow hint taunts when stuck.
    hints_enabled: bool = False
    # GP-6: unconfirmed; turns in the same room without progress to trigger hint.
    stuck_turn_threshold: int = 3

    # --- Mercy (restart point and journal auto-fill) ---
    # GP-6: unconfirmed; "last_room" vs "start" (EASY restarts at last visited room, HARD at start).
    restart_point_mode: str = "start"
    # GP-6: unconfirmed; EASY auto-records death causes into journal, HARD requires self-learning.
    auto_fill_journal_on_death: bool = False

    # --- Pressure (expiring choices and hesitation) ---
    # GP-6: unconfirmed; HARD causes certain hesitant choices to decay/expire.
    choice_expiry_enabled: bool = False
    # GP-6: unconfirmed; turn budget before an expiring choice decays.
    default_expiry_turns: int = 3


# Config instances for each supported difficulty level.
# Monotonic generosity: EASY >= MEDIUM >= HARD.
# MEDIUM reproduces the pre-slice baseline exactly.
_EASY_CONFIG = DifficultyConfig(
    initial_lantern=100,  # GP-6: unconfirmed (clamped to max capacity 100)
    initial_composure=100,  # GP-6: unconfirmed
    hints_enabled=True,  # GP-6: unconfirmed
    stuck_turn_threshold=3,  # GP-6: unconfirmed
    restart_point_mode="last_room",  # GP-6: unconfirmed
    auto_fill_journal_on_death=True,  # GP-6: unconfirmed
    choice_expiry_enabled=False,  # GP-6: unconfirmed
    default_expiry_turns=0,  # GP-6: unconfirmed
)

_MEDIUM_CONFIG = DifficultyConfig(
    initial_lantern=100,  # Pre-slice baseline
    initial_composure=100,  # Pre-slice baseline
    hints_enabled=False,  # Standard: no free hint narration
    stuck_turn_threshold=999,  # Never triggers
    restart_point_mode="start",  # Pre-slice baseline: restart from the beginning
    auto_fill_journal_on_death=False,  # Pre-slice baseline
    choice_expiry_enabled=False,  # Pre-slice baseline: choices wait indefinitely
    default_expiry_turns=0,
)

_HARD_CONFIG = DifficultyConfig(
    initial_lantern=70,  # GP-6: unconfirmed (tighter oil constraint)
    initial_composure=70,  # GP-6: unconfirmed (shaken nerve)
    hints_enabled=False,  # GP-6: unconfirmed (silent shadow)
    stuck_turn_threshold=999,  # GP-6: unconfirmed
    restart_point_mode="start",  # GP-6: unconfirmed (full restart from the beginning)
    auto_fill_journal_on_death=False,  # GP-6: unconfirmed (no free journal entries)
    choice_expiry_enabled=True,  # GP-6: unconfirmed (hesitation penalty)
    default_expiry_turns=3,  # GP-6: unconfirmed (3-turn window)
)

_CONFIG_MAP: dict[str, DifficultyConfig] = {
    "EASY": _EASY_CONFIG,
    "MEDIUM": _MEDIUM_CONFIG,
    "HARD": _HARD_CONFIG,
}


def get_difficulty_config(difficulty: str | None = None) -> DifficultyConfig:
    """Return the DifficultyConfig for the specified difficulty string.

    Unknown, lowercase, empty, or None values fall back safely to MEDIUM.
    Never raises an exception on malformed input.
    """
    if not difficulty:
        return _MEDIUM_CONFIG
    normalized = str(difficulty).strip().upper()
    return _CONFIG_MAP.get(normalized, _MEDIUM_CONFIG)
