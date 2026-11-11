"""Unit tests for the three front door key routes and two telegraphed traps (Task F06)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_genuine_key_opens_front_door(content):
    # Route 1: Genuine key from Library secret drawer
    lib = next(r for r in content["rooms"] if r["id"] == "old_library")
    key_choice = next(c for c in lib["choices"] if c["id"] == "library_take_genuine_key")

    state = RunState.fresh_run()
    res = resolve_choice(key_choice, state)
    assert res.refused is False
    assert state.has_item("front_door_key")


def test_kitchen_trap_route_telegraphed(content):
    # Route 2: Kitchen basin trap
    kitchen = next(r for r in content["rooms"] if r["id"] == "blood_kitchen")
    trap_choice = next(c for c in kitchen["choices"] if c["id"] == "kitchen_take_basin_key")

    assert trap_choice["tier"] == "death"
    telegraphs = trap_choice.get("telegraphs", [])
    assert len(telegraphs) >= 2
    assert any("steam" in t or "warmth" in t for t in telegraphs)
    assert any("pulse" in t or "spring" in t for t in telegraphs)

    death_room = next(r for r in content["rooms"] if r["id"] == "kitchen_trap_death")
    assert death_room["tier"] == "death"
    cause = trap_choice.get("cause") or death_room.get("cause")
    assert "barbed iron" in cause.lower() or "wrist" in cause.lower()


def test_clock_trap_route_telegraphed(content):
    # Route 3: Hall grandfather clock trap
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    clock_choice = next(c for c in hall["choices"] if c["id"] == "hall_inspect_clock")

    assert clock_choice["tier"] == "death"
    telegraphs = clock_choice.get("telegraphs", [])
    assert len(telegraphs) >= 2
    assert any("pendulum" in t or "ticks" in t for t in telegraphs)
    assert any("brass" in t or "gear" in t for t in telegraphs)

    death_room = next(r for r in content["rooms"] if r["id"] == "clock_trap_death")
    assert death_room["tier"] == "death"
    cause = clock_choice.get("cause") or death_room.get("cause")
    assert "counterweight" in cause.lower() or "crushing" in cause.lower()
