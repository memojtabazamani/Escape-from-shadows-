"""Unit tests for instant text and reduce-motion accessibility mode (Task H03)."""

import pytest
from textual.app import App
from textual.widgets import Static
from screens.game import GameScreen


class MutedApp(App):
    def __init__(self):
        super().__init__()
        self.config = {"music": False, "sound": False}

    async def on_mount(self) -> None:
        await self.push_screen(GameScreen())


@pytest.mark.anyio
async def test_instant_text_when_music_disabled():
    app = MutedApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        assert screen.is_music_enabled() is False

        # Text is immediately and completely mounted on screen
        text_widget = screen.query_one("#scene-text", Static)
        assert len(str(text_widget.content)) > 10


@pytest.mark.anyio
async def test_no_timers_created_when_music_disabled():
    app = MutedApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        assert screen._typewriter_timer is None
        assert screen._pulse_timer is None
