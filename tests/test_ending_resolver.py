"""Tests for ending resolution engine (Task B02)."""

import pytest
from game.ending_resolver import (
    has_all_memory_fragments,
    resolve_escape_ending,
    resolve_terminal_event,
)
from game.state import RunState


def test_resolve_quiet_exit_by_default():
    """AC-7: Standard exit with normal oil and key yields the_quiet_exit."""
    state = RunState.fresh_run()
    state.add_item("front_door_key")
    state.lantern = 50
    assert resolve_escape_ending(state) == "the_quiet_exit"
    assert resolve_terminal_event(state, "door_escape") == "the_quiet_exit"


def test_resolve_what_the_book_knew():
    """AC-8: Escaping having read The Book yields what_the_book_knew."""
    state = RunState.fresh_run()
    state.set_flag("read_the_book")
    state.lantern = 40
    assert resolve_escape_ending(state) == "what_the_book_knew"

    # Also works via knows_dog_name from library completion
    state2 = RunState.fresh_run()
    state2.set_flag("knows_dog_name")
    state2.lantern = 40
    assert resolve_escape_ending(state2) == "what_the_book_knew"


def test_resolve_the_new_shadow_zero_oil():
    """AC-9: Escaping with 0 oil yields the_new_shadow."""
    state = RunState.fresh_run()
    state.lantern = 0
    # Even if book was read, zero oil takes precedence over book
    state.set_flag("read_the_book")
    assert resolve_escape_ending(state) == "the_new_shadow"


def test_resolve_meat_and_silence():
    """AC-6: Escaping after feeding dog meat (and not whistling) yields meat_and_silence."""
    state = RunState.fresh_run()
    state.set_flag("fed_dog_meat")
    state.lantern = 40
    assert resolve_escape_ending(state) == "meat_and_silence"

    # Also with content flag dog_pacified_meat
    state2 = RunState.fresh_run()
    state2.set_flag("dog_pacified_meat")
    state2.lantern = 40
    assert resolve_escape_ending(state2) == "meat_and_silence"

    # But if tamed with whistle instead, does not trigger meat_and_silence
    state2.set_flag("dog_whistled_away")
    assert resolve_escape_ending(state2) == "the_quiet_exit"


def test_resolve_homecoming_precedence():
    """AC-10: 3 memory fragments collected supersedes zero oil and book knowledge."""
    state = RunState.fresh_run()
    state.lantern = 0
    state.set_flag("read_the_book")
    state.set_flag("dog_pacified_meat")

    # Add 3 memory fragments
    state.add_item("memory_photograph")
    state.add_item("memory_child_drawing")
    state.add_item("memory_tomorrow_receipt")

    assert has_all_memory_fragments(state) is True
    assert resolve_escape_ending(state) == "homecoming"
    assert resolve_terminal_event(state, "door_escape") == "homecoming"

    # Also works with Slice C canonical items
    state_c = RunState.fresh_run()
    state_c.add_item("old_photograph")
    state_c.add_item("child_drawing")
    state_c.add_item("dated_receipt")
    assert has_all_memory_fragments(state_c) is True
    assert resolve_escape_ending(state_c) == "homecoming"


def test_resolve_stay_choice():
    """AC-11: Explicitly refusing exit triggers stay ending."""
    state = RunState.fresh_run()
    assert resolve_terminal_event(state, "refuse_exit") == "stay"
    assert resolve_terminal_event(state, "stay") == "stay"
    assert resolve_terminal_event(state, "ending_stay") == "stay"
    assert resolve_terminal_event(state, "hall_front_door_stay") == "stay"


def test_resolve_the_long_walk_early_hall_death():
    """AC-5: Death in first room within turn <= 3 resolves to the_long_walk."""
    state = RunState.fresh_run()
    state.current_room = "hall"
    state.turn_count = 1
    state.visited = {"hall"}

    assert resolve_terminal_event(state, "hall_death") == "the_long_walk"
    assert resolve_terminal_event(state, "death") == "the_long_walk"
    assert resolve_terminal_event(state, "ending_long_walk") == "the_long_walk"
    assert resolve_terminal_event(state, "hall_accept_dark") == "the_long_walk"


def test_resolve_death_outside_hall_or_later_is_not_long_walk():
    """Deaths in other rooms or after prolonged exploration are standard deaths."""
    # Later in run (> 3 turns)
    state = RunState.fresh_run()
    state.current_room = "hall"
    state.turn_count = 5
    state.visited = {"hall"}
    assert resolve_terminal_event(state, "hall_death") == "death"
    assert resolve_terminal_event(state, "death") == "death"

    # In another room
    state2 = RunState.fresh_run()
    state2.current_room = "blood_kitchen"
    state2.turn_count = 2
    state2.visited = {"hall", "blood_kitchen"}
    assert resolve_terminal_event(state2, "hall_death") == "death"
    assert resolve_terminal_event(state2, "death") == "death"

    # In another room on turn 1 even if visited set only has hall
    state3 = RunState.fresh_run()
    state3.current_room = "blood_kitchen"
    state3.turn_count = 1
    state3.visited = {"hall"}
    assert resolve_terminal_event(state3, "death") == "death"


def test_resolve_shadow_walk():
    """Terminal event for voluntary shadow walk resolves properly."""
    state = RunState.fresh_run()
    assert resolve_terminal_event(state, "shadow_walk") == "shadow_walk"
    assert resolve_terminal_event(state, "shadow_walk_ending") == "shadow_walk"
    assert resolve_terminal_event(state, "hall_surrender_shadow") == "shadow_walk"
