"""Unit tests for lantern refills and trade mechanics (Task F07)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_oil_canister_refills_lantern(content):
    kitchen = next(r for r in content["rooms"] if r["id"] == "blood_kitchen")
    take_oil_choice = next(c for c in kitchen["choices"] if c["id"] == "kitchen_take_oil")

    state = RunState.fresh_run()
    state.lantern = 30  # Low oil
    init_composure = state.composure

    # Refill lantern directly from the canister
    res = resolve_choice(take_oil_choice, state)
    assert res.refused is False
    assert state.lantern == 100  # Clamped to max
    assert state.composure == init_composure - 5
    assert state.has_flag("kitchen_oil_claimed")


def test_kitchen_oil_trade_requires_composure(content):
    kitchen = next(r for r in content["rooms"] if r["id"] == "blood_kitchen")
    take_oil_choice = next(c for c in kitchen["choices"] if c["id"] == "kitchen_take_oil")

    state = RunState.fresh_run()
    state.composure = 2  # Not enough composure

    res = resolve_choice(take_oil_choice, state)
    assert res.refused is True
    assert "composure above 5" in res.reason


def test_matchbox_restores_composure_and_grants_item(content):
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    matchbox_choice = next(c for c in hall["choices"] if c["id"] == "hall_take_matchbox")

    state = RunState.fresh_run()
    state.composure = 70
    res = resolve_choice(matchbox_choice, state)
    assert res.refused is False
    assert state.has_item("matchbox")
    assert state.composure == 80
