"""Tests for the composure model, drains, recovery, and clamping (Task D01)."""
from pathlib import Path
import pytest

from game.composure import (
    COMPOSURE_MIN,
    COMPOSURE_MAX,
    DISTORTION_THRESHOLD,
    spend_composure,
    restore_composure,
    is_distorted,
    is_zero_composure,
)
from game.content_schema import load_content, validate_content
from game.effects import apply_effects, check_requirements, resolve_choice
from game.state import RunState


def test_composure_clamps_at_both_ends():
    """Composure must clamp between 0 and 100 on direct construction, spend, and restore."""
    state = RunState(composure=150)
    assert state.composure == 100

    state2 = RunState(composure=-20)
    assert state2.composure == 0

    state3 = RunState.fresh_run()
    # Spend more than available
    spent = state3.spend_composure(150)
    assert spent == 100
    assert state3.composure == 0

    # Restore more than max
    restored = state3.restore_composure(200)
    assert restored == 100
    assert state3.composure == 100


def test_drain_returns_what_actually_happened():
    """House style contract: spend returns the delta actually deducted."""
    state = RunState(composure=30)

    # Spend 10
    actual = spend_composure(state, 10)
    assert actual == 10
    assert state.composure == 20

    # Spend 25 (only 20 left)
    actual2 = spend_composure(state, 25)
    assert actual2 == 20
    assert state.composure == 0

    # Negative spend is treated as 0
    actual_neg = spend_composure(state, -10)
    assert actual_neg == 0
    assert state.composure == 0


def test_recovery_follows_the_modeled_list():
    """Restore returns the delta actually restored and respects the ceiling."""
    state = RunState(composure=85)

    actual = restore_composure(state, 10)
    assert actual == 10
    assert state.composure == 95

    actual2 = restore_composure(state, 10)
    assert actual2 == 5
    assert state.composure == 100

    actual_neg = restore_composure(state, -10)
    assert actual_neg == 0
    assert state.composure == 100


def test_zero_composure_does_not_end_the_run():
    """AC-11: Zero composure does NOT kill the player and does not end the run."""
    state = RunState.fresh_run()
    state.spend_composure(100)
    assert state.composure == 0
    assert is_zero_composure(state) is True
    # Run is still alive and operable; turn advancement is not blocked
    state.advance_turn()
    assert state.turn_count == 1
    assert state.composure == 0


def test_start_value_honours_the_difficulty_parameter():
    """Generosity parameters from B02 set starting composure per difficulty."""
    easy_run = RunState.fresh_run("EASY")
    assert easy_run.composure == 100

    med_run = RunState.fresh_run("MEDIUM")
    assert med_run.composure == 100

    hard_run = RunState.fresh_run("HARD")
    assert hard_run.composure == 70


def test_snapshot_round_trips_composure():
    """Snapshot/restore must carry composure accurately."""
    state = RunState.fresh_run()
    state.spend_composure(35)
    assert state.composure == 65

    data = state.snapshot()
    assert data["composure"] == 65

    restored_state = RunState.fresh_run()
    restored_state.restore(data)
    assert restored_state.composure == 65


def test_pre_slice_snapshot_restores_with_a_default_composure():
    """Backward compatibility: legacy snapshot without 'composure' restores to default 100."""
    legacy_data = {
        "lantern": 80,
        "turn_count": 5,
        "current_room": "hall",
        "visited": ["hall"],
        "held_items": ["matchbox"],
        "flags": ["knows_exit"],
        "difficulty": "MEDIUM",
    }
    state = RunState.fresh_run()
    state.restore(legacy_data)
    assert state.composure == 100
    assert state.lantern == 80


def test_content_authored_composure_effects_work():
    """Composure drain and recovery verbs work via resolve_choice."""
    content_path = Path("data/content.json")
    content = load_content(content_path)
    assert validate_content(content) == []

    rooms_by_id = {r["id"]: r for r in content["rooms"]}
    state = RunState.fresh_run()
    assert state.composure == 100

    # hall_right drains 5 composure
    hall = rooms_by_id["hall"]
    to_library = next(c for c in hall["choices"] if c["id"] == "hall_right")
    res1 = resolve_choice(to_library, state)
    assert res1.refused is False
    assert state.composure == 95

    # library_read drains 15 composure
    library = rooms_by_id["old_library"]
    read_book = next(c for c in library["choices"] if c["id"] == "library_read")
    res2 = resolve_choice(read_book, state)
    assert res2.refused is False
    assert state.composure == 80

    # hall_take_matchbox restores 10 composure
    take_matchbox = next(c for c in hall["choices"] if c["id"] == "hall_take_matchbox")
    res3 = resolve_choice(take_matchbox, state)
    assert res3.refused is False
    assert state.composure == 90
