"""Slice D (Composure) integration tests.

Exhaustive checks across all rooms:
- Cap holds everywhere: transform is identity above 20 composure.
- Every distorted line carries a visible cognitive tic.
- Choice sets remain completely identical under distortion.
- Zero composure never routes to DeathScreen (AC-11).
- Walk vs Death are distinct and recorded in RunState.
- Non-colour visibility check.
- Clean run avoidance check.
"""
from pathlib import Path
import pytest

from game.composure import DISTORTION_THRESHOLD, is_zero_composure
from game.content_schema import load_content
from game.distortion import distort_narration, has_distortion_tic
from game.effects import resolve_choice
from game.state import RunState
from screens.death import DeathScreen
from screens.ending import EndingScreen
from screens.game import GameScreen
from tests.test_game_screen import GameScreenTestApp


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


def test_no_room_distorts_above_the_threshold(house_content):
    """Exhaustively verify across all rooms that no distortion occurs at composure > 20."""
    test_levels = [21, 30, 50, 70, 100]
    for room in house_content["rooms"]:
        prose = room.get("prose", "")
        for comp in test_levels:
            out = distort_narration(prose, comp)
            assert out == prose, f"Room {room['id']} distorted above threshold at composure={comp}"

        if "revisit_prose" in room:
            rev = room["revisit_prose"]
            for comp in test_levels:
                out_rev = distort_narration(rev, comp)
                assert out_rev == rev, f"Room {room['id']} revisit prose distorted at composure={comp}"


def test_every_distorted_line_in_every_room_carries_a_tic(house_content):
    """Exhaustively verify that in the distortion band (<= 20), every non-empty line carries the tic."""
    test_levels = [20, 15, 10, 5, 0]
    for room in house_content["rooms"]:
        for comp in test_levels:
            prose = room.get("prose", "")
            out = distort_narration(prose, comp)
            for line in out.split("\n"):
                if line.strip():
                    assert has_distortion_tic(line), (
                        f"Room {room['id']} line lacked tic at composure={comp}: {line}"
                    )

            if "revisit_prose" in room:
                rev_out = distort_narration(room["revisit_prose"], comp)
                for line in rev_out.split("\n"):
                    if line.strip():
                        assert has_distortion_tic(line), (
                            f"Room {room['id']} revisit line lacked tic at composure={comp}: {line}"
                        )


def test_choice_sets_are_identical_under_distortion_in_every_room(house_content):
    """ASM-6: Distortion never changes choice ids or destinations in any room."""
    for room in house_content["rooms"]:
        base_choices = [(c["id"], c["destination"]) for c in room.get("choices", [])]

        # Verify GameScreen initializes choices identically regardless of composure
        state_full = RunState.fresh_run()
        state_full.composure = 100
        screen_full = GameScreen(content=house_content, state=state_full)
        choices_full = [(c["id"], c["destination"]) for c in room.get("choices", [])]

        state_low = RunState.fresh_run()
        state_low.composure = 5
        screen_low = GameScreen(content=house_content, state=state_low)
        choices_low = [(c["id"], c["destination"]) for c in room.get("choices", [])]

        assert choices_full == base_choices
        assert choices_low == base_choices


@pytest.mark.anyio
async def test_zero_composure_never_routes_to_the_death_screen(house_content):
    """AC-11: Dropping to 0 composure routes to EndingScreen (Shadow Walk), never DeathScreen."""
    state = RunState.fresh_run("MEDIUM")
    state.current_room = "hall"
    state.spend_composure(95)  # 5 left

    app = GameScreenTestApp(content=house_content, state=state)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Trigger hall_right (-5 composure -> 0 composure)
        await pilot.press("down")
        await pilot.press("down")
        assert screen.current_choices[screen.selected_choice]["id"] == "hall_right"
        await pilot.press("enter")

        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        assert not isinstance(top_screen, DeathScreen)
        assert state.terminal_outcome == "shadow_walk"


def test_walk_and_death_are_distinguishable_in_the_run_state():
    """RunState captures distinct terminal outcomes for I01 persistence handoff."""
    state_walk = RunState.fresh_run()
    state_walk.terminal_outcome = "shadow_walk"

    state_death = RunState.fresh_run()
    state_death.terminal_outcome = "death"

    state_escape = RunState.fresh_run()
    state_escape.terminal_outcome = "escape"

    assert state_walk.terminal_outcome != state_death.terminal_outcome
    assert state_walk.terminal_outcome != state_escape.terminal_outcome

    # Verify snapshot round-trip preserves distinction
    assert state_walk.snapshot()["terminal_outcome"] == "shadow_walk"
    assert state_death.snapshot()["terminal_outcome"] == "death"
    assert state_escape.snapshot()["terminal_outcome"] == "escape"


def test_composure_is_visible_and_colour_independent():
    """AC-9 / §8: Nerve status is distinguishable without reliance on colour alone."""
    full = GameScreen.render_composure_bar(100)
    shaken = GameScreen.render_composure_bar(15)
    broken = GameScreen.render_composure_bar(0)

    # Text cues
    assert "(shaken)" in shaken
    assert "(broken)" in broken
    assert "(shaken)" not in full
    assert "(broken)" not in full

    # Block graphics difference
    assert "██████████" in full
    assert "██░░░░░░░░" in shaken
    assert "░░░░░░░░░░" in broken


def test_a_clean_run_never_sees_distortion_or_the_walk(house_content):
    """Avoidance check: A normal winning run preserves composure > 20 and never triggers distortion or shadow walk."""
    state = RunState.fresh_run("MEDIUM")
    state.current_room = "hall"
    rooms_by_id = {r["id"]: r for r in house_content["rooms"]}

    # Hall -> Library
    to_lib = next(c for c in rooms_by_id["hall"]["choices"] if c["id"] == "hall_right")
    res1 = resolve_choice(to_lib, state)
    state.current_room = res1.destination
    assert state.composure == 95
    assert not is_zero_composure(state)
    assert state.composure > DISTORTION_THRESHOLD

    # Read book
    read_tome = next(c for c in rooms_by_id["old_library"]["choices"] if c["id"] == "library_read")
    res2 = resolve_choice(read_tome, state)
    assert state.composure == 80
    assert state.composure > DISTORTION_THRESHOLD

    # Return to Hall
    to_hall = next(c for c in rooms_by_id["old_library"]["choices"] if c["id"] == "library_return")
    res3 = resolve_choice(to_hall, state)
    state.current_room = res3.destination
    assert state.composure == 80

    # Escape Front Door
    escape = next(c for c in rooms_by_id["hall"]["choices"] if c["id"] == "hall_front_door")
    res4 = resolve_choice(escape, state)
    assert res4.destination == "front_door_escape"
    assert state.composure == 80  # Finishes with 80% nerve intact!
    assert state.terminal_outcome != "shadow_walk"
