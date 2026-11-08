I am building a terminal adventure game in Python using the Textual framework. 

Currently, my project consists of two files:
1. `index.py`: Subclasses `App` with a main menu ("START GAME", "SETTINGS", "ABOUT", "EXIT").
2. `settings.py`: Subclasses `Screen` (`SettingsScreen`) containing interactive toggles/cycles for game options (e.g., "DIFFICULTY" [EASY, MEDIUM, HARD], "SOUND" [ON/OFF], "MUSIC" [ON/OFF], and "EXIT").

I need to implement a clean, production-grade JSON-based settings persistence system following the Separation of Concerns principle.

Please implement the following architecture:

### 1. Dedicated Settings Manager (`config.py`):
Create a `SettingsManager` class that:
- Uses Python's built-in `json` and `pathlib.Path` modules.
- Stores configuration in a local `settings.json` file.
- Defines a robust dictionary of default settings (e.g., `{"difficulty": "MEDIUM", "sound": True, "music": True}`).
- Implements a `.load()` method that safely reads `settings.json`. If the file does not exist, is empty, or contains invalid/corrupted JSON, it gracefully falls back to the default values and creates/repairs the file without crashing.
- Implements a `.save()` method that writes the current configuration dictionary to `settings.json` with clean indentation (`indent=4`).
- Provides clean getter/setter helper methods or dictionary-like access (`get(key, default)`, `set(key, value)`).

### 2. Integration with `index.py`:
- Initialize `SettingsManager` during app initialization (`__init__` or `on_mount`).
- Expose the manager on the app instance (`self.config`) so all screens and downstream game systems can access it globally.
- Ensure the main game reads values (like current difficulty) directly from `self.config`.

### 3. Integration with `settings.py` (`SettingsScreen`):
- Upon opening `SettingsScreen`, load the active values from `self.app.config`.
- When the user cycles "DIFFICULTY" or toggles "MUSIC" / "SOUND", immediately update the in-memory config and call `.save()` (or save when exiting the screen).
- Ensure the UI status and labels reflect the persisted values correctly on mount.
- Handle screen dismissal properly using `self.app.pop_screen()`.

Please provide the complete, runnable code for:
- `config.py`
- Refactored `settings.py`
- Refactored `index.py`
- An example of the resulting `settings.json` structure