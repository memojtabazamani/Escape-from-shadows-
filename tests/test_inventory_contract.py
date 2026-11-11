"""Tests for inventory effect verbs and requirement predicates (Task C02)."""

import pytest

from game.content_schema import validate_content, ValidationProblem
from game.effects import (
    check_requirements,
    apply_effects,
    resolve_choice,
    _apply_one,
)
from game.state import RunState


def test_each_new_predicate_resolves_correctly():
    state = RunState.fresh_run()
    state.add_item("matchbox")

    # lacks_item
    req_lacks_matchbox = [{"predicate": "lacks_item", "item": "matchbox"}]
    req_lacks_key = [{"predicate": "lacks_item", "item": "brass_key"}]
    assert check_requirements(req_lacks_matchbox, state).satisfied is False
    assert check_requirements(req_lacks_key, state).satisfied is True

    # has_free_slot
    assert check_requirements([{"predicate": "has_free_slot"}], state).satisfied is True
    # Fill remaining 5 slots
    for i in range(5):
        state.add_item(f"fill_{i}")
    assert check_requirements([{"predicate": "has_free_slot"}], state).satisfied is False

    # inventory_under
    assert check_requirements([{"predicate": "inventory_under", "count": 10}], state).satisfied is True
    assert check_requirements([{"predicate": "inventory_under", "count": 6}], state).satisfied is False


def test_full_pack_refuses_a_grant_with_a_reason():
    state = RunState.fresh_run()
    for i in range(6):
        state.add_item(f"item_{i}")

    choice = {
        "id": "take_gem",
        "label": "Take the glowing gem",
        "destination": "hall",
        "effects": [{"verb": "grant_item", "item": "gem"}],
    }

    result = resolve_choice(choice, state)
    assert result.refused is True
    assert "Inventory full" in result.reason
    assert "gem" in result.reason
    assert "gem" not in state.held_items


def test_new_verbs_roll_back_with_their_neighbours():
    state = RunState.fresh_run()
    state.add_item("key")
    initial_lantern = state.lantern

    # First effect drops key (valid), second effect spends 500 oil (invalid/fails)
    effects = [
        {"verb": "drop_item", "item": "key"},
        {"verb": "spend_oil", "amount": "invalid_numeric"},
    ]

    result = apply_effects(effects, state)
    assert result.success is False

    # All-or-nothing rollback: key must still be held, lantern unchanged
    assert state.has_item("key") is True
    assert state.lantern == initial_lantern


def test_unknown_verb_still_raises():
    state = RunState.fresh_run()
    with pytest.raises(ValueError, match="unknown effect verb"):
        _apply_one({"verb": "teleport_player", "target": "void"}, state)

    with pytest.raises(ValueError, match="unknown requirement predicate"):
        check_requirements([{"predicate": "is_nighttime"}], state)


def test_validator_accepts_the_new_names_and_rejects_unknown_ones():
    valid_content = {
        "start_room": "room1",
        "rooms": [
            {
                "id": "room1",
                "name": "Room One",
                "prose": "A room.",
                "choices": [
                    {
                        "id": "c1",
                        "label": "Drop key",
                        "destination": "room1",
                        "effects": [{"verb": "drop_item", "item": "key"}],
                        "requirements": [{"predicate": "has_free_slot"}],
                    },
                    {
                        "id": "c2",
                        "label": "Spend key",
                        "destination": "room1",
                        "effects": [{"verb": "spend_item", "item": "key"}],
                        "requirements": [
                            {"predicate": "lacks_item", "item": "curse"},
                            {"predicate": "inventory_under", "count": 5},
                        ],
                    },
                ],
            }
        ],
    }
    assert validate_content(valid_content) == []

    # Invalid verb
    invalid_verb_content = {
        "start_room": "room1",
        "rooms": [
            {
                "id": "room1",
                "name": "Room One",
                "prose": "A room.",
                "choices": [
                    {
                        "id": "c1",
                        "label": "Fly",
                        "destination": "room1",
                        "effects": [{"verb": "fly_away"}],
                    }
                ],
            }
        ],
    }
    problems = validate_content(invalid_verb_content)
    assert any("must be one of" in str(p) for p in problems)
