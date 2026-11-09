from textual.app import App
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Center, Middle, Vertical

from config import SettingsManager
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
        self.options = ["START GAME", "SETTINGS", "ABOUT", "EXIT"]
        self.selected = 0

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

        if selected_option == "START GAME":
            difficulty = self.app.config.get("difficulty", "MEDIUM")
            status.update(f"Starting game with difficulty: {difficulty}...")
        elif selected_option == "SETTINGS":
            status.update("Settings selected.")
            self.push_screen(SettingsScreen())
        elif selected_option == "ABOUT":
            status.update("Dark Quest - Version 1.0")
        elif selected_option == "EXIT":
            self.app.exit()
