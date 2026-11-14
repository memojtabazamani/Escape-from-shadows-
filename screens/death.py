"""Death screen component for Escape from Shadows.

Follows SUGGEST.md §9.2 four-part death structure:
1. How you died, in one sentence (cause, rendered verbatim from structured data).
2. What you learned (reserved placeholder region for I03).
3. What you could have done (reserved placeholder region for I04, greyed out).
4. Actions: "Again" and "Back to menu".

Style & constraints (§7.3, §7.4, §13):
- No ASCII art on death screen (§7.3 reserves ASCII art for title, Hell Dog, and endings).
- Red is strictly reserved for the Shadow (§7.4); red styling only applies when the
  Shadow is explicitly present in the death cause.
- Selectable cursor-based menu only (no single-letter typed friction).
- "Back to menu" clears any active run state on app so no resumable corpse is left.
"""

from __future__ import annotations

from typing import Any, Optional
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Center, Middle, Vertical

from game.difficulty import get_difficulty_config
from game.state import RunState


class DeathScreen(Screen):
    """Terminal death screen displaying structured death cause and recovery options."""

    CSS = """
    DeathScreen {
        background: #080808;
        color: #d0d0d0;
    }

    #death-container {
        width: 100%;
        height: 100%;
        align: center middle;
    }

    #death-panel {
        width: 72;
        max-width: 90%;
        height: auto;
        border: solid #333333;
        background: #101010;
        padding: 1 2;
    }

    #death-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #death-cause {
        text-align: center;
        color: #f0f0f0;
        margin-bottom: 1;
    }

    #death-learned {
        text-align: center;
        color: #d4a373; /* Amber for lore / lesson */
        margin-bottom: 1;
    }

    #death-could-have-done {
        text-align: center;
        color: #555555; /* Dim greyed-out hint */
        margin-bottom: 1;
    }

    #death-menu {
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

    def __init__(
        self,
        cause: str,
        lesson: str = "",
        could_have_done: str = "",
        content: Optional[dict[str, Any]] = None,
        state: Optional[RunState] = None,
    ) -> None:
        super().__init__()
        self.cause: str = cause
        self.lesson: str = lesson
        self.could_have_done: str = could_have_done
        self.content: Optional[dict[str, Any]] = content
        self.state: Optional[RunState] = state
        self.options: list[str] = ["AGAIN", "BACK TO MENU"]
        self.selected: int = 0

    @property
    def is_shadow_death(self) -> bool:
        """Check whether the cause involves the Shadow, governing §7.4 red reservation."""
        return "shadow" in self.cause.lower()

    def render_title(self) -> str:
        """Render title, reserving red strictly for Shadow presence (§7.4)."""
        if self.is_shadow_death:
            return "[bold #e63946]DARKNESS CLAIMS YOU[/]"
        return "[bold #b0b0b0]YOU HAVE PERISHED[/]"

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
        widget = self.query_one("#death-menu", Static)
        widget.update(self.render_menu())

    def is_easy_difficulty(self) -> bool:
        """True if current difficulty setting is EASY."""
        if self.state and self.state.difficulty == "EASY":
            return True
        if hasattr(self, "app") and self.app is not None:
            config = getattr(self.app, "config", None)
            if config and hasattr(config, "get") and config.get("difficulty") == "EASY":
                return True
            if isinstance(config, dict) and config.get("difficulty") == "EASY":
                return True
        return False

    def on_mount(self) -> None:
        from game.save import delete_saved_game
        delete_saved_game()
        from game.profile import record_death, unlock_ending
        record_death()
        if self.state:
            is_early_hall = (
                self.state.has_flag("early_hall_death")
                or (
                    self.state.current_room in ("hall", "left_doorway_death", "clock_trap_death")
                    and self.state.turn_count <= 3
                    and self.state.visited.issubset({"hall", "left_doorway_death", "clock_trap_death"})
                )
            )
            if is_early_hall:
                unlock_ending("the_long_walk")

    def compose(self):
        with Center(id="death-container"):
            with Middle():
                with Vertical(id="death-panel"):
                    yield Static(self.render_title(), id="death-title")
                    yield Static(self.cause, id="death-cause")
                    learned_text = f"What you learned: {self.lesson}" if self.lesson else "What you learned: The darkness here was absolute; heed the oil reserve."
                    yield Static(learned_text, id="death-learned")
                    hint_text = f"Could have done: {self.could_have_done}" if (self.is_easy_difficulty() and self.could_have_done) else ""
                    yield Static(hint_text, id="death-could-have-done")
                    yield Static(self.render_menu(), id="death-menu")
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
        """Start a run based on difficulty mercy parameters."""
        from screens.game import GameScreen

        diff = self.state.difficulty if self.state else "MEDIUM"
        cfg = get_difficulty_config(diff)

        if cfg.restart_point_mode == "last_room" and self.state and self.state.recorded_restart_room:
            fresh_run = RunState.fresh_run(difficulty=diff)
            fresh_run.current_room = self.state.recorded_restart_room
            fresh_run.visit(self.state.recorded_restart_room)
            fresh_run.journal = self.state.journal
        else:
            fresh_run = RunState.fresh_run(difficulty=diff)

        # Update active run reference on app
        if hasattr(self.app, "active_run"):
            self.app.active_run = fresh_run

        # Switch directly to GameScreen with new run
        self.app.switch_screen(GameScreen(content=self.content, state=fresh_run))

    def action_back_to_menu(self) -> None:
        """Return to main menu, clearing any resumable run state."""
        if hasattr(self.app, "active_run"):
            self.app.active_run = None

        # Pop back to the main menu screen if present, or pop self
        while len(self.app.screen_stack) > 1:
            top_screen = self.app.screen
            if top_screen.__class__.__name__ == "MainMenuScreen":
                break
            self.app.pop_screen()
