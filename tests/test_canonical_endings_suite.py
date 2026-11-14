"""Comprehensive test suite for all 7 canonical endings (Task B06).

Covers AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, AC-12, §2.3, §7.3, §9.4.
Verifies that:
1. Every canonical ending resolves deterministically from real/simulated game states.
2. Mounting EndingScreen displays the correct title, prose, and ASCII vignette.
3. Every ending persists into the permanent PlayerProfile meta-progression.
"""

from pathlib import Path
import pytest
from textual.app import App
from textual.widgets import Static

from game.content_schema import load_content
from game.ending_resolver import (
    has_all_memory_fragments,
    resolve_escape_ending,
    resolve_terminal_event,
)
from game.endings import CANONICAL_ENDINGS, CANONICAL_ENDINGS_LIST
from game.endings_art import get_ending_ascii
from game.profile import load_profile
from game.state import RunState
from screens.death import DeathScreen
from screens.ending import EndingScreen
from screens.game import GameScreen


class EndingMountApp(App):
    def __init__(self, ending_id: str, content: dict):
        super().__init__()
        self.ending_id = ending_id
        self.content = content

    async def on_mount(self) -> None:
        await self.push_screen(
            EndingScreen(
                content=self.content,
                ending_id=self.ending_id,
            )
        )


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


@pytest.fixture(autouse=True)
def clean_profile(tmp_path, monkeypatch):
    profile_path = tmp_path / "test_profile.json"
    monkeypatch.setattr("game.profile.DEFAULT_PROFILE_PATH", profile_path)
    if profile_path.exists():
        profile_path.unlink()
    yield
    if profile_path.exists():
        profile_path.unlink()


# 1. State resolution tests ----------------------------------------------------

def test_resolution_the_long_walk():
    """Ending 1: The Long Walk (Hall demise within turn <= 3)."""
    state = RunState.fresh_run()
    state.current_room = "hall"
    state.turn_count = 1
    state.visited = {"hall"}
    assert resolve_terminal_event(state, "hall_death") == "the_long_walk"
    assert resolve_terminal_event(state, "death") == "the_long_walk"


def test_resolution_meat_and_silence():
    """Ending 2: Meat and Silence (fed meat to dog without whistling)."""
    state = RunState.fresh_run()
    state.lantern = 50
    state.set_flag("dog_pacified_meat")
    assert resolve_escape_ending(state) == "meat_and_silence"
    assert resolve_terminal_event(state, "door_escape") == "meat_and_silence"


def test_resolution_the_quiet_exit():
    """Ending 3: The Quiet Exit (standard front door exit with key)."""
    state = RunState.fresh_run()
    state.lantern = 60
    state.add_item("front_door_key")
    assert resolve_escape_ending(state) == "the_quiet_exit"
    assert resolve_terminal_event(state, "door_escape") == "the_quiet_exit"


def test_resolution_what_the_book_knew():
    """Ending 4: What the Book Knew (read The Book and escaped)."""
    state = RunState.fresh_run()
    state.lantern = 30
    state.set_flag("read_the_book")
    assert resolve_escape_ending(state) == "what_the_book_knew"
    assert resolve_terminal_event(state, "door_escape") == "what_the_book_knew"


def test_resolution_the_new_shadow():
    """Ending 5: The New Shadow (lantern oil == 0 upon escape)."""
    state = RunState.fresh_run()
    state.lantern = 0
    # Overrides book reading and dog meat
    state.set_flag("read_the_book")
    state.set_flag("dog_pacified_meat")
    assert resolve_escape_ending(state) == "the_new_shadow"
    assert resolve_terminal_event(state, "door_escape") == "the_new_shadow"


def test_resolution_homecoming():
    """Ending 6: Homecoming (secret ending holding all 3 memory fragments)."""
    state = RunState.fresh_run()
    state.lantern = 0
    state.set_flag("read_the_book")
    state.add_item("memory_photograph")
    state.add_item("memory_child_drawing")
    state.add_item("memory_tomorrow_receipt")

    assert has_all_memory_fragments(state) is True
    assert resolve_escape_ending(state) == "homecoming"
    assert resolve_terminal_event(state, "door_escape") == "homecoming"


def test_resolution_stay():
    """Ending 7: Stay (refusal at the threshold)."""
    state = RunState.fresh_run()
    assert resolve_terminal_event(state, "refuse_exit") == "stay"
    assert resolve_terminal_event(state, "ending_stay") == "stay"


# 2. UI presentation & profile persistence for all 7 endings -------------------

@pytest.mark.anyio
@pytest.mark.parametrize("meta", CANONICAL_ENDINGS_LIST)
async def test_all_seven_endings_render_and_persist(meta, content):
    """Mounting EndingScreen for each canonical ending renders correctly and records to profile."""
    ending_id = meta.id

    # Lookup content record
    endings_content = {e["id"]: e for e in content.get("endings", [])}
    assert ending_id in endings_content, f"Content missing entry for {ending_id}"
    record = endings_content[ending_id]

    app = EndingMountApp(ending_id=ending_id, content=content)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingScreen)
        assert screen.ending_id == ending_id

        # Verify title and prose match content record
        title_widget = screen.query_one("#ending-title", Static)
        prose_widget = screen.query_one("#ending-prose", Static)
        assert str(title_widget.content) == record["title"]
        assert str(prose_widget.content) == record["prose"]

        # Verify ASCII vignette is rendered cleanly
        ascii_widget = screen.query_one("#ending-ascii", Static)
        expected_ascii = get_ending_ascii(ending_id)
        assert str(ascii_widget.content) == expected_ascii

        # Verify profile has registered the unlocked ending
        profile = load_profile()
        assert ending_id in profile.unlocked_endings


# 3. Live GameScreen UI integration tests --------------------------------------

class GameSuiteApp(App):
    def __init__(self, content: dict, state: RunState):
        super().__init__()
        self._content = content
        self._state = state

    async def on_mount(self) -> None:
        await self.push_screen(GameScreen(content=self._content, state=self._state))


@pytest.mark.anyio
async def test_game_screen_routes_zero_oil_escape_to_the_new_shadow(content):
    """AC-9: Escaping through the front door with zero lantern oil produces The New Shadow ending, not DeathScreen."""
    state = RunState.fresh_run()
    state.set_flag("knows_exit")
    state.lantern = 0  # Zero oil

    app = GameSuiteApp(content=content, state=state)
    async with app.run_test() as pilot:
        # Choice 0 in hall when knows_exit is set is hall_front_door
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)
        assert game_screen.current_choices[game_screen.selected_choice]["id"] == "hall_front_door"

        # Select escape
        await pilot.press("enter")

        # Crucial assertion: Must NOT be DeathScreen! Must be EndingScreen!
        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        assert not isinstance(top_screen, DeathScreen)
        assert top_screen.ending_id == "the_new_shadow"

        # Unlocked in profile
        profile = load_profile()
        assert "the_new_shadow" in profile.unlocked_endings
        assert profile.total_escapes >= 1


@pytest.mark.anyio
async def test_game_screen_routes_homecoming_even_with_zero_oil(content):
    """AC-10: 3 memory fragments collected takes top precedence over zero oil escape."""
    state = RunState.fresh_run()
    state.set_flag("knows_exit")
    state.lantern = 0
    state.add_item("memory_photograph")
    state.add_item("memory_child_drawing")
    state.add_item("memory_tomorrow_receipt")

    app = GameSuiteApp(content=content, state=state)
    async with app.run_test() as pilot:
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Select escape
        await pilot.press("enter")

        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        assert top_screen.ending_id == "homecoming"

        profile = load_profile()
        assert "homecoming" in profile.unlocked_endings
        assert profile.total_escapes >= 1


@pytest.mark.anyio
async def test_shadow_walk_does_not_unlock_quiet_exit_or_record_escape(content):
    """Dropping to 0 composure routes to shadow_walk, does NOT unlock the_quiet_exit, and does not record an escape."""
    state = RunState.fresh_run()
    state.current_room = "hall"
    state.spend_composure(95)  # 5 composure left

    app = GameSuiteApp(content=content, state=state)
    async with app.run_test() as pilot:
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Move down to hall_right (costs 5 composure, reducing composure to 0)
        # 0: hall_front_door (not visible without knows_exit)
        # Choices: 0=hall_staircase, 1=hall_right
        hall_right_idx = next(
            i for i, c in enumerate(game_screen.current_choices)
            if c["id"] == "hall_right"
        )
        for _ in range(hall_right_idx):
            await pilot.press("down")
        assert game_screen.selected_choice == hall_right_idx

        await pilot.press("enter")

        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        assert top_screen.ending_id == "shadow_walk"

        profile = load_profile()
        assert "the_quiet_exit" not in profile.unlocked_endings
        assert profile.total_escapes == 0
