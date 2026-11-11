"""Unit tests for Old Yard content (Task F04)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_old_yard_schema_valid(content):
    problems = validate_content(content)
    assert problems == [], f"Validation problems: {[str(p) for p in problems]}"


def test_silver_whistle_obtainable(content):
    yard = next(r for r in content["rooms"] if r["id"] == "old_yard")
    whistle_choice = next(c for c in yard["choices"] if c["id"] == "yard_take_whistle")

    state = RunState.fresh_run()
    res = resolve_choice(whistle_choice, state)
    assert res.refused is False
    assert state.has_item("silver_whistle")


def test_wall_cannot_be_climbed(content):
    yard = next(r for r in content["rooms"] if r["id"] == "old_yard")
    wall_choice = next(c for c in yard["choices"] if c["id"] == "yard_inspect_wall")

    state = RunState.fresh_run()
    init_composure = state.composure
    init_oil = state.lantern
    res = resolve_choice(wall_choice, state)

    assert res.refused is False
    assert res.destination == "old_yard"  # Never escapes
    assert state.composure == init_composure - 5
    assert state.lantern == init_oil - 2


def test_old_yard_prose_budget(content):
    yard = next(r for r in content["rooms"] if r["id"] == "old_yard")
    lines = yard["prose"].split("\n")
    assert len(lines) <= 20
    assert len(lines) >= 3


def test_approach_doghouse_telegraphs_beast(content):
    yard = next(r for r in content["rooms"] if r["id"] == "old_yard")
    dog_choice = next(c for c in yard["choices"] if c["id"] == "yard_approach_doghouse")
    assert dog_choice["destination"] == "yard_doghouse_encounter"
    assert len(dog_choice.get("telegraphs", [])) >= 1
