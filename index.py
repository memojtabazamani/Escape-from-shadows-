from typing import Optional
from textual.app import App

from config import SettingsManager
from game.state import RunState
from screens.main_menu import MainMenuScreen


class TerminalGame(App):
    CSS = """
    Screen {
        align: center middle;
        background: #101820;
    }

    #panel {
        width: 60;
        height: auto;
        border: round cyan;
        padding: 2 4;
        background: #17232d;
    }

    #title {
        text-align: center;
        color: cyan;
        text-style: bold;
        padding-bottom: 1;
    }

    #subtitle {
        text-align: center;
        color: #94a3b8;
        padding-bottom: 2;
    }
    """

    def __init__(self):
        super().__init__()
        self.config = SettingsManager()
        self.active_run: Optional[RunState] = None

    def on_mount(self):
        self.push_screen(MainMenuScreen())


if __name__ == "__main__":
    app = TerminalGame()
    app.run()
