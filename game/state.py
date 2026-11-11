"""Run state for a single attempt at Escape from Shadows.

Phase 1 keeps the state deliberately small: only what the two-room vertical
slice needs.  Everything here is plain data; no Textual widgets, no I/O, and
no screen references.

Field table
-----------
lantern      : int              Current oil, 0-100.  Clamped on every write.
visited      : set[str]         Room identifiers the player has entered.
held_items   : set[str]         Item identifiers currently held (ASM-6: uncapped).
flags        : set[str]         Named boolean flags (e.g. knowledge gained).
turn_count   : int              Number of turns elapsed, never decreases.

Snapshot/restore
----------------
`snapshot()` returns a JSON-serializable dict.
`restore(data)` updates the run from a dict; missing keys use the same
defaults as a fresh run.  This contract is what Phase 2's save/load will build
on top of.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from game.difficulty import get_difficulty_config
from game.journal import Journal
from game.multiturn import MultiTurnAction


# Lantern scale used throughout Phase 1.
_LANTERN_MIN = 0
_LANTERN_MAX = 100

# Composure scale (SUGGEST.md §3.2).
_COMPOSURE_MIN = 0
_COMPOSURE_MAX = 100

# Inventory capacity (SUGGEST.md §3.3, ASM-5).
# A hard cap of 6 slots forces real tactical choices without excessive micro.
INVENTORY_CAP: int = 6


@dataclass
class RunState:
    """Everything about one attempt at the game."""

    lantern: int = _LANTERN_MAX
    composure: int = _COMPOSURE_MAX
    turn_count: int = 0
    current_room: str = ""
    visited: set[str] = field(default_factory=set)
    held_items: list[str] = field(default_factory=list)
    flags: set[str] = field(default_factory=set)
    difficulty: str = "MEDIUM"
    recorded_restart_room: str = ""
    journal: Journal = field(default_factory=Journal)
    consecutive_room_turns: int = 0
    delivered_hints: set[str] = field(default_factory=set)
    terminal_outcome: str = ""
    active_action: Optional[MultiTurnAction] = None

    def __post_init__(self) -> None:
        # Ensure construction also respects bounds and types.
        self.lantern = self._clamp_lantern(self.lantern)
        self.composure = self._clamp_composure(self.composure)
        self.visited = set(self.visited)
        self.flags = set(self.flags)
        self.difficulty = str(self.difficulty)
        self.recorded_restart_room = str(self.recorded_restart_room)
        self.consecutive_room_turns = max(0, int(self.consecutive_room_turns))
        self.delivered_hints = set(self.delivered_hints)
        if not isinstance(self.journal, Journal):
            self.journal = Journal()

        # Deduplicate held_items preserving order and clamp to INVENTORY_CAP
        clean_items: list[str] = []
        seen_items: set[str] = set()
        for raw_item in self.held_items:
            item_str = str(raw_item)
            if item_str not in seen_items and len(clean_items) < INVENTORY_CAP:
                seen_items.add(item_str)
                clean_items.append(item_str)
        self.held_items = clean_items

    @classmethod
    def fresh_run(cls, difficulty: str = "MEDIUM") -> "RunState":
        """Return a brand-new run with generosity parameters applied."""
        cfg = get_difficulty_config(difficulty)
        return cls(
            lantern=cfg.initial_lantern,
            composure=cfg.initial_composure,
            difficulty=difficulty,
        )

    @staticmethod
    def _clamp_lantern(value: int) -> int:
        """Clamp lantern to the valid range, hardening against bad callers."""
        return max(_LANTERN_MIN, min(_LANTERN_MAX, int(value)))

    @staticmethod
    def _clamp_composure(value: int) -> int:
        """Clamp composure to 0-100, hardening against bad callers."""
        return max(_COMPOSURE_MIN, min(_COMPOSURE_MAX, int(value)))

    # Composure -----------------------------------------------------------

    def spend_composure(self, amount: int) -> int:
        """Spend up to *amount* composure. Returns the amount actually spent."""
        if amount < 0:
            amount = 0
        old = self.composure
        self.composure = self._clamp_composure(self.composure - amount)
        return old - self.composure

    def restore_composure(self, amount: int) -> int:
        """Restore up to *amount* composure. Returns the amount actually restored."""
        if amount < 0:
            amount = 0
        old = self.composure
        self.composure = self._clamp_composure(self.composure + amount)
        return self.composure - old

    # Lantern --------------------------------------------------------------

    def spend_lantern(self, amount: int) -> int:
        """Spend up to *amount* oil.  Returns the amount actually spent.

        The lantern never drops below zero.  A negative *amount* is treated
        as zero spend.
        """
        if amount < 0:
            amount = 0
        old = self.lantern
        self.lantern = self._clamp_lantern(self.lantern - amount)
        return old - self.lantern

    def restore_lantern(self, amount: int = _LANTERN_MAX) -> int:
        """Restore up to *amount* oil, clamping at _LANTERN_MAX. Returns amount restored."""
        if amount < 0:
            amount = 0
        old = self.lantern
        self.lantern = self._clamp_lantern(self.lantern + amount)
        return self.lantern - old

    def has_light(self) -> bool:
        """True while any oil remains."""
        return self.lantern > _LANTERN_MIN

    # Turns ---------------------------------------------------------------

    def advance_turn(self) -> None:
        """Advance the turn counter by one."""
        self.turn_count += 1
        self.consecutive_room_turns += 1

    # Visited rooms -------------------------------------------------------

    def visit(self, room_id: str) -> bool:
        """Record that the player has entered *room_id*.

        Returns True if this was the first visit, False otherwise.
        Non-terminal safe rooms update recorded_restart_room.
        """
        if room_id != self.current_room:
            self.consecutive_room_turns = 0
            self.current_room = room_id

        first = room_id not in self.visited
        self.visited.add(room_id)
        if not room_id.startswith("the_threshold_"):
            self.recorded_restart_room = room_id
        return first

    def has_visited(self, room_id: str) -> bool:
        """True if the player has entered *room_id*."""
        return room_id in self.visited

    # Held items (6-slot cap per §3.3) -----------------------------------

    def can_add_item(self) -> bool:
        """True if the inventory has free capacity (< 6 items)."""
        return len(self.held_items) < INVENTORY_CAP

    def free_slots(self) -> int:
        """Return the number of remaining open inventory slots."""
        return max(0, INVENTORY_CAP - len(self.held_items))

    def add_item(self, item_id: str) -> bool:
        """Add an item to inventory.

        Returns True if the item is held (including when already present).
        Returns False if inventory is full (6/6 slots) and refuses the item.
        """
        item_str = str(item_id)
        if item_str in self.held_items:
            return True
        if not self.can_add_item():
            return False
        self.held_items.append(item_str)
        return True

    def remove_item(self, item_id: str) -> bool:
        """Remove an item if held. Returns True if removed, False otherwise."""
        item_str = str(item_id)
        if item_str in self.held_items:
            self.held_items.remove(item_str)
            return True
        return False

    def drop_item(self, item_id: str) -> bool:
        """Explicit drop operation (alias for remove_item)."""
        return self.remove_item(item_id)

    def has_item(self, item_id: str) -> bool:
        """True if the item is currently held."""
        return str(item_id) in self.held_items

    # Flags ---------------------------------------------------------------

    def set_flag(self, flag: str) -> None:
        """Set a named flag."""
        self.flags.add(flag)

    def clear_flag(self, flag: str) -> None:
        """Clear a named flag."""
        self.flags.discard(flag)

    def has_flag(self, flag: str) -> bool:
        """Read a flag; unset flags safely return False."""
        return flag in self.flags

    # Multi-turn actions --------------------------------------------------

    def start_multiturn(
        self,
        action_id: str,
        total_steps: int,
        step_costs: list[dict[str, Any]] | None = None,
        completion_effects: list[dict[str, Any]] | None = None,
        cancel_effects: list[dict[str, Any]] | None = None,
    ) -> MultiTurnAction:
        """Start a new multi-turn action, replacing any existing one."""
        self.active_action = MultiTurnAction(
            action_id=action_id,
            total_steps=total_steps,
            current_step=0,
            step_costs=list(step_costs or []),
            completion_effects=list(completion_effects or []),
            cancel_effects=list(cancel_effects or []),
        )
        return self.active_action

    def advance_multiturn(self) -> tuple[bool, list[dict[str, Any]]]:
        """Advance ongoing action by one step.

        Returns (is_complete, effects_to_apply).
        When complete, active_action is cleared and completion_effects are returned.
        Otherwise, step_costs are returned.
        """
        if not self.active_action:
            return False, []
        completed = self.active_action.advance()
        if completed:
            effects = list(self.active_action.completion_effects)
            self.active_action = None
            return True, effects
        return False, list(self.active_action.step_costs)

    def cancel_multiturn(self) -> list[dict[str, Any]]:
        """Cancel ongoing action, clearing it and returning cancel_effects."""
        if not self.active_action:
            return []
        effects = list(self.active_action.cancel_effects)
        self.active_action = None
        return effects

    def has_active_multiturn(self, action_id: str | None = None) -> bool:
        """True if an action (optionally matching action_id) is in progress."""
        if self.active_action is None:
            return False
        if action_id is not None and self.active_action.action_id != action_id:
            return False
        return True

    # Snapshot / restore --------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        """Return a JSON-serializable copy of the run state."""
        return {
            "lantern": self.lantern,
            "composure": self.composure,
            "turn_count": self.turn_count,
            "current_room": self.current_room,
            "visited": sorted(self.visited),
            "held_items": list(self.held_items),
            "flags": sorted(self.flags),
            "difficulty": self.difficulty,
            "recorded_restart_room": self.recorded_restart_room,
            "journal": self.journal.to_dict(),
            "consecutive_room_turns": self.consecutive_room_turns,
            "delivered_hints": sorted(self.delivered_hints),
            "terminal_outcome": self.terminal_outcome,
            "active_action": self.active_action.to_dict() if self.active_action else None,
        }

    def restore(self, data: dict[str, Any]) -> None:
        """Update this run from a snapshot dict.

        Missing keys fall back to fresh-run defaults. Extra keys are ignored.
        Tolerates legacy snapshots with set/list items and clamps to INVENTORY_CAP.
        """
        defaults = self.__class__()
        self.lantern = self._clamp_lantern(data.get("lantern", defaults.lantern))
        self.composure = self._clamp_composure(data.get("composure", defaults.composure))
        self.turn_count = max(0, data.get("turn_count", defaults.turn_count))
        self.current_room = str(data.get("current_room", defaults.current_room))
        self.visited = set(data.get("visited", defaults.visited))
        self.terminal_outcome = str(data.get("terminal_outcome", defaults.terminal_outcome))

        raw_items = data.get("held_items", defaults.held_items)
        clean_items: list[str] = []
        seen_items: set[str] = set()
        if isinstance(raw_items, (list, set, tuple)):
            for raw_item in raw_items:
                item_str = str(raw_item)
                if item_str not in seen_items and len(clean_items) < INVENTORY_CAP:
                    seen_items.add(item_str)
                    clean_items.append(item_str)
        self.held_items = clean_items

        self.flags = set(data.get("flags", defaults.flags))
        self.difficulty = str(data.get("difficulty", defaults.difficulty))
        self.recorded_restart_room = str(data.get("recorded_restart_room", defaults.recorded_restart_room))
        self.consecutive_room_turns = max(0, int(data.get("consecutive_room_turns", defaults.consecutive_room_turns)))
        self.delivered_hints = set(data.get("delivered_hints", defaults.delivered_hints))
        if "journal" in data and isinstance(data["journal"], list):
            self.journal = Journal.from_dict(data["journal"])
        if "active_action" in data and isinstance(data["active_action"], dict):
            self.active_action = MultiTurnAction.from_dict(data["active_action"])
        else:
            self.active_action = None
