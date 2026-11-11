import pytest
from pathlib import Path
from textual.app import App

from index import TerminalGame
from screens.main_menu import MainMenuScreen
from screens.game import GameScreen
from screens.death import DeathScreen
from screens.ending import EndingScreen
from game.state import RunState
from game.save import save_to_disk, load_from_disk, has_saved_game, delete_saved_game, DEFAULT_SAVE_PATH
from game.content_schema import load_content


def test_save_round_trip_custom_path(tmp_path):
    save_file = tmp_path / "custom_save.json"
    state = RunState.fresh_run(difficulty="HARD")
    state.current_room = "blood_kitchen"
    state.spend_lantern(25)
    state.add_item("rusty_cleaver")
    state.set_flag("has_meat")
    state.journal.add_entry("ROOM_DISCOVERY", "test note")

    assert save_to_disk(state, path=save_file) is True
    assert has_saved_game(path=save_file) is True

    restored = load_from_disk(path=save_file)
    assert restored is not None
    assert restored.current_room == "blood_kitchen"
    assert restored.difficulty == "HARD"
    assert restored.lantern == 45
    assert restored.has_item("rusty_cleaver") is True
    assert restored.has_flag("has_meat") is True
    assert len(restored.journal.entries) == 1
    assert restored.journal.entries[0].text == "test note"

    assert delete_saved_game(path=save_file) is True
    assert has_saved_game(path=save_file) is False


@pytest.mark.anyio
async def test_continue_enabled_when_save_file_present():
    state = RunState.fresh_run()
    state.spend_lantern(20)
    save_to_disk(state)

    app = TerminalGame()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, MainMenuScreen)
        assert screen.options[0] == "CONTINUE"
        assert "START GAME" in screen.options

        # Press enter on CONTINUE
        await pilot.press("enter")
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)
        assert game_screen.state.lantern == 80


@pytest.mark.anyio
async def test_continue_hidden_when_no_save_file():
    delete_saved_game()
    app = TerminalGame()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, MainMenuScreen)
        assert "CONTINUE" not in screen.options
        assert screen.options[0] == "START GAME"


@pytest.mark.anyio
async def test_escape_saves_and_allows_continue_resume():
    delete_saved_game()
    app = TerminalGame()
    async with app.run_test() as pilot:
        # Start game
        await pilot.press("enter")
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Mutate run
        game_screen.state.spend_lantern(35)
        game_screen.state.add_item("matchbox")
        assert game_screen.state.lantern == 65

        # Press escape to return to menu
        await pilot.press("escape")
        menu_screen = pilot.app.screen
        assert isinstance(menu_screen, MainMenuScreen)
        assert menu_screen.options[0] == "CONTINUE"
        assert has_saved_game() is True

        # Select CONTINUE
        await pilot.press("enter")
        resumed_screen = pilot.app.screen
        assert isinstance(resumed_screen, GameScreen)
        assert resumed_screen.state.lantern == 65
        assert resumed_screen.state.has_item("matchbox") is True


@pytest.mark.anyio
async def test_death_deletes_save_file():
    state = RunState.fresh_run()
    save_to_disk(state)
    assert has_saved_game() is True

    # Mount DeathScreen
    death_screen = DeathScreen(cause="Darkness consumed you.", state=state)
    app = App()
    async with app.run_test() as pilot:
        await pilot.app.push_screen(death_screen)
        assert has_saved_game() is False


@pytest.mark.anyio
async def test_ending_deletes_save_file():
    state = RunState.fresh_run()
    save_to_disk(state)
    assert has_saved_game() is True

    # Mount EndingScreen
    ending_screen = EndingScreen(title="Escaped", prose="You escaped the house.")
    app = App()
    async with app.run_test() as pilot:
        await pilot.app.push_screen(ending_screen)
        assert has_saved_game() is False
