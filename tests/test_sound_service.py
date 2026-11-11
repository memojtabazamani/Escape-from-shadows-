"""Unit tests for the terminal system bell horror sound service (Task H01)."""

import pytest
from game.sound import (
    play_cue,
    is_sound_enabled,
    CUE_DOOR_OPEN,
    CUE_DOG_CHAIN,
    CUE_SHADOW_WHISPER,
)


class DummyConfigApp:
    def __init__(self, sound=True):
        self.config = {"sound": sound}
        self.bell_count = 0

    def bell(self):
        self.bell_count += 1


def test_bell_emitted_when_sound_enabled():
    app = DummyConfigApp(sound=True)
    assert is_sound_enabled(app) is True

    played = play_cue(app, CUE_DOOR_OPEN)
    assert played is True
    assert app.bell_count == 1

    played = play_cue(app, CUE_DOG_CHAIN)
    assert played is True
    assert app.bell_count == 2

    played = play_cue(app, CUE_SHADOW_WHISPER)
    assert played is True
    assert app.bell_count == 3


def test_bell_suppressed_when_sound_disabled():
    app = DummyConfigApp(sound=False)
    assert is_sound_enabled(app) is False

    played = play_cue(app, CUE_DOOR_OPEN)
    assert played is False
    assert app.bell_count == 0


def test_invalid_cue_raises_value_error():
    app = DummyConfigApp(sound=True)
    with pytest.raises(ValueError, match="Unknown sound cue"):
        play_cue(app, "unknown_random_cue")


def test_sound_fails_gracefully_in_headless_env():
    # An app without bell method or None app
    app = None
    assert is_sound_enabled(app) is False
    assert play_cue(app, CUE_DOOR_OPEN) is False
