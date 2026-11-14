"""Unit tests for PlayerProfile meta-progression persistence (Task A01)."""

import json
from pathlib import Path
import pytest

from game.profile import (
    DEFAULT_PROFILE_PATH,
    PlayerProfile,
    delete_profile,
    get_profile_path,
    get_unlocked_endings,
    load_profile,
    record_death,
    record_escape,
    save_profile,
    unlock_ending,
)
from game.save import delete_saved_game, save_to_disk, has_saved_game
from game.state import RunState


def test_default_profile_when_file_absent(tmp_path: Path):
    """Loading without an existing file returns an empty default profile."""
    profile_path = tmp_path / "non_existent_profile.json"
    profile = load_profile(profile_path)

    assert isinstance(profile, PlayerProfile)
    assert profile.unlocked_endings == set()
    assert profile.total_escapes == 0
    assert profile.total_deaths == 0
    assert profile.is_ending_unlocked("the_quiet_exit") is False


def test_atomic_save_and_load_roundtrip(tmp_path: Path):
    """Saving and loading profile round-trips unlocked endings and stats."""
    profile_path = tmp_path / "subfolder" / "profile.json"
    profile = PlayerProfile(
        unlocked_endings={"the_quiet_exit", "meat_and_silence"},
        total_escapes=2,
        total_deaths=5,
    )

    saved = save_profile(profile, profile_path)
    assert saved is True
    assert profile_path.exists()

    loaded = load_profile(profile_path)
    assert loaded.unlocked_endings == {"the_quiet_exit", "meat_and_silence"}
    assert loaded.total_escapes == 2
    assert loaded.total_deaths == 5
    assert loaded.is_ending_unlocked("the_quiet_exit") is True
    assert loaded.is_ending_unlocked("what_the_book_knew") is False


def test_idempotent_unlock(tmp_path: Path):
    """Unlocking the same ending multiple times does not duplicate or corrupt."""
    profile_path = tmp_path / "profile.json"

    # First unlock
    res1 = unlock_ending("the_quiet_exit", profile_path)
    assert res1 is True
    unlocked = get_unlocked_endings(profile_path)
    assert unlocked == {"the_quiet_exit"}

    # Duplicate unlock
    res2 = unlock_ending("the_quiet_exit", profile_path)
    assert res2 is True
    unlocked = get_unlocked_endings(profile_path)
    assert unlocked == {"the_quiet_exit"}

    # Another ending
    unlock_ending("the_long_walk", profile_path)
    unlocked = get_unlocked_endings(profile_path)
    assert unlocked == {"the_quiet_exit", "the_long_walk"}


def test_corrupt_profile_fallback(tmp_path: Path):
    """Malformed or invalid JSON recovers safely to a clean default profile."""
    profile_path = tmp_path / "corrupt_profile.json"

    # Corrupt JSON syntax
    profile_path.write_text("{not valid json syntax", encoding="utf-8")
    loaded = load_profile(profile_path)
    assert isinstance(loaded, PlayerProfile)
    assert loaded.unlocked_endings == set()

    # Empty file
    profile_path.write_text("", encoding="utf-8")
    loaded_empty = load_profile(profile_path)
    assert loaded_empty.unlocked_endings == set()

    # Non-dict JSON
    profile_path.write_text('["list", "instead", "of", "dict"]', encoding="utf-8")
    loaded_list = load_profile(profile_path)
    assert loaded_list.unlocked_endings == set()


def test_record_escape_and_death(tmp_path: Path):
    """Tallies for escapes and deaths increment correctly."""
    profile_path = tmp_path / "stats_profile.json"

    record_escape(profile_path)
    record_escape(profile_path)
    record_death(profile_path)

    loaded = load_profile(profile_path)
    assert loaded.total_escapes == 2
    assert loaded.total_deaths == 1


def test_profile_isolated_from_save_file(tmp_path: Path):
    """Deleting run savegame does not delete or affect meta profile."""
    save_path = tmp_path / "savegame.json"
    profile_path = tmp_path / "profile.json"

    state = RunState.fresh_run()
    save_to_disk(state, path=save_path)
    assert has_saved_game(path=save_path) is True

    unlock_ending("what_the_book_knew", path=profile_path)
    assert "what_the_book_knew" in get_unlocked_endings(path=profile_path)

    # Delete run save
    delete_saved_game(path=save_path)
    assert has_saved_game(path=save_path) is False

    # Profile must remain intact
    assert "what_the_book_knew" in get_unlocked_endings(path=profile_path)


def test_delete_profile(tmp_path: Path):
    """Deleting profile file cleanly removes it."""
    profile_path = tmp_path / "to_delete.json"
    save_profile(PlayerProfile(), profile_path)
    assert profile_path.exists() is True

    deleted = delete_profile(profile_path)
    assert deleted is True
    assert profile_path.exists() is False

    # Deleting non-existent file returns False
    assert delete_profile(profile_path) is False


def test_unlock_ending_rejects_empty_or_invalid_id(tmp_path: Path):
    """Calling unlock_ending with empty or non-string ID safely returns False."""
    profile_path = tmp_path / "edge_profile.json"
    assert unlock_ending("", profile_path) is False
    assert unlock_ending("   ", profile_path) is False
    assert unlock_ending(None, profile_path) is False  # type: ignore[arg-type]
    assert get_unlocked_endings(profile_path) == set()


def test_from_dict_cleans_entries_and_clamps_negative_stats():
    """Deserializing profile cleans invalid/blank IDs and clamps negative numbers."""
    raw = {
        "unlocked_endings": ["the_quiet_exit", "", "   ", 123, None, "meat_and_silence"],
        "total_escapes": -5,
        "total_deaths": -12,
    }
    profile = PlayerProfile.from_dict(raw)
    assert profile.unlocked_endings == {"the_quiet_exit", "meat_and_silence"}
    assert profile.total_escapes == 0
    assert profile.total_deaths == 0


def test_get_profile_path_fallback():
    """Empty or None path argument falls back to DEFAULT_PROFILE_PATH."""
    assert get_profile_path(None) == DEFAULT_PROFILE_PATH
    assert get_profile_path("") == DEFAULT_PROFILE_PATH
    assert get_profile_path(Path("custom.json")) == Path("custom.json")
