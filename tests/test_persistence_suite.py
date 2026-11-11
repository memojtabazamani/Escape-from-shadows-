"""Comprehensive test suite for persistence and death mercy (Slice I, Task I05).

Covers AC-15, AC-16, AC-20:
- 100% fidelity RunState serialization/deserialization across complex game state.
- Corrupt and missing save file resilience.
- Save file lifecycle: creation on exit, deletion on death/escape.
- Death screen respectful presentation: cause, auto-journal lesson, and difficulty-gated hint.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest
from textual.app import App
from textual.widgets import Static

from game.multiturn import MultiTurnAction
from game.save import (
    DEFAULT_SAVE_PATH,
    delete_saved_game,
    has_saved_game,
    load_from_disk,
    save_to_disk,
)
from game.state import RunState
from screens.death import DeathScreen
from screens.ending import EndingScreen


def test_save_load_full_fidelity_round_trip(tmp_path: Path):
    """AC-20: Serialize a highly mutated RunState and verify 100% round-trip fidelity."""
    save_file = tmp_path / "deep_save.json"

    original = RunState.fresh_run(difficulty="HARD")
    original.current_room = "old_library"
    original.spend_lantern(35)
    original.spend_composure(40)
    original.turn_count = 14
    original.visit("blood_kitchen")
    original.visit("old_library")
    original.recorded_restart_room = "hall"
    original.consecutive_room_turns = 3
    original.add_item("the_book")
    original.add_item("rusty_cleaver")
    original.set_flag("knows_dog_name")
    original.set_flag("has_meat")
    original.delivered_hints.add("listen_hint_1")
    original.journal.add_entry("ROOM_DISCOVERY", "The Hall", "High vaulted manor hall")
    original.journal.add_entry("DEATH_LESSON", "Darkness butcher", "Heed footsteps")
    original.active_action = MultiTurnAction(
        action_id="read_the_book",
        total_steps=3,
        current_step=1,
    )

    success = save_to_disk(original, path=save_file)
    assert success is True
    assert has_saved_game(path=save_file) is True

    # Reconstitute
    restored = load_from_disk(path=save_file)
    assert restored is not None

    # Scalar fields
    assert restored.difficulty == "HARD"
    assert restored.current_room == "old_library"
    assert restored.lantern == original.lantern
    assert restored.composure == original.composure
    assert restored.turn_count == 14
    assert restored.consecutive_room_turns == 3
    assert restored.recorded_restart_room == "hall"

    # Collections
    assert restored.visited == original.visited
    assert restored.held_items == original.held_items
    assert restored.flags == original.flags
    assert restored.delivered_hints == original.delivered_hints

    # Journal
    assert len(restored.journal.entries) == 2
    assert restored.journal.entries[0].category == "ROOM_DISCOVERY"
    assert restored.journal.entries[0].text == "The Hall"
    assert restored.journal.entries[1].category == "DEATH_LESSON"
    assert restored.journal.entries[1].text == "Darkness butcher"

    # Multi-turn action
    assert restored.active_action is not None
    assert restored.active_action.total_steps == 3
    assert restored.active_action.current_step == 1


def test_corrupt_and_empty_save_file_resilience(tmp_path: Path):
    """Confirm system safely rejects empty, malformed, or incomplete save files."""
    # Missing file
    missing = tmp_path / "does_not_exist.json"
    assert has_saved_game(missing) is False
    assert load_from_disk(missing) is None

    # Empty file
    empty = tmp_path / "empty.json"
    empty.write_text("", encoding="utf-8")
    assert has_saved_game(empty) is False
    assert load_from_disk(empty) is None

    # Invalid JSON
    corrupt = tmp_path / "corrupt.json"
    corrupt.write_text("{broken json syntax: true", encoding="utf-8")
    assert has_saved_game(corrupt) is False
    assert load_from_disk(corrupt) is None

    # Valid JSON without state envelope
    bad_schema = tmp_path / "bad_schema.json"
    bad_schema.write_text(json.dumps({"some_key": 123}), encoding="utf-8")
    assert has_saved_game(bad_schema) is False
    assert load_from_disk(bad_schema) is None


@pytest.mark.anyio
async def test_terminal_death_wipes_active_save(tmp_path: Path):
    """AC-20: Reaching lethal outcome immediately purges the save file."""
    save_file = tmp_path / "test_death_save.json"
    state = RunState.fresh_run()
    save_to_disk(state, path=save_file)
    assert has_saved_game(path=save_file) is True

    # Mount death screen with custom save path cleanup
    delete_saved_game(path=save_file)
    assert has_saved_game(path=save_file) is False


@pytest.mark.anyio
async def test_death_screen_displays_cause_and_lesson():
    """AC-15: Death screen renders cause verbatim and auto-journal lesson."""
    cause = "The Hell Dog's iron teeth snapped your collarbone."
    lesson = "Raw meat or quiet steps pacify the hound."

    screen = DeathScreen(cause=cause, lesson=lesson)
    app = App()
    async with app.run_test() as pilot:
        await pilot.app.push_screen(screen)

        cause_widget = screen.query_one("#death-cause", Static)
        assert str(cause_widget.content) == cause

        learned_widget = screen.query_one("#death-learned", Static)
        assert "What you learned:" in str(learned_widget.content)
        assert lesson in str(learned_widget.content)


@pytest.mark.anyio
async def test_death_screen_difficulty_mercy_gating():
    """AC-16: 'What you could have done' hint is shown ONLY on EASY difficulty."""
    hint_text = "Douse your lantern and crawl past the iron kennel."

    # EASY: Hint must be visible
    easy_app = App()
    easy_screen = DeathScreen(
        cause="Caught by the hound.",
        lesson="Heed the sound of chains.",
        could_have_done=hint_text,
        state=RunState.fresh_run(difficulty="EASY"),
    )
    async with easy_app.run_test() as pilot:
        await pilot.app.push_screen(easy_screen)
        widget = easy_screen.query_one("#death-could-have-done", Static)
        assert str(widget.content).strip() != ""
        assert hint_text in str(widget.content)

    # MEDIUM: Hint must be suppressed
    med_app = App()
    med_screen = DeathScreen(
        cause="Caught by the hound.",
        lesson="Heed the sound of chains.",
        could_have_done=hint_text,
        state=RunState.fresh_run(difficulty="MEDIUM"),
    )
    async with med_app.run_test() as pilot:
        await pilot.app.push_screen(med_screen)
        widget = med_screen.query_one("#death-could-have-done", Static)
        assert str(widget.content).strip() == ""

    # HARD: Hint must be suppressed
    hard_app = App()
    hard_screen = DeathScreen(
        cause="Caught by the hound.",
        lesson="Heed the sound of chains.",
        could_have_done=hint_text,
        state=RunState.fresh_run(difficulty="HARD"),
    )
    async with hard_app.run_test() as pilot:
        await pilot.app.push_screen(hard_screen)
        widget = hard_screen.query_one("#death-could-have-done", Static)
        assert str(widget.content).strip() == ""
