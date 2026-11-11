from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Vertical, Horizontal, Container


class GameScreen(Screen):
    """The central gameplay screen featuring three fixed zones: scene, status, and footer."""

    CSS = """
    GameScreen {
        background: #0d0d0d;
        color: #d0d0d0;
    }

    #game-container {
        width: 100%;
        height: 100%;
        layout: vertical;
    }

    /* Scene Zone - upper section for room text and choices (never scrolls internally) */
    #scene-zone {
        height: 1fr;
        min-height: 16;
        border: solid #333333;
        padding: 1 2;
        background: #111111;
    }

    #scene-header {
        height: 1;
        dock: top;
        color: #ffffff;
        text-style: bold;
    }

    #scene-text {
        color: #8a8a8a;
        margin-top: 1;
        margin-bottom: 1;
    }

    #scene-choices {
        height: auto;
        margin-top: 1;
    }

    /* Status Zone - middle/lower section for vital bars and prompt line */
    #status-zone {
        height: auto;
        min-height: 4;
        border-top: solid #444444;
        border-bottom: solid #444444;
        padding: 0 2;
        background: #141414;
    }

    #status-resources {
        height: 1;
        layout: horizontal;
        color: #d4a373; /* Amber for time/light/resources */
    }

    #lantern-status {
        width: 1fr;
    }

    #composure-status {
        width: 1fr;
        text-align: right;
    }

    #prompt-line {
        height: 1;
        color: #48cae4; /* Cyan for player actions */
    }

    /* Footer Zone */
    #footer-zone {
        height: 1;
        dock: bottom;
        background: #000000;
        color: #666666;
    }
    """

    BINDINGS = [
        ("up", "move_up", "Navigate Up"),
        ("down", "move_down", "Navigate Down"),
        ("enter", "select", "Select"),
        ("escape", "back", "Back"),
    ]

    def compose(self):
        with Vertical(id="game-container"):
            with Vertical(id="scene-zone"):
                yield Static("", id="scene-header")
                yield Static("", id="scene-text")
                yield Container(id="scene-choices")
            with Vertical(id="status-zone"):
                with Horizontal(id="status-resources"):
                    yield Static("", id="lantern-status")
                    yield Static("", id="composure-status")
                yield Static("> ", id="prompt-line")
        yield Footer(id="footer-zone")

    def action_move_up(self) -> None:
        pass

    def action_move_down(self) -> None:
        pass

    def action_select(self) -> None:
        pass

    def action_back(self) -> None:
        self.app.pop_screen()
