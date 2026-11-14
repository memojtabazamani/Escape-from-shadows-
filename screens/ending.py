"""Ending screen component for Escape from Shadows (Phase 3 Slice B, Task B04).

Follows SUGGEST.md §2.3, §7.3, and §9.4:
- Renders the ending room's name and prose from structured data.
- Displays the dedicated ASCII art vignette conforming to §7.3 rarity rules.
- Permanently unlocks the ending in PlayerProfile on mount.
- Increments escape tally for successful escapes.
- Navigation options: "AGAIN", "BACK TO MENU", and "VIEW GALLERY".
- "Back to menu" clears any active run state on app so no resumable state lingers.
"""

from __future__ import annotations

from typing import Any, Optional
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Center, Middle, Vertical

from game.endings_art import get_ending_ascii
from game.profile import unlock_ending, record_escape


class EndingScreen(Screen):
    """Terminal ending screen displaying narrative resolution, ASCII vignette, and options."""

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

    #ending-ascii {
        text-align: center;
        color: #48cae4;
        margin-top: 1;
        margin-bottom: 1;
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

    @property
    def ending_marker(self) -> str:
        """Adaptive ending marker adhering to §7.3 restraint."""
        if self.ending_id == "stay":
            return "·  ·  ·  [ THE CHOICE ]  ·  ·  ·"
        elif self.ending_id in ("the_long_walk", "shadow_walk"):
            return "·  ·  ·  [ THE THRESHOLD ]  ·  ·  ·"
        return self.ENDING_MARKER

    def __init__(
        self,
        room: Optional[dict[str, Any]] = None,
        content: Optional[dict[str, Any]] = None,
        title: Optional[str] = None,
        prose: Optional[str] = None,
        ending_id: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.room: dict[str, Any] = room or {}
        self.content: Optional[dict[str, Any]] = content

        # Resolve ending_id with intelligent fallback
        if ending_id:
            self.ending_id: str = str(ending_id)
        elif "ending_id" in self.room:
            self.ending_id = str(self.room["ending_id"])
        elif self.room.get("id") == "ending_stay":
            self.ending_id = "stay"
        elif self.room.get("id") == "ending_long_walk":
            self.ending_id = "the_long_walk"
        elif self.room.get("id") == "shadow_walk_ending":
            self.ending_id = "shadow_walk"
        else:
            self.ending_id = "the_quiet_exit"

        # Helper to load content dictionary if not provided
        content_dict = self.content
        if content_dict is None:
            try:
                from game.content_schema import load_content
                content_dict = load_content("data/content.json")
            except Exception:
                content_dict = None

        # Resolve title: explicit param -> room name (if explicit) -> content endings -> ending metadata -> "SURVIVED"
        if title is not None:
            self.title = str(title)
        elif "name" in self.room and self.room["name"]:
            self.title = str(self.room["name"])
        elif content_dict and "endings" in content_dict:
            found_title = ""
            for e in content_dict["endings"]:
                if isinstance(e, dict) and e.get("id") == self.ending_id:
                    found_title = str(e.get("title", ""))
                    break
            self.title = found_title if found_title else "SURVIVED"
        else:
            from game.endings import get_ending_metadata
            meta = get_ending_metadata(self.ending_id)
            self.title = meta.title if meta else "SURVIVED"

        # Resolve prose: explicit param -> room prose (if explicit) -> content endings prose -> metadata summary -> ""
        if prose is not None:
            self.prose = str(prose)
        elif "prose" in self.room and self.room["prose"]:
            self.prose = str(self.room["prose"])
        elif content_dict and "endings" in content_dict:
            found_prose = ""
            for e in content_dict["endings"]:
                if isinstance(e, dict) and e.get("id") == self.ending_id:
                    found_prose = str(e.get("prose", ""))
                    break
            self.prose = found_prose
        else:
            from game.endings import get_ending_metadata
            meta = get_ending_metadata(self.ending_id)
            self.prose = meta.summary if meta else ""

        self.options: list[str] = ["AGAIN", "BACK TO MENU", "VIEW GALLERY"]
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
        from game.endings import CANONICAL_ENDINGS
        if self.ending_id in CANONICAL_ENDINGS:
            unlock_ending(self.ending_id)
        if self.ending_id in ("meat_and_silence", "the_quiet_exit", "what_the_book_knew", "the_new_shadow", "homecoming"):
            record_escape()

    def compose(self):
        with Center(id="ending-container"):
            with Middle():
                with Vertical(id="ending-panel"):
                    yield Static(self.ending_marker, id="ending-marker")
                    yield Static(get_ending_ascii(self.ending_id), id="ending-ascii")
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
        elif choice == "VIEW GALLERY":
            self.action_view_gallery()

    def action_view_gallery(self) -> None:
        """Push EndingsGalleryScreen to inspect discovered endings."""
        from screens.gallery import EndingsGalleryScreen
        self.app.push_screen(EndingsGalleryScreen())

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
