# Escape from Shadows — General Documentation

## Overview

**Escape from Shadows** is a terminal-based adventure game built with Python and the [Textual](https://textual.textualize.io/) framework. Players navigate a dark, threatening manor where light is life, every room incurs an oil cost, and darkness brings death by the Shadow.

## Features

- **Terminal User Interface (TUI):** Clean, keyboard-driven interface styled with Textual CSS across three dedicated zones (scene, status, footer).
- **Interactive Gameplay Loop:** Navigate rooms, inspect choices, examine sensory telegraphs, and unlock exits.
- **Lantern Oil Economy:** Quantized 10-cell bar reflecting oil depletion; first-visit costs (10 oil), revisit discounts (5 oil), and careful-action costs (25 oil).
- **Honest Consequence Model:** Telegraphed deaths with structured causes and lessons; quiet escape resolutions.
- **Data-Driven Architecture:** All room prose, choices, requirements, and effects live in JSON data files (`data/content.json`).
- **Settings Screen:** Adjust difficulty (Easy / Medium / Hard), sound, and music preferences.

## Requirements

- Python 3.10 or newer
- Textual, pytest, anyio

## Installation

1. Clone the repository.
2. Install dependencies:

```bash
pip install textual pytest anyio
```

## Usage

Start the application from the project root:

```bash
python index.py
```

Use the arrow keys to navigate choices, Enter to select, and Escape to go back or return to menu.

## Controls

| Key      | Action                              |
|----------|-------------------------------------|
| ↑ / ↓    | Move choice / menu cursor           |
| ← / →    | Change setting value                |
| Enter    | Select choice / toggle setting      |
| j / J    | Open in-game journal overlay        |
| Escape   | Go back / return to menu (auto-saves)|

## Project Structure

```text
.
├── index.py                 # Application entry point (TerminalGame)
├── config.py                # JSON settings persistence (SettingsManager)
├── data/
│   └── content.json         # Declarative room, choice, item, and consequence data
├── game/
│   ├── state.py             # RunState model with snapshot/restore & inventory cap
│   ├── content_schema.py    # Schema definitions, loader, and validator
│   ├── effects.py           # Requirements and effects resolution engine
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
│   ├── settings.py          # Settings screen (Difficulty, Sound, Music)
│   ├── game.py              # Gameplay screen with scene, status, and footer zones
│   ├── death.py             # Terminal death screen with structured cause, lesson & hint
│   ├── ending.py            # Terminal escape ending screen
│   └── journal.py           # Journal modal overlay (j/J)
├── tests/                   # Complete regression test suite (263 passing tests)
├── docs/
│   ├── GENERAL_DOC.md       # This document
│   ├── SUGGEST.md           # Master game design specification
│   ├── PHASE1/              # Phase 1 planning archive (superseded by PHASE2)
│   └── PHASE2/              # Phase 2: The House plan and task directory
├── AGENTS.md                # Instructions for AI assistants
├── README.md                # Project overview
└── LICENSE                  # MIT License
```

## Configuration

Game settings (difficulty, sound, music) are persisted to a local `settings.json` file via `config.py` (`SettingsManager`). The settings screen reads from and writes to `self.app.config`, and changes are saved immediately.

## Development Notes

- The main application class is `TerminalGame`, defined in `index.py`. It owns `self.config` and the active run state (`self.active_run`).
- Each screen inherits from `textual.screen.Screen`.
- Shared state is managed via `self.app` across screens.
- Run tests: `python -m pytest`

## Roadmap & Phase 3 Handoff

Phase 2 ("The House") is complete with all 55 tasks implemented across 9 vertical slices.

Planned for **Phase 3 — The Shadow**:
- Shadow as a pursuing entity with rules (lit-room rule, pursuit timer)
- Shadow dialogue drawn from the player's own history
- 5–7 ending spread and endings gallery
- Three memory fragments

## License

This project is licensed under the MIT License. See `LICENSE` for details.
