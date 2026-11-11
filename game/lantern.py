"""Lantern drain rules and cost calculator for Escape from Shadows.

Every room the player enters costs oil. Drains are faster for slow, careful
actions (reading, searching) and slower in rooms already lit (revisits).
At zero oil, darkness falls and the Shadow can reach the player.

Design rules (SUGGEST.md §3.1, §4.1, §4.2):
- Drains are constants with names defined once at module level.
- Revisiting a room costs less than a first visit.
- Slow/careful actions cost significantly more than a standard step.
- Helpers are pure calculations that do not mutate RunState directly.
- Running out of oil triggers a telegraphed death consequence with a clear cause.
"""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from game.state import RunState

# Drain amounts (MEDIUM difficulty baseline)
FIRST_VISIT_DRAIN: int = 10
REVISIT_DRAIN: int = 5
CAREFUL_ACTION_DRAIN: int = 25
STEP_ACTION_DRAIN: int = 10

# Warning and terminal consequence thresholds
LOW_OIL_WARNING_THRESHOLD: int = 30

ZERO_OIL_DEATH_CAUSE: str = (
    "The lantern guttered out and darkness swallowed you; the Shadow claimed you."
)
ZERO_OIL_DEATH_LESSON: str = (
    "Light is your only shield against the Shadow; never let the wick burn dry."
)

ZERO_OIL_TELEGRAPHS: list[str] = [
    "The flame sputters and drops to a shivering ember; the edges of the room dissolve into blackness.",
    "A freezing draft washes over your neck, carrying the quiet certainty of something waiting in the dark.",
]


def drain_for_room(state: RunState, room_id: str) -> int:
    """Calculate oil cost to enter a room.

    Returns REVISIT_DRAIN if the player has previously visited the room,
    otherwise returns FIRST_VISIT_DRAIN. This function is pure and does
    not mutate *state*.
    """
    if state.has_visited(room_id):
        return REVISIT_DRAIN
    return FIRST_VISIT_DRAIN


def drain_for_action(kind: str = "careful") -> int:
    """Calculate oil cost for a slow/careful action.

    Careful actions (such as reading a heavy tome or searching behind furniture)
    drain substantially more oil than simple navigation steps.
    """
    if kind.lower() in ("careful", "read", "search"):
        return CAREFUL_ACTION_DRAIN
    return STEP_ACTION_DRAIN


def is_low_oil(state: RunState) -> bool:
    """Check if the lantern oil has reached or fallen below the warning threshold."""
    return 0 < state.lantern <= LOW_OIL_WARNING_THRESHOLD


def is_zero_oil(state: RunState) -> bool:
    """Check if the lantern is completely empty."""
    return state.lantern == 0


def get_zero_oil_consequence() -> dict[str, Any]:
    """Return the structured death consequence for total light loss."""
    return {
        "tier": "death",
        "cause": ZERO_OIL_DEATH_CAUSE,
        "lesson": ZERO_OIL_DEATH_LESSON,
        "telegraphs": list(ZERO_OIL_TELEGRAPHS),
    }
