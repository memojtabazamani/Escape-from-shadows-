# Escape from Shadows 

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A terminal-based adventure game built with Python and [Textual](https://textual.textualize.io/). Navigate dark menus, configure your experience, and prepare to escape the shadows.

## Features

- 🎮 **Keyboard-Driven Menu System** — Navigate with arrow keys and Enter/Escape.
- ⚙️ **In-Game Settings** — Adjust difficulty, sound, and music.
- ️ **Terminal UI** — Styled with Textual CSS for a polished console experience.
- 🧩 **Modular Structure** — Screens and game logic are separated for easy expansion.

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd "Escape-from-shadows 👻"
```

2. Install the required dependency:

```bash
pip install textual
```

## Usage

Run the game from the project root:

```bash
python index.py
```

### Controls

| Key      | Action                              |
|----------|-------------------------------------|
| ↑ / ↓    | Move selection up / down            |
| ← / →    | Change the value of a setting       |
| Enter    | Confirm selection or toggle a value |
| Escape   | Go back / exit                      |

## Project Structure

```text
.
├── index.py                 # Application entry point
├── config.py                # JSON settings persistence (SettingsManager)
├── screens/
│   ├── main_menu.py         # Main menu screen (stub)
│   └── settings.py          # Settings screen
├── game/
│   └── settings_manager.py  # Settings management logic (stub)
├── docs/
│   └── GENERAL_DOC.md       # General documentation
├── AGENTS.md                # Agent / contributor guidelines
├── README.md                # This file
└── LICENSE                  # MIT License
```

## Development

- Follow PEP 8 and use type hints where practical.
- Keep screen logic in `screens/` and shared game state in `game/`.
- Run `python -m py_compile index.py screens/*.py game/*.py` before committing to catch syntax errors.

## Documentation

- For general documentation, see [`docs/GENERAL_DOC.md`](docs/GENERAL_DOC.md).
- For contributor / agent guidelines, see [`AGENTS.md`](AGENTS.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
