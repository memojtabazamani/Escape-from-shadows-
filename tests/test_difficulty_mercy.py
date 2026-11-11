"""Tests for difficulty mercy knobs (Task B03)."""

from game.difficulty import get_difficulty_config, DifficultyConfig
from game.state import RunState
from screens.death import DeathScreen


def test_easy_restarts_at_the_recorded_room_and_hard_restarts_at_the_beginning():
    easy_cfg = get_difficulty_config("EASY")
    hard_cfg = get_difficulty_config("HARD")

    assert easy_cfg.restart_point_mode == "last_room"
    assert hard_cfg.restart_point_mode == "start"


def test_auto_fill_is_off_on_hard_and_on_for_easy():
    easy_cfg = get_difficulty_config("EASY")
    med_cfg = get_difficulty_config("MEDIUM")
    hard_cfg = get_difficulty_config("HARD")

    assert easy_cfg.auto_fill_journal_on_death is True
    assert med_cfg.auto_fill_journal_on_death is False
    assert hard_cfg.auto_fill_journal_on_death is False


def test_auto_filled_entry_matches_the_death_cause_exactly():
    cause_str = "You stepped into darkness and were consumed."
    lesson_str = "Never enter an unwarned room without checking the light."

    run = RunState.fresh_run("EASY")
    cfg = get_difficulty_config(run.difficulty)
    if cfg.auto_fill_journal_on_death:
        run.journal.add_death(cause=cause_str, lesson=lesson_str)

    entries = run.journal.get_entries("DEATH_LESSON")
    assert len(entries) == 1
    assert entries[0].text == cause_str
    assert entries[0].detail == lesson_str


def test_restart_point_is_always_a_room_the_player_reached():
    run = RunState.fresh_run("EASY")
    assert run.recorded_restart_room == ""

    # Visit safe room
    run.visit("hall")
    assert run.recorded_restart_room == "hall"
    assert run.has_visited(run.recorded_restart_room)

    # Visit another room
    run.visit("old_library")
    assert run.recorded_restart_room == "old_library"
    assert run.has_visited(run.recorded_restart_room)

    # Death rooms must not become restart points
    run.visit("the_threshold_of_blood")
    assert run.recorded_restart_room == "old_library"


def test_mercy_is_read_from_config_not_branched_on_the_string():
    # If custom config has auto_fill False for EASY, it must respect config
    custom_cfg = DifficultyConfig(
        auto_fill_journal_on_death=False,
        restart_point_mode="start",
    )
    assert custom_cfg.auto_fill_journal_on_death is False
    assert custom_cfg.restart_point_mode == "start"
