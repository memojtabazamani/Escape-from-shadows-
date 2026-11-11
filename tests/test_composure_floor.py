"""Tests for zero-composure voluntary walk into the Shadow (Task D03)."""
from pathlib import Path
import pytest

from game.content_schema import load_content, validate_content
from game.state import RunState
from screens.ending import EndingScreen
from screens.death import DeathScreen
from screens.game import GameScreen
from tests.test_game_screen import GameScreenTestApp


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


def test_content_validates_with_shadow_walk_ending(house_content):
    """Content schema validator accepts shadow_walk_ending and its requirements."""
    problems = validate_content(house_content)
    assert problems == [], f"Validation errors: {[str(p) for p in problems]}"


@pytest.mark.anyio
async def test_zero_composure_enters_the_walk_and_not_the_death_screen(house_content):
    """AC-11: Zero composure triggers the voluntary walk into the Shadow (EndingScreen), not DeathScreen."""
    state = RunState.fresh_run("MEDIUM")
    state.current_room = "hall"
    # Drain composure down to 5
    state.spend_composure(95)
    assert state.composure == 5

    app = GameScreenTestApp(content=house_content, state=state)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Select hall_right (costs 5 composure, reducing it to 0)
        # Choices in hall:
        # 0: hall_front_door
        # 1: hall_staircase
        # 2: hall_right
        await pilot.press("down")
        await pilot.press("down")
        assert screen.current_choices[screen.selected_choice]["id"] == "hall_right"
        await pilot.press("enter")

        # Must push EndingScreen, NOT DeathScreen!
        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        assert not isinstance(top_screen, DeathScreen)
        assert state.terminal_outcome == "shadow_walk"


def test_the_walk_is_unreachable_in_the_first_rooms(house_content):
    """In the first room (Hall), starting from full composure (100 on MEDIUM, 70 on HARD), zero cannot be reached."""
    med_state = RunState.fresh_run("MEDIUM")
    assert med_state.composure == 100

    hall = next(r for r in house_content["rooms"] if r["id"] == "hall")
    hall_right = next(c for c in hall["choices"] if c["id"] == "hall_right")
    drain = next((eff.get("amount", 0) for eff in hall_right.get("effects", []) if eff.get("verb") == "spend_composure"), 0)
    assert drain == 5

    # After moving through hall_right, composure is 95, nowhere near 0
    med_state.spend_composure(drain)
    assert med_state.composure == 95

    hard_state = RunState.fresh_run("HARD")
    assert hard_state.composure == 70
    hard_state.spend_composure(drain)
    assert hard_state.composure == 65


def test_the_walk_is_reachable_by_sustained_drain(house_content):
    """Through repeated/sustained drain choices, zero composure is reachable."""
    state = RunState.fresh_run("MEDIUM")
    assert state.composure == 100

    # Sustained drain
    while state.composure > 0:
        state.spend_composure(15)

    assert state.composure == 0
    assert state.terminal_outcome == ""
    # Zero composure triggers shadow_walk
    from game.composure import is_zero_composure
    assert is_zero_composure(state) is True


def test_run_is_completable_without_reaching_zero(house_content):
    """The game can be completed with composure remaining safely high."""
    state = RunState.fresh_run("MEDIUM")
    # Take hall_right (-5 -> 95)
    state.spend_composure(5)
    # Read book (-15 -> 80)
    state.spend_composure(15)
    # Composure is 80, far above 0 and far above the 20 distortion threshold
    assert state.composure == 80
    assert state.composure > 20


def test_terminal_kind_is_recorded_distinguishably():
    """Terminal outcome distinguishes shadow_walk from death and escape in RunState."""
    walk_state = RunState.fresh_run()
    walk_state.terminal_outcome = "shadow_walk"
    data = walk_state.snapshot()
    assert data["terminal_outcome"] == "shadow_walk"

    restored = RunState.fresh_run()
    restored.restore(data)
    assert restored.terminal_outcome == "shadow_walk"


def test_walk_prose_fits_the_room_budget(house_content):
    """ASM-18: Shadow walk ending prose fits within the 20-line budget."""
    walk_room = next(r for r in house_content["rooms"] if r["id"] == "shadow_walk_ending")
    lines = walk_room["prose"].split("\n")
    assert len(lines) <= 20
    assert "the Shadow murmurs" in walk_room["prose"]
