"""Tests for inventory display and the drop-to-take UI flow in GameScreen."""
import pytest
from textual.app import App, ComposeResult
from textual.widgets import Static

from game.state import RunState
from screens.game import GameScreen


SAMPLE_ITEMS_CONTENT = {
    "start_room": "hall",
    "items": [
        {"id": "matchbox", "name": "Matchbox", "description": "Three sulfur matches"},
        {"id": "the_book", "name": "The Book", "description": "Leather-bound book"},
        {"id": "rusty_cleaver", "name": "Rusty Cleaver", "description": "Heavy blade"},
        {"id": "silver_whistle", "name": "Silver Whistle", "description": "Tarnished whistle"},
        {"id": "dogs_tooth", "name": "Dog's Tooth", "description": "Sharp canine"},
        {"id": "front_door_key", "name": "Front Door Key", "description": "Wrought iron key"},
        {"id": "bone_token", "name": "Bone Token", "description": "Carved bone"},
    ],
    "rooms": [
        {
            "id": "hall",
            "name": "Entrance Hall",
            "prose": "Cold stone floor.",
            "choices": [
                {
                    "id": "take_bone_token",
                    "label": "Take Bone Token",
                    "destination": "hall",
                    "requirements": [{"predicate": "has_free_slot"}],
                    "effects": [{"verb": "grant_item", "item": "bone_token"}],
                }
            ],
        }
    ],
}


class GameScreenHostApp(App[None]):
    def __init__(self, screen: GameScreen) -> None:
        super().__init__()
        self._screen = screen

    def compose(self) -> ComposeResult:
        yield from ()

    def on_mount(self) -> None:
        self.push_screen(self._screen)


@pytest.mark.anyio
async def test_inventory_renders_in_the_status_zone() -> None:
    state = RunState.fresh_run()
    screen = GameScreen(content=SAMPLE_ITEMS_CONTENT, state=state)
    app = GameScreenHostApp(screen)

    async with app.run_test():
        status_zone = screen.query_one("#status-zone")
        inv_widget = status_zone.query_one("#inventory-status")
        assert inv_widget is not None


@pytest.mark.anyio
async def test_empty_inventory_renders_a_deliberate_state() -> None:
    state = RunState.fresh_run()
    screen = GameScreen(content=SAMPLE_ITEMS_CONTENT, state=state)
    app = GameScreenHostApp(screen)

    async with app.run_test():
        inv_text = screen.render_inventory_status()
        assert "0/6" in inv_text
        assert "carrying nothing" in inv_text


@pytest.mark.anyio
async def test_full_pack_is_visible_before_a_refusal() -> None:
    state = RunState.fresh_run()
    for item in ["matchbox", "rusty_cleaver", "the_book", "silver_whistle", "dogs_tooth", "front_door_key"]:
        state.add_item(item)
    assert len(state.held_items) == 6

    screen = GameScreen(content=SAMPLE_ITEMS_CONTENT, state=state)
    app = GameScreenHostApp(screen)

    async with app.run_test():
        inv_text = screen.render_inventory_status()
        assert "6/6 FULL" in inv_text
        assert "Matchbox" in inv_text
        assert "Front Door Key" in inv_text


@pytest.mark.anyio
async def test_drop_then_take_completes_the_original_action() -> None:
    state = RunState.fresh_run()
    for item in ["matchbox", "rusty_cleaver", "the_book", "silver_whistle", "dogs_tooth", "front_door_key"]:
        state.add_item(item)
    assert len(state.held_items) == 6

    screen = GameScreen(content=SAMPLE_ITEMS_CONTENT, state=state)
    app = GameScreenHostApp(screen)

    async with app.run_test():
        # Select first choice ("Take Bone Token") which fails due to full pack
        screen.action_select()
        assert screen.drop_mode is True

        # Drop options displayed: 0..5 are held items, 6 is Cancel
        # Drop selected is 0 ("matchbox")
        screen.action_select()

        # Matchbox should be dropped, and bone_token should now be held
        assert screen.drop_mode is False
        assert "matchbox" not in state.held_items
        assert "bone_token" in state.held_items
        assert len(state.held_items) == 6


@pytest.mark.anyio
async def test_cancel_leaves_state_completely_unchanged() -> None:
    state = RunState.fresh_run()
    for item in ["matchbox", "rusty_cleaver", "the_book", "silver_whistle", "dogs_tooth", "front_door_key"]:
        state.add_item(item)
    original_items = list(state.held_items)

    screen = GameScreen(content=SAMPLE_ITEMS_CONTENT, state=state)
    app = GameScreenHostApp(screen)

    async with app.run_test():
        # Trigger drop mode
        screen.action_select()
        assert screen.drop_mode is True

        # Cancel via action_back (Escape)
        screen.action_back()

        assert screen.drop_mode is False
        assert state.held_items == original_items
        assert "bone_token" not in state.held_items
