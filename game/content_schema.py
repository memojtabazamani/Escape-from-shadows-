"""Content record format and validator for Escape from Shadows.

The game world is described by plain data records kept separate from the
engine.  This module defines the shape of those records and a validator that
catches mistakes before a player can see them.

Record shape (JSON-compatible)
-------------------------------
Room:
  id          str   required  machine identifier, unique in the set
  name        str   required  display name shown to the player
  prose       str   required  arrival text, kept short enough for one screen
  choices     list  required  list of Choice records

Choice:
  id            str   required  unique choice identifier
  label         str   required  text shown on the choice line
  destination   str   required  room id to move to after resolving this choice
  tier          str   optional  one of "scar", "setback", "death"; default "scar"
  telegraphs    list  optional  list of str warnings shown before the choice
  requirements  list  optional  list of Requirement records; all must pass
  effects       list  optional  list of Effect records applied on success

Effect (declarative operation):
  verb  str  one of "spend_oil", "grant_item", "set_flag"
  ... plus verb-specific keys (amount, item, flag)

Requirement (condition over run state):
  predicate  str  one of "has_flag", "has_item", "lantern_above"
  ... plus predicate-specific keys

Validator rules
---------------
- Rooms and choices have the required fields.
- Room ids and choice ids are unique.
- Every choice destination resolves to an existing room.
- A choice with tier "death" must have at least two telegraphs.
- Every referenced effect verb and requirement predicate is known.
- Every room is reachable from the configured start room.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Valid tiers from SUGGEST.md §4.1.
TIERS = {"scar", "setback", "death"}

# Valid effect verbs and the keys they require.
EFFECT_VERBS: dict[str, dict[str, set[str]]] = {
    "spend_oil": {"required": {"amount"}, "optional": set()},
    "grant_item": {"required": {"item"}, "optional": set()},
    "set_flag": {"required": {"flag"}, "optional": set()},
}

# Valid requirement predicates and the keys they require.
REQUIREMENT_PREDICATES: dict[str, dict[str, set[str]]] = {
    "has_flag": {"required": {"flag"}, "optional": set()},
    "has_item": {"required": {"item"}, "optional": set()},
    "lantern_above": {"required": {"amount"}, "optional": set()},
}


@dataclass
class ValidationProblem:
    """A single validation issue, naming where it lives."""

    record: str
    field: str
    message: str

    def __str__(self) -> str:
        return f"[{self.record} / {self.field}] {self.message}"


def load_content(path: str | Path) -> dict[str, Any]:
    """Load a content set from a JSON file."""
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def validate_content(content: dict[str, Any]) -> list[ValidationProblem]:
    """Validate an entire content set and return all problems found."""
    problems: list[ValidationProblem] = []

    if not isinstance(content, dict):
        return [ValidationProblem("<root>", "<root>", "content must be a dict with 'rooms' and optional 'start_room'")]

    rooms = content.get("rooms")
    if not isinstance(rooms, list):
        problems.append(ValidationProblem("<root>", "rooms", "'rooms' must be a list of room records"))
        return problems

    start_room = content.get("start_room", "hall")
    if not isinstance(start_room, str):
        problems.append(ValidationProblem("<root>", "start_room", "'start_room' must be a string"))
        return problems

    room_ids: set[str] = set()
    choice_ids: set[str] = set()
    rooms_by_id: dict[str, dict[str, Any]] = {}

    for index, room in enumerate(rooms):
        problems.extend(_validate_room(room, index, room_ids, choice_ids))
        if isinstance(room, dict) and isinstance(room.get("id"), str):
            rooms_by_id[room["id"]] = room

    # Cross-record checks
    problems.extend(_validate_destinations(rooms_by_id))
    problems.extend(_validate_death_telegraphs(rooms_by_id))
    problems.extend(_validate_reachability(rooms_by_id, start_room))

    return problems


def _validate_room(
    room: Any,
    index: int,
    room_ids: set[str],
    choice_ids: set[str],
) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    prefix = f"rooms[{index}]"

    if not isinstance(room, dict):
        problems.append(ValidationProblem(prefix, "<room>", "room must be a dict"))
        return problems

    room_id = room.get("id")
    if not isinstance(room_id, str):
        problems.append(ValidationProblem(prefix, "id", "room id must be a string"))
        return problems

    record_name = f"room:{room_id}"

    if room_id in room_ids:
        problems.append(ValidationProblem(record_name, "id", f"duplicate room id '{room_id}'"))
    else:
        room_ids.add(room_id)

    for field in ("name", "prose"):
        value = room.get(field)
        if not isinstance(value, str):
            problems.append(ValidationProblem(record_name, field, "must be a string"))

    choices = room.get("choices")
    if not isinstance(choices, list):
        problems.append(ValidationProblem(record_name, "choices", "must be a list of choice records"))
        return problems

    for choice_index, choice in enumerate(choices):
        problems.extend(_validate_choice(choice, choice_index, record_name, room_id, choice_ids))

    return problems


def _validate_choice(
    choice: Any,
    index: int,
    record_name: str,
    room_id: str,
    choice_ids: set[str],
) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    choice_prefix = f"{record_name}.choices[{index}]"

    if not isinstance(choice, dict):
        problems.append(ValidationProblem(choice_prefix, "<choice>", "choice must be a dict"))
        return problems

    choice_id = choice.get("id")
    if not isinstance(choice_id, str):
        problems.append(ValidationProblem(choice_prefix, "id", "choice id must be a string"))
        return problems

    if choice_id in choice_ids:
        problems.append(ValidationProblem(choice_prefix, "id", f"duplicate choice id '{choice_id}'"))
    else:
        choice_ids.add(choice_id)

    label = choice.get("label")
    if not isinstance(label, str):
        problems.append(ValidationProblem(choice_prefix, "label", "must be a string"))

    destination = choice.get("destination")
    if not isinstance(destination, str):
        problems.append(ValidationProblem(choice_prefix, "destination", "must be a string (room id)"))

    tier = choice.get("tier", "scar")
    if tier not in TIERS:
        problems.append(ValidationProblem(choice_prefix, "tier", f"must be one of {sorted(TIERS)}"))

    telegraphs = choice.get("telegraphs", [])
    if not isinstance(telegraphs, list) or not all(isinstance(t, str) for t in telegraphs):
        problems.append(ValidationProblem(choice_prefix, "telegraphs", "must be a list of strings"))

    effects = choice.get("effects", [])
    if not isinstance(effects, list):
        problems.append(ValidationProblem(choice_prefix, "effects", "must be a list of effect records"))
    else:
        for effect_index, effect in enumerate(effects):
            problems.extend(_validate_effect(effect, choice_prefix, "effects", effect_index))

    requirements = choice.get("requirements", [])
    if not isinstance(requirements, list):
        problems.append(ValidationProblem(choice_prefix, "requirements", "must be a list of requirement records"))
    else:
        for req_index, requirement in enumerate(requirements):
            problems.extend(_validate_requirement(requirement, choice_prefix, "requirements", req_index))

    return problems


def _validate_effect(
    effect: Any,
    choice_prefix: str,
    field_name: str,
    index: int,
) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    effect_prefix = f"{choice_prefix}.{field_name}[{index}]"

    if not isinstance(effect, dict):
        problems.append(ValidationProblem(effect_prefix, "<effect>", "effect must be a dict"))
        return problems

    verb = effect.get("verb")
    if verb not in EFFECT_VERBS:
        problems.append(ValidationProblem(effect_prefix, "verb", f"must be one of {sorted(EFFECT_VERBS)}"))
        return problems

    spec = EFFECT_VERBS[verb]
    _check_keys(effect, effect_prefix, spec["required"], spec["optional"], problems)
    return problems


def _validate_requirement(
    requirement: Any,
    choice_prefix: str,
    field_name: str,
    index: int,
) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    req_prefix = f"{choice_prefix}.{field_name}[{index}]"

    if not isinstance(requirement, dict):
        problems.append(ValidationProblem(req_prefix, "<requirement>", "requirement must be a dict"))
        return problems

    predicate = requirement.get("predicate")
    if predicate not in REQUIREMENT_PREDICATES:
        problems.append(ValidationProblem(req_prefix, "predicate", f"must be one of {sorted(REQUIREMENT_PREDICATES)}"))
        return problems

    spec = REQUIREMENT_PREDICATES[predicate]
    _check_keys(requirement, req_prefix, spec["required"], spec["optional"], problems)
    return problems


def _check_keys(
    record: dict[str, Any],
    prefix: str,
    required: set[str],
    optional: set[str],
    problems: list[ValidationProblem],
) -> None:
    allowed = required | optional | {"verb", "predicate"}
    for key in required:
        if key not in record:
            problems.append(ValidationProblem(prefix, key, f"required for {record.get('verb') or record.get('predicate')}"))
    for key in record:
        if key not in allowed:
            problems.append(ValidationProblem(prefix, key, f"unknown key '{key}'"))


def _validate_destinations(rooms_by_id: dict[str, dict[str, Any]]) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    for room in rooms_by_id.values():
        for choice in room.get("choices", []):
            destination = choice.get("destination")
            if isinstance(destination, str) and destination not in rooms_by_id:
                problems.append(
                    ValidationProblem(
                        f"room:{room['id']}.choice:{choice['id']}",
                        "destination",
                        f"destination '{destination}' does not match any room id",
                    )
                )
    return problems


def _validate_death_telegraphs(rooms_by_id: dict[str, dict[str, Any]]) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    for room in rooms_by_id.values():
        for choice in room.get("choices", []):
            if choice.get("tier") == "death":
                telegraphs = choice.get("telegraphs", [])
                if not isinstance(telegraphs, list) or len(telegraphs) < 2:
                    problems.append(
                        ValidationProblem(
                            f"room:{room['id']}.choice:{choice['id']}",
                            "telegraphs",
                            "death-tier choice must have at least two telegraphs",
                        )
                    )
    return problems


def _validate_reachability(
    rooms_by_id: dict[str, dict[str, Any]],
    start_room: str,
) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []

    if start_room not in rooms_by_id:
        problems.append(ValidationProblem("<root>", "start_room", f"start room '{start_room}' does not exist"))
        return problems

    reachable: set[str] = set()
    stack = [start_room]

    while stack:
        current_id = stack.pop()
        if current_id in reachable:
            continue
        reachable.add(current_id)
        room = rooms_by_id[current_id]
        for choice in room.get("choices", []):
            destination = choice.get("destination")
            if isinstance(destination, str) and destination not in reachable and destination in rooms_by_id:
                stack.append(destination)

    unreachable = set(rooms_by_id) - reachable
    for room_id in sorted(unreachable):
        problems.append(ValidationProblem(f"room:{room_id}", "<reachability>", f"room '{room_id}' is unreachable from '{start_room}'"))

    return problems


# Sample content used by the validator tests and by A04's proof step.
SAMPLE_CONTENT: dict[str, Any] = {
    "start_room": "hall",
    "rooms": [
        {
            "id": "hall",
            "name": "The Hall",
            "prose": "A high hall.  Two doorways lead away from the candlelight.",
            "choices": [
                {
                    "id": "hall_left",
                    "label": "Step through the left doorway",
                    "destination": "left_doorway_death",
                    "tier": "death",
                    "telegraphs": [
                        "Warm air, wrong-air, washes over your hand.",
                        "Something sticky pulls at your boot-sole when you shift your weight.",
                    ],
                },
                {
                    "id": "hall_right",
                    "label": "Take the right-hand passage",
                    "destination": "old_library",
                },
            ],
        },
        {
            "id": "left_doorway_death",
            "name": "The Left Doorway",
            "prose": "One step is all it takes.  The dark is faster than you are.",
            "choices": [],
        },
        {
            "id": "old_library",
            "name": "Old Library",
            "prose": "Shelves lean like tired sentinels.  A book lies open on the lectern.",
            "choices": [
                {
                    "id": "library_read",
                    "label": "Read the open book",
                    "destination": "old_library",
                    "tier": "setback",
                    "effects": [
                        {"verb": "spend_oil", "amount": 30},
                        {"verb": "set_flag", "flag": "knows_exit"},
                    ],
                },
                {
                    "id": "library_return",
                    "label": "Return to the hall",
                    "destination": "hall",
                },
            ],
        },
    ],
}
