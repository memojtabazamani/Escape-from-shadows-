# Escape from Shadows — General Documentation

## Overview

**Escape from Shadows** is a terminal-based adventure game built with Python and the [Textual](https://textual.textualize.io/) framework. The project provides a polished Text User Interface (TUI) with a main menu, settings, and about screens, laying the foundation for future gameplay.

## Features

- **Terminal User Interface (TUI):** Clean, keyboard-driven menus styled with Textual CSS.
- **Main Menu:** Start game, Settings, About, Exit.
- **Settings Screen:** Adjust difficulty (Easy / Medium / Hard), toggle sound, and toggle music.
- **Keyboard Navigation:** Full arrow-key and Enter/Escape control.
- **Extensible Structure:** Separate modules for screens and game logic, making it easy to add new features.

## Requirements

- Python 3.10 or newer
- Textual

## Installation

1. Clone the repository.
2. Install dependencies:

```bash
pip install textual
```

## Usage

Start the application from the project root:

```bash
python index.py
```

Use the arrow keys to navigate, Enter to select, and Escape to go back or quit.

## Controls

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
├── screens/
│   ├── main_menu.py         # Main menu screen (stub)
│   └── settings.py          # Settings screen implementation
├── game/
│   └── settings_manager.py  # Settings management logic (stub)
├── docs/
│   └── GENERAL_DOC.md       # This document
├── AGENTS.md                # Instructions for AI assistants
├── README.md                # Project overview
└── LICENSE                  # MIT License
```

## Configuration

Game settings such as difficulty, sound, and music are currently managed in memory via the settings screen. Persistent storage will be handled by `game/settings_manager.py` as the project grows.

## Development Notes

- The main application class is `TerminalGame`, defined in `index.py`.
- Each screen is a separate class inheriting from `textual.screen.Screen`.
- Shared state (e.g., `difficulty`) is stored on the app object and accessed via `self.app` inside screens.

## Future Plans

- Implement `main_menu.py` with richer visuals and a game-start flow.
- Implement `settings_manager.py` to persist settings to a file.
- Add the actual gameplay screen and adventure mechanics.
- Add unit tests for screen navigation and settings logic.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
