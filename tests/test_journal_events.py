"""Tests for automatic journal event recording on room entry and death (Task E02)."""
from pathlib import Path
import pytest

from game.content_schema import load_content
from game.journal import CATEGORY_DEATH, CATEGORY_ROOM, CATEGORY_SHADOW
from game.state import RunState
from screens.game import GameScreen
from tests.test_game_screen import GameScreenTestApp


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


@pytest.mark.anyio
async def test_room_entry_logs_journal_record(house_content):
    """Entering a room automatically writes a ROOM_DISCOVERY entry."""
    state = RunState.fresh_run()
    app = GameScreenTestApp(content=house_content, state=state)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # On initial mount into Hall, hall discovery should be logged
        entries = state.journal.get_entries(CATEGORY_ROOM)
        assert len(entries) >= 1
        assert any(e.text == "hall" for e in entries)

        # Move to old_library (choice 2)
        await pilot.press("down")
        await pilot.press("down")
        assert screen.current_choices[screen.selected_choice]["id"] == "hall_right"
        await pilot.press("enter")

        # Now old_library is logged too
        lib_entries = [e for e in state.journal.get_entries(CATEGORY_ROOM) if e.text == "old_library"]
        assert len(lib_entries) == 1
        assert "Old Library" in lib_entries[0].detail


@pytest.mark.anyio
async def test_revisiting_room_does_not_duplicate_entry(house_content):
    """Backtracking into a previously seen room does not duplicate its journal record."""
    state = RunState.fresh_run()
    app = GameScreenTestApp(content=house_content, state=state)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Hall -> Library
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("enter")
        assert screen.state.current_room == "old_library"

        # Library -> Hall (return)
        # Choice 1 is library_return
        await pilot.press("down")
        assert screen.current_choices[screen.selected_choice]["id"] == "library_return"
        await pilot.press("enter")
        assert screen.state.current_room == "hall"

        # Hall entries must still be exactly 1
        hall_entries = [e for e in state.journal.get_entries(CATEGORY_ROOM) if e.text == "hall"]
        assert len(hall_entries) == 1


@pytest.mark.anyio
async def test_death_trigger_records_lesson(house_content):
    """Experiencing a fatal action records the death cause and lesson in the journal."""
    state = RunState.fresh_run()
    app = GameScreenTestApp(content=house_content, state=state)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Step into left archway (choice 3: hall_left)
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("down")
        assert screen.current_choices[screen.selected_choice]["id"] == "hall_left"
        await pilot.press("enter")

        # Death entry was recorded
        death_entries = state.journal.get_entries(CATEGORY_DEATH)
        assert len(death_entries) >= 1
        assert "butchered in the dark" in death_entries[0].text.lower()
