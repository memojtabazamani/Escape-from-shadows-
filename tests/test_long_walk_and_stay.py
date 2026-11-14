"""Tests for The Long Walk and Stay narrative branches (Task B05)."""

from pathlib import Path
import pytest
from textual.app import App

from game.content_schema import load_content
from game.ending_resolver import resolve_terminal_event
from game.profile import load_profile
from game.state import RunState
from screens.death import DeathScreen
from screens.ending import EndingScreen
from screens.game import GameScreen


class GameTestApp(App):
    def __init__(self, content=None, state=None):
        super().__init__()
        self._content = content or load_content(Path("data/content.json"))
        self._state = state or RunState.fresh_run()

    async def on_mount(self) -> None:
        await self.push_screen(GameScreen(content=self._content, state=self._state))


@pytest.fixture(autouse=True)
def clean_profile(tmp_path, monkeypatch):
    profile_path = tmp_path / "test_profile.json"
    monkeypatch.setattr("game.profile.DEFAULT_PROFILE_PATH", profile_path)
    if profile_path.exists():
        profile_path.unlink()
    yield
    if profile_path.exists():
        profile_path.unlink()


@pytest.mark.anyio
async def test_early_hall_demise_triggers_the_long_walk():
    """AC-5: Fatal choice in the Hall during the first turns unlocks the_long_walk in profile."""
    content = load_content(Path("data/content.json"))
    state = RunState.fresh_run()
    # At start of run
    assert state.turn_count == 0

    app = GameTestApp(content=content, state=state)
    async with app.run_test() as pilot:
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Hall choices: 0=front_door (locked), 1=staircase, 2=right, 3=left (death)
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("down")
        assert game_screen.current_choices[game_screen.selected_choice]["id"] == "hall_left"

        # Execute death choice
        await pilot.press("enter")
        top_screen = pilot.app.screen
        assert isinstance(top_screen, DeathScreen)

        # Profile has recorded the_long_walk
        profile = load_profile()
        assert "the_long_walk" in profile.unlocked_endings


@pytest.mark.anyio
async def test_front_door_refusal_triggers_stay():
    """AC-11: Choosing to bolt the door from the inside triggers the Stay ending."""
    content = load_content(Path("data/content.json"))
    state = RunState.fresh_run()
    state.set_flag("knows_exit")

    app = GameTestApp(content=content, state=state)
    async with app.run_test() as pilot:
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Find hall_front_door_stay choice
        stay_choice_idx = next(
            i for i, c in enumerate(game_screen.current_choices)
            if c["id"] == "hall_front_door_stay"
        )

        for _ in range(stay_choice_idx):
            await pilot.press("down")
        assert game_screen.selected_choice == stay_choice_idx

        # Select Stay
        await pilot.press("enter")
        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        assert top_screen.ending_id == "stay"

        # Profile has recorded stay
        profile = load_profile()
        assert "stay" in profile.unlocked_endings


@pytest.mark.anyio
async def test_hall_accept_dark_routes_to_the_long_walk():
    """AC-5: Explicitly walking into the silent dark in the hall triggers the_long_walk."""
    content = load_content(Path("data/content.json"))
    state = RunState.fresh_run()

    app = GameTestApp(content=content, state=state)
    async with app.run_test() as pilot:
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        dark_choice_idx = next(
            i for i, c in enumerate(game_screen.current_choices)
            if c["id"] == "hall_accept_dark"
        )

        for _ in range(dark_choice_idx):
            await pilot.press("down")
        assert game_screen.selected_choice == dark_choice_idx

        # Select Accept Dark
        await pilot.press("enter")
        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        assert top_screen.ending_id == "the_long_walk"

        profile = load_profile()
        assert "the_long_walk" in profile.unlocked_endings
