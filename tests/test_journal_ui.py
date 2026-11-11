"""Tests for Journal overlay screen UI and keybinds (Task E03)."""
import pytest
from textual.app import App, ComposeResult
from textual.widgets import Static

from game.journal import Journal
from screens.game import GameScreen
from screens.journal import JournalScreen
from tests.test_game_screen import GameScreenTestApp


class JournalHostApp(App[None]):
    def __init__(self, journal: Journal) -> None:
        super().__init__()
        self._journal = journal

    def compose(self) -> ComposeResult:
        yield from ()

    def on_mount(self) -> None:
        self.push_screen(JournalScreen(self._journal))


@pytest.mark.anyio
async def test_journal_screen_mounts_cleanly():
    """JournalScreen renders populated sections without error."""
    journal = Journal()
    journal.add_room("hall", "The Hall", "Cold stone arches.")
    journal.add_death("Butchered in darkness", "Never step blindly.")
    journal.add_shadow_line("The flame is guttering...", "Near alcove")

    app = JournalHostApp(journal)
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, JournalScreen)

        # Check rendered content contains entries
        text_widget = screen.query_one("#journal-text", Static)
        rendered = str(text_widget.content)
        assert "The Hall" in rendered
        assert "Butchered in darkness" in rendered
        assert "The flame is guttering..." in rendered


@pytest.mark.anyio
async def test_journal_screen_empty_state():
    """Mounting with an empty journal displays the graceful blank-pages message."""
    empty_journal = Journal()
    app = JournalHostApp(empty_journal)

    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, JournalScreen)

        text_widget = screen.query_one("#journal-text", Static)
        rendered = str(text_widget.content)
        assert "pages are blank" in rendered.lower()


@pytest.mark.anyio
async def test_journal_keybind_registered():
    """Pressing 'j' during gameplay opens the JournalScreen, and 'escape' returns."""
    from game.content_schema import load_content
    from game.state import RunState
    from pathlib import Path

    content = load_content(Path("data/content.json"))
    state = RunState.fresh_run()
    app = GameScreenTestApp(content=content, state=state)

    async with app.run_test() as pilot:
        game_screen = pilot.app.screen
        assert isinstance(game_screen, GameScreen)

        # Press 'j' to open journal
        await pilot.press("j")
        top_screen = pilot.app.screen
        assert isinstance(top_screen, JournalScreen)

        # Press 'escape' to dismiss
        await pilot.press("escape")
        restored_screen = pilot.app.screen
        assert isinstance(restored_screen, GameScreen)
