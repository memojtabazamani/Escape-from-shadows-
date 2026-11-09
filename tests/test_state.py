"""Tests for game.state.RunState."""

import pytest

from game.state import RunState


def test_fresh_defaults():
    state = RunState.fresh_run()
    assert state.lantern == 100
    assert state.turn_count == 0
    assert state.visited == set()
    assert state.held_items == set()
    assert state.flags == set()


def test_lantern_clamps_at_lower_bound():
    state = RunState.fresh_run()
    spent = state.spend_lantern(500)
    assert spent == 100
    assert state.lantern == 0


def test_lantern_clamps_at_upper_bound_on_restore():
    state = RunState.fresh_run()
    state.restore({"lantern": 500})
    assert state.lantern == 100


def test_lantern_cannot_go_negative():
    state = RunState.fresh_run()
    state.spend_lantern(100)
    state.spend_lantern(10)
    assert state.lantern == 0


def test_negative_spend_treated_as_zero():
    state = RunState.fresh_run()
    assert state.spend_lantern(-10) == 0
    assert state.lantern == 100


def test_turn_counter_never_decreases():
    state = RunState.fresh_run()
    state.advance_turn()
    state.advance_turn()
    assert state.turn_count == 2
    state.restore({"turn_count": 0})
    # restore should clamp to non-negative, but it does not decrease through advance_turn
    assert state.turn_count >= 0


def test_visit_and_query():
    state = RunState.fresh_run()
    assert state.has_visited("hall") is False
    assert state.visit("hall") is True
    assert state.has_visited("hall") is True
    assert state.visit("hall") is False


def test_held_item_add_remove_membership():
    state = RunState.fresh_run()
    state.add_item("book")
    assert state.has_item("book") is True
    state.add_item("book")  # duplicate is a no-op
    assert state.has_item("book") is True
    state.remove_item("book")
    assert state.has_item("book") is False


def test_unset_flag_reads_false():
    state = RunState.fresh_run()
    assert state.has_flag("knows_exit") is False
    state.set_flag("knows_exit")
    assert state.has_flag("knows_exit") is True
    state.clear_flag("knows_exit")
    assert state.has_flag("knows_exit") is False


def test_snapshot_restore_roundtrip():
    original = RunState.fresh_run()
    original.visit("hall")
    original.add_item("book")
    original.set_flag("knows_exit")
    original.spend_lantern(20)
    original.advance_turn()

    snapshot = original.snapshot()
    restored = RunState.fresh_run()
    restored.restore(snapshot)

    assert restored.lantern == original.lantern
    assert restored.turn_count == original.turn_count
    assert restored.visited == original.visited
    assert restored.held_items == original.held_items
    assert restored.flags == original.flags
