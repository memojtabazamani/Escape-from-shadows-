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
├── screens/
│   ├── main_menu.py         # Main menu screen (currently stubbed)
│   └── settings.py          # Settings screen for difficulty, sound, music
├── game/
│   └── settings_manager.py  # Settings persistence/logic (currently stubbed)
├── docs/
│   └── GENERAL_DOC.md       # General user and developer documentation
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

- **Add a new menu option:** Update `self.options` and `action_select()` in `index.py`.
- **Add a new screen:** Create a class inheriting from `textual.screen.Screen`, add navigation in `index.py`, and push it with `self.push_screen(NewScreen())`.
- **Persist settings:** Use `config.py` (`SettingsManager`). Access it via `self.app.config` in screens.
- **Style the UI:** Edit the `CSS` class attribute on screens or the main app.

## Controls

| Key      | Action                |
|----------|---------------------- |
| ↑ / ↓    | Navigate menu         |
| Enter    | Select / toggle value |
| ← / →    | Change setting value  |
| Escape   | Exit / back           |

## Things to Avoid

- Do not introduce GUI libraries; this is a terminal UI project.
- Do not commit `__pycache__`, `.venv`, or IDE-specific files.
- Do not hard-code paths; use cross-platform Python APIs.

## Quick Checks Before Committing

1. Run `python index.py` and verify the app starts without errors.
2. Navigate the menu with arrow keys and ensure Enter/Escape work.
3. Run `python -m py_compile index.py config.py screens/*.py game/*.py` to catch syntax errors.
