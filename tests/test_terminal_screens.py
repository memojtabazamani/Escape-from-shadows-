import pytest
from textual.app import App
from textual.widgets import Static

from screens.death import DeathScreen
from screens.ending import EndingScreen
from screens.game import GameScreen
from screens.main_menu import MainMenuScreen
from game.content_schema import load_content
from game.state import RunState


class DeathScreenTestApp(App):
    def __init__(self, cause="A falling stone crushed your lantern.", lesson="", content=None):
        super().__init__()
        self._cause = cause
        self._lesson = lesson
        self._content = content
        self.active_run = RunState.fresh_run()

    async def on_mount(self) -> None:
        await self.push_screen(
            DeathScreen(
                cause=self._cause,
                lesson=self._lesson,
                content=self._content,
            )
        )


class EndingScreenTestApp(App):
    def __init__(self, room=None, content=None):
        super().__init__()
        self._room = room or {
            "id": "front_door_escape",
            "name": "The Threshold of Night",
            "prose": "You slip outside into the biting night fog. You survived.",
            "tier": "ending",
            "choices": [],
        }
        self._content = content
        self.active_run = RunState.fresh_run()

    async def on_mount(self) -> None:
        await self.push_screen(
            EndingScreen(
                room=self._room,
                content=self._content,
            )
        )


@pytest.mark.anyio
async def test_death_screen_shows_the_cause_verbatim():
    structured_cause = "You stepped blindly past the warned threshold and were butchered in the dark."
    app = DeathScreenTestApp(cause=structured_cause)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)

        cause_widget = screen.query_one("#death-cause", Static)
        assert str(cause_widget.content) == structured_cause


@pytest.mark.anyio
async def test_death_screen_offers_again_and_menu():
    app = DeathScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)

        assert screen.options == ["AGAIN", "BACK TO MENU"]
        assert screen.selected == 0

        # Down moves to BACK TO MENU
        await pilot.press("down")
        assert screen.selected == 1

        # Down wraps to AGAIN
        await pilot.press("down")
        assert screen.selected == 0

        # Up wraps to BACK TO MENU
        await pilot.press("up")
        assert screen.selected == 1


@pytest.mark.anyio
async def test_back_to_menu_leaves_no_resumable_state():
    app = DeathScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)
        assert app.active_run is not None

        # Select BACK TO MENU
        await pilot.press("down")
        await pilot.press("enter")

        # Active run is cleared
        assert app.active_run is None


@pytest.mark.anyio
async def test_ending_screen_shows_the_ending_and_returns():
    room_data = {
        "id": "front_door_escape",
        "name": "The Threshold of Night",
        "prose": "You slip outside into the biting night fog. You survived.",
        "tier": "ending",
        "choices": [],
    }
    app = EndingScreenTestApp(room=room_data)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, EndingScreen)

        title_widget = screen.query_one("#ending-title", Static)
        prose_widget = screen.query_one("#ending-prose", Static)
        assert str(title_widget.content) == room_data["name"]
        assert str(prose_widget.content) == room_data["prose"]

        # Back to menu clears active run
        assert app.active_run is not None
        await pilot.press("down")  # Select BACK TO MENU
        await pilot.press("enter")
        assert app.active_run is None


def test_death_screen_uses_no_ascii_art():
    import inspect
    from screens import death

    source = inspect.getsource(death)
    # Mechanical check: No multiline ASCII art strings or drawings
    # §7.3 reserves ASCII art for title, Hell Dog, and endings.
    for line in source.splitlines():
        trimmed = line.strip()
        if trimmed.startswith(("#", '"""', "'''")):
            continue
        assert not any(symbol * 4 in trimmed for symbol in ["/", "\\", "|", "_", "*", "#"]), (
            f"Suspicious ASCII art pattern found in death screen: {trimmed}"
        )


@pytest.mark.anyio
async def test_red_reservation_strictly_enforced():
    """§7.4: Red is strictly reserved for the Shadow.

    If the Shadow caused the death, red appears on the title.
    If another entity (e.g. butcher's iron) caused the death, red is NOT used.
    """
    # Non-shadow death: no red in title
    app_non_shadow = DeathScreenTestApp(cause="You were butchered by jagged iron.")
    async with app_non_shadow.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)
        title_text = screen.render_title()
        assert "red" not in title_text.lower()
        assert "#e63946" not in title_text

    # Shadow death: red is permitted for Shadow
    app_shadow = DeathScreenTestApp(cause="The lantern died and the Shadow claimed you.")
    async with app_shadow.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)
        title_text = screen.render_title()
        assert "#e63946" in title_text


@pytest.mark.anyio
async def test_death_screen_frame_accommodates_i03_and_i04_reserved_regions():
    """Verify that DeathScreen has placeholder DOM nodes for I03 and I04 without restructuring."""
    app = DeathScreenTestApp(
        cause="Lethal strike.",
        lesson="Listen to the sound of dripping next time.",
    )
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)
        assert screen.query_one("#death-cause") is not None
        assert screen.query_one("#death-learned") is not None
        assert screen.query_one("#death-could-have-done") is not None


class GameRoutingTestApp(App):
    def __init__(self, content=None, state=None):
        super().__init__()
        self._content = content
        self._state = state

    async def on_mount(self) -> None:
        await self.push_screen(GameScreen(content=self._content, state=self._state))


@pytest.mark.anyio
async def test_game_screen_routes_death_to_death_screen():
    content = load_content("data/content.json")
    app = GameRoutingTestApp(content=content)

    async with app.run_test() as pilot:
        # Navigate to left archway (choice index 3)
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("down")
        await pilot.press("enter")

        # Top screen is now DeathScreen
        top_screen = pilot.app.screen
        assert isinstance(top_screen, DeathScreen)
        cause_widget = top_screen.query_one("#death-cause", Static)
        assert "butchered in the dark" in str(cause_widget.content)


@pytest.mark.anyio
async def test_game_screen_routes_ending_to_ending_screen():
    content = load_content("data/content.json")
    state = RunState.fresh_run()
    state.set_flag("knows_exit")

    app = GameRoutingTestApp(content=content, state=state)

    async with app.run_test() as pilot:
        # Front door choice is at index 0 and has flag 'knows_exit'
        await pilot.press("enter")

        # Top screen is now EndingScreen
        top_screen = pilot.app.screen
        assert isinstance(top_screen, EndingScreen)
        prose_widget = top_screen.query_one("#ending-prose", Static)
        assert "survived" in str(prose_widget.content).lower()
