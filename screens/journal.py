"""Journal overlay screen for Escape from Shadows (Task E03).

Displays recorded room discoveries, death lessons, and Shadow whispers.
Accessible via 'j' key during gameplay and dismissible with Escape or 'j'.
Does not advance turns or drain oil.
"""

from __future__ import annotations

from typing import Optional
from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Static

from game.journal import (
    CATEGORY_DEATH,
    CATEGORY_ROOM,
    CATEGORY_SHADOW,
    Journal,
)


class JournalScreen(Screen):
    """Overlay screen displaying the player's journal."""

    CSS = """
    JournalScreen {
        background: #080808;
        color: #d0d0d0;
        align: center middle;
    }

    #journal-container {
        width: 80;
        max-width: 95%;
        height: 85%;
        border: solid #444444;
        background: #111111;
        padding: 1 2;
    }

    #journal-header {
        text-align: center;
        text-style: bold;
        color: #f0f0f0;
        margin-bottom: 1;
        border-bottom: solid #333333;
    }

    #journal-content {
        height: 1fr;
        color: #cccccc;
    }

    #journal-footer {
        text-align: center;
        color: #666666;
        margin-top: 1;
        border-top: solid #333333;
    }
    """

    BINDINGS = [
        ("escape", "dismiss_journal", "Close"),
        ("j", "dismiss_journal", "Close"),
    ]

    def __init__(self, journal: Optional[Journal] = None) -> None:
        super().__init__()
        self.journal = journal if journal is not None else Journal()

    def render_content(self) -> str:
        if not self.journal.entries:
            return "[dim italic]The pages are blank. No discoveries, lessons, or whispers have been recorded yet.[/]"

        blocks: list[str] = []

        # Room discoveries
        rooms = self.journal.get_entries(CATEGORY_ROOM)
        if rooms:
            blocks.append("[bold #d4a373]DISCOVERIES[/]")
            for r in rooms:
                blocks.append(f"  [bold white]• {r.detail or r.text}[/]")
            blocks.append("")

        # Death lessons
        deaths = self.journal.get_entries(CATEGORY_DEATH)
        if deaths:
            blocks.append("[bold #d4a373]LESSONS OF THE GRAVE[/]")
            for d in deaths:
                lesson_text = f" — [italic]{d.detail}[/]" if d.detail else ""
                blocks.append(f"  [bold white]• {d.text}[/]{lesson_text}")
            blocks.append("")

        # Shadow whispers
        whispers = self.journal.get_entries(CATEGORY_SHADOW)
        if whispers:
            blocks.append("[bold #e63946]SHADOW WHISPERS[/]")
            for w in whispers:
                context_str = f" [dim]({w.detail})[/]" if w.detail else ""
                blocks.append(f"  [italic #e63946]\"{w.text}\"[/]{context_str}")
            blocks.append("")

        return "\n".join(blocks).rstrip()

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                with Vertical(id="journal-container"):
                    yield Static("— THE JOURNAL —", id="journal-header")
                    with VerticalScroll(id="journal-content"):
                        yield Static(self.render_content(), id="journal-text")
                    yield Static("Press [bold]Escape[/bold] or [bold]J[/bold] to return to the dark.", id="journal-footer")

    def action_dismiss_journal(self) -> None:
        self.app.pop_screen()
