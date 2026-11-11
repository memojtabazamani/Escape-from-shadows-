"""Unit tests for the four distinct Hell Dog solutions (Task G02).

Four solutions from SUGGEST.md §4.3:
1. Move slowly (costs oil & composure, clean passage).
2. Move quickly (sprint, tests composure, bypasses noise).
3. Throw meat (pacifies dog).
4. Whistle (requires book, sets dog_whistled_away).
"""

from pathlib import Path
import pytest
from game.content_schema import load_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_solution_slow_costs_oil_and_composure(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    slow_choice = next(c for c in kennel["choices"] if c["id"] == "dog_slow")

    state = RunState.fresh_run()
    init_oil = state.lantern
    init_comp = state.composure

    res = resolve_choice(slow_choice, state)
    assert res.refused is False
    assert res.destination == "old_yard"
    assert state.lantern == init_oil - 3
    assert state.composure == init_comp - 2
    assert state.has_flag("dog_bypassed_slowly")


def test_solution_sprint_requires_high_composure(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    sprint_choice = next(c for c in kennel["choices"] if c["id"] == "dog_sprint")

    # High composure: passes
    state = RunState.fresh_run()
    state.composure = 60
    res = resolve_choice(sprint_choice, state)
    assert res.refused is False
    assert res.destination == "old_yard"
    assert state.composure == 45
    assert state.has_flag("dog_bypassed_sprint")

    # Low composure: refused
    low_state = RunState.fresh_run()
    low_state.composure = 15
    res = resolve_choice(sprint_choice, low_state)
    assert res.refused is True
    assert "composure above 20" in res.reason


def test_solution_meat_pacifies_dog(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    meat_choice = next(c for c in kennel["choices"] if c["id"] == "dog_feed_meat")

    # Without meat flag: refused
    state = RunState.fresh_run()
    res = resolve_choice(meat_choice, state)
    assert res.refused is True
    assert "requires flag 'has_meat'" in res.reason

    # With meat flag: pacified
    state.set_flag("has_meat")
    res = resolve_choice(meat_choice, state)
    assert res.refused is False
    assert res.destination == "old_yard"
    assert state.has_flag("dog_pacified_meat")


def test_solutions_are_mutually_distinct(content):
    """Guards against RISK-9: All four solutions have distinct flag and consequence profiles."""
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    choices = {c["id"]: c for c in kennel["choices"]}

    slow_effects = {e.get("verb"): e for e in choices["dog_slow"]["effects"]}
    sprint_effects = {e.get("verb"): e for e in choices["dog_sprint"]["effects"]}
    meat_effects = {e.get("verb"): e for e in choices["dog_feed_meat"]["effects"]}
    whistle_effects = {e.get("verb"): e for e in choices["dog_whistle_named"]["effects"]}

    # Mutual distinctness checks
    assert slow_effects.keys() != sprint_effects.keys()
    assert slow_effects.keys() != meat_effects.keys()
    assert sprint_effects.keys() != meat_effects.keys()
    assert whistle_effects.keys() != slow_effects.keys()
