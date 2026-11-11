"""Unit tests for The Hall hub and connections (Task F05)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_the_hall_links_all_rooms(content):
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    destinations = {c["destination"] for c in hall["choices"]}

    assert "blood_kitchen" in destinations
    assert "old_library" in destinations
    assert "old_yard" in destinations
    assert "front_door_escape" in destinations


def test_matchbox_obtainable(content):
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    matchbox_choice = next(c for c in hall["choices"] if c["id"] == "hall_take_matchbox")

    state = RunState.fresh_run()
    res = resolve_choice(matchbox_choice, state)
    assert res.refused is False
    assert state.has_item("matchbox")


def test_the_hall_prose_budget(content):
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    lines = hall["prose"].split("\n")
    assert len(lines) <= 20
    assert len(lines) >= 3


def test_front_door_progression(content):
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    door_choice = next(c for c in hall["choices"] if c["id"] == "hall_front_door")

    # Without prerequisite: refused
    state = RunState.fresh_run()
    res = resolve_choice(door_choice, state)
    assert res.refused is True

    # With prerequisite: yields to escape
    state.set_flag("knows_exit")
    res = resolve_choice(door_choice, state)
    assert res.refused is False
    assert res.destination == "front_door_escape"
