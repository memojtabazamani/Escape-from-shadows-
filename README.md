# Escape from Shadows 

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A terminal-based adventure game built with Python and [Textual](https://textual.textualize.io/). Navigate dark menus, configure your experience, and prepare to escape the shadows.

## Features

- 🎮 **Keyboard-Driven Adventure** — Navigate rooms and make choices with arrow keys and Enter/Escape without typed input friction.
- 🕯️ **Lantern Survival System** — Manage a 10-cell quantized lantern bar where exploration and careful actions drain oil; darkness is fatal.
- 🎒 **Six-Slot Inventory System** — 6 canonical items, strict capacity limit, requirement gating, and drop-to-take replacement flow.
- 🧠 **Composure & Sanity Model** — Sensory distortion tics below 20% composure and voluntary walk into the Shadow at zero composure.
- 📖 **In-Game Journal** — Keybound overlay (`j`/`J`) logging room discoveries, death lessons, and Shadow whispers.
- 🐕 **The House & The Hell Dog** — Explore The Hall, Blood Kitchen, Old Library, and Old Yard; evade or pacify the hound via four distinct solutions.
- 🔔 **Atmospheric Audio & Visual Rhythm** — Horror system bell sound cues, smooth typewriter prose reveal (any-key skip), and heartbeat border pulsing with reduce-motion toggle.
- 💾 **Single-Slot Save & Continue** — Atomic JSON persistence with `CONTINUE` menu action; auto-saves on quit, purges on death or victory.
- 💀 **Honest Death & Escape Endings** — Unwarned deaths are strictly forbidden; terminal screens present verbatim structured causes, lessons, and difficulty-gated hints.
- ⚙️ **Persistent Settings** — Configure difficulty (Easy, Medium, Hard), sound, and music via `SettingsManager`.
- 🧪 **Comprehensive Regression Net** — 260+ unit, integration, and pilot tests guarding navigation, state mutation, and the full game loop.

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd "Escape-from-shadows 👻"
```

2. Install the required dependencies:

```bash
pip install textual pytest anyio
```

## Usage

Run the game from the project root:

```bash
python index.py
```

### Controls

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
│   ├── content_schema.py    # Content schemas, loader, and validator
│   ├── effects.py           # Requirement and effect resolution engine
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
│   ├── GENERAL_DOC.md       # User and developer documentation
│   ├── SUGGEST.md           # Master game design specification
│   ├── PHASE1/              # Phase 1 planning archive (superseded by PHASE2)
│   └── PHASE2/              # Phase 2: The House plan and task directory
├── AGENTS.md                # Instructions for AI assistants
├── README.md                # This file
└── LICENSE                  # MIT License
```

## Development & Testing

- Follow PEP 8 and use type hints.
- Run tests: `python -m pytest`
- Run syntax compile checks:
  `python -c "import py_compile, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('*.py') + glob.glob('screens/*.py') + glob.glob('game/*.py') + glob.glob('tests/*.py')]"`

## Documentation

- For general documentation, see [`docs/GENERAL_DOC.md`](docs/GENERAL_DOC.md).
- For contributor and AI agent instructions, see [`AGENTS.md`](AGENTS.md).
- For game architecture and master design, see [`docs/SUGGEST.md`](docs/SUGGEST.md).
- For Phase 2 tasks and execution plans, see [`docs/PHASE2/`](docs/PHASE2/).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
