"""Tests for Main Menu wiring of the ENDINGS gallery option (Task A04)."""

import pytest
from textual.widgets import Static

from game.save import delete_saved_game, save_to_disk
from game.state import RunState
from index import TerminalGame
from screens.gallery import EndingsGalleryScreen
from screens.main_menu import MainMenuScreen


@pytest.mark.anyio
async def test_main_menu_includes_endings_option_without_save():
    """When no save file exists, ENDINGS is present at index 1."""
    delete_saved_game()
    app = TerminalGame()

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, MainMenuScreen)
        assert "ENDINGS" in screen.options
        assert screen.options == ["START GAME", "ENDINGS", "SETTINGS", "ABOUT", "EXIT"]


@pytest.mark.anyio
async def test_main_menu_includes_endings_option_with_save():
    """When save file exists, CONTINUE is at index 0 and ENDINGS is at index 2."""
    state = RunState.fresh_run()
    save_to_disk(state)

    try:
        app = TerminalGame()
        async with app.run_test() as pilot:
            screen = pilot.app.screen
            assert isinstance(screen, MainMenuScreen)
            assert "ENDINGS" in screen.options
            assert screen.options == ["CONTINUE", "START GAME", "ENDINGS", "SETTINGS", "ABOUT", "EXIT"]
    finally:
        delete_saved_game()


@pytest.mark.anyio
async def test_selecting_endings_pushes_gallery_screen():
    """Selecting ENDINGS pushes EndingsGalleryScreen, and Escape returns to MainMenu."""
    delete_saved_game()
    app = TerminalGame()

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, MainMenuScreen)

        # Move down from START GAME (0) to ENDINGS (1)
        await pilot.press("down")
        assert screen.options[screen.selected] == "ENDINGS"

        # Press Enter to open Gallery
        await pilot.press("enter")
        gallery_screen = pilot.app.screen
        assert isinstance(gallery_screen, EndingsGalleryScreen)

        # Press Escape to return to MainMenuScreen
        await pilot.press("escape")
        restored_screen = pilot.app.screen
        assert isinstance(restored_screen, MainMenuScreen)


@pytest.mark.anyio
async def test_selecting_endings_with_save_preserves_selection_on_return():
    """When save exists, selecting ENDINGS and pressing Escape preserves cursor on ENDINGS."""
    state = RunState.fresh_run()
    save_to_disk(state)

    try:
        app = TerminalGame()
        async with app.run_test() as pilot:
            screen = pilot.app.screen
            assert isinstance(screen, MainMenuScreen)
            assert screen.options == ["CONTINUE", "START GAME", "ENDINGS", "SETTINGS", "ABOUT", "EXIT"]

            # Move down to ENDINGS (index 2)
            await pilot.press("down")
            await pilot.press("down")
            assert screen.selected == 2
            assert screen.options[screen.selected] == "ENDINGS"

            # Open Gallery
            await pilot.press("enter")
            assert isinstance(pilot.app.screen, EndingsGalleryScreen)

            # Return to MainMenu
            await pilot.press("escape")
            restored = pilot.app.screen
            assert isinstance(restored, MainMenuScreen)
            # Selection should stay on ENDINGS (index 2), NOT reset to 0
            assert restored.selected == 2
            assert restored.options[restored.selected] == "ENDINGS"
    finally:
        delete_saved_game()
