"""Multi-turn action tracking for Escape from Shadows (Task F01).

SUGGEST.md §6 & §11:
Supports activities taking multiple consecutive turns (such as reading the Book
in the Old Library across three consecutive turns, with door opened while reading).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class MultiTurnAction:
    """An ongoing activity that progresses across consecutive turns."""

    action_id: str
    total_steps: int
    current_step: int = 0
    step_costs: list[dict[str, Any]] = field(default_factory=list)
    completion_effects: list[dict[str, Any]] = field(default_factory=list)
    cancel_effects: list[dict[str, Any]] = field(default_factory=list)

    def advance(self) -> bool:
        """Increment current_step. Returns True if target steps reached/completed."""
        self.current_step += 1
        return self.is_complete()

    def is_complete(self) -> bool:
        """Check if action has achieved all required steps."""
        return self.current_step >= self.total_steps

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "total_steps": self.total_steps,
            "current_step": self.current_step,
            "step_costs": [dict(c) for c in self.step_costs],
            "completion_effects": [dict(e) for e in self.completion_effects],
            "cancel_effects": [dict(c) for c in self.cancel_effects],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MultiTurnAction":
        return cls(
            action_id=str(data.get("action_id", "")),
            total_steps=int(data.get("total_steps", 1)),
            current_step=int(data.get("current_step", 0)),
            step_costs=list(data.get("step_costs", [])),
            completion_effects=list(data.get("completion_effects", [])),
            cancel_effects=list(data.get("cancel_effects", [])),
        )
