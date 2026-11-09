"""Tests for game.effects resolver."""

import pytest

from game.effects import apply_effects, check_requirements, resolve_choice
from game.state import RunState


# -----------------------------------------------------------------------------
# Requirement predicates
# ------------------------------------------------------------------------------

def test_has_flag_requirement():
    state = RunState.fresh_run()
    state.set_flag("knows_exit")
    result = check_requirements([{"predicate": "has_flag", "flag": "knows_exit"}], state)
    assert result.satisfied is True
    result = check_requirements([{"predicate": "has_flag", "flag": "missing"}], state)
    assert result.satisfied is False


def test_has_item_requirement():
    state = RunState.fresh_run()
    state.add_item("book")
    result = check_requirements([{"predicate": "has_item", "item": "book"}], state)
    assert result.satisfied is True
    result = check_requirements([{"predicate": "has_item", "item": "lantern"}], state)
    assert result.satisfied is False


def test_lantern_above_requirement():
    state = RunState.fresh_run()
    state.spend_lantern(50)
    result = check_requirements([{"predicate": "lantern_above", "amount": 20}], state)
    assert result.satisfied is True
    result = check_requirements([{"predicate": "lantern_above", "amount": 80}], state)
    assert result.satisfied is False


def test_requirement_evaluation_has_no_side_effects():
    state = RunState.fresh_run()
    state.spend_lantern(20)
    state.advance_turn()
    before = state.snapshot()
    check_requirements([{"predicate": "has_flag", "flag": "missing"}], state)
    assert state.snapshot() == before


# -----------------------------------------------------------------------------
# Effect application
# ------------------------------------------------------------------------------

def test_apply_effects_changes_expected_fields():
    state = RunState.fresh_run()
    result = apply_effects(
        [
            {"verb": "spend_oil", "amount": 30},
            {"verb": "set_flag", "flag": "knows_exit"},
            {"verb": "grant_item", "item": "book"},
        ],
        state,
    )
    assert result.success is True
    assert state.lantern == 70
    assert state.has_flag("knows_exit") is True
    assert state.has_item("book") is True


def test_apply_effects_is_all_or_nothing():
    state = RunState.fresh_run()
    before = state.snapshot()
    result = apply_effects(
        [
            {"verb": "spend_oil", "amount": 10},
            {"verb": "unknown_verb"},
        ],
        state,
    )
    assert result.success is False
    assert state.snapshot() == before


def test_unknown_verb_fails_loudly():
    state = RunState.fresh_run()
    result = apply_effects([{"verb": "unknown_verb"}], state)
    assert result.success is False
    assert "unknown effect verb" in result.reason


def test_unknown_predicate_fails_loudly():
    state = RunState.fresh_run()
    with pytest.raises(ValueError, match="unknown requirement predicate"):
        check_requirements([{"predicate": "unknown_predicate"}], state)


# -----------------------------------------------------------------------------
# Choice resolution
# ------------------------------------------------------------------------------

def test_tier_reporting():
    state = RunState.fresh_run()
    scar = resolve_choice({"destination": "x", "tier": "scar", "effects": []}, state)
    assert scar.tier == "scar"

    death = resolve_choice({"destination": "x", "tier": "death", "effects": []}, state)
    assert death.tier == "death"


def test_refused_choice_changes_nothing():
    state = RunState.fresh_run()
    before = state.snapshot()
    choice = {
        "destination": "x",
        "tier": "scar",
        "requirements": [{"predicate": "has_flag", "flag": "missing"}],
        "effects": [{"verb": "spend_oil", "amount": 50}],
    }
    result = resolve_choice(choice, state)
    assert result.refused is True
    assert result.reason == "requires flag 'missing'"
    assert state.snapshot() == before
