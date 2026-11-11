# Agent Instructions

This file guides AI assistants and contributors working on **Escape from Shadows**.

## Project Identity

- **Name:** Escape from Shadows (in-game title: *Dark Quest*)
- **Type:** Terminal-based adventure game UI
- **Framework:** [Textual](https://textual.textualize.io/) (Python TUI framework)
- **Runtime:** Python 3.10+
- **License:** MIT

## Architecture

```text
.
├── index.py                 # Application entry point; hosts TerminalGame app
├── config.py                # JSON settings persistence (SettingsManager)
├── data/
│   └── content.json         # Declarative room, choice, item, and consequence data
├── game/
│   ├── state.py             # RunState model with snapshot/restore & inventory cap
│   ├── content_schema.py    # Schema definitions, loader, and validator
│   ├── effects.py           # Requirements checker and effect applicator
│   ├── lantern.py           # Lantern drain rules and cost calculator
│   ├── difficulty.py        # Difficulty parameters and knob configurations
│   ├── composure.py         # Composure threshold calculations
│   ├── distortion.py        # Unreliable narration text distortion
│   ├── hints.py             # Stuck hint calculation on Easy difficulty
│   ├── journal.py           # Journal model & category tracking
│   ├── multiturn.py         # Multi-turn continuous action engine
│   ├── sound.py             # Bell-based audio dispatch service
│   └── save.py              # Single-slot atomic JSON persistence
├── screens/
│   ├── main_menu.py         # Main menu screen (Start, Continue, Settings, Exit)
│   ├── settings.py          # Settings screen for difficulty, sound, music
│   ├── game.py              # Gameplay screen with scene, status, and footer zones
│   ├── death.py             # Terminal death screen with structured cause, lesson & hint
│   ├── ending.py            # Terminal victory/escape screen
│   └── journal.py           # Journal modal overlay (j/J)
├── tests/                   # Full pytest regression suite (263 passing tests)
├── docs/
│   ├── GENERAL_DOC.md       # General user and developer documentation
│   ├── SUGGEST.md           # Master game design specification
│   ├── PHASE1/              # Phase 1 planning archive (superseded by PHASE2)
│   └── PHASE2/              # Phase 2: The House plan and task directory
└── AGENTS.md                # This file
```

## Tech Stack

- Python 3.10 or newer
- Textual (`pip install textual`)

## How to Run

```bash
python index.py
```

## Coding Conventions

- Use **type hints** where practical (`ComposeResult` is already used in `index.py`).
- Follow **PEP 8** for Python code.
- Keep screen logic in `screens/` and shared game state in `game/`.
- Use `self.app` to share state between screens (see `settings.py` for examples).
- Avoid heavy logic inside `compose()`; delegate to helper methods.

## Common Tasks

- **Add a new menu option:** Update `self.options` and `action_select()` in `screens/main_menu.py`.
- **Add a new screen:** Create a class inheriting from `textual.screen.Screen`, add navigation in `index.py`, and push it with `self.push_screen(NewScreen())`.
- **Persist settings:** Use `config.py` (`SettingsManager`). Access it via `self.app.config` in screens.
- **Style the UI:** Edit the `CSS` class attribute on screens or the main app.

## Controls

| Key      | Action                |
|----------|---------------------- |
| ↑ / ↓    | Navigate menu / choices|
| Enter    | Select / toggle value |
| ← / →    | Change setting value  |
| j / J    | Open in-game journal  |
| Escape   | Exit / back (auto-save)|

## Things to Avoid

- Do not introduce GUI libraries; this is a terminal UI project.
- Do not commit `__pycache__`, `.venv`, or IDE-specific files.
- Do not hard-code paths; use cross-platform Python APIs.

## Quick Checks Before Committing

1. Run `python index.py` and verify the app starts without errors.
2. Navigate the menu with arrow keys and ensure Enter/Escape work.
3. Run `python -m py_compile index.py config.py screens/*.py` to catch syntax errors.
