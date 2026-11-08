from textual.widgets import Static, Footer
from textual.containers import Center, Middle, Vertical
from textual.screen import Screen

from config import SettingsManager


class SettingsScreen(Screen):
    CSS = """
        #menu {
        color: red
          }
    """
    BINDINGS = [
        ("up", "move_up", "Up"),
        ("down", "move_down", "Down"),
        ("left", "prev_difficulty", "Prev Value"),
        ("right", "next_difficulty", "Next Value"),
        ("enter", "select", "Select"),
        ("escape", "quit", "Back"),
    ]

    DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]
    SOUND_MUSIC_OPTIONS = ["OFF", "ON"]

    def __init__(self):
        super().__init__()
        self.options = [
            "DIFFICULTY",
            "SOUND",
            "MUSIC",
            "EXIT",
        ]
        self.selected = 0
        self.diff_index = 1
        self.music_enable = True
        self.sound_enable = True

    @property
    def config(self) -> SettingsManager:
        """Shortcut to the application's settings manager."""
        return self.app.config

    def on_mount(self):
        """Load the persisted values into the settings screen."""
        current_difficulty = self.config.get("difficulty", "MEDIUM")
        if current_difficulty in self.DIFFICULTIES:
            self.diff_index = self.DIFFICULTIES.index(current_difficulty)
        else:
            self.diff_index = 1

        self.sound_enable = self.config.get("sound", True)
        self.music_enable = self.config.get("music", True)
        self.update_menu()

    def compose(self):
        with Center():
            with Middle():
                with Vertical(id="panel"):
                    yield Static("SETTINGS", id="title")
                    yield Static("CONFIGURE YOUR GAME", id="subtitle")
                    yield Static(self.render_menu(), id="menu")
                    yield Static("Use Enter or Arrow keys to change values", id="status")
        yield Footer()

    def _persist_state(self) -> None:
        """Update the in-memory config and save it immediately."""
        self.config.set("difficulty", self.DIFFICULTIES[self.diff_index])
        self.config.set("sound", self.sound_enable)
        self.config.set("music", self.music_enable)

    def toggle_sound(self):
        self.sound_enable = not self.sound_enable
        self._persist_state()
        self.update_menu()
        current_sound = self.SOUND_MUSIC_OPTIONS[self.sound_enable]
        self.query_one("#status", Static).update(f"Sound set to {current_sound}")

    def toggle_music(self):
        self.music_enable = not self.music_enable
        self._persist_state()
        self.update_menu()
        current_music = self.SOUND_MUSIC_OPTIONS[self.music_enable]
        self.query_one("#status", Static).update(f"Music set to {current_music}")

    def render_menu(self):
        lines = []
        for index, option in enumerate(self.options):
            if option == "DIFFICULTY":
                current_diff = self.DIFFICULTIES[self.diff_index]
                display_text = f"DIFFICULTY:  < {current_diff} >"
            else:
                display_text = option
            if option == "SOUND":
                current_sound = self.SOUND_MUSIC_OPTIONS[self.sound_enable]
                display_text = f"SOUND: < {current_sound} >"
            if option == "MUSIC":
                current_music = self.SOUND_MUSIC_OPTIONS[self.music_enable]
                display_text = f"MUSIC: < {current_music} >"
            if index == self.selected:
                lines.append(f"[bold cyan]  > {display_text}[/]")
            else:
                lines.append(f"    {display_text}")

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

    def cycle_difficulty(self, step=1):
        self.diff_index = (self.diff_index + step) % len(self.DIFFICULTIES)
        self._persist_state()
        self.update_menu()
        selected_diff = self.DIFFICULTIES[self.diff_index]
        self.query_one("#status", Static).update(f"Difficulty set to {selected_diff}")

    def action_next_difficulty(self):
        if self.options[self.selected] == "DIFFICULTY":
            self.cycle_difficulty(1)

    def action_prev_difficulty(self):
        if self.options[self.selected] == "DIFFICULTY":
            self.cycle_difficulty(-1)

    def action_select(self):
        current_option = self.options[self.selected]
        status = self.query_one("#status", Static)

        if current_option == "DIFFICULTY":
            self.cycle_difficulty(1)
        elif current_option == "SOUND":
            self.toggle_sound()
        elif current_option == "MUSIC":
            self.toggle_music()
        elif current_option == "EXIT":
            self.app.pop_screen()

    def action_quit(self):
        self.app.pop_screen()
