"""Comprehensive integration test suite for Profile persistence and Endings Gallery (Task A05).

Covers:
- Cross-run profile lifecycle and persistence isolation
- Textual Pilot rendering across ratio states (0 of 7, 4 of 7, 7 of 7)
- Unlocked title revelation vs locked silhouette masking
- Full menu-to-gallery navigation loop
"""

from pathlib import Path
import pytest
from textual.app import App, ComposeResult
from textual.widgets import Static

from game.endings import CANONICAL_ENDINGS, TOTAL_CANONICAL_ENDINGS
from game.profile import (
    PlayerProfile,
    delete_profile,
    get_unlocked_endings,
    load_profile,
    save_profile,
    unlock_ending,
)
from game.save import delete_saved_game, has_saved_game, save_to_disk
from game.state import RunState
from index import TerminalGame
from screens.gallery import EndingsGalleryScreen
from screens.main_menu import MainMenuScreen


class GalleryTestHost(App[None]):
    """Host harness for isolated gallery screen testing."""

    def __init__(self, profile: PlayerProfile) -> None:
        super().__init__()
        self._profile = profile

    def compose(self) -> ComposeResult:
        yield from ()

    def on_mount(self) -> None:
        self.push_screen(EndingsGalleryScreen(self._profile))


def test_profile_lifecycle_across_runs(tmp_path: Path):
    """Profile unlocks persist independently from run state and survive savegame deletion."""
    profile_path = tmp_path / "data" / "profile.json"
    save_path = tmp_path / "savegame.json"

    # 1. Starting with no profile file produces empty set
    initial_profile = load_profile(profile_path)
    assert initial_profile.unlocked_endings == set()

    # 2. Calling unlock_ending updates disk
    assert unlock_ending("the_quiet_exit", profile_path) is True
    assert get_unlocked_endings(profile_path) == {"the_quiet_exit"}

    # 3. Game run starts and saves
    state = RunState.fresh_run()
    save_to_disk(state, path=save_path)
    assert has_saved_game(path=save_path) is True

    # 4. Another ending unlocked during run
    assert unlock_ending("what_the_book_knew", profile_path) is True
    assert get_unlocked_endings(profile_path) == {"the_quiet_exit", "what_the_book_knew"}

    # 5. Run finishes / dies / terminates -> single-run save is purged
    assert delete_saved_game(path=save_path) is True
    assert has_saved_game(path=save_path) is False

    # 6. Profile still has all unlocked endings
    final_profile = load_profile(profile_path)
    assert final_profile.unlocked_endings == {"the_quiet_exit", "what_the_book_knew"}


@pytest.mark.anyio
async def test_gallery_tally_states_pilot():
    """EndingsGalleryScreen displays exact ratio strings ('0 OF 7', '4 OF 7', '7 OF 7')."""
    # State 1: 0 OF 7
    p0 = PlayerProfile(unlocked_endings=set())
    app0 = GalleryTestHost(p0)
    async with app0.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)
        tally = str(screen.query_one("#gallery-tally", Static).content)
        assert "0 OF 7" in tally
        assert "DISCOVERED: 0 OF 7" in tally

    # State 2: 4 OF 7
    p4 = PlayerProfile(
        unlocked_endings={
            "the_long_walk",
            "meat_and_silence",
            "the_quiet_exit",
            "what_the_book_knew",
        }
    )
    app4 = GalleryTestHost(p4)
    async with app4.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)
        tally = str(screen.query_one("#gallery-tally", Static).content)
        assert "4 OF 7" in tally
        assert "DISCOVERED: 4 OF 7" in tally

    # State 3: 7 OF 7
    p7 = PlayerProfile(unlocked_endings=set(CANONICAL_ENDINGS.keys()))
    app7 = GalleryTestHost(p7)
    async with app7.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)
        tally = str(screen.query_one("#gallery-tally", Static).content)
        assert "7 OF 7" in tally
        assert "DISCOVERED: 7 OF 7" in tally


@pytest.mark.anyio
async def test_gallery_obscures_locked_and_reveals_unlocked_pilot():
    """Locked cards do not reveal true titles; unlocked cards reveal titles and summaries."""
    profile = PlayerProfile(unlocked_endings={"the_quiet_exit", "homecoming"})
    app = GalleryTestHost(profile)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)

        cards_content = str(screen.query_one("#gallery-cards", Static).content)

        # Unlocked endings: titles & summaries visible
        assert "The Quiet Exit" in cards_content
        assert "You unlatched the heavy front door and stepped out into the night." in cards_content

        assert "Homecoming" in cards_content
        assert "The three memory fragments revealed what the manor truly was: your home." in cards_content

        # Locked endings: titles strictly hidden
        assert "The Long Walk" not in cards_content
        assert "Meat and Silence" not in cards_content
        assert "What the Book Knew" not in cards_content
        assert "The New Shadow" not in cards_content
        assert "Stay" not in cards_content

        # Locked placeholders and hints visible
        assert "[ ? ? ? ? ? ? ? ? ]" in cards_content
        assert "Hint: A single misstep where the candles end." in cards_content
        assert "Hint: When the front door stands wide, choose not to cross the threshold." in cards_content


@pytest.mark.anyio
async def test_menu_to_gallery_navigation_and_return_pilot():
    """Selecting ENDINGS from MainMenuScreen opens Gallery and Escape returns cleanly."""
    delete_saved_game()
    app = TerminalGame()

    async with app.run_test() as pilot:
        # Start at main menu
        menu = pilot.app.screen
        assert isinstance(menu, MainMenuScreen)
        assert "ENDINGS" in menu.options

        # Navigate down from START GAME to ENDINGS
        await pilot.press("down")
        assert menu.options[menu.selected] == "ENDINGS"

        # Enter pushes EndingsGalleryScreen
        await pilot.press("enter")
        gallery = pilot.app.screen
        assert isinstance(gallery, EndingsGalleryScreen)

        # In gallery, navigate down then up
        await pilot.press("down")
        assert gallery.selected == 1
        await pilot.press("up")
        assert gallery.selected == 0

        # Press Enter to toggle details expansion
        await pilot.press("enter")
        assert gallery.expanded is True
        await pilot.press("enter")
        assert gallery.expanded is False

        # Escape pops back to MainMenuScreen
        await pilot.press("escape")
        restored_menu = pilot.app.screen
        assert isinstance(restored_menu, MainMenuScreen)
