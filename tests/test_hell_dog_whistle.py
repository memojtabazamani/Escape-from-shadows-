"""Unit tests for the Silver Whistle and dog's delayed return (Task G03)."""

from pathlib import Path
import pytest
from game.content_schema import load_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_whistle_without_book_fails(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    unnamed_choice = next(c for c in kennel["choices"] if c["id"] == "dog_whistle_unnamed")
    named_choice = next(c for c in kennel["choices"] if c["id"] == "dog_whistle_named")

    state = RunState.fresh_run()
    state.add_item("silver_whistle")
    assert not state.has_flag("knows_dog_name")

    # Named choice refused
    res_named = resolve_choice(named_choice, state)
    assert res_named.refused is True
    assert "requires flag 'knows_dog_name'" in res_named.reason

    # Unnamed choice triggers setback
    init_comp = state.composure
    res_unnamed = resolve_choice(unnamed_choice, state)
    assert res_unnamed.refused is False
    assert state.composure == init_comp - 10
    assert not state.has_flag("dog_whistled_away")


def test_whistle_with_book_banishes_dog(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    named_choice = next(c for c in kennel["choices"] if c["id"] == "dog_whistle_named")

    state = RunState.fresh_run()
    state.add_item("silver_whistle")
    state.set_flag("knows_dog_name")

    res = resolve_choice(named_choice, state)
    assert res.refused is False
    assert res.destination == "old_yard"
    assert state.has_flag("dog_whistled_away")


def test_dog_reappears_at_front_door_if_whistled(content):
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    climax_choice = next(c for c in hall["choices"] if c["id"] == "hall_escape_dog_climax")

    # If dog was not whistled away, climax choice is refused
    state = RunState.fresh_run()
    state.set_flag("knows_exit")
    res = resolve_choice(climax_choice, state)
    assert res.refused is True
    assert "requires flag 'dog_whistled_away'" in res.reason

    # If dog WAS whistled away, climax choice yields escape with tension
    state.set_flag("dog_whistled_away")
    res = resolve_choice(climax_choice, state)
    assert res.refused is False
    assert res.destination == "front_door_escape"
    assert state.has_flag("escaped_dog_climax")
