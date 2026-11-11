from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.state import RunState
from game.effects import resolve_choice


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


def test_content_validates_clean(house_content):
    problems = validate_content(house_content)
    assert problems == [], f"Validation problems found: {[str(p) for p in problems]}"


def test_hall_is_the_start_room(house_content):
    assert house_content.get("start_room") == "hall"
    hall_room = next((r for r in house_content["rooms"] if r["id"] == "hall"), None)
    assert hall_room is not None
    assert hall_room["name"] == "The Hall"


def test_front_door_refuses_without_the_knowledge_flag(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    door_choice = next(c for c in hall_room["choices"] if c["id"] == "hall_front_door")

    state = RunState.fresh_run()
    state.current_room = "hall"
    assert state.has_flag("knows_exit") is False

    result = resolve_choice(door_choice, state)
    assert result.refused is True
    assert "requires flag 'knows_exit'" in result.reason
    assert state.current_room == "hall"


def test_front_door_yields_with_the_knowledge_flag(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    door_choice = next(c for c in hall_room["choices"] if c["id"] == "hall_front_door")

    state = RunState.fresh_run()
    state.current_room = "hall"
    state.set_flag("knows_exit")

    result = resolve_choice(door_choice, state)
    assert result.refused is False
    assert result.destination == "front_door_escape"



def test_hall_staircase_refuses_without_implying_walkable_room(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    stair_choice = next(c for c in hall_room["choices"] if c["id"] == "hall_staircase")

    state = RunState.fresh_run()
    result = resolve_choice(stair_choice, state)
    assert result.refused is True
    assert "requires flag 'staircase_passable'" in result.reason


def test_hall_prose_fits_the_line_budget(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    prose = hall_room["prose"]
    lines = prose.split("\n")
    # Budget is <= 20 usable lines (ASM-18)
    assert len(lines) <= 20
    assert len(lines) >= 3  # Sufficient descriptive depth


def test_library_is_reachable_from_the_hall(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    library_choice = next(c for c in hall_room["choices"] if c["destination"] == "old_library")
    assert library_choice is not None

    lib_room = next((r for r in house_content["rooms"] if r["id"] == "old_library"), None)
    assert lib_room is not None
    assert lib_room["name"] == "Old Library"

    # Return choice leads back to the hall
    return_choice = next((c for c in lib_room["choices"] if c["id"] == "library_return"), None)
    assert return_choice is not None
    assert return_choice["destination"] == "hall"


def test_book_read_spends_oil_and_sets_the_knowledge_flag(house_content):
    from game.lantern import CAREFUL_ACTION_DRAIN

    lib_room = next(r for r in house_content["rooms"] if r["id"] == "old_library")
    read_choice = next(c for c in lib_room["choices"] if c["id"] == "library_read")

    # The cost must match CAREFUL_ACTION_DRAIN
    spend_effect = next(e for e in read_choice["effects"] if e["verb"] == "spend_oil")
    assert spend_effect["amount"] == CAREFUL_ACTION_DRAIN

    # The flag must be 'knows_exit'
    flag_effect = next(e for e in read_choice["effects"] if e["verb"] == "set_flag")
    assert flag_effect["flag"] == "knows_exit"

    # Executing the read resolves properly
    state = RunState.fresh_run()
    state.lantern = 100
    state.current_room = "old_library"
    assert state.has_flag("knows_exit") is False

    result = resolve_choice(read_choice, state)
    assert result.refused is False
    assert state.lantern == 100 - CAREFUL_ACTION_DRAIN
    assert state.has_flag("knows_exit") is True


def test_library_prose_fits_the_line_budget(house_content):
    lib_room = next(r for r in house_content["rooms"] if r["id"] == "old_library")
    prose = lib_room["prose"]
    lines = prose.split("\n")
    # Budget is <= 20 usable lines (ASM-18)
    assert len(lines) <= 20
    assert len(lines) >= 3

    # Prose contains the sentinel shelves, lectern, and watched atmosphere
    lower_prose = prose.lower()
    assert "sentinels" in lower_prose or "shelves" in lower_prose
    assert "lectern" in lower_prose or "tome" in lower_prose
    assert "watching" in lower_prose or "breath" in lower_prose

    # No pursuit mechanics, timer, or Shadow entity mentioned
    assert "pursuit" not in lower_prose
    assert "shadow moves" not in lower_prose


def test_second_read_follows_the_recorded_decision(house_content):
    """Decision: Repeat at full cost.

    Reading a second time costs full CAREFUL_ACTION_DRAIN again and re-affirms
    the 'knows_exit' flag. It is repeatable at a cost, but not farmable.
    """
    from game.lantern import CAREFUL_ACTION_DRAIN

    lib_room = next(r for r in house_content["rooms"] if r["id"] == "old_library")
    read_choice = next(c for c in lib_room["choices"] if c["id"] == "library_read")

    state = RunState.fresh_run()
    state.lantern = 100
    state.current_room = "old_library"

    # First read
    result1 = resolve_choice(read_choice, state)
    assert result1.refused is False
    assert state.lantern == 100 - CAREFUL_ACTION_DRAIN
    assert state.has_flag("knows_exit") is True

    # Second read: repeats at full cost
    result2 = resolve_choice(read_choice, state)
    assert result2.refused is False
    assert state.lantern == 100 - (2 * CAREFUL_ACTION_DRAIN)
    assert state.has_flag("knows_exit") is True


def test_no_house_prose_hardcoded_in_screens(house_content):
    screens_dir = Path("screens")
    screen_files = list(screens_dir.glob("*.py"))
    assert len(screen_files) > 0

    all_screens_code = "\n".join(f.read_text(encoding="utf-8") for f in screen_files)
    for room in house_content["rooms"]:
        prose = room["prose"]
        assert prose not in all_screens_code, f"House prose was found hardcoded in screens: '{prose}'"


def test_left_doorway_has_two_distinct_telegraphs(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    left_choice = next(c for c in hall_room["choices"] if c["id"] == "hall_left")

    telegraphs = left_choice.get("telegraphs", [])
    assert len(telegraphs) >= 2

    # Distinct in sensory kind: thermal/air vs auditory/dripping
    assert any("warm" in t or "air" in t or "draft" in t for t in telegraphs)
    assert any("dripping" in t or "scrape" in t or "echoes" in t for t in telegraphs)


def test_reaching_the_doorway_produces_a_death_with_a_cause(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    left_choice = next(c for c in hall_room["choices"] if c["id"] == "hall_left")
    assert left_choice.get("tier") == "death"

    death_room = next(r for r in house_content["rooms"] if r["id"] == "left_doorway_death")
    assert death_room.get("tier") == "death"
    assert death_room.get("choices") == []

    cause = left_choice.get("cause") or death_room.get("cause")
    assert isinstance(cause, str)
    assert len(cause.strip()) > 0
    # Must be a single sentence
    assert cause.endswith(".")
    assert cause.count(".") == 1


def test_death_is_unreachable_without_selecting_the_doorway(house_content):
    for room in house_content["rooms"]:
        for choice in room.get("choices", []):
            if choice["id"] != "hall_left":
                assert choice.get("destination") != "left_doorway_death", (
                    f"Choice '{choice['id']}' in room '{room['id']}' unexpectedly leads to death"
                )


def test_run_is_completable_without_the_doorway(house_content):
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    lib_choice = next(c for c in hall_room["choices"] if c["destination"] == "old_library")
    assert lib_choice is not None

    lib_room = next(r for r in house_content["rooms"] if r["id"] == "old_library")
    return_choice = next(c for c in lib_room["choices"] if c["destination"] == "hall")
    assert return_choice is not None


@pytest.mark.anyio
async def test_death_placeholder_receives_cause_and_drains_room_oil(house_content):
    from screens.game import GameScreen
    from tests.test_game_screen import GameScreenTestApp
    from textual.widgets import Static

    app = GameScreenTestApp(content=house_content)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        assert screen.state.current_room == "hall"
        assert screen.state.lantern == 100

        # Navigate down to "hall_left" (choice index 3: front_door, staircase, right, left)
        await pilot.press("down")  # 1
        await pilot.press("down")  # 2
        await pilot.press("down")  # 3
        assert screen.current_choices[screen.selected_choice]["id"] == "hall_left"

        await pilot.press("enter")

        # Destination reached
        assert screen.state.current_room == "left_doorway_death"
        # First-visit entry drain applied (10 oil)
        assert screen.state.lantern == 90
        # Cause recorded on screen
        assert screen.last_death_cause is not None
        assert "butchered in the dark" in screen.last_death_cause

        # Prompt line displays the structured cause
        prompt = screen.query_one("#prompt-line", Static)
        assert screen.last_death_cause in str(prompt.content)


def test_ending_prose_fits_the_line_budget(house_content):
    ending_room = next(r for r in house_content["rooms"] if r["id"] == "front_door_escape")
    prose = ending_room["prose"]
    lines = prose.split("\n")
    # Budget is <= 20 usable lines (ASM-18)
    assert len(lines) <= 20
    assert len(lines) >= 3

    # Quiet, standard win register (§2.3)
    lower = prose.lower()
    assert "survived" in lower or "fog" in lower or "night" in lower
    assert ending_room.get("tier") == "ending"
    assert ending_room.get("choices") == []


def test_both_terminal_states_are_reachable_independently(house_content):
    # Terminal 1: Death
    hall_room = next(r for r in house_content["rooms"] if r["id"] == "hall")
    death_choice = next(c for c in hall_room["choices"] if c["destination"] == "left_doorway_death")
    state_death = RunState.fresh_run()
    res_death = resolve_choice(death_choice, state_death)
    assert res_death.refused is False
    assert res_death.destination == "left_doorway_death"

    # Terminal 2: Escape ending (without visiting death)
    state_escape = RunState.fresh_run()
    lib_choice = next(c for c in hall_room["choices"] if c["destination"] == "old_library")
    res_lib = resolve_choice(lib_choice, state_escape)
    assert res_lib.destination == "old_library"

    lib_room = next(r for r in house_content["rooms"] if r["id"] == "old_library")
    read_choice = next(c for c in lib_room["choices"] if c["id"] == "library_read")
    res_read = resolve_choice(read_choice, state_escape)
    assert res_read.refused is False
    assert state_escape.has_flag("knows_exit") is True

    door_choice = next(c for c in hall_room["choices"] if c["id"] == "hall_front_door")
    res_door = resolve_choice(door_choice, state_escape)
    assert res_door.refused is False
    assert res_door.destination == "front_door_escape"


@pytest.mark.anyio
async def test_second_visit_to_hall_presents_echo_prose(house_content):
    from screens.game import GameScreen
    from tests.test_game_screen import GameScreenTestApp
    from textual.widgets import Static

    app = GameScreenTestApp(content=house_content)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # First visit: hall initial prose
        text_widget = screen.query_one("#scene-text", Static)
        assert "swollen shut" in str(text_widget.content)

        # Move to library (choice 2)
        await pilot.press("down")  # 1: staircase
        await pilot.press("down")  # 2: old_library
        await pilot.press("enter")
        assert screen.state.current_room == "old_library"

        # Return to hall (choice 1 in library: 0 is read, 1 is return)
        await pilot.press("down")  # 1: library_return
        await pilot.press("enter")
        assert screen.state.current_room == "hall"

        # Second visit: echo prose acknowledged (Pillar 3)
        revisit_text = screen.query_one("#scene-text", Static)
        assert "You step back into the vaulted silence" in str(revisit_text.content)




