"""Unit tests for Old Library multi-turn Book reading rework (Task F03)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_library_content_valid(content):
    problems = validate_content(content)
    assert problems == [], f"Validation problems: {[str(p) for p in problems]}"


def test_book_reading_requires_three_turns_and_grants_knowledge_flag(content):
    lib = next(r for r in content["rooms"] if r["id"] == "old_library")
    start_choice = next(c for c in lib["choices"] if c["id"] == "library_study_multiturn")
    cont_choice = next(c for c in lib["choices"] if c["id"] == "library_continue_reading")

    state = RunState.fresh_run()
    initial_oil = state.lantern

    # 1. Start multi-turn reading
    res = resolve_choice(start_choice, state)
    assert res.refused is False
    assert state.has_active_multiturn("read_book")
    assert state.active_action.current_step == 0
    assert not state.has_flag("knows_dog_name")

    # 2. Advance step 1
    res = resolve_choice(cont_choice, state)
    assert res.refused is False
    assert state.lantern == initial_oil - 1
    assert state.active_action.current_step == 1
    assert not state.has_flag("knows_dog_name")

    # 3. Advance step 2
    res = resolve_choice(cont_choice, state)
    assert res.refused is False
    assert state.lantern == initial_oil - 2
    assert state.active_action.current_step == 2
    assert not state.has_flag("knows_dog_name")

    # 4. Advance step 3 (completion)
    res = resolve_choice(cont_choice, state)
    assert res.refused is False
    assert state.active_action is None
    assert state.has_flag("knows_dog_name")
    assert state.has_flag("library_door_ajar")
    assert state.has_item("front_door_key")


def test_book_reading_abort(content):
    lib = next(r for r in content["rooms"] if r["id"] == "old_library")
    start_choice = next(c for c in lib["choices"] if c["id"] == "library_study_multiturn")
    cont_choice = next(c for c in lib["choices"] if c["id"] == "library_continue_reading")
    abort_choice = next(c for c in lib["choices"] if c["id"] == "library_interrupt_reading")

    state = RunState.fresh_run()
    resolve_choice(start_choice, state)
    resolve_choice(cont_choice, state)
    assert state.active_action.current_step == 1

    initial_composure = state.composure
    res = resolve_choice(abort_choice, state)
    assert res.refused is False
    assert state.active_action is None
    assert not state.has_flag("knows_dog_name")
    # Cancel penalty applied
    assert state.composure == initial_composure - 3


def test_library_take_book(content):
    lib = next(r for r in content["rooms"] if r["id"] == "old_library")
    book_choice = next(c for c in lib["choices"] if c["id"] == "library_search_alcove")

    state = RunState.fresh_run()
    res = resolve_choice(book_choice, state)
    assert res.refused is False
    assert state.has_item("the_book")
