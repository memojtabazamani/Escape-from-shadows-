"""Canonical endings schema and static registry (Phase 3 Slice A, Task A02).

SUGGEST.md §2.3 & §9.4:
Defines the canonical 7-ending catalog and structured metadata:
1. The Long Walk
2. Meat and Silence
3. The Quiet Exit
4. What the Book Knew
5. The New Shadow
6. Homecoming
7. Stay
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class EndingMetadata:
    """Structured metadata for a canonical game ending."""

    id: str
    number: int
    title: str
    tone: str
    hint: str
    summary: str


CANONICAL_ENDINGS: dict[str, EndingMetadata] = {
    "the_long_walk": EndingMetadata(
        id="the_long_walk",
        number=1,
        title="The Long Walk",
        tone="Failure, but the shadow respects you",
        hint="A single misstep where the candles end.",
        summary="You perished at the very threshold of the house.",
    ),
    "meat_and_silence": EndingMetadata(
        id="meat_and_silence",
        number=2,
        title="Meat and Silence",
        tone="Ugly survival",
        hint="The beast hungers for red iron and warm marrow.",
        summary="You fed the Hell Dog and slipped past in the grease and quiet.",
    ),
    "the_quiet_exit": EndingMetadata(
        id="the_quiet_exit",
        number=3,
        title="The Quiet Exit",
        tone="Standard win",
        hint="The latch yields to patience and the key.",
        summary="You unlatched the heavy front door and stepped out into the night.",
    ),
    "what_the_book_knew": EndingMetadata(
        id="what_the_book_knew",
        number=4,
        title="What the Book Knew",
        tone="Best \"true\" ending",
        hint="Three turns of patient reading illuminate the dark.",
        summary="You read the forbidden tome to completion and escaped with its truths.",
    ),
    "the_new_shadow": EndingMetadata(
        id="the_new_shadow",
        number=5,
        title="The New Shadow",
        tone="You got out. Something came with you.",
        hint="Reach the threshold after the lantern has guttered into ashes.",
        summary="You escaped in pitch darkness. You did not leave alone.",
    ),
    "homecoming": EndingMetadata(
        id="homecoming",
        number=6,
        title="Homecoming",
        tone="Secret ending, recontextualizes the house",
        hint="Recover the photograph, the drawing, and the receipt dated tomorrow.",
        summary="The three memory fragments revealed what the manor truly was: your home.",
    ),
    "stay": EndingMetadata(
        id="stay",
        number=7,
        title="Stay",
        tone="The player chooses the house",
        hint="When the front door stands wide, choose not to cross the threshold.",
        summary="You stood before the open night, turned around, and closed the door.",
    ),
}

CANONICAL_ENDINGS_LIST: list[EndingMetadata] = list(CANONICAL_ENDINGS.values())
TOTAL_CANONICAL_ENDINGS: int = len(CANONICAL_ENDINGS)


def get_ending_metadata(ending_id: str) -> Optional[EndingMetadata]:
    """Retrieve metadata for an ending by canonical ID, or None if unknown."""
    return CANONICAL_ENDINGS.get(ending_id)


def get_all_canonical_endings() -> list[EndingMetadata]:
    """Retrieve all canonical ending records in numeric order."""
    return sorted(CANONICAL_ENDINGS.values(), key=lambda e: e.number)
