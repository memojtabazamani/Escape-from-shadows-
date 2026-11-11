"""Tests for game/difficulty.py (Task B01)."""

from game.difficulty import DifficultyConfig, get_difficulty_config


def test_each_difficulty_produces_a_distinct_config():
    easy = get_difficulty_config("EASY")
    medium = get_difficulty_config("MEDIUM")
    hard = get_difficulty_config("HARD")

    assert easy != medium
    assert medium != hard
    assert easy != hard


def test_unknown_difficulty_falls_back_to_medium():
    medium = get_difficulty_config("MEDIUM")
    assert get_difficulty_config(None) == medium
    assert get_difficulty_config("") == medium
    assert get_difficulty_config("NIGHTMARE") == medium
    assert get_difficulty_config(123) == medium  # type: ignore[arg-type]


def test_medium_reproduces_the_pre_slice_defaults():
    cfg = get_difficulty_config("MEDIUM")
    assert cfg.initial_lantern == 100
    assert cfg.initial_composure == 100
    assert cfg.hints_enabled is False
    assert cfg.choice_expiry_enabled is False
    assert cfg.auto_fill_journal_on_death is False
    assert cfg.restart_point_mode == "start"


def test_config_carries_no_content_identifiers():
    forbidden_ids = {
        "hall",
        "old_library",
        "blood_kitchen",
        "old_yard",
        "the_threshold_of_blood",
        "the_threshold_of_night",
        "tome_heavy",
        "key",
        "cleaver",
        "matches",
        "meat",
    }
    for diff in ["EASY", "MEDIUM", "HARD"]:
        cfg = get_difficulty_config(diff)
        for field_name in cfg.__dataclass_fields__:
            val = getattr(cfg, field_name)
            assert str(val).lower() not in forbidden_ids
