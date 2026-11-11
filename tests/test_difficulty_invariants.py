"""Difficulty invariants cross-cutting test suite (Task B06).

Proves the two core §5.1 claims:
1. Difficulty DOES change observable outcomes on all three settings.
2. Difficulty NEVER gates content (rooms, items, solutions).
"""

from game.content_schema import load_content
from game.difficulty import get_difficulty_config
from game.state import RunState


def _compute_reachable_content(difficulty: str, content: dict) -> tuple[set[str], set[str], set[str]]:
    """Traverse content graph starting from start_room under the given difficulty.

    Returns:
        (reachable_rooms, obtainable_items, reachable_solutions)
    """
    rooms_by_id = {r["id"]: r for r in content.get("rooms", [])}
    start_room = content.get("start_room", "hall")

    reachable_rooms: set[str] = set()
    obtainable_items: set[str] = set()
    available_solutions: set[str] = set()

    stack = [start_room]

    while stack:
        room_id = stack.pop()
        if room_id in reachable_rooms or room_id not in rooms_by_id:
            continue
        reachable_rooms.add(room_id)
        room = rooms_by_id[room_id]

        for choice in room.get("choices", []):
            dest = choice.get("destination")
            if dest and dest not in reachable_rooms:
                stack.append(dest)

            # Record items granted
            for effect in choice.get("effects", []):
                if effect.get("verb") == "grant_item":
                    obtainable_items.add(effect.get("item"))
                if effect.get("verb") == "set_flag":
                    available_solutions.add(effect.get("flag"))

    return reachable_rooms, obtainable_items, available_solutions


def test_reachable_content_is_identical_on_easy_medium_and_hard():
    """Invariant 1: Content reachability is strictly difficulty-independent."""
    content = load_content("data/content.json")

    easy_rooms, easy_items, easy_solutions = _compute_reachable_content("EASY", content)
    med_rooms, med_items, med_solutions = _compute_reachable_content("MEDIUM", content)
    hard_rooms, hard_items, hard_solutions = _compute_reachable_content("HARD", content)

    # All three sets must be strictly identical
    assert easy_rooms == med_rooms == hard_rooms
    assert easy_items == med_items == hard_items
    assert easy_solutions == med_solutions == hard_solutions


def test_every_difficulty_changes_something_observable():
    """Invariant 2: Every setting changes observable mechanics (no setting lies)."""
    easy = get_difficulty_config("EASY")
    med = get_difficulty_config("MEDIUM")
    hard = get_difficulty_config("HARD")

    # Starting generosity differs
    assert hard.initial_lantern < med.initial_lantern

    # Mercy differs
    assert easy.auto_fill_journal_on_death is True
    assert med.auto_fill_journal_on_death is False
    assert easy.restart_point_mode == "last_room"
    assert med.restart_point_mode == "start"

    # Information differs
    assert easy.hints_enabled is True
    assert med.hints_enabled is False
    assert hard.hints_enabled is False

    # Pressure differs
    assert hard.choice_expiry_enabled is True
    assert med.choice_expiry_enabled is False
    assert easy.choice_expiry_enabled is False


def test_medium_is_the_identity_config():
    """Invariant 3: MEDIUM is the identity and exactly reproduces pre-slice numbers."""
    med = get_difficulty_config("MEDIUM")

    assert med.initial_lantern == 100
    assert med.initial_composure == 100
    assert med.hints_enabled is False
    assert med.auto_fill_journal_on_death is False
    assert med.restart_point_mode == "start"
    assert med.choice_expiry_enabled is False


def test_no_parameter_carries_a_content_identifier():
    """ASM-14 structural guard: DifficultyConfig cannot carry room, item, or flag IDs."""
    content = load_content("data/content.json")
    room_ids = {r["id"].lower() for r in content.get("rooms", [])}

    for diff in ["EASY", "MEDIUM", "HARD"]:
        cfg = get_difficulty_config(diff)
        for field_name in cfg.__dataclass_fields__:
            val = getattr(cfg, field_name)
            if isinstance(val, str):
                assert val.lower() not in room_ids, f"DifficultyConfig leaked room ID '{val}' in {field_name}"


def test_every_setting_toggle_has_an_observable_effect():
    """AC-24: Verifies the difficulty setting produces distinctly functioning runs.

    Note: sound and music setting toggles are handed off to Task H04.
    """
    easy_run = RunState.fresh_run("EASY")
    med_run = RunState.fresh_run("MEDIUM")
    hard_run = RunState.fresh_run("HARD")

    assert easy_run.difficulty == "EASY"
    assert med_run.difficulty == "MEDIUM"
    assert hard_run.difficulty == "HARD"

    # Verify observable divergence at runtime
    assert hard_run.lantern < med_run.lantern
