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
from typing import Any


# Lantern scale used throughout Phase 1.
_LANTERN_MIN = 0
_LANTERN_MAX = 100


@dataclass
class RunState:
    """Everything about one attempt at the game."""

    lantern: int = _LANTERN_MAX
    turn_count: int = 0
    visited: set[str] = field(default_factory=set)
    held_items: set[str] = field(default_factory=set)
    flags: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        # Ensure construction also respects bounds and types.
        self.lantern = self._clamp_lantern(self.lantern)
        self.visited = set(self.visited)
        self.held_items = set(self.held_items)
        self.flags = set(self.flags)

    @classmethod
    def fresh_run(cls) -> "RunState":
        """Return a brand-new run with default values."""
        return cls()

    @staticmethod
    def _clamp_lantern(value: int) -> int:
        """Clamp lantern to the valid range, hardening against bad callers."""
        return max(_LANTERN_MIN, min(_LANTERN_MAX, int(value)))

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

    def has_light(self) -> bool:
        """True while any oil remains."""
        return self.lantern > _LANTERN_MIN

    # Turns ---------------------------------------------------------------

    def advance_turn(self) -> None:
        """Advance the turn counter by one."""
        self.turn_count += 1

    # Visited rooms -------------------------------------------------------

    def visit(self, room_id: str) -> bool:
        """Record that the player has entered *room_id*.

        Returns True if this was the first visit, False otherwise.
        """
        first = room_id not in self.visited
        self.visited.add(room_id)
        return first

    def has_visited(self, room_id: str) -> bool:
        """True if the player has entered *room_id*."""
        return room_id in self.visited

    # Held items ----------------------------------------------------------

    def add_item(self, item_id: str) -> None:
        """Add an item to the held set.  Duplicates are a no-op."""
        self.held_items.add(item_id)

    def remove_item(self, item_id: str) -> None:
        """Remove an item if it is held."""
        self.held_items.discard(item_id)

    def has_item(self, item_id: str) -> bool:
        """True if the item is currently held."""
        return item_id in self.held_items

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

    # Snapshot / restore --------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        """Return a JSON-serializable copy of the run state."""
        return {
            "lantern": self.lantern,
            "turn_count": self.turn_count,
            "visited": sorted(self.visited),
            "held_items": sorted(self.held_items),
            "flags": sorted(self.flags),
        }

    def restore(self, data: dict[str, Any]) -> None:
        """Update this run from a snapshot dict.

        Missing keys fall back to fresh-run defaults.  Extra keys are ignored.
        """
        defaults = self.__class__()
        self.lantern = self._clamp_lantern(data.get("lantern", defaults.lantern))
        self.turn_count = max(0, data.get("turn_count", defaults.turn_count))
        self.visited = set(data.get("visited", defaults.visited))
        self.held_items = set(data.get("held_items", defaults.held_items))
        self.flags = set(data.get("flags", defaults.flags))
