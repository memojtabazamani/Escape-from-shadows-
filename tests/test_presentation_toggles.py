"""Unit and integration tests for presentation toggles (Sound & Music) (Task H04).

Verifies AC-18, AC-19, AC-24: No setting lies; toggles produce observable differences.
"""

import pytest
from textual.app import App
from textual.widgets import Static
from game.sound import play_cue, CUE_DOOR_OPEN
from screens.game import GameScreen


class ToggleTestApp(App):
    def __init__(self, sound=True, music=True):
        super().__init__()
        self.config = {"sound": sound, "music": music}
        self.bell_rings = 0

    def bell(self):
        self.bell_rings += 1

    async def on_mount(self) -> None:
        await self.push_screen(GameScreen())


def test_sound_toggle_controls_bell_emission():
    # Sound ON
    app_on = ToggleTestApp(sound=True)
    res = play_cue(app_on, CUE_DOOR_OPEN)
    assert res is True
    assert app_on.bell_rings == 1

    # Sound OFF
    app_off = ToggleTestApp(sound=False)
    res = play_cue(app_off, CUE_DOOR_OPEN)
    assert res is False
    assert app_off.bell_rings == 0


@pytest.mark.anyio
async def test_music_toggle_controls_visual_rhythm():
    # Music ON
    app_on = ToggleTestApp(music=True)
    async with app_on.run_test() as pilot:
        screen_on = pilot.app.screen
        assert screen_on.is_music_enabled() is True
        assert screen_on._pulse_timer is not None

    # Music OFF
    app_off = ToggleTestApp(music=False)
    async with app_off.run_test() as pilot:
        screen_off = pilot.app.screen
        assert screen_off.is_music_enabled() is False
        assert screen_off._pulse_timer is None
        assert screen_off._typewriter_timer is None
