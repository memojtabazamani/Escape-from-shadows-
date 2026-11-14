"""Endings Gallery screen displaying all canonical endings as silhouettes or unlocked entries (Task A03).

SUGGEST.md §9.4:
A screen listing all endings as silhouettes: the ones you got are named,
the ones you missed are just counts ('3 of 7'). Achievements without the
pop-up gamification — just a quiet record of what you've seen.
"""

from __future__ import annotations

from typing import Any, Optional
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle, Vertical
from textual.containers import VerticalScroll as _VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Static

from game.endings import (
    CANONICAL_ENDINGS,
    CANONICAL_ENDINGS_LIST,
    TOTAL_CANONICAL_ENDINGS,
    EndingMetadata,
    get_all_canonical_endings,
)
from game.profile import PlayerProfile, load_profile


class VerticalScroll(_VerticalScroll):
    """VerticalScroll container with focus suppression for gallery navigation."""

    can_focus: bool = False

    def __init__(self, *children: Any, can_focus: bool = False, **kwargs: Any) -> None:
        try:
            super().__init__(*children, can_focus=can_focus, **kwargs)
        except TypeError:
            super().__init__(*children, **kwargs)
        self.can_focus = can_focus


class EndingsGalleryScreen(Screen):
    """Screen displaying all 7 endings as silhouettes or unlocked entries."""

    CSS = """
    EndingsGalleryScreen {
        background: #080808;
        color: #d0d0d0;
        align: center middle;
    }

    #gallery-container {
        width: 82;
        max-width: 95%;
        height: 88%;
        border: solid #444444;
        background: #111111;
        padding: 1 2;
    }

    #gallery-header {
        text-align: center;
        text-style: bold;
        color: #f0f0f0;
        margin-bottom: 0;
    }

    #gallery-tally {
        text-align: center;
        color: #d4a373;
        text-style: bold;
        margin-bottom: 1;
        border-bottom: solid #333333;
    }

    #gallery-scroll {
        height: 1fr;
        scrollbar-gutter: stable;
    }

    #gallery-cards {
        color: #cccccc;
    }

    #gallery-details {
        min-height: 3;
        height: auto;
        max-height: 5;
        border-top: solid #333333;
        margin-top: 1;
        padding-top: 1;
        color: #94a3b8;
    }

    #gallery-footer {
        text-align: center;
        color: #666666;
        margin-top: 1;
        border-top: solid #222222;
    }
    """

    BINDINGS = [
        Binding("up", "move_up", "Up", priority=True),
        Binding("down", "move_down", "Down", priority=True),
        Binding("enter", "select", "Details", priority=True),
        Binding("escape", "dismiss_gallery", "Back", priority=True),
        Binding("q", "dismiss_gallery", "Back", priority=True),
    ]

    def __init__(self, profile: Optional[PlayerProfile] = None) -> None:
        super().__init__()
        self.profile: PlayerProfile = profile if profile is not None else load_profile()
        self.selected: int = 0
        self.expanded: bool = False

    def on_mount(self) -> None:
        """Ensure child scroll container does not intercept navigation focus."""
        try:
            scroll = self.query_one("#gallery-scroll")
            scroll.can_focus = False
        except Exception:
            pass

    def render_tally(self) -> str:
        """Render discovery tally string."""
        endings = get_all_canonical_endings()
        unlocked_count = sum(1 for e in endings if self.profile.is_ending_unlocked(e.id))
        return f"DISCOVERED: {unlocked_count} OF {TOTAL_CANONICAL_ENDINGS}"

    def render_cards(self) -> str:
        """Render all 7 canonical ending cards with unlocked titles or silhouettes."""
        endings = get_all_canonical_endings()
        blocks: list[str] = []

        for index, e in enumerate(endings):
            is_unlocked = self.profile.is_ending_unlocked(e.id)
            is_selected = (index == self.selected)
            cursor = "[bold #d4a373]▸ [/]" if is_selected else "  "

            if is_unlocked:
                header = f"{cursor}[bold white]#{e.number}. {e.title}[/]  [dim cyan][{e.tone}][/]"
                body = f"     [#b0b0b0]{e.summary}[/]"
            else:
                header = f"{cursor}[bold #666666]#{e.number}. [ ? ? ? ? ? ? ? ? ][/]  [dim #555555][LOCKED][/]"
                body = f"     [dim italic #777777]Hint: {e.hint}[/]"

            blocks.append(f"{header}\n{body}")

        return "\n\n".join(blocks)

    def render_details(self) -> str:
        """Render detail summary or teaser for the currently selected card."""
        endings = get_all_canonical_endings()
        if not (0 <= self.selected < len(endings)):
            return ""

        e = endings[self.selected]
        is_unlocked = self.profile.is_ending_unlocked(e.id)

        if is_unlocked:
            if self.expanded:
                return (
                    f"[bold #d4a373]Ending #{e.number}: {e.title}[/]  [dim cyan][{e.tone}][/]\n"
                    f"[cyan]{e.summary}[/]\n"
                    f"[dim italic #d4a373]Unlock Path: {e.hint}[/]"
                )
            return f"[bold #d4a373]Ending #{e.number}: {e.title}[/]\n[cyan]{e.summary}[/]"

        if self.expanded:
            return (
                f"[bold #666666]Ending #{e.number}: [ SILHOUETTE ][/]\n"
                f"[dim italic]Hint: {e.hint}[/]\n"
                f"[dim #555555]Status: Locked — explore the house to uncover this path.[/]"
            )
        return f"[bold #666666]Ending #{e.number}: [ SILHOUETTE ][/]\n[dim italic]Hint: {e.hint}[/]"

    def update_view(self) -> None:
        """Refresh static widgets after cursor movements."""
        try:
            self.query_one("#gallery-tally", Static).update(self.render_tally())
            self.query_one("#gallery-cards", Static).update(self.render_cards())
            self.query_one("#gallery-details", Static).update(self.render_details())
            scroll = self.query_one("#gallery-scroll", VerticalScroll)
            scroll.scroll_to(y=self.selected * 3, animate=False)
        except Exception:
            pass

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                with Vertical(id="gallery-container"):
                    yield Static("— ENDINGS GALLERY —", id="gallery-header")
                    yield Static(self.render_tally(), id="gallery-tally")
                    with VerticalScroll(id="gallery-scroll", can_focus=False):
                        yield Static(self.render_cards(), id="gallery-cards")
                    yield Static(self.render_details(), id="gallery-details")
                    yield Static(
                        "Press [bold]↑/↓[/bold] to navigate, [bold]Enter[/bold] for details, [bold]Escape[/bold] to return.",
                        id="gallery-footer",
                    )
        yield Footer()

    def action_move_up(self) -> None:
        count = len(get_all_canonical_endings())
        if count > 0:
            self.selected = (self.selected - 1) % count
        self.update_view()

    def action_move_down(self) -> None:
        count = len(get_all_canonical_endings())
        if count > 0:
            self.selected = (self.selected + 1) % count
        self.update_view()

    def action_select(self) -> None:
        self.expanded = not self.expanded
        self.update_view()

    def action_dismiss_gallery(self) -> None:
        self.app.pop_screen()
