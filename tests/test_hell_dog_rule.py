"""Unit tests for the Hell Dog freeze rule (Task G01).

Rule from SUGGEST.md §6: It only moves when you do. Standing still is safe and costs oil.
"""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_standing_still_costs_oil_and_composure_without_beast_attacking(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    freeze_choice = next(c for c in kennel["choices"] if c["id"] == "dog_freeze")

    state = RunState.fresh_run()
    init_oil = state.lantern
    init_comp = state.composure

    res = resolve_choice(freeze_choice, state)
    assert res.refused is False
    assert res.destination == "yard_doghouse_encounter"  # Stays safely in encounter
    assert state.lantern == init_oil - 1
    assert state.composure == init_comp - 1
    assert state.has_flag("knows_dog_freezes")


def test_freeze_choice_has_clear_observational_telegraph(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    freeze_choice = next(c for c in kennel["choices"] if c["id"] == "dog_freeze")
    telegraphs = freeze_choice.get("telegraphs", [])
    assert len(telegraphs) >= 1
    assert any("waiting for you to move" in t.lower() or "does not advance" in t.lower() for t in telegraphs)
