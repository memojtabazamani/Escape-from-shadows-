import pytest
from textual.app import App, ComposeResult
from screens.game import GameScreen


class GameScreenTestApp(App):
    def compose(self) -> ComposeResult:
        yield GameScreen()


@pytest.mark.anyio
async def test_game_screen_mounts_with_three_zones():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.query_one(GameScreen)
        assert screen is not None

        # Verify Scene Zone and sub-elements
        scene_zone = screen.query_one("#scene-zone")
        assert scene_zone is not None
        assert screen.query_one("#scene-header") is not None
        assert screen.query_one("#scene-text") is not None
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
        screen = pilot.app.query_one(GameScreen)
        bindings = {b[0]: b[2] for b in screen.BINDINGS}
        assert "up" in bindings
        assert "down" in bindings
        assert "enter" in bindings
        assert "escape" in bindings
