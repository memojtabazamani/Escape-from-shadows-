"""Ending screen component for Escape from Shadows.

Follows SUGGEST.md §2.3 and §9.2:
- Renders the ending room's name and prose verbatim from structured data.
- Quiet, standard win register (an exit into cold night air, not an epic triumph).
- Allowed minimal ASCII border marker per §7.3 ("each ending").
- Navigation options: "AGAIN" and "BACK TO MENU".
- "Back to menu" clears any active run state on app so no resumable state lingers.
"""

from __future__ import annotations

from typing import Any, Optional
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Center, Middle, Vertical


class EndingScreen(Screen):
    """Terminal ending screen displaying the narrative resolution and exit options."""

    CSS = """
    EndingScreen {
        background: #080808;
        color: #d0d0d0;
    }

    #ending-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }

    #ending-panel {
        width: 74;
        max-width: 90%;
        height: auto;
        border: solid #444444;
        background: #111111;
        padding: 1 2;
    }

    #ending-marker {
        text-align: center;
        color: #555555;
    }

    #ending-title {
        text-align: center;
        text-style: bold;
        color: #f0f0f0;
        margin-top: 1;
        margin-bottom: 1;
    }

    #ending-prose {
        text-align: left;
        color: #b0b0b0;
        margin-bottom: 1;
    }

    #ending-menu {
        margin-top: 1;
        color: #48cae4;
    }

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
        ("escape", "back_to_menu", "Back to Menu"),
    ]

    # Minimal decorative marker allowed for endings per §7.3
    ENDING_MARKER: str = "·  ·  ·  [ THE ESCAPE ]  ·  ·  ·"

    def __init__(
        self,
        room: Optional[dict[str, Any]] = None,
        content: Optional[dict[str, Any]] = None,
        title: str = "SURVIVED",
        prose: str = "",
    ) -> None:
        super().__init__()
        self.room: dict[str, Any] = room or {}
        self.content: Optional[dict[str, Any]] = content
        self.title: str = self.room.get("name", title)
        self.prose: str = self.room.get("prose", prose)
        self.options: list[str] = ["AGAIN", "BACK TO MENU"]
        self.selected: int = 0

    def render_menu(self) -> str:
        """Render cursor-based choices."""
        lines = []
        for index, option in enumerate(self.options):
            if index == self.selected:
                lines.append(f"[bold cyan]  > {option}[/]")
            else:
                lines.append(f"[cyan]    {option}[/]")
        return "\n".join(lines)

    def update_menu(self) -> None:
        widget = self.query_one("#ending-menu", Static)
        widget.update(self.render_menu())

    def on_mount(self) -> None:
        from game.save import delete_saved_game
        delete_saved_game()

    def compose(self):
        with Center(id="ending-container"):
            with Middle():
                with Vertical(id="ending-panel"):
                    yield Static(self.ENDING_MARKER, id="ending-marker")
                    yield Static(self.title, id="ending-title")
                    yield Static(self.prose, id="ending-prose")
                    yield Static(self.render_menu(), id="ending-menu")
        yield Footer(id="footer-zone")

    def action_move_up(self) -> None:
        self.selected = (self.selected - 1) % len(self.options)
        self.update_menu()

    def action_move_down(self) -> None:
        self.selected = (self.selected + 1) % len(self.options)
        self.update_menu()

    def action_select(self) -> None:
        choice = self.options[self.selected]
        if choice == "AGAIN":
            self.action_again()
        elif choice == "BACK TO MENU":
            self.action_back_to_menu()

    def action_again(self) -> None:
        """Start a fresh run."""
        from screens.game import GameScreen

        if hasattr(self.app, "active_run"):
            self.app.active_run = None

        self.app.switch_screen(GameScreen(content=self.content))

    def action_back_to_menu(self) -> None:
        """Return to main menu, clearing any resumable run state."""
        if hasattr(self.app, "active_run"):
            self.app.active_run = None

        while len(self.app.screen_stack) > 1:
            top_screen = self.app.screen
            if top_screen.__class__.__name__ == "MainMenuScreen":
                break
            self.app.pop_screen()
