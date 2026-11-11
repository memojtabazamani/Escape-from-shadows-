"""In-memory Journal model for Escape from Shadows.

Follows SUGGEST.md §3.4 and §5.1:
Records player discoveries across a run — rooms visited, death causes/lessons
witnessed, and lines spoken by the Shadow.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

CATEGORY_ROOM = "ROOM_DISCOVERY"
CATEGORY_DEATH = "DEATH_LESSON"
CATEGORY_SHADOW = "SHADOW_WHISPER"


@dataclass
class JournalEntry:
    """A single record in the journal."""

    category: str
    text: str
    detail: str = ""

    def to_dict(self) -> dict[str, str]:
        return {
            "category": self.category,
            "text": self.text,
            "detail": self.detail,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "JournalEntry":
        return cls(
            category=str(data.get("category", "")),
            text=str(data.get("text", "")),
            detail=str(data.get("detail", "")),
        )


@dataclass
class Journal:
    """Container for journal entries with deduplication."""

    entries: list[JournalEntry] = field(default_factory=list)

    def add_entry(self, category: str, text: str, detail: str = "") -> bool:
        """Add entry if not already present. Returns True if newly added."""
        for entry in self.entries:
            if entry.category == category and entry.text == text:
                if detail and not entry.detail:
                    entry.detail = detail
                return False
        self.entries.append(JournalEntry(category=category, text=text, detail=detail))
        return True

    def add_room(self, room_id: str, title: str = "", notes: str = "") -> bool:
        return self.add_entry(CATEGORY_ROOM, text=room_id, detail=f"{title}: {notes}" if title else notes)

    def add_death(self, cause: str, lesson: str = "") -> bool:
        return self.add_entry(CATEGORY_DEATH, text=cause, detail=lesson)

    def add_shadow_line(self, line: str, context: str = "") -> bool:
        return self.add_entry(CATEGORY_SHADOW, text=line, detail=context)

    def get_entries(self, category: Optional[str] = None) -> list[JournalEntry]:
        if category is None:
            return list(self.entries)
        return [e for e in self.entries if e.category == category]

    def to_dict(self) -> list[dict[str, str]]:
        return [e.to_dict() for e in self.entries]

    @classmethod
    def from_dict(cls, data: list[dict[str, Any]]) -> "Journal":
        journal = cls()
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    journal.entries.append(JournalEntry.from_dict(item))
        return journal
