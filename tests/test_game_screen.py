from pathlib import Path
import pytest
from textual.app import App
from textual.widgets import Static

from screens.game import GameScreen
from game.content_schema import SAMPLE_CONTENT


class GameScreenTestApp(App):
    def __init__(self, content=None, state=None):
        super().__init__()
        self._content = content
        self._state = state

    async def on_mount(self) -> None:
        await self.push_screen(GameScreen(content=self._content, state=self._state))


@pytest.mark.anyio
async def test_game_screen_mounts_with_three_zones():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        # Verify Scene Zone and sub-elements
        scene_zone = screen.query_one("#scene-zone")
        assert scene_zone is not None
        assert screen.query_one("#scene-header") is not None
        assert screen.query_one("#scene-text") is not None
        assert screen.query_one("#scene-telegraphs") is not None
        assert screen.query_one("#scene-choices") is not None

        # Verify Status Zone and sub-elements
        status_zone = screen.query_one("#status-zone")
        assert status_zone is not None
        assert screen.query_one("#status-resources") is not None
        assert screen.query_one("#lantern-status") is not None
        assert screen.query_one("#composure-status") is not None
        assert screen.query_one("#prompt-line") is not None

        # Verify Footer Zone
        footer_zone = screen.query_one("#footer-zone")
        assert footer_zone is not None


@pytest.mark.anyio
async def test_footer_lists_key_hints():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        bindings = {b[0]: b[2] for b in screen.BINDINGS}
        assert "up" in bindings
        assert "down" in bindings
        assert "enter" in bindings
        assert "escape" in bindings


@pytest.mark.anyio
async def test_screen_renders_room_name_and_prose():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        start_room_id = SAMPLE_CONTENT["start_room"]
        start_room = next(r for r in SAMPLE_CONTENT["rooms"] if r["id"] == start_room_id)

        header = screen.query_one("#scene-header", Static)
        text = screen.query_one("#scene-text", Static)

        assert str(header.content) == start_room["name"]
        assert str(text.content) == start_room["prose"]
        assert screen.state.current_room == start_room_id
        assert screen.state.has_visited(start_room_id)


def test_unknown_room_id_fails_loudly():
    screen = GameScreen()
    with pytest.raises(KeyError, match="Unknown room id: 'nonexistent_chamber'"):
        screen.get_room("nonexistent_chamber")


def test_no_room_prose_hardcoded_in_screens():
    screens_dir = Path("screens")
    screen_files = list(screens_dir.glob("*.py"))
    assert len(screen_files) > 0

    all_screens_code = "\n".join(f.read_text(encoding="utf-8") for f in screen_files)
    for room in SAMPLE_CONTENT["rooms"]:
        prose = room["prose"]
        assert prose not in all_screens_code, f"Room prose was found hardcoded in screens: '{prose}'"


@pytest.mark.anyio
async def test_arrow_keys_move_the_choice_cursor():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        assert screen.selected_choice == 0
        assert len(screen.current_choices) == 2

        # Move down
        await pilot.press("down")
        assert screen.selected_choice == 1

        # Move down again (wraps to 0)
        await pilot.press("down")
        assert screen.selected_choice == 0

        # Move up (wraps to 1)
        await pilot.press("up")
        assert screen.selected_choice == 1


@pytest.mark.anyio
async def test_selecting_a_choice_moves_to_its_destination():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        # Select second choice: "Take the right-hand passage" -> "old_library"
        await pilot.press("down")
        await pilot.press("enter")

        assert screen.state.current_room == "old_library"
        assert screen.state.turn_count == 1

        header = screen.query_one("#scene-header", Static)
        assert str(header.content) == "Old Library"


@pytest.mark.anyio
async def test_refused_choice_shows_reason_and_does_not_move():
    gated_content = {
        "start_room": "gated_room",
        "rooms": [
            {
                "id": "gated_room",
                "name": "Gated Room",
                "prose": "A locked gate.",
                "choices": [
                    {
                        "id": "open_gate",
                        "label": "Open the iron gate",
                        "destination": "inner_sanctum",
                        "requirements": [{"predicate": "has_item", "item": "iron_key"}],
                    }
                ],
            },
            {
                "id": "inner_sanctum",
                "name": "Inner Sanctum",
                "prose": "Within.",
                "choices": [],
            },
        ],
    }

    app = GameScreenTestApp(content=gated_content)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        assert screen.state.current_room == "gated_room"

        await pilot.press("enter")

        # Did not transition
        assert screen.state.current_room == "gated_room"
        assert screen.state.turn_count == 0

        prompt = screen.query_one("#prompt-line", Static)
        assert "requires item 'iron_key'" in str(prompt.content)


@pytest.mark.anyio
async def test_unselectable_choice_never_ends_the_run():
    gated_content = {
        "start_room": "gated_room",
        "rooms": [
            {
                "id": "gated_room",
                "name": "Gated Room",
                "prose": "A locked gate.",
                "choices": [
                    {
                        "id": "fatal_looking_gate",
                        "label": "Force the lock",
                        "destination": "death_room",
                        "tier": "death",
                        "telegraphs": [
                            "Poison needles gleam in the keyhole.",
                            "A dead rat lies beneath the lock mechanism.",
                        ],
                        "requirements": [{"predicate": "has_flag", "flag": "impossible_flag"}],
                    }
                ],
            },
            {
                "id": "death_room",
                "name": "Death Room",
                "prose": "You perished.",
                "choices": [],
            },
        ],
    }

    app = GameScreenTestApp(content=gated_content)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        await pilot.press("enter")
        # Run state remains alive and unchanged
        assert screen.state.current_room == "gated_room"
        assert screen.state.has_light() is True


def test_lantern_bar_reflects_state_value():
    assert GameScreen.render_lantern_bar(100) == "██████████"
    assert GameScreen.render_lantern_bar(50) == "█████░░░░░"
    assert GameScreen.render_lantern_bar(30) == "███░░░░░░░"
    assert GameScreen.render_lantern_bar(0) == "░░░░░░░░░░"
    assert GameScreen.render_lantern_bar(-10) == "░░░░░░░░░░"
    assert GameScreen.render_lantern_bar(150) == "██████████"


@pytest.mark.anyio
async def test_status_zone_shows_turn_count():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        turn_widget = screen.query_one("#turn-status", Static)
        assert str(turn_widget.content) == "turn 0"

        # Make a move
        await pilot.press("enter")
        assert str(turn_widget.content) == "turn 1"


@pytest.mark.anyio
async def test_low_oil_warning_uses_amber_not_red():
    from game.state import RunState
    low_oil_state = RunState.fresh_run()
    low_oil_state.lantern = 20  # below threshold 30

    app = GameScreenTestApp(state=low_oil_state)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        lantern_widget = screen.query_one("#lantern-status", Static)
        rendered_text = str(lantern_widget.content)

        # Must indicate low oil
        assert "low oil" in rendered_text
        # Guarding §7.4 red reservation:
        assert "red" not in rendered_text.lower()
        # Uses Amber
        assert screen.AMBER_COLOR in rendered_text


@pytest.mark.anyio
async def test_turn_counter_has_no_explanatory_label():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)

        turn_widget = screen.query_one("#turn-status", Static)
        rendered = str(turn_widget.content).lower()

        # Mechanical check of §3.5: No explanatory or escalation labels
        prohibited_words = ["danger", "dread", "death", "limit", "time", "clock", "warning", "threat"]
        for word in prohibited_words:
            assert word not in rendered, f"Turn counter leaked explanatory label: '{word}'"
