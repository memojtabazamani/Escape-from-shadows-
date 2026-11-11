import pytest
from pathlib import Path
from textual.widgets import Static

from index import TerminalGame
from screens.main_menu import MainMenuScreen
from screens.game import GameScreen
from game.state import RunState


@pytest.mark.anyio
async def test_start_game_pushes_the_gameplay_screen():
    app = TerminalGame()
    async with app.run_test() as pilot:
        # App starts on MainMenuScreen
        assert isinstance(pilot.app.screen, MainMenuScreen)
        assert pilot.app.active_run is None

        # Select "START GAME" (selected index 0)
        await pilot.press("enter")

        # Now active screen is GameScreen
        top_screen = pilot.app.screen
        assert isinstance(top_screen, GameScreen)
        assert pilot.app.active_run is not None
        assert top_screen.state is pilot.app.active_run
        assert top_screen.state.lantern == 100
        assert top_screen.state.current_room == "hall"


@pytest.mark.anyio
async def test_second_run_starts_from_a_fresh_state():
    app = TerminalGame()
    async with app.run_test() as pilot:
        # First run: start game
        await pilot.press("enter")
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Mutate run state in first run
        game_screen.state.spend_lantern(50)
        game_screen.state.set_flag("knows_exit")
        assert game_screen.state.lantern == 50
        assert game_screen.state.has_flag("knows_exit") is True

        # Escape back to menu
        await pilot.press("escape")
        assert isinstance(pilot.app.screen, MainMenuScreen)
        assert pilot.app.active_run is None

        # Second run: select START GAME
        if pilot.app.screen.options[0] == "CONTINUE":
            await pilot.press("down")
        await pilot.press("enter")
        second_game_screen = pilot.app.screen
        assert isinstance(second_game_screen, GameScreen)
        assert pilot.app.active_run is not None
        assert second_game_screen.state is pilot.app.active_run

        # Fresh state verified
        assert second_game_screen.state.lantern == 100
        assert second_game_screen.state.has_flag("knows_exit") is False
        assert second_game_screen.state.turn_count == 0


@pytest.mark.anyio
async def test_escape_from_gameplay_returns_to_the_menu():
    app = TerminalGame()
    async with app.run_test() as pilot:
        # Start game
        await pilot.press("enter")
        assert isinstance(pilot.app.screen, GameScreen)
        assert pilot.app.active_run is not None

        # Escape
        await pilot.press("escape")
        assert isinstance(pilot.app.screen, MainMenuScreen)
        assert pilot.app.active_run is None


def test_menu_does_not_branch_on_difficulty():
    """Guard §11: Ensure start game lifecycle has not introduced premature difficulty branching."""
    import inspect
    from screens import main_menu

    source = inspect.getsource(main_menu.MainMenuScreen.action_select)
    # Check lines inside "START GAME" block
    lines = source.splitlines()
    start_game_block = []
    in_start = False
    for line in lines:
        if 'selected_option == "START GAME"' in line:
            in_start = True
            continue
        if in_start:
            if 'elif selected_option' in line:
                break
            start_game_block.append(line)

    block_str = "\n".join(start_game_block)
    assert "if difficulty ==" not in block_str
    assert "if difficulty in" not in block_str
    assert "match difficulty" not in block_str
