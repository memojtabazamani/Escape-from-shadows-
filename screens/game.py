from __future__ import annotations

from typing import Any, Optional
from textual.screen import Screen
from textual.widgets import Static, Footer
from textual.containers import Vertical, Horizontal

from game.state import RunState
from game.content_schema import SAMPLE_CONTENT, validate_content
from game.difficulty import get_difficulty_config
from game.hints import get_stuck_hint
from game.effects import resolve_choice
from game.lantern import drain_for_room, is_zero_oil, get_zero_oil_consequence
from game.composure import is_zero_composure
from game.distortion import distort_narration
from game.sound import play_cue, CUE_DOOR_OPEN, CUE_DOG_CHAIN, CUE_SHADOW_WHISPER
from screens.death import DeathScreen
from screens.ending import EndingScreen
from screens.journal import JournalScreen


class GameScreen(Screen):
    """The central gameplay screen featuring three fixed zones: scene, status, and footer."""

    LOW_OIL_THRESHOLD: int = 30
    AMBER_COLOR: str = "#d4a373"

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

    #scene-zone.pulse-beat {
        border: solid #555555;
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

    #scene-telegraphs {
        color: #b08968;
        margin-bottom: 1;
    }

    #scene-choices {
        height: auto;
        color: #48cae4;
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

    #turn-status {
        width: auto;
        padding: 0 2;
        color: #888888;
    }

    #composure-status {
        width: 1fr;
        text-align: right;
    }

    #inventory-status {
        height: 1;
        color: #d4a373;
        margin-top: 1;
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
        ("j", "open_journal", "Journal"),
        ("escape", "back", "Back"),
    ]

    def __init__(
        self,
        content: Optional[dict[str, Any]] = None,
        state: Optional[RunState] = None,
    ) -> None:
        super().__init__()
        self.content = content if content is not None else SAMPLE_CONTENT
        problems = validate_content(self.content)
        if problems:
            raise ValueError(f"Invalid game content: {', '.join(str(p) for p in problems)}")

        self.rooms_by_id = {room["id"]: room for room in self.content.get("rooms", [])}
        items_list = self.content.get("items", [])
        self.items_by_id = {it["id"]: it for it in items_list if isinstance(it, dict) and "id" in it}
        self.state = state if state is not None else RunState.fresh_run()
        if not self.state.current_room:
            self.state.current_room = str(self.content.get("start_room", "hall"))

        self.current_choices: list[dict[str, Any]] = []
        self.selected_choice: int = 0
        self.last_death_cause: Optional[str] = None
        self.drop_mode: bool = False
        self.pending_grant_choice: Optional[dict[str, Any]] = None
        self.drop_options: list[tuple[str, str]] = []
        self.drop_selected: int = 0
        self._typewriter_timer: Any = None
        self._pulse_timer: Any = None
        self._target_prose: str = ""
        self._typewriter_index: int = 0

    @staticmethod
    def render_lantern_bar(lantern_val: int) -> str:
        """Render 0-100 lantern oil as a 10-cell block bar."""
        clamped = max(0, min(100, int(lantern_val)))
        filled = round(clamped / 10)
        empty = 10 - filled
        return "█" * filled + "░" * empty

    def get_item_name(self, item_id: str) -> str:
        """Lookup readable name for an item or fallback to item_id."""
        item_info = self.items_by_id.get(item_id, {})
        return item_info.get("name", item_id)

    def render_inventory_status(self) -> str:
        """Render pack capacity indicator and carried item list."""
        count = len(self.state.held_items)
        cap = 6
        if count == 0:
            return f"PACK [{self.AMBER_COLOR}][0/{cap}][/]: [dim](carrying nothing)[/]"

        item_names = [f"[#ffffff]{self.get_item_name(item_id)}[/]" for item_id in self.state.held_items]
        joined = ", ".join(item_names)
        if count >= cap:
            return f"PACK [bold {self.AMBER_COLOR}][{count}/{cap} FULL][/]: {joined}"
        return f"PACK [{self.AMBER_COLOR}][{count}/{cap}][/]: {joined}"

    @classmethod
    def render_composure_bar(cls, comp_val: int) -> str:
        """Render 0-100 composure as a 10-cell block bar with text state cues."""
        clamped = max(0, min(100, int(comp_val)))
        filled = round(clamped / 10)
        empty = 10 - filled
        bar = "█" * filled + "░" * empty
        if clamped <= 0:
            return f"NERVE [{cls.AMBER_COLOR}]{bar} (broken)[/]"
        elif clamped <= 20:
            return f"NERVE [{cls.AMBER_COLOR}]{bar} (shaken)[/]"
        return f"NERVE {bar}"

    def update_status(self) -> None:
        """Refresh lantern bar, turn counter, inventory, and status in the status zone."""
        lantern_widget = self.query_one("#lantern-status", Static)
        turn_widget = self.query_one("#turn-status", Static)
        inv_widget = self.query_one("#inventory-status", Static)
        comp_widget = self.query_one("#composure-status", Static)

        bar = self.render_lantern_bar(self.state.lantern)
        if self.state.lantern <= self.LOW_OIL_THRESHOLD:
            lantern_text = f"LANTERN [{self.AMBER_COLOR}]{bar} (low oil)[/]"
        else:
            lantern_text = f"LANTERN {bar}"
        lantern_widget.update(lantern_text)
        turn_widget.update(f"turn {self.state.turn_count}")
        inv_widget.update(self.render_inventory_status())
        comp_widget.update(self.render_composure_bar(self.state.composure))

    def get_room(self, room_id: str) -> dict[str, Any]:
        """Lookup a room record by id or fail loudly with KeyError."""
        if room_id not in self.rooms_by_id:
            raise KeyError(f"Unknown room id: '{room_id}'")
        return self.rooms_by_id[room_id]

    def render_room(self, room_id: str) -> None:
        """Render the room name, prose, telegraphs, and choices from content into the scene zone."""
        room = self.get_room(room_id)
        is_revisit = self.state.has_visited(room_id)
        self.state.current_room = room_id
        self.state.visit(room_id)

        if not is_revisit:
            note = room.get("journal_note") or room.get("prose", "").split("\n")[0]
            self.state.journal.add_room(room_id, room.get("name", ""), note)

        header = self.query_one("#scene-header", Static)
        text = self.query_one("#scene-text", Static)
        telegraphs_widget = self.query_one("#scene-telegraphs", Static)

        header.update(room.get("name", ""))
        prose = room.get("revisit_prose") if is_revisit and "revisit_prose" in room else room.get("prose", "")
        prose = distort_narration(prose, self.state.composure)
        self._target_prose = prose

        if self.is_music_enabled():
            self._typewriter_index = 0
            text.update("")
            self._clean_typewriter()
            self._typewriter_timer = self.set_interval(0.015, self._typewriter_tick)
            self._start_pulse()
        else:
            self._clean_typewriter()
            self._stop_pulse()
            text.update(prose)

        self.current_choices = list(room.get("choices", []))
        self.selected_choice = 0

        # Collect telegraphs from all choices in the room
        all_telegraphs: list[str] = []
        for choice in self.current_choices:
            for tele in choice.get("telegraphs", []):
                all_telegraphs.append(f"[italic]· {tele}[/]")

        hint = get_stuck_hint(self.state)
        if hint:
            all_telegraphs.append(f"[bold #e63946]The Shadow murmurs:[/] [italic #e63946]\"{hint}\"[/]")
            self.state.journal.add_shadow_line(hint, context=f"Room: {room.get('name', room_id)}")
            play_cue(self.app, CUE_SHADOW_WHISPER)

        if room_id == "yard_doghouse_encounter":
            play_cue(self.app, CUE_DOG_CHAIN)
        elif room_id == "shadow_walk_ending":
            play_cue(self.app, CUE_SHADOW_WHISPER)
        elif self.state.has_flag("library_door_ajar") and "door_ajar_sound" not in self.state.delivered_hints:
            self.state.delivered_hints.add("door_ajar_sound")
            play_cue(self.app, CUE_DOOR_OPEN)

        expiry_cue = self.get_nearing_expiry_cue()
        if expiry_cue:
            all_telegraphs.append(expiry_cue)

        telegraphs_widget.update("\n".join(all_telegraphs))
        self.update_choices()
        self.update_status()

    def is_music_enabled(self) -> bool:
        """True if visual rhythm (typewriter & pulsing) is enabled in settings."""
        if not hasattr(self, "app") or self.app is None:
            return False
        config = getattr(self.app, "config", None)
        if config is None:
            return False
        if hasattr(config, "get"):
            return bool(config.get("music", True))
        if isinstance(config, dict):
            return bool(config.get("music", True))
        return False

    def _typewriter_tick(self) -> None:
        """Stream next slice of characters into scene prose."""
        try:
            text = self.query_one("#scene-text", Static)
        except Exception:
            self._clean_typewriter()
            return
        self._typewriter_index += 3
        if self._typewriter_index >= len(self._target_prose):
            text.update(self._target_prose)
            self._clean_typewriter()
        else:
            text.update(self._target_prose[:self._typewriter_index])

    def _finish_typewriter(self) -> None:
        """Instantly finish typewriter animation upon key press."""
        if getattr(self, "_typewriter_timer", None) is not None:
            self._clean_typewriter()
            try:
                text = self.query_one("#scene-text", Static)
                text.update(self._target_prose)
            except Exception:
                pass

    def _clean_typewriter(self) -> None:
        """Stop and clear active typewriter interval."""
        if getattr(self, "_typewriter_timer", None) is not None:
            self._typewriter_timer.stop()
            self._typewriter_timer = None

    def _start_pulse(self) -> None:
        """Begin slow heartbeat border pulsing on scene panel."""
        if getattr(self, "_pulse_timer", None) is None:
            self._pulse_timer = self.set_interval(1.5, self._toggle_pulse)

    def _stop_pulse(self) -> None:
        """Stop heartbeat border pulsing."""
        if getattr(self, "_pulse_timer", None) is not None:
            self._pulse_timer.stop()
            self._pulse_timer = None
        try:
            scene_zone = self.query_one("#scene-zone")
            scene_zone.remove_class("pulse-beat")
        except Exception:
            pass

    def _toggle_pulse(self) -> None:
        """Toggle subtle border glow class."""
        try:
            scene_zone = self.query_one("#scene-zone")
            scene_zone.toggle_class("pulse-beat")
        except Exception:
            pass

    def is_choice_expired(self, choice: dict[str, Any]) -> bool:
        """Check if choice has expired due to hesitation on HARD difficulty."""
        cfg = get_difficulty_config(self.state.difficulty)
        if not cfg.choice_expiry_enabled:
            return False
        expires_after = choice.get("expires_after_turns")
        if expires_after is None:
            return False
        return self.state.consecutive_room_turns >= int(expires_after)

    def get_nearing_expiry_cue(self) -> Optional[str]:
        """Return warning cue if an expiring choice is about to expire."""
        cfg = get_difficulty_config(self.state.difficulty)
        if not cfg.choice_expiry_enabled:
            return None
        for choice in self.current_choices:
            expires_after = choice.get("expires_after_turns")
            if expires_after is not None:
                remaining = int(expires_after) - self.state.consecutive_room_turns
                if remaining == 1:
                    return f"[italic #d4a373]Time is slipping away... 1 turn before an opportunity closes[/]"
        return None

    def render_choices(self) -> str:
        """Render choice list or drop options when in drop mode."""
        if self.drop_mode:
            lines = ["[bold #d4a373]Pack is full! Select an item to drop:[/bold #d4a373]"]
            for idx, item_id in enumerate(self.state.held_items):
                name = self.get_item_name(item_id)
                prefix = "  > " if idx == self.drop_selected else "    "
                style = "bold cyan" if idx == self.drop_selected else "cyan"
                lines.append(f"[{style}]{prefix}Drop {name}[/]")
            cancel_idx = len(self.state.held_items)
            prefix = "  > " if cancel_idx == self.drop_selected else "    "
            style = "bold dim" if cancel_idx == self.drop_selected else "dim"
            lines.append(f"[{style}]{prefix}Cancel (keep current items)[/]")
            return "\n".join(lines)

        if not self.current_choices:
            return ""

        lines = []
        for index, choice in enumerate(self.current_choices):
            label = choice.get("label", "")
            if self.is_choice_expired(choice):
                expiry_note = choice.get("expiry_text") or "opportunity lost"
                lines.append(f"[dim strike]    {label} ({expiry_note})[/]")
            elif index == self.selected_choice:
                lines.append(f"[bold cyan]  > {label}[/]")
            else:
                lines.append(f"[cyan]    {label}[/]")
        return "\n".join(lines)

    def update_choices(self) -> None:
        """Update choices widget display."""
        choices_widget = self.query_one("#scene-choices", Static)
        choices_widget.update(self.render_choices())

    def compose(self):
        with Vertical(id="game-container"):
            with Vertical(id="scene-zone"):
                yield Static("", id="scene-header")
                yield Static("", id="scene-text")
                yield Static("", id="scene-telegraphs")
                yield Static("", id="scene-choices")
            with Vertical(id="status-zone"):
                with Horizontal(id="status-resources"):
                    yield Static("", id="lantern-status")
                    yield Static("", id="turn-status")
                    yield Static("", id="composure-status")
                yield Static("", id="inventory-status")
                yield Static("> ", id="prompt-line")
        yield Footer(id="footer-zone")

    def on_mount(self) -> None:
        self.render_room(self.state.current_room)

    def on_unmount(self) -> None:
        self._clean_typewriter()
        self._stop_pulse()

    def on_key(self, event) -> None:
        if getattr(self, "_typewriter_timer", None) is not None:
            self._finish_typewriter()

    def action_move_up(self) -> None:
        if self.drop_mode:
            total_drop_options = len(self.state.held_items) + 1
            self.drop_selected = (self.drop_selected - 1) % total_drop_options
            self.update_choices()
            return
        if self.current_choices:
            self.selected_choice = (self.selected_choice - 1) % len(self.current_choices)
            self.update_choices()

    def action_move_down(self) -> None:
        if self.drop_mode:
            total_drop_options = len(self.state.held_items) + 1
            self.drop_selected = (self.drop_selected + 1) % total_drop_options
            self.update_choices()
            return
        if self.current_choices:
            self.selected_choice = (self.selected_choice + 1) % len(self.current_choices)
            self.update_choices()

    def start_drop_mode(self, choice: dict[str, Any]) -> None:
        """Enter drop selection mode when pack is full and a new item is offered."""
        self.drop_mode = True
        self.pending_grant_choice = choice
        self.drop_selected = 0
        self.update_choices()

    def cancel_drop(self) -> None:
        """Exit drop mode without dropping or taking anything."""
        self.drop_mode = False
        self.pending_grant_choice = None
        self.drop_selected = 0
        prompt_line = self.query_one("#prompt-line", Static)
        prompt_line.update("> Drop cancelled.")
        self.update_choices()

    def _execute_choice(self, choice: dict[str, Any]) -> None:
        """Execute a validated choice, advancing turns and handling outcomes."""
        prompt_line = self.query_one("#prompt-line", Static)

        if self.is_choice_expired(choice):
            prompt_line.update(f"> [dim strike]{choice.get('expiry_text') or 'That choice is no longer available.'}[/]")
            return

        has_grant = any(
            isinstance(eff, dict) and eff.get("verb") == "grant_item"
            for eff in choice.get("effects", [])
        )
        if has_grant and not self.state.can_add_item() and len(self.state.held_items) > 0:
            self.start_drop_mode(choice)
            prompt_line.update("> [dim]Pack is full (6/6). Choose an item to drop.[/]")
            return

        result = resolve_choice(choice, self.state)

        if result.refused:
            if "pack is full" in result.reason.lower() and len(self.state.held_items) > 0:
                self.start_drop_mode(choice)
                prompt_line.update(f"> [dim]{result.reason} Choose an item to drop.[/]")
                return
            prompt_line.update(f"> [dim]{result.reason}[/]")
            return

        # Apply room transition oil drain
        if result.destination != self.state.current_room:
            oil_drain = drain_for_room(self.state, result.destination)
            self.state.spend_lantern(oil_drain)

        self.state.advance_turn()
        dest_room = self.get_room(result.destination)

        # Check if destination is a terminal ending
        if choice.get("tier") == "ending" or dest_room.get("tier") == "ending":
            from game.ending_resolver import resolve_terminal_event
            dest_id = result.destination
            ending_id = resolve_terminal_event(self.state, dest_id)

            self.state.terminal_outcome = ending_id
            from game.save import delete_saved_game
            delete_saved_game()
            prompt_line.update(f"> {choice.get('label', '')}")
            self.render_room(result.destination)

            end_title = dest_room.get("name")
            end_prose = dest_room.get("prose")
            for e in self.content.get("endings", []):
                if isinstance(e, dict) and e.get("id") == ending_id:
                    end_title = e.get("title", end_title)
                    end_prose = e.get("prose", end_prose)
                    break

            self.app.push_screen(
                EndingScreen(
                    room=dest_room,
                    content=self.content,
                    title=end_title,
                    prose=end_prose,
                    ending_id=ending_id,
                )
            )
            return

        # Check zero-composure voluntary walk (AC-11)
        if is_zero_composure(self.state):
            self.state.terminal_outcome = "shadow_walk"
            walk_room = self.get_room("shadow_walk_ending")
            self.render_room("shadow_walk_ending")
            self.app.push_screen(
                EndingScreen(
                    room=walk_room,
                    content=self.content,
                    ending_id="shadow_walk",
                )
            )
            return

        # Check zero-oil consequence
        if is_zero_oil(self.state):
            if self.state.current_room == "hall" and self.state.turn_count <= 3:
                self.state.set_flag("early_hall_death")
            self.state.terminal_outcome = "death"
            from game.save import delete_saved_game
            delete_saved_game()
            consequence = get_zero_oil_consequence()
            self.last_death_cause = consequence["cause"]
            self.state.journal.add_death(consequence["cause"], consequence.get("lesson", ""))
            self.render_room(result.destination)
            self.app.push_screen(
                DeathScreen(
                    cause=consequence["cause"],
                    lesson=consequence["lesson"],
                    content=self.content,
                    state=self.state,
                )
            )
            return

        if choice.get("tier") == "death" or dest_room.get("tier") == "death":
            if self.state.current_room == "hall" and self.state.turn_count <= 3:
                self.state.set_flag("early_hall_death")
            self.state.terminal_outcome = "death"
            from game.save import delete_saved_game
            delete_saved_game()
            cause = choice.get("cause") or dest_room.get("cause") or "You perished in the dark."
            lesson = choice.get("lesson") or dest_room.get("lesson") or ""
            self.last_death_cause = cause
            self.state.journal.add_death(cause, lesson)
            prompt_line.update(f"> {cause}")
            self.render_room(result.destination)
            self.app.push_screen(
                DeathScreen(
                    cause=cause,
                    lesson=lesson,
                    content=self.content,
                    state=self.state,
                )
            )
            return

        prompt_line.update(f"> {choice.get('label', '')}")
        self.render_room(result.destination)

    def action_select(self) -> None:
        prompt_line = self.query_one("#prompt-line", Static)

        if self.drop_mode:
            if self.drop_selected < len(self.state.held_items):
                dropped_id = self.state.held_items[self.drop_selected]
                dropped_name = self.get_item_name(dropped_id)
                self.state.drop_item(dropped_id)
                prompt_line.update(f"> Dropped {dropped_name}.")
                choice_to_retry = self.pending_grant_choice
                self.drop_mode = False
                self.pending_grant_choice = None
                self.drop_selected = 0
                self.update_status()
                if choice_to_retry:
                    self._execute_choice(choice_to_retry)
                else:
                    self.update_choices()
            else:
                self.cancel_drop()
            return

        if not self.current_choices:
            return

        choice = self.current_choices[self.selected_choice]
        self._execute_choice(choice)

    def action_open_journal(self) -> None:
        """Open the in-memory journal overlay."""
        self.app.push_screen(JournalScreen(self.state.journal))

    def action_back(self) -> None:
        if self.drop_mode:
            self.cancel_drop()
            return
        if self.state and not self.state.terminal_outcome:
            from game.save import save_to_disk
            save_to_disk(self.state)
        if hasattr(self.app, "active_run"):
            self.app.active_run = None
        self.app.pop_screen()
