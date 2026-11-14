"""Ending resolution engine for Escape from Shadows (Phase 3 Slice B, Task B02).

SUGGEST.md §2.3:
Precedence hierarchy for resolving the 7 canonical endings:
1. homecoming (secret / 3 memory fragments)
2. the_new_shadow (lantern <= 0)
3. what_the_book_knew (read the book)
4. meat_and_silence (fed dog meat without whistle)
5. the_quiet_exit (standard exit)

Choice branches:
- stay (refused exit at threshold)
- the_long_walk (died early in hall)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.state import RunState


CANONICAL_MEMORY_FRAGMENTS: tuple[str, ...] = (
    "memory_photograph",
    "memory_child_drawing",
    "memory_tomorrow_receipt",
)

SLICE_C_MEMORY_FRAGMENTS: tuple[str, ...] = (
    "old_photograph",
    "child_drawing",
    "dated_receipt",
)

LEGACY_MEMORY_FRAGMENTS: tuple[str, ...] = (
    "photograph",
    "child_drawing",
    "tomorrow_receipt",
)


def has_all_memory_fragments(state: RunState) -> bool:
    """Return True if the state contains all three memory fragments (by item or flag)."""
    if state.has_flag("all_memory_fragments") or state.has_flag("has_all_memory_fragments"):
        return True

    # Support Slice C helper property / method if present
    if hasattr(state, "has_all_memory_fragments"):
        attr = getattr(state, "has_all_memory_fragments")
        if callable(attr):
            if attr():
                return True
        elif bool(attr):
            return True

    # Support Slice C fragments set/collection if present
    if hasattr(state, "memory_fragments"):
        frags = getattr(state, "memory_fragments")
        if isinstance(frags, (set, list, tuple)) and len(frags) >= 3:
            return True

    held = set(state.held_items)
    if set(CANONICAL_MEMORY_FRAGMENTS).issubset(held):
        return True
    if set(SLICE_C_MEMORY_FRAGMENTS).issubset(held):
        return True
    if set(LEGACY_MEMORY_FRAGMENTS).issubset(held):
        return True

    # Fuzzy match by item semantics
    has_photo = any("photo" in item.lower() for item in held)
    has_drawing = any("drawing" in item.lower() for item in held)
    has_receipt = any("receipt" in item.lower() for item in held)
    if has_photo and has_drawing and has_receipt:
        return True

    return False


def resolve_escape_ending(state: RunState) -> str:
    """Determine ending ID when escaping through the threshold according to §2.3 precedence."""
    # 1. Secret ending: 3/3 memory fragments collected
    if has_all_memory_fragments(state):
        return "homecoming"

    # 2. Zero lantern oil breach escape
    if state.lantern <= 0:
        return "the_new_shadow"

    # 3. Read The Book
    if state.has_flag("read_the_book") or state.has_flag("knows_dog_name"):
        return "what_the_book_knew"

    # 4. Hell Dog pacified with meat and not tamed with whistle
    fed_meat = state.has_flag("dog_pacified_meat") or state.has_flag("fed_dog_meat")
    whistled = state.has_flag("dog_whistled_away")
    if fed_meat and not whistled:
        return "meat_and_silence"

    # 5. Default standard escape
    return "the_quiet_exit"


def resolve_terminal_event(state: RunState, trigger: str) -> str:
    """Determine final ending or terminal ID based on trigger event and run context."""
    trigger_lower = trigger.strip().lower()

    if trigger_lower in ("door_escape", "escape", "front_door_escape", "exit", "hall_front_door", "hall_escape_dog_climax"):
        return resolve_escape_ending(state)

    if trigger_lower in ("refuse_exit", "stay", "ending_stay", "bolt_door", "hall_front_door_stay"):
        return "stay"

    if trigger_lower in ("the_long_walk", "long_walk", "ending_long_walk", "hall_accept_dark"):
        return "the_long_walk"

    if trigger_lower in ("hall_death", "early_death"):
        if state.has_flag("early_hall_death") or (
            state.turn_count <= 3
            and (len(state.visited) <= 1 or state.visited.issubset({"hall", "left_doorway_death", "clock_trap_death"}))
        ):
            return "the_long_walk"
        return "death"

    if trigger_lower == "death":
        # Check early hall death criteria: died in Hall or immediately from Hall within turn count <= 3
        in_hall = state.current_room in ("hall", "left_doorway_death", "clock_trap_death")
        if state.has_flag("early_hall_death") or (
            in_hall
            and state.turn_count <= 3
            and (len(state.visited) <= 1 or state.visited.issubset({"hall", "left_doorway_death", "clock_trap_death"}))
        ):
            return "the_long_walk"
        return "death"

    if trigger_lower in ("shadow_walk", "shadow_walk_ending", "hall_surrender_shadow"):
        return "shadow_walk"

    # Fallback to escape resolution if empty or default
    if trigger_lower in ("", "default"):
        return resolve_escape_ending(state)

    return trigger
