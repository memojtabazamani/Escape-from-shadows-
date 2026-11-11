"""Tests for difficulty choice pressure on HARD (Task B05)."""

from game.content_schema import load_content
from game.difficulty import get_difficulty_config
from game.state import RunState
from screens.game import GameScreen


def test_choice_expires_on_hard_only():
    expiring_choice = {
        "id": "test_choice",
        "label": "Snatch the key",
        "destination": "hall",
        "expires_after_turns": 2,
        "expiry_text": "The key slipped away.",
    }

    # EASY: never expires even after 5 turns
    easy_state = RunState.fresh_run("EASY")
    easy_state.consecutive_room_turns = 5
    easy_screen = GameScreen(state=easy_state)
    assert not easy_screen.is_choice_expired(expiring_choice)

    # MEDIUM: never expires
    med_state = RunState.fresh_run("MEDIUM")
    med_state.consecutive_room_turns = 5
    med_screen = GameScreen(state=med_state)
    assert not med_screen.is_choice_expired(expiring_choice)

    # HARD: expires once consecutive turns reaches threshold
    hard_state = RunState.fresh_run("HARD")
    hard_state.consecutive_room_turns = 1
    hard_screen = GameScreen(state=hard_state)
    assert not hard_screen.is_choice_expired(expiring_choice)

    hard_state.consecutive_room_turns = 2
    assert hard_screen.is_choice_expired(expiring_choice)


def test_expiry_is_preceded_by_a_visible_cue():
    hard_state = RunState.fresh_run("HARD")
    hard_state.consecutive_room_turns = 1
    screen = GameScreen(state=hard_state)
    screen.current_choices = [
        {
            "id": "c1",
            "label": "Search alcove",
            "expires_after_turns": 2,
        }
    ]

    cue = screen.get_nearing_expiry_cue()
    assert cue is not None
    assert "Time is slipping away" in cue


def test_room_remains_playable_after_an_expiry():
    # In old_library, when library_search_alcove expires, library_read and library_return still exist
    content = load_content("data/content.json")
    library = next(r for r in content["rooms"] if r["id"] == "old_library")

    hard_state = RunState.fresh_run("HARD")
    hard_state.current_room = "old_library"
    hard_state.consecutive_room_turns = 10
    screen = GameScreen(content=content, state=hard_state)
    screen.current_choices = list(library["choices"])

    active_choices = [c for c in screen.current_choices if not screen.is_choice_expired(c)]
    assert len(active_choices) >= 2
    # Reading and returning remain valid
    assert any(c["id"] == "library_read" for c in active_choices)
    assert any(c["id"] == "library_return" for c in active_choices)


def test_reachable_content_is_identical_on_every_difficulty():
    content = load_content("data/content.json")

    def get_reachable_rooms(diff: str) -> set[str]:
        state = RunState.fresh_run(diff)
        visited = set()
        stack = [content.get("start_room", "hall")]
        rooms_by_id = {r["id"]: r for r in content["rooms"]}

        while stack:
            curr = stack.pop()
            if curr in visited or curr not in rooms_by_id:
                continue
            visited.add(curr)
            for ch in rooms_by_id[curr].get("choices", []):
                dest = ch.get("destination")
                if dest and dest not in visited:
                    stack.append(dest)
        return visited

    easy_rooms = get_reachable_rooms("EASY")
    med_rooms = get_reachable_rooms("MEDIUM")
    hard_rooms = get_reachable_rooms("HARD")

    assert easy_rooms == med_rooms == hard_rooms


def test_expiry_is_not_reported_as_a_requirement_failure():
    # Expired choice is filtered / struck-through, never mapped to check_requirements failure
    from game.effects import resolve_choice

    choice = {
        "id": "c1",
        "label": "Search alcove",
        "destination": "old_library",
        "expires_after_turns": 2,
        "expiry_text": "Too late.",
        "requirements": [],
    }
    state = RunState.fresh_run("HARD")
    state.consecutive_room_turns = 5

    # resolve_choice sees empty requirements and is not refused by requirements
    result = resolve_choice(choice, state)
    assert result.refused is False

    # But screen knows it's expired
    screen = GameScreen(state=state)
    assert screen.is_choice_expired(choice)
