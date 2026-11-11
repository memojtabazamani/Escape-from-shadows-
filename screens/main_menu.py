from pathlib import Path
from textual.app import App
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Center, Middle, Vertical

from config import SettingsManager
from game.content_schema import load_content
from game.state import RunState
from screens.game import GameScreen
from screens.settings import SettingsScreen


class MainMenuScreen(Screen):
    CSS = """
    #menu {
        height: auto;
        padding: 1 2;
        color: white;
    }

    #status {
        color: green;
        text-align: center;
        padding-top: 2;
    }
    """

    BINDINGS = [
        ("up", "move_up", "Up"),
        ("down", "move_down", "Down"),
        ("enter", "select", "Select"),
        ("escape", "quit", "Exit"),
    ]

    def __init__(self):
        super().__init__()
        from game.save import has_saved_game
        if has_saved_game():
            self.options = ["CONTINUE", "START GAME", "SETTINGS", "ABOUT", "EXIT"]
        else:
            self.options = ["START GAME", "SETTINGS", "ABOUT", "EXIT"]
        self.selected = 0

    def refresh_options(self) -> None:
        from game.save import has_saved_game
        if has_saved_game():
            self.options = ["CONTINUE", "START GAME", "SETTINGS", "ABOUT", "EXIT"]
            self.selected = 0
        else:
            self.options = ["START GAME", "SETTINGS", "ABOUT", "EXIT"]
            if self.selected >= len(self.options):
                self.selected = 0

        try:
            self.update_menu()
        except Exception:
            pass

    def on_mount(self) -> None:
        self.refresh_options()

    def on_screen_resume(self) -> None:
        self.refresh_options()

    def compose(self):
        with Center():
            with Middle():
                with Vertical(id="panel"):
                    yield Static("DARK QUEST", id="title")
                    yield Static("A TERMINAL ADVENTURE", id="subtitle")
                    yield Static(self.render_menu(), id="menu")
                    yield Static("Welcome, Adventurer!", id="status")
        yield Footer()

    def render_menu(self):
        lines = []
        for index, option in enumerate(self.options):
            if index == self.selected:
                lines.append(f"[bold cyan]  > {option}[/]")
            else:
                lines.append(f"    {option}")
        return "\n\n".join(lines)

    def update_menu(self):
        menu = self.query_one("#menu", Static)
        menu.update(self.render_menu())

    def action_move_up(self):
        self.selected = (self.selected - 1) % len(self.options)
        self.update_menu()

    def action_move_down(self):
        self.selected = (self.selected + 1) % len(self.options)
        self.update_menu()

    def action_select(self):
        selected_option = self.options[self.selected]
        status = self.query_one("#status", Static)

        if selected_option == "CONTINUE":
            from game.save import load_from_disk
            restored_state = load_from_disk()
            if restored_state:
                status.update("Resuming run...")
                if hasattr(self.app, "active_run"):
                    self.app.active_run = restored_state
                content_path = Path("data/content.json")
                content = load_content(content_path) if content_path.exists() else None
                self.app.push_screen(GameScreen(content=content, state=restored_state))
            else:
                status.update("No save found.")
                self.refresh_options()
        elif selected_option == "START GAME":
            from game.save import delete_saved_game
            delete_saved_game()
            status.update("Entering the house...")
            diff = "MEDIUM"
            if hasattr(self.app, "config") and hasattr(self.app.config, "get"):
                diff = self.app.config.get("difficulty") or "MEDIUM"
            fresh_run = RunState.fresh_run(difficulty=diff)
            if hasattr(self.app, "active_run"):
                self.app.active_run = fresh_run
            content_path = Path("data/content.json")
            content = load_content(content_path) if content_path.exists() else None
            self.app.push_screen(GameScreen(content=content, state=fresh_run))
        elif selected_option == "SETTINGS":
            status.update("Settings selected.")
            self.app.push_screen(SettingsScreen())
        elif selected_option == "ABOUT":
            status.update("Dark Quest - Version 1.0")
        elif selected_option == "EXIT":
            self.app.exit()
