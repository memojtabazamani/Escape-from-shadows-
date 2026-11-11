import pytest
from textual.app import App
from textual.widgets import Static

from screens.death import DeathScreen
from game.state import RunState


class DeathScreenDifficultyHostApp(App):
    def __init__(self, difficulty="MEDIUM", could_have_done="Light your match before proceeding."):
        super().__init__()
        self._difficulty = difficulty
        self._could_have_done = could_have_done
        self.config = {"difficulty": difficulty}

    async def on_mount(self) -> None:
        state = RunState.fresh_run(difficulty=self._difficulty)
        await self.push_screen(
            DeathScreen(
                cause="The floor gave way in the pitch black.",
                lesson="A light source reveals rotting timbers.",
                could_have_done=self._could_have_done,
                state=state,
            )
        )


@pytest.mark.anyio
async def test_hint_rendered_on_easy():
    app = DeathScreenDifficultyHostApp(difficulty="EASY", could_have_done="Light your match before proceeding.")
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, DeathScreen)

        hint_widget = screen.query_one("#death-could-have-done", Static)
        assert str(hint_widget.content).strip() != ""
        assert "Could have done:" in str(hint_widget.content)
        assert "Light your match before proceeding." in str(hint_widget.content)


@pytest.mark.anyio
async def test_hint_hidden_on_medium_and_hard():
    for diff in ["MEDIUM", "HARD"]:
        app = DeathScreenDifficultyHostApp(difficulty=diff, could_have_done="Light your match before proceeding.")
        async with app.run_test() as pilot:
            screen = pilot.app.screen
            assert isinstance(screen, DeathScreen)

            hint_widget = screen.query_one("#death-could-have-done", Static)
            # On MEDIUM and HARD, hint is empty string / hidden
            assert str(hint_widget.content).strip() == ""
