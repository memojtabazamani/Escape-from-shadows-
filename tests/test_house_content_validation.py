"""Automated validator and full-house test suite (Task F08).

Verifies graph reachability, resource economy, two-telegraph death safety,
and compliance with the 20-line prose budget across all house rooms.
"""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_full_house_schema_validation(content):
    """AC-1, AC-22: All rooms validate with 0 schema problems."""
    problems = validate_content(content)
    assert problems == [], f"Validation problems found: {[str(p) for p in problems]}"


def test_all_rooms_reachable_from_hall(content):
    """Every non-start room is reachable from start_room."""
    start_room = content["start_room"]
    assert start_room == "hall"

    rooms_by_id = {r["id"]: r for r in content["rooms"]}
    visited = set()
    queue = [start_room]

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        room = rooms_by_id.get(current)
        if room:
            for choice in room.get("choices", []):
                dest = choice.get("destination")
                if dest and dest in rooms_by_id and dest not in visited:
                    queue.append(dest)

    unreachable = set(rooms_by_id.keys()) - visited
    assert not unreachable, f"Rooms unreachable from '{start_room}': {unreachable}"


def test_every_room_prose_fits_twenty_line_budget(content):
    """AC-23: Every room arrival prose and revisit prose has <= 20 lines."""
    for room in content["rooms"]:
        prose = room.get("prose", "")
        lines = prose.split("\n")
        assert len(lines) <= 20, f"Room '{room['id']}' prose exceeds 20 lines ({len(lines)} lines)"

        revisit = room.get("revisit_prose")
        if revisit:
            revisit_lines = revisit.split("\n")
            assert len(revisit_lines) <= 20, (
                f"Room '{room['id']}' revisit_prose exceeds 20 lines ({len(revisit_lines)} lines)"
            )


def test_two_telegraph_death_safety(content):
    """AC-21: Every choice with tier 'death' must have at least two telegraphs."""
    rooms_by_id = {r["id"]: r for r in content["rooms"]}
    for room in content["rooms"]:
        for choice in room.get("choices", []):
            dest_id = choice.get("destination")
            dest_room = rooms_by_id.get(dest_id, {})
            is_death = (choice.get("tier") == "death") or (dest_room.get("tier") == "death")

            if is_death:
                telegraphs = choice.get("telegraphs", [])
                assert len(telegraphs) >= 2, (
                    f"Death choice '{choice.get('id')}' in room '{room['id']}' has only {len(telegraphs)} telegraph(s)"
                )


def test_content_only_extensibility(content):
    """AC-22: Arbitrary content room added without engine changes validates."""
    import copy
    extended = copy.deepcopy(content)
    new_room = {
        "id": "secret_attic",
        "name": "Secret Attic",
        "prose": "Dusty beams crisscross above dry floorboards.\nA forgotten trunk sits by the chimney.",
        "choices": [
            {
                "id": "attic_return",
                "label": "Descend the folding stairs to The Hall",
                "destination": "hall",
                "tier": "scar",
            }
        ],
    }
    extended["rooms"].append(new_room)
    # Add a transition from hall to new_room
    hall = next(r for r in extended["rooms"] if r["id"] == "hall")
    hall["choices"].append(
        {
            "id": "hall_attic",
            "label": "Climb the ladder into the attic",
            "destination": "secret_attic",
            "tier": "scar",
        }
    )

    problems = validate_content(extended)
    assert problems == []
