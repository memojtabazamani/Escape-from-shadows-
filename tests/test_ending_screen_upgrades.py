"""Tests for EndingScreen upgrades: ASCII vignettes, profile unlocking, and gallery link (Task B04)."""

import pytest
from textual.app import App
from textual.widgets import Static

from game.profile import PlayerProfile, delete_profile, load_profile, save_profile
from game.endings_art import get_ending_ascii
from screens.ending import EndingScreen
from screens.gallery import EndingsGalleryScreen


class EndingApp(App):
    def __init__(self, ending_id="the_quiet_exit", room=None, content=None):
        super().__init__()
        self.ending_id = ending_id
        self.room = room
        self.content = content

    async def on_mount(self) -> None:
        await self.push_screen(
            EndingScreen(
                room=self.room,
                content=self.content,
                ending_id=self.ending_id,
            )
        )


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
async def test_ending_mount_unlocks_profile_ending():
    """AC-1, AC-4: Mounting EndingScreen persists the unlocked ending ID to profile immediately."""
    profile_before = load_profile()
    assert "what_the_book_knew" not in profile_before.unlocked_endings

    app = EndingApp(ending_id="what_the_book_knew")
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingScreen)
        assert screen.ending_id == "what_the_book_knew"

        profile_after = load_profile()
        assert "what_the_book_knew" in profile_after.unlocked_endings
        assert profile_after.total_escapes >= 1


@pytest.mark.anyio
async def test_ending_screen_renders_ascii_art():
    """AC-12: EndingScreen renders the dedicated ASCII art widget conforming to §7.3."""
    app = EndingApp(ending_id="stay")
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingScreen)

        ascii_widget = screen.query_one("#ending-ascii", Static)
        expected_art = get_ending_ascii("stay")
        assert str(ascii_widget.content) == expected_art


@pytest.mark.anyio
async def test_gallery_option_navigation():
    """AC-3, Task B04: Navigating to VIEW GALLERY and pressing Enter pushes EndingsGalleryScreen."""
    app = EndingApp(ending_id="the_quiet_exit")
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingScreen)
        assert "VIEW GALLERY" in screen.options

        # Options are: AGAIN (0), BACK TO MENU (1), VIEW GALLERY (2)
        # Navigate to VIEW GALLERY
        await pilot.press("down")
        await pilot.press("down")
        assert screen.selected == 2
        assert screen.options[screen.selected] == "VIEW GALLERY"

        # Press Enter to open gallery
        await pilot.press("enter")
        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingsGalleryScreen)


@pytest.mark.anyio
async def test_ending_screen_adaptive_marker_and_escape_tally():
    """Stay and The Long Walk do not increment escapes, but Stay unlocks and displays [ THE CHOICE ]."""
    # 1. Stay
    app_stay = EndingApp(ending_id="stay")
    async with app_stay.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingScreen)
        marker_widget = screen.query_one("#ending-marker", Static)
        assert "THE CHOICE" in str(marker_widget.content)

        profile = load_profile()
        assert "stay" in profile.unlocked_endings
        assert profile.total_escapes == 0

    # 2. The Long Walk
    app_walk = EndingApp(ending_id="the_long_walk")
    async with app_walk.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingScreen)
        marker_widget = screen.query_one("#ending-marker", Static)
        assert "THE THRESHOLD" in str(marker_widget.content)

        profile = load_profile()
        assert "the_long_walk" in profile.unlocked_endings
        assert profile.total_escapes == 0
