"""Comprehensive test suite for the Journal slice (Task E04).

Covers:
- Category filtering and deduplication.
- Snapshot serialization and restoration integrity.
- Room discovery and death lesson automatic logging.
- Shadow whisper logging.
- JournalScreen display and keybinding integration.
"""
from pathlib import Path
import pytest

from game.content_schema import load_content
from game.journal import (
    CATEGORY_DEATH,
    CATEGORY_ROOM,
    CATEGORY_SHADOW,
    Journal,
    JournalEntry,
)
from game.state import RunState
from screens.game import GameScreen
from screens.journal import JournalScreen
from tests.test_game_screen import GameScreenTestApp


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


def test_journal_category_filtering():
    journal = Journal()
    journal.add_room("hall", "The Hall", "High arches")
    journal.add_death("Butchered", "Never step blindly")
    journal.add_shadow_line("Whisper text", "Context")

    assert len(journal.get_entries()) == 3
    assert len(journal.get_entries(CATEGORY_ROOM)) == 1
    assert len(journal.get_entries(CATEGORY_DEATH)) == 1
    assert len(journal.get_entries(CATEGORY_SHADOW)) == 1
    assert len(journal.get_entries("NON_EXISTENT")) == 0


def test_journal_deduplication_and_idempotency():
    journal = Journal()
    assert journal.add_room("hall", "The Hall", "Note 1") is True
    assert journal.add_room("hall", "The Hall", "Note 2") is False
    assert len(journal.get_entries(CATEGORY_ROOM)) == 1

    assert journal.add_death("Fell in dark", "Lesson 1") is True
    assert journal.add_death("Fell in dark", "Lesson 2") is False
    assert len(journal.get_entries(CATEGORY_DEATH)) == 1


def test_journal_snapshot_restoration_fidelity():
    original = RunState.fresh_run()
    original.journal.add_room("hall", "The Hall", "Entrance note")
    original.journal.add_death("Dark death", "Watch oil")
    original.journal.add_shadow_line("Turn back", "Shadow warning")

    data = original.snapshot()
    restored = RunState.fresh_run()
    restored.restore(data)

    assert len(restored.journal.entries) == 3
    room_entry = restored.journal.get_entries(CATEGORY_ROOM)[0]
    assert room_entry.text == "hall"
    assert "Entrance note" in room_entry.detail

    death_entry = restored.journal.get_entries(CATEGORY_DEATH)[0]
    assert death_entry.text == "Dark death"
    assert death_entry.detail == "Watch oil"

    shadow_entry = restored.journal.get_entries(CATEGORY_SHADOW)[0]
    assert shadow_entry.text == "Turn back"


@pytest.mark.anyio
async def test_end_to_end_journal_gameplay_flow(house_content):
    """Full integration: enter room, check journal, take action, open journal overlay, dismiss."""
    state = RunState.fresh_run()
    app = GameScreenTestApp(content=house_content, state=state)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # 1. Hall was recorded
        assert any(e.text == "hall" for e in state.journal.get_entries(CATEGORY_ROOM))

        # 2. Press 'j' to open journal overlay
        await pilot.press("j")
        journal_screen = pilot.app.screen
        assert isinstance(journal_screen, JournalScreen)
        content_text = journal_screen.render_content()
        assert "The Hall" in content_text

        # 3. Press 'escape' to return to game
        await pilot.press("escape")
        assert isinstance(pilot.app.screen, GameScreen)

        # 4. Turn count did not advance by opening/closing journal
        assert screen.state.turn_count == 0
        assert screen.state.lantern == 100
