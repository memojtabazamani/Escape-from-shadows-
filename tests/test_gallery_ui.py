"""Tests for Endings Gallery screen UI and keybinds (Task A03)."""

import pytest
from textual.app import App, ComposeResult
from textual.widgets import Static

from game.endings import CANONICAL_ENDINGS, TOTAL_CANONICAL_ENDINGS
from game.profile import PlayerProfile
from screens.gallery import EndingsGalleryScreen


class GalleryHostApp(App[None]):
    """Test host app for mounting EndingsGalleryScreen."""

    def __init__(self, profile: PlayerProfile) -> None:
        super().__init__()
        self._profile = profile

    def compose(self) -> ComposeResult:
        yield from ()

    def on_mount(self) -> None:
        self.push_screen(EndingsGalleryScreen(self._profile))


@pytest.mark.anyio
async def test_gallery_renders_all_seven_cards():
    """All 7 canonical endings appear in numeric order on the screen."""
    profile = PlayerProfile(unlocked_endings={"the_quiet_exit"})
    app = GalleryHostApp(profile)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)

        cards_widget = screen.query_one("#gallery-cards", Static)
        cards_text = str(cards_widget.content)

        for number in range(1, TOTAL_CANONICAL_ENDINGS + 1):
            assert f"#{number}." in cards_text


@pytest.mark.anyio
async def test_gallery_shows_unlocked_vs_locked_styling():
    """Unlocked cards show true titles while locked cards show silhouettes."""
    profile = PlayerProfile(unlocked_endings={"the_quiet_exit", "meat_and_silence"})
    app = GalleryHostApp(profile)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)

        cards_widget = screen.query_one("#gallery-cards", Static)
        cards_text = str(cards_widget.content)

        # Unlocked: The Quiet Exit and Meat and Silence
        assert "The Quiet Exit" in cards_text
        assert "Meat and Silence" in cards_text
        assert "You unlatched the heavy front door" in cards_text

        # Locked: What the Book Knew and The Long Walk
        assert "What the Book Knew" not in cards_text
        assert "The Long Walk" not in cards_text
        assert "The New Shadow" not in cards_text
        assert "Homecoming" not in cards_text
        assert "Stay" not in cards_text
        assert "[ ? ? ? ? ? ? ? ? ]" in cards_text
        assert "Hint: Three turns of patient reading" in cards_text


@pytest.mark.anyio
async def test_gallery_tally_calculation():
    """Tally string accurately displays X OF 7 across empty, partial, and full discovery."""
    # 0 of 7
    p0 = PlayerProfile(unlocked_endings=set())
    app0 = GalleryHostApp(p0)
    async with app0.run_test() as pilot0:
        tally0 = str(pilot0.app.screen.query_one("#gallery-tally", Static).content)
        assert "0 OF 7" in tally0

    # 3 of 7
    p3 = PlayerProfile(unlocked_endings={"the_long_walk", "meat_and_silence", "the_quiet_exit"})
    app3 = GalleryHostApp(p3)
    async with app3.run_test() as pilot3:
        tally3 = str(pilot3.app.screen.query_one("#gallery-tally", Static).content)
        assert "3 OF 7" in tally3

    # 7 of 7
    p7 = PlayerProfile(unlocked_endings=set(CANONICAL_ENDINGS.keys()))
    app7 = GalleryHostApp(p7)
    async with app7.run_test() as pilot7:
        tally7 = str(pilot7.app.screen.query_one("#gallery-tally", Static).content)
        assert "7 OF 7" in tally7


@pytest.mark.anyio
async def test_gallery_cursor_navigation_and_details():
    """Navigating with Up and Down moves selection and updates detail pane."""
    profile = PlayerProfile(unlocked_endings={"the_long_walk", "meat_and_silence"})
    app = GalleryHostApp(profile)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)
        assert screen.selected == 0

        # Initial selected detail is ending #1 (unlocked)
        details_widget = screen.query_one("#gallery-details", Static)
        assert "The Long Walk" in str(details_widget.content)

        # Move down to #2 (unlocked)
        await pilot.press("down")
        assert screen.selected == 1
        assert "Meat and Silence" in str(details_widget.content)

        # Move down to #3 (locked)
        await pilot.press("down")
        assert screen.selected == 2
        assert "SILHOUETTE" in str(details_widget.content)

        # Press Up to return to #2
        await pilot.press("up")
        assert screen.selected == 1
        assert "Meat and Silence" in str(details_widget.content)


@pytest.mark.anyio
async def test_gallery_enter_toggles_expanded_details():
    """Pressing Enter toggles expanded details showing criteria or locked status."""
    profile = PlayerProfile(unlocked_endings={"the_long_walk"})
    app = GalleryHostApp(profile)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingsGalleryScreen)
        assert screen.expanded is False

        details_widget = screen.query_one("#gallery-details", Static)
        assert "Unlock Path:" not in str(details_widget.content)

        # Press Enter to expand details for unlocked ending
        await pilot.press("enter")
        assert screen.expanded is True
        assert "Unlock Path:" in str(details_widget.content)
        assert "A single misstep where the candles end." in str(details_widget.content)

        # Press Enter again to collapse
        await pilot.press("enter")
        assert screen.expanded is False
        assert "Unlock Path:" not in str(details_widget.content)

        # Move to locked ending #2 and expand
        await pilot.press("down")
        await pilot.press("enter")
        assert screen.expanded is True
        assert "Status: Locked" in str(details_widget.content)


@pytest.mark.anyio
async def test_gallery_escape_dismisses_screen():
    """Pressing Escape pops the gallery screen."""
    profile = PlayerProfile()
    app = GalleryHostApp(profile)

    async with app.run_test() as pilot:
        assert isinstance(pilot.app.screen, EndingsGalleryScreen)
        await pilot.press("escape")
        # Screen popped, returns to base app screen
        assert not isinstance(pilot.app.screen, EndingsGalleryScreen)
