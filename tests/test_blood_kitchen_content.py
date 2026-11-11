"""Unit tests for Blood Kitchen room content (Task F02)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_blood_kitchen_schema_valid(content):
    problems = validate_content(content)
    assert problems == [], f"Validation problems: {[str(p) for p in problems]}"


def test_blood_kitchen_entry_costs_composure(content):
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    kitchen_choice = next(c for c in hall["choices"] if c["destination"] == "blood_kitchen")
    assert kitchen_choice["tier"] == "scar"

    state = RunState.fresh_run()
    initial_composure = state.composure
    result = resolve_choice(kitchen_choice, state)

    assert result.refused is False
    assert result.destination == "blood_kitchen"
    assert state.composure < initial_composure
    assert state.composure == initial_composure - 2


def test_blood_kitchen_items_obtainable(content):
    kitchen = next(r for r in content["rooms"] if r["id"] == "blood_kitchen")

    cleaver_choice = next(c for c in kitchen["choices"] if c["id"] == "kitchen_take_cleaver")
    meat_choice = next(c for c in kitchen["choices"] if c["id"] == "kitchen_take_meat")
    oil_choice = next(c for c in kitchen["choices"] if c["id"] == "kitchen_take_oil")

    # Take cleaver (costs composure)
    state = RunState.fresh_run()
    res = resolve_choice(cleaver_choice, state)
    assert res.refused is False
    assert state.has_item("rusty_cleaver")
    assert state.composure == 92

    # Take meat (sets flag)
    res = resolve_choice(meat_choice, state)
    assert res.refused is False
    assert state.has_flag("has_meat")

    # Refill oil from canister (restores oil to max, costs composure)
    state.lantern = 30
    res = resolve_choice(oil_choice, state)
    assert res.refused is False
    assert state.lantern == 100
    assert state.has_flag("kitchen_oil_claimed")
    assert state.composure == 87


def test_blood_kitchen_prose_budget(content):
    kitchen = next(r for r in content["rooms"] if r["id"] == "blood_kitchen")
    lines = kitchen["prose"].split("\n")
    assert len(lines) <= 20
    assert len(lines) >= 3


def test_blood_kitchen_safe_retreat_to_hall(content):
    kitchen = next(r for r in content["rooms"] if r["id"] == "blood_kitchen")
    return_choice = next(c for c in kitchen["choices"] if c["id"] == "kitchen_return")
    assert return_choice["destination"] == "hall"
