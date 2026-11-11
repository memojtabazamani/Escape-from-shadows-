"""Shadow hint system for EASY difficulty (Task B04).

Design rules (§5.1, §4.2, §7.4, ASM-11):
- Hints fire on EASY only; MEDIUM and HARD stay completely silent.
- The Shadow is not an entity; it speaks once when the player is stuck and is gone.
- Hints point, never state: they provide actionable cues without walkthrough spoilers.
- Hints only reference content the player has already encountered or can see.
- No hint is delivered twice in a single run.
- Delivered lines are recorded in the journal under SHADOW_WHISPER.
- Red styling [#e63946] is strictly reserved for the Shadow (§7.4).
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING
from game.difficulty import get_difficulty_config

if TYPE_CHECKING:
    from game.state import RunState


# Hint table keyed by room id and condition
# Format: (hint_id, condition_callable, hint_prose)
_HINTS_DATA: list[dict[str, str]] = [
    {
        "id": "hall_unvisited_library",
        "room": "hall",
        "prose": "The eastern archway smells of tallow and cold ink. You pace like a caged animal instead of stepping through.",
        "condition": "needs_library",
    },
    {
        "id": "hall_read_tome",
        "room": "hall",
        "prose": "You have walked the library and touched the cold air, yet you left without reading what the sentinel shelves concealed.",
        "condition": "needs_tome",
    },
    {
        "id": "old_library_heavy_tome",
        "room": "old_library",
        "prose": "Your light wavers across the pedestal. The black volume rests right before your eyes, waiting for your hands.",
        "condition": "in_library_unread",
    },
]


def check_hint_condition(hint_id: str, state: RunState) -> bool:
    """Evaluate whether the condition for a specific hint is satisfied."""
    has_read_tome = state.has_flag("knows_exit")
    visited_library = state.has_visited("old_library")

    if hint_id == "hall_unvisited_library":
        return not visited_library and not has_read_tome
    elif hint_id == "hall_read_tome":
        return visited_library and not has_read_tome
    elif hint_id == "old_library_heavy_tome":
        return not has_read_tome
    return False


def get_stuck_hint(state: RunState) -> Optional[str]:
    """Return a usable Shadow hint if the player is stuck on EASY difficulty.

    Returns None if:
    - Difficulty does not have hints_enabled (MEDIUM or HARD).
    - Player has not spent enough consecutive turns in the room.
    - No un-delivered hint matches the current game condition.
    """
    cfg = get_difficulty_config(state.difficulty)
    if not cfg.hints_enabled:
        return None

    if state.consecutive_room_turns < cfg.stuck_turn_threshold:
        return None

    current_room = state.current_room
    for hint in _HINTS_DATA:
        hint_id = hint["id"]
        if hint["room"] == current_room and hint_id not in state.delivered_hints:
            if check_hint_condition(hint_id, state):
                # Mark delivered and record to journal
                state.delivered_hints.add(hint_id)
                hint_text = hint["prose"]
                state.journal.add_shadow_line(hint_text, context=current_room)
                return hint_text

    return None
