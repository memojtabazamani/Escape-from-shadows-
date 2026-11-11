import copy
import pytest
from pathlib import Path
from textual.widgets import Static

from index import TerminalGame
from screens.game import GameScreen
from screens.death import DeathScreen
from screens.ending import EndingScreen
from screens.main_menu import MainMenuScreen
from game.content_schema import load_content, validate_content
from game.state import RunState
from game.lantern import (
    FIRST_VISIT_DRAIN,
    REVISIT_DRAIN,
    CAREFUL_ACTION_DRAIN,
    drain_for_room,
)


@pytest.fixture
def base_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


@pytest.mark.anyio
async def test_a_full_run_can_be_completed():
    """Happy path: Start from menu -> Hall -> Library -> Read book -> Return -> Front door -> Ending."""
    app = TerminalGame()
    async with app.run_test() as pilot:
        # 1. Main menu: select START GAME
        assert isinstance(pilot.app.screen, MainMenuScreen)
        await pilot.press("enter")

        # 2. Arrived in Hall
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)
        assert game_screen.state.current_room == "hall"
        assert game_screen.state.lantern == 100
        assert game_screen.state.turn_count == 0

        # Choices in hall:
        # 0: hall_front_door (gated by knows_exit)
        # 1: hall_staircase (gated)
        # 2: hall_right -> old_library
        # 3: hall_left -> left_doorway_death
        await pilot.press("down")  # 1: staircase
        await pilot.press("down")  # 2: library
        assert game_screen.current_choices[game_screen.selected_choice]["id"] == "hall_right"
        await pilot.press("enter")

        # 3. Arrived in Old Library (first visit: -10 oil)
        assert game_screen.state.current_room == "old_library"
        assert game_screen.state.lantern == 90
        assert game_screen.state.turn_count == 1
        assert game_screen.state.has_flag("knows_exit") is False

        # Choices in library:
        # 0: library_read (costs 25 oil, sets knows_exit)
        # 1: library_return -> hall
        assert game_screen.selected_choice == 0
        await pilot.press("enter")

        # 4. Book read resolved
        assert game_screen.state.has_flag("knows_exit") is True
        assert game_screen.state.lantern == 90 - CAREFUL_ACTION_DRAIN  # 65
        assert game_screen.state.turn_count == 2

        # 5. Return to Hall (choice 1)
        await pilot.press("down")  # 1: library_return
        assert game_screen.current_choices[game_screen.selected_choice]["id"] == "library_return"
        await pilot.press("enter")

        # 6. Revisit Hall (revisit discount: -5 oil)
        assert game_screen.state.current_room == "hall"
        assert game_screen.state.lantern == 65 - REVISIT_DRAIN  # 60
        assert game_screen.state.turn_count == 3

        # Echo check: revisit prose rendered
        await pilot.press("space")
        scene_text = game_screen.query_one("#scene-text", Static)
        assert "You step back into the vaulted silence" in str(scene_text.content)

        # 7. Front door choice now yields because knows_exit is True (choice 0)
        assert game_screen.selected_choice == 0
        assert game_screen.current_choices[0]["id"] == "hall_front_door"
        await pilot.press("enter")

        # 8. Reached EndingScreen!
        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        prose_widget = top_screen.query_one("#ending-prose", Static)
        assert "survived" in str(prose_widget.content).lower()


@pytest.mark.anyio
async def test_a_run_can_end_in_the_telegraphed_death():
    """Failure path: Start -> Hall -> Left doorway (warned twice) -> DeathScreen with cause."""
    app = TerminalGame()
    async with app.run_test() as pilot:
        # Start game
        await pilot.press("enter")
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Telegraph check in hall: telegraphs rendered in scene zone before choice
        tele_widget = game_screen.query_one("#scene-telegraphs", Static)
        rendered_tele = str(tele_widget.content)
        assert "warm, unnatural air" in rendered_tele
        assert "wet, rhythmic dripping" in rendered_tele

        # Navigate to left archway (choice 3)
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("down")
        assert game_screen.current_choices[game_screen.selected_choice]["id"] == "hall_left"

        # Step into death
        await pilot.press("enter")

        # Pushed DeathScreen
        top_screen = pilot.app.screen
        assert isinstance(top_screen, DeathScreen)
        cause_widget = top_screen.query_one("#death-cause", Static)
        assert "butchered in the dark" in str(cause_widget.content)


@pytest.mark.anyio
async def test_a_requirement_failure_does_not_move_the_player():
    """Refusal path: Unsatisfied requirements leave the player unmoved and turn count unchanged."""
    app = TerminalGame()
    async with app.run_test() as pilot:
        await pilot.press("enter")
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)
        assert game_screen.state.current_room == "hall"
        assert game_screen.state.turn_count == 0

        # Attempt 1: Front door without knows_exit (choice 0)
        await pilot.press("enter")
        assert game_screen.state.current_room == "hall"
        assert game_screen.state.turn_count == 0
        prompt = game_screen.query_one("#prompt-line", Static)
        assert "requires flag 'knows_exit'" in str(prompt.content)

        # Attempt 2: Staircase without staircase_passable (choice 1)
        await pilot.press("down")
        assert game_screen.current_choices[game_screen.selected_choice]["id"] == "hall_staircase"
        await pilot.press("enter")
        assert game_screen.state.current_room == "hall"
        assert game_screen.state.turn_count == 0
        prompt = game_screen.query_one("#prompt-line", Static)
        assert "requires flag 'staircase_passable'" in str(prompt.content)


def test_oil_is_spent_by_movement_and_never_goes_negative():
    """Lantern path: Pure drain calculator and RunState clamp behavior."""
    state = RunState.fresh_run()
    assert state.lantern == 100

    # First visit cost
    cost1 = drain_for_room(state, "new_chamber")
    assert cost1 == FIRST_VISIT_DRAIN
    state.spend_lantern(cost1)
    state.visit("new_chamber")
    assert state.lantern == 90

    # Revisit cost
    cost2 = drain_for_room(state, "new_chamber")
    assert cost2 == REVISIT_DRAIN
    state.spend_lantern(cost2)
    assert state.lantern == 85

    # Overdrain clamps to 0 and reports actual amount deducted
    spent = state.spend_lantern(200)
    assert spent == 85
    assert state.lantern == 0
    assert state.has_light() is False


@pytest.mark.anyio
async def test_a_new_room_plays_without_touching_the_loop(base_content):
    """Content-only proof (AC-22 seed): Add a synthetic room to content and play it seamlessly."""
    synthetic_content = copy.deepcopy(base_content)

    # Add a synthetic room: 'secret_observatory'
    synthetic_room = {
        "id": "secret_observatory",
        "name": "The Secret Observatory",
        "prose": "Dusty brass astrolabes point toward cold constellation glass above.",
        "choices": [
            {
                "id": "observatory_return",
                "label": "Climb back down to the hall",
                "destination": "hall",
                "tier": "scar",
            }
        ],
    }
    synthetic_content["rooms"].append(synthetic_room)

    # Link from hall to secret_observatory
    hall_room = next(r for r in synthetic_content["rooms"] if r["id"] == "hall")
    hall_room["choices"].append(
        {
            "id": "hall_secret_ladder",
            "label": "Climb the concealed spiral ladder",
            "destination": "secret_observatory",
            "tier": "scar",
        }
    )

    # Content schema validator verifies it is 100% valid
    problems = validate_content(synthetic_content)
    assert problems == [], f"Synthetic content validation errors: {problems}"

    # Play it in GameScreen
    from screens.game import GameScreen
    from tests.test_game_screen import GameScreenTestApp

    app = GameScreenTestApp(content=synthetic_content)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Select the newly added choice (at index 4)
        ladder_index = next(
            i for i, c in enumerate(screen.current_choices) if c["id"] == "hall_secret_ladder"
        )
        for _ in range(ladder_index):
            await pilot.press("down")
        assert screen.current_choices[screen.selected_choice]["id"] == "hall_secret_ladder"
        await pilot.press("enter")

        # Player transitioned into the synthetic room!
        assert screen.state.current_room == "secret_observatory"
        header = screen.query_one("#scene-header", Static)
        assert str(header.content) == "The Secret Observatory"
        text = screen.query_one("#scene-text", Static)
        assert "astrolabes" in str(text.content)

        # Return choice works
        await pilot.press("enter")
        assert screen.state.current_room == "hall"


def test_every_room_fits_one_screen_at_a_narrow_width(base_content):
    """AC-23: Mechanical check ensuring every room's prose is <= 20 lines (ASM-18)."""
    for room in base_content["rooms"]:
        prose = room.get("prose", "")
        lines = prose.split("\n")
        assert len(lines) <= 20, (
            f"Room '{room['id']}' exceeded prose budget: {len(lines)} lines > 20"
        )
        if "revisit_prose" in room:
            revisit_lines = room["revisit_prose"].split("\n")
            assert len(revisit_lines) <= 20, (
                f"Room '{room['id']}' revisit_prose exceeded budget: {len(revisit_lines)} lines > 20"
            )
