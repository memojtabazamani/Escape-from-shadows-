"""Tests for Journal model and RunState integration (Task E01)."""
import pytest

from game.journal import (
    CATEGORY_DEATH,
    CATEGORY_ROOM,
    CATEGORY_SHADOW,
    Journal,
    JournalEntry,
)
from game.state import RunState


def test_journal_initialization_empty():
    journal = Journal()
    assert len(journal.entries) == 0
    assert len(journal.get_entries()) == 0


def test_journal_add_distinct_categories():
    journal = Journal()

    added_room = journal.add_room("hall", "The Hall", "High stone arches.")
    assert added_room is True

    added_death = journal.add_death("Butchered in darkness", "Never step blindly.")
    assert added_death is True

    added_shadow = journal.add_shadow_line("The flame is burning down...", "EASY hint")
    assert added_shadow is True

    assert len(journal.entries) == 3
    assert len(journal.get_entries(CATEGORY_ROOM)) == 1
    assert len(journal.get_entries(CATEGORY_DEATH)) == 1
    assert len(journal.get_entries(CATEGORY_SHADOW)) == 1


def test_journal_deduplication():
    journal = Journal()

    res1 = journal.add_room("hall", "The Hall", "High stone arches.")
    assert res1 is True

    # Re-adding same room id returns False and does not duplicate entry
    res2 = journal.add_room("hall", "The Hall", "Second visit notes.")
    assert res2 is False
    assert len(journal.get_entries(CATEGORY_ROOM)) == 1


def test_journal_state_snapshot_roundtrip():
    state = RunState.fresh_run()
    state.journal.add_room("hall", "The Hall", "First room seen.")
    state.journal.add_death("Fell in dark", "Carry light.")
    state.journal.add_shadow_line("You hesitated too long.", "Library alcove")

    data = state.snapshot()
    assert len(data["journal"]) == 3

    restored = RunState.fresh_run()
    restored.restore(data)
    assert len(restored.journal.entries) == 3

    rooms = restored.journal.get_entries(CATEGORY_ROOM)
    assert len(rooms) == 1
    assert rooms[0].text == "hall"
    assert "The Hall" in rooms[0].detail

    deaths = restored.journal.get_entries(CATEGORY_DEATH)
    assert len(deaths) == 1
    assert deaths[0].text == "Fell in dark"
    assert deaths[0].detail == "Carry light."
