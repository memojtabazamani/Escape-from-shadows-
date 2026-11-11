"""Unit tests for visual rhythm, typewriter text, and pulse effect (Task H02)."""

import pytest
from textual.app import App
from screens.game import GameScreen


class VisualRhythmApp(App):
    def __init__(self, music=True):
        super().__init__()
        self.config = {"music": music}

    async def on_mount(self) -> None:
        await self.push_screen(GameScreen())


@pytest.mark.anyio
async def test_typewriter_active_when_music_enabled():
    app = VisualRhythmApp(music=True)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        assert screen.is_music_enabled() is True
        # Typewriter or pulse timer is active
        assert screen._pulse_timer is not None


@pytest.mark.anyio
async def test_typewriter_skip_on_keypress():
    app = VisualRhythmApp(music=True)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Pressing any key finishes the typewriter instantly
        await pilot.press("space")
        assert screen._typewriter_timer is None


@pytest.mark.anyio
async def test_timer_cleanup_on_unmount():
    app = VisualRhythmApp(music=True)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        screen.on_unmount()
        assert screen._typewriter_timer is None
        assert screen._pulse_timer is None
