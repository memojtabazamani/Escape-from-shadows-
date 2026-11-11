"""Tests for difficulty hints on EASY (Task B04)."""

from game.hints import get_stuck_hint
from game.state import RunState


def test_hints_fire_on_easy_and_never_on_medium_or_hard():
    # Setup state that is stuck in hall (needs library)
    easy_run = RunState.fresh_run("EASY")
    easy_run.visit("hall")
    easy_run.consecutive_room_turns = 3

    med_run = RunState.fresh_run("MEDIUM")
    med_run.visit("hall")
    med_run.consecutive_room_turns = 3

    hard_run = RunState.fresh_run("HARD")
    hard_run.visit("hall")
    hard_run.consecutive_room_turns = 3

    # Easy gets a hint
    hint = get_stuck_hint(easy_run)
    assert hint is not None
    assert "tallow and cold ink" in hint

    # Medium and Hard never get a hint
    assert get_stuck_hint(med_run) is None
    assert get_stuck_hint(hard_run) is None


def test_a_hint_is_not_delivered_twice():
    run = RunState.fresh_run("EASY")
    run.visit("hall")
    run.consecutive_room_turns = 5

    first = get_stuck_hint(run)
    assert first is not None

    # Calling again in the same state produces None (already delivered)
    second = get_stuck_hint(run)
    assert second is None


def test_hints_only_reference_encountered_content():
    # In hall before visiting library, hint only mentions visible eastern archway
    run = RunState.fresh_run("EASY")
    run.visit("hall")
    run.consecutive_room_turns = 3

    hint = get_stuck_hint(run)
    assert hint is not None
    # Doesn't spoil room names like "the_threshold_of_night" or "blood_kitchen"
    assert "threshold" not in hint.lower()
    assert "kitchen" not in hint.lower()


def test_hint_does_not_fire_during_a_competent_run():
    # A competent run visits a room and moves on before consecutive turns reach threshold 3
    run = RunState.fresh_run("EASY")
    run.visit("hall")
    assert get_stuck_hint(run) is None

    run.advance_turn()
    assert run.consecutive_room_turns == 1
    assert get_stuck_hint(run) is None

    # Leaves to library
    run.visit("old_library")
    assert run.consecutive_room_turns == 0
    assert get_stuck_hint(run) is None


def test_delivered_hints_are_recorded_for_the_journal():
    run = RunState.fresh_run("EASY")
    run.visit("hall")
    run.consecutive_room_turns = 3

    hint = get_stuck_hint(run)
    assert hint is not None

    shadow_entries = run.journal.get_entries("SHADOW_WHISPER")
    assert len(shadow_entries) == 1
    assert shadow_entries[0].text == hint
    assert shadow_entries[0].detail == "hall"
