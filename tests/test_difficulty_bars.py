"""Tests for difficulty bar generosity (Task B02)."""

from game.difficulty import get_difficulty_config
from game.lantern import (
    FIRST_VISIT_DRAIN,
    REVISIT_DRAIN,
    CAREFUL_ACTION_DRAIN,
    drain_for_room,
    drain_for_action,
)
from game.state import RunState


def test_easy_medium_hard_are_monotonic_on_both_bars():
    easy = get_difficulty_config("EASY")
    medium = get_difficulty_config("MEDIUM")
    hard = get_difficulty_config("HARD")

    # Monotonic: EASY >= MEDIUM >= HARD
    assert easy.initial_lantern >= medium.initial_lantern >= hard.initial_lantern
    assert easy.initial_composure >= medium.initial_composure >= hard.initial_composure


def test_medium_matches_the_shipped_defaults():
    medium = get_difficulty_config("MEDIUM")
    assert medium.initial_lantern == 100
    assert medium.initial_composure == 100

    run = RunState.fresh_run("MEDIUM")
    assert run.lantern == 100


def test_generosity_is_applied_at_run_start_only():
    easy_run = RunState.fresh_run("EASY")
    med_run = RunState.fresh_run("MEDIUM")
    hard_run = RunState.fresh_run("HARD")

    # Initial lantern reflects initial generosity
    assert easy_run.lantern == 100
    assert med_run.lantern == 100
    assert hard_run.lantern == 70

    # Per-step drain does not change with difficulty
    assert drain_for_room(easy_run, "room1") == FIRST_VISIT_DRAIN
    assert drain_for_room(med_run, "room1") == FIRST_VISIT_DRAIN
    assert drain_for_room(hard_run, "room1") == FIRST_VISIT_DRAIN

    assert drain_for_action("careful") == CAREFUL_ACTION_DRAIN


def test_zero_oil_consequence_is_reachable_on_every_difficulty():
    for diff in ["EASY", "MEDIUM", "HARD"]:
        run = RunState.fresh_run(diff)
        assert run.has_light()
        run.spend_lantern(200)
        assert run.lantern == 0
        assert not run.has_light()


def test_generosity_does_not_change_requirement_satisfiability():
    # In Phase 1 / Phase 2, reading the heavy tome costs 25.
    # On HARD (starting 70), after hall visit (0) and library first visit (10),
    # oil is 60, which comfortably satisfies the 25 oil requirement.
    hard_run = RunState.fresh_run("HARD")
    oil_spent = hard_run.spend_lantern(FIRST_VISIT_DRAIN)
    assert oil_spent == 10
    assert hard_run.lantern >= 25
