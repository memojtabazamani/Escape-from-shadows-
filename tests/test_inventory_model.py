"""Tests for six-slot inventory in RunState (Task C01)."""

from game.effects import apply_effects, resolve_choice
from game.state import INVENTORY_CAP, RunState


def test_a_sixth_item_fits_and_a_seventh_is_refused():
    state = RunState.fresh_run()
    assert state.free_slots() == 6

    # Add 6 items
    for i in range(1, 7):
        assert state.can_add_item() is True
        assert state.add_item(f"item_{i}") is True
        assert state.free_slots() == 6 - i

    assert len(state.held_items) == 6
    assert state.can_add_item() is False
    assert state.free_slots() == 0

    # 7th item is refused
    assert state.add_item("item_7") is False
    assert len(state.held_items) == 6
    assert "item_7" not in state.held_items


def test_drop_frees_exactly_one_slot():
    state = RunState.fresh_run()
    for i in range(1, 7):
        state.add_item(f"item_{i}")

    assert state.free_slots() == 0
    assert state.drop_item("item_3") is True
    assert state.free_slots() == 1
    assert "item_3" not in state.held_items

    # Now a new item can fit
    assert state.add_item("new_item") is True
    assert state.free_slots() == 0
    assert state.has_item("new_item") is True


def test_restore_accepts_a_pre_slice_snapshot_and_reports_drops():
    # Legacy snapshot had a set of items, potentially more than 6 if corrupted
    legacy_data = {
        "lantern": 80,
        "turn_count": 5,
        "current_room": "hall",
        "visited": ["hall", "old_library"],
        "held_items": {"key", "cleaver", "meat", "matches", "book", "tome", "extra_item_7"},
        "flags": ["knows_exit"],
    }
    state = RunState.fresh_run()
    state.restore(legacy_data)

    assert state.lantern == 80
    assert len(state.held_items) == INVENTORY_CAP
    assert state.free_slots() == 0


def test_snapshot_round_trips_the_new_shape():
    original = RunState.fresh_run()
    original.add_item("matches")
    original.add_item("cleaver")
    original.add_item("meat")

    snapshot = original.snapshot()
    assert isinstance(snapshot["held_items"], list)
    assert snapshot["held_items"] == ["matches", "cleaver", "meat"]

    restored = RunState.fresh_run()
    restored.restore(snapshot)
    assert restored.held_items == ["matches", "cleaver", "meat"]
    assert restored.free_slots() == 3


def test_grant_item_reports_a_truthful_reason_when_full():
    state = RunState.fresh_run()
    for i in range(1, 7):
        state.add_item(f"item_{i}")

    choice = {
        "id": "take_key",
        "label": "Take the rusty iron key",
        "destination": "hall",
        "effects": [
            {"verb": "grant_item", "item": "iron_key"},
        ],
    }

    result = resolve_choice(choice, state)
    assert result.refused is True
    assert "Inventory full" in result.reason
    assert "iron_key" in result.reason
    assert "iron_key" not in state.held_items


def test_has_item_and_lantern_behaviour_are_unchanged():
    state = RunState.fresh_run()
    state.add_item("knife")
    assert state.has_item("knife") is True
    assert state.has_item("sword") is False

    # Lantern behaviour is completely independent
    assert state.lantern == 100
    state.spend_lantern(20)
    assert state.lantern == 80
    assert state.has_item("knife") is True
