"""Slice C (Inventory) integration tests.

Covers:
- The cap as an unyielding boundary (7 items cannot be held by any route).
- Transactionality of the drop flow (cancel changes nothing).
- Fairness invariant (run is completable with an empty inventory).
- Ledger closure (all defined items are placed or recorded as deferred).
- Items found in their assigned rooms.
- Full pack never blocks the ending.
"""
from pathlib import Path
import pytest

from game.content_schema import load_content
from game.state import RunState
from game.effects import (
    apply_effects,
    check_requirements,
    resolve_choice,
    _apply_one,
)
from screens.game import GameScreen
from tests.test_game_screen import GameScreenTestApp


DEFERRED_PLACEMENTS = {
    "rusty_cleaver": "F02 (Blood Kitchen)",
    "silver_whistle": "F07 (Observatory)",
    "dogs_tooth": "G03 (The Hell Dog)",
    "front_door_key": "F06 (Three-route Key)",
}


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


def test_seven_items_cannot_be_held_by_any_route():
    """Assert the 6-slot boundary cannot be bypassed by any verb, predicate, or state manipulation."""
    state = RunState.fresh_run()
    six_items = ["item1", "item2", "item3", "item4", "item5", "item6"]
    for it in six_items:
        assert state.add_item(it) is True

    assert len(state.held_items) == 6
    assert state.free_slots() == 0
    assert state.can_add_item() is False

    # Route 1: direct add_item
    assert state.add_item("item7") is False
    assert len(state.held_items) == 6

    # Route 2: grant_item effect verb fails all-or-nothing
    eff_res = apply_effects([{"verb": "grant_item", "item": "item7"}], state)
    assert eff_res.success is False
    assert "Inventory full" in eff_res.reason
    assert len(state.held_items) == 6

    # Direct _apply_one raises ValueError
    with pytest.raises(ValueError, match="Inventory full"):
        _apply_one({"verb": "grant_item", "item": "item7"}, state)
    assert len(state.held_items) == 6

    # Route 3: has_free_slot requirement predicate rejects
    req_res = check_requirements([{"predicate": "has_free_slot"}], state)
    assert req_res.satisfied is False
    assert any("pack is full" in r for r in req_res.reasons)

    # Route 4: inventory_under predicate rejects
    req_under = check_requirements([{"predicate": "inventory_under", "count": 6}], state)
    assert req_under.satisfied is False


@pytest.mark.anyio
async def test_cancel_changes_nothing_at_all(house_content):
    """Canceling drop mode restores the exact prior state: items, room, turn, and oil."""
    state = RunState.fresh_run()
    state.current_room = "hall"
    six_items = ["matchbox", "rusty_cleaver", "the_book", "silver_whistle", "dogs_tooth", "front_door_key"]
    for it in six_items:
        state.add_item(it)

    initial_items = list(state.held_items)
    initial_room = state.current_room
    initial_turn = state.turn_count
    initial_oil = state.lantern

    screen = GameScreen(content=house_content, state=state)
    app = GameScreenTestApp(content=house_content, state=state)

    async with app.run_test() as pilot:
        active_screen = pilot.app.screen
        assert isinstance(active_screen, GameScreen)

        # Trigger drop mode by attempting to take matchbox when full
        matchbox_choice = next(
            c for c in active_screen.current_choices if c["id"] == "hall_take_matchbox"
        )
        active_screen._execute_choice(matchbox_choice)
        assert active_screen.drop_mode is True

        # Cancel drop mode
        active_screen.cancel_drop()
        assert active_screen.drop_mode is False

        # Verify nothing changed at all
        assert state.held_items == initial_items
        assert state.current_room == initial_room
        assert state.turn_count == initial_turn
        assert state.lantern == initial_oil


def test_run_is_completable_with_an_empty_inventory(house_content):
    """Fairness invariant (ASM-14): The game is 100% winnable without holding any items."""
    state = RunState.fresh_run()
    state.current_room = "hall"
    assert len(state.held_items) == 0

    rooms_by_id = {r["id"]: r for r in house_content["rooms"]}

    # Hall -> Library
    hall = rooms_by_id["hall"]
    to_library = next(c for c in hall["choices"] if c["destination"] == "old_library")
    res1 = resolve_choice(to_library, state)
    assert res1.refused is False
    state.current_room = res1.destination

    # Library -> Read lectern (sets knows_exit)
    library = rooms_by_id["old_library"]
    read_lectern = next(c for c in library["choices"] if c["id"] == "library_read")
    res2 = resolve_choice(read_lectern, state)
    assert res2.refused is False
    assert state.has_flag("knows_exit") is True

    # Library -> Return to Hall
    to_hall = next(c for c in library["choices"] if c["destination"] == "hall")
    res3 = resolve_choice(to_hall, state)
    assert res3.refused is False
    state.current_room = res3.destination

    # Hall -> Front door escape
    front_door = next(c for c in hall["choices"] if c["id"] == "hall_front_door")
    res4 = resolve_choice(front_door, state)
    assert res4.refused is False
    assert res4.destination == "front_door_escape"
    assert rooms_by_id[res4.destination]["tier"] == "ending"

    # Held items stayed 0 throughout
    assert len(state.held_items) == 0


def test_every_defined_item_is_placed_or_recorded_as_deferred(house_content):
    """Ledger closure: every defined item is either placed in content or assigned an owning task."""
    defined_items = {it["id"] for it in house_content.get("items", [])}
    assert len(defined_items) == 6

    # Collect all items granted in content choices
    placed_items = set()
    for room in house_content.get("rooms", []):
        for choice in room.get("choices", []):
            for effect in choice.get("effects", []):
                if effect.get("verb") == "grant_item":
                    placed_items.add(effect.get("item"))

    for item_id in defined_items:
        if item_id not in placed_items:
            assert item_id in DEFERRED_PLACEMENTS, (
                f"Item '{item_id}' is defined but neither placed in content nor in DEFERRED_PLACEMENTS ledger"
            )


def test_items_found_in_their_own_room(house_content):
    """Placed items are granted only in their §3.3 assigned rooms."""
    expected_rooms = {
        "matchbox": "hall",
        "the_book": "old_library",
    }
    for room in house_content.get("rooms", []):
        for choice in room.get("choices", []):
            for effect in choice.get("effects", []):
                if effect.get("verb") == "grant_item":
                    item_id = effect.get("item")
                    if item_id in expected_rooms:
                        assert room["id"] == expected_rooms[item_id], (
                            f"Item '{item_id}' granted in '{room['id']}', expected '{expected_rooms[item_id]}'"
                        )


def test_full_pack_never_blocks_the_ending(house_content):
    """Even with a full 6/6 pack, victory choices cannot be blocked by inventory cap."""
    state = RunState.fresh_run()
    for it in ["matchbox", "rusty_cleaver", "the_book", "silver_whistle", "dogs_tooth", "front_door_key"]:
        state.add_item(it)
    assert len(state.held_items) == 6
    state.current_room = "hall"
    state.set_flag("knows_exit")

    hall = next(r for r in house_content["rooms"] if r["id"] == "hall")
    front_door = next(c for c in hall["choices"] if c["id"] == "hall_front_door")

    res = resolve_choice(front_door, state)
    assert res.refused is False
    assert res.destination == "front_door_escape"
