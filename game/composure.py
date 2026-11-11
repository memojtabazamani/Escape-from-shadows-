"""Composure stat rules and threshold helpers.

SUGGEST.md §3.2 & AC-11:
"Lantern is time. Composure is nerve.
Drops when you witness something awful, when the Shadow speaks to you, or when you run.
At zero composure you don't die — you walk into the Shadow voluntarily.
Different, scarier, recoverable with a story consequence."

CRITICAL INVARIANT:
Zero composure DOES NOT kill the player. It is not health and must never be treated
as a fatal death condition.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.state import RunState

COMPOSURE_MIN: int = 0
COMPOSURE_MAX: int = 100

# ASM-6 & §3.2: "only the last 20% of the bar distorts text"
DISTORTION_THRESHOLD: int = 20


def spend_composure(state: RunState, amount: int) -> int:
    """Spend up to *amount* composure. Returns the amount actually spent.

    Clamped to COMPOSURE_MIN. Negative amounts are treated as 0 spend.
    Zero composure does NOT end the run.
    """
    if amount < 0:
        amount = 0
    return state.spend_composure(amount)


def restore_composure(state: RunState, amount: int) -> int:
    """Restore up to *amount* composure. Returns the amount actually restored.

    Clamped to COMPOSURE_MAX. Negative amounts are treated as 0 restore.
    """
    if amount < 0:
        amount = 0
    return state.restore_composure(amount)


def is_distorted(state: RunState) -> bool:
    """Return True if composure has dropped into the last 20% distortion band (<= 20)."""
    return state.composure <= DISTORTION_THRESHOLD


def is_zero_composure(state: RunState) -> bool:
    """Return True if composure has reached 0 (triggers the voluntary walk)."""
    return state.composure <= COMPOSURE_MIN
