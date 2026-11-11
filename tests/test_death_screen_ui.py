import pytest
from textual.app import App
from textual.widgets import Static

from screens.death import DeathScreen
from game.state import RunState


class DeathScreenHostApp(App):
    def __init__(self, cause="Death strikes.", lesson="", could_have_done="", state=None):
        super().__init__()
        self._cause = cause
        self._lesson = lesson
        self._could_have_done = could_have_done
        self._state = state or RunState.fresh_run()

    async def on_mount(self) -> None:
        await self.push_screen(
            DeathScreen(
                cause=self._cause,
                lesson=self._lesson,
                could_have_done=self._could_have_done,
                state=self._state,
            )
        )


@pytest.mark.anyio
async def test_death_screen_renders_cause_and_lesson():
    app = DeathScreenHostApp(
        cause="You stepped into the razor pit.",
        lesson="Look before stepping into unlit cellar depressions.",
    )
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)

        cause_widget = screen.query_one("#death-cause", Static)
        assert "You stepped into the razor pit." in str(cause_widget.content)

        learned_widget = screen.query_one("#death-learned", Static)
        assert "What you learned:" in str(learned_widget.content)
        assert "Look before stepping into unlit cellar depressions." in str(learned_widget.content)


@pytest.mark.anyio
async def test_death_screen_buttons_present():
    app = DeathScreenHostApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)
        assert screen.options == ["AGAIN", "BACK TO MENU"]
        assert screen.selected == 0

        menu_widget = screen.query_one("#death-menu", Static)
        assert "AGAIN" in str(menu_widget.content)
        assert "BACK TO MENU" in str(menu_widget.content)


@pytest.mark.anyio
async def test_death_screen_fallback_lesson():
    app = DeathScreenHostApp(cause="Sudden darkness.", lesson="")
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)

        learned_widget = screen.query_one("#death-learned", Static)
        assert "heed the oil reserve" in str(learned_widget.content)
