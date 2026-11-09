"""Tests for game.content_schema validator."""

import pytest

from game.content_schema import SAMPLE_CONTENT, validate_content


def _room(**kwargs):
    defaults = {
        "id": "room",
        "name": "Room",
        "prose": "A room.",
        "choices": [],
    }
    defaults.update(kwargs)
    return defaults


def _choice(**kwargs):
    defaults = {
        "id": "choice",
        "label": "Go",
        "destination": "room",
        "tier": "scar",
    }
    defaults.update(kwargs)
    return defaults


def test_valid_room_validates():
    content = {
        "start_room": "room",
        "rooms": [_room()],
    }
    assert validate_content(content) == []


def test_dangling_destination_reported():
    content = {
        "start_room": "room",
        "rooms": [
            _room(choices=[_choice(destination="missing")]),
        ],
    }
    problems = validate_content(content)
    assert len(problems) == 1
    assert "destination" in problems[0].field
    assert "missing" in problems[0].message


def test_missing_required_field_reported():
    bad_room = {"id": "room", "name": "Room", "choices": []}
    content = {
        "start_room": "room",
        "rooms": [bad_room],
    }
    problems = validate_content(content)
    assert any(p.field == "prose" for p in problems)


def test_death_fewer_than_two_telegraphs_rejected():
    content = {
        "start_room": "room",
        "rooms": [
            _room(
                choices=[
                    _choice(
                        tier="death",
                        telegraphs=["only one warning"],
                    )
                ]
            )
        ],
    }
    problems = validate_content(content)
    assert any("two telegraphs" in p.message for p in problems)


def test_duplicate_identifier_rejected():
    content = {
        "start_room": "room",
        "rooms": [
            _room(id="room"),
            _room(id="room"),
        ],
    }
    problems = validate_content(content)
    assert any("duplicate room id" in p.message for p in problems)


def test_unreachable_room_reported():
    content = {
        "start_room": "room",
        "rooms": [
            _room(id="room", choices=[_choice(id="c1", destination="room")]),
            _room(id="unreachable"),
        ],
    }
    problems = validate_content(content)
    assert any("unreachable" in p.message for p in problems)


def test_baseline_rooms_validate():
    """The sample content models the baseline hall/library loop and validates."""
    problems = validate_content(SAMPLE_CONTENT)
    assert problems == []
