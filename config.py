"""Persistent JSON settings management for Escape from Shadows."""

import json
from pathlib import Path
from typing import Any


class SettingsManager:
    """Manages game settings stored in a local JSON file.

    The manager provides safe loading, default fallbacks, and immediate
    persistence. It is intentionally dependency-free beyond the Python
    standard library so it can be imported anywhere in the project.
    """

    DEFAULT_SETTINGS = {
        "difficulty": "MEDIUM",
        "sound": True,
        "music": True,
    }

    def __init__(self, file_path: str | Path = "settings.json") -> None:
        """Initialize the manager and load existing settings.

        Args:
            file_path: Path to the JSON settings file. Defaults to
                ``settings.json`` in the working directory.
        """
        self._path = Path(file_path)
        self._settings: dict[str, Any] = {}
        self.load()

    @property
    def path(self) -> Path:
        """Path to the underlying settings file."""
        return self._path

    def load(self) -> None:
        """Load settings from disk.

        If the file is missing, empty, or corrupt, reset to defaults and
        persist a clean copy so the next run starts from a known-good state.
        """
        loaded: dict[str, Any] = {}

        if self._path.exists() and self._path.stat().st_size > 0:
            try:
                with self._path.open("r", encoding="utf-8") as file:
                    loaded = json.load(file)
                if not isinstance(loaded, dict):
                    raise ValueError("Settings file must contain a JSON object")
            except (json.JSONDecodeError, OSError, ValueError):
                loaded = {}

        # Merge loaded values over defaults to ensure every expected key exists
        # and unknown/corrupt files are repaired transparently.
        self._settings = {**self.DEFAULT_SETTINGS, **loaded}
        self.save()

    def save(self) -> None:
        """Persist the current settings dictionary to disk."""
        self._path.write_text(
            json.dumps(self._settings, indent=4) + "\n",
            encoding="utf-8",
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value by key.

        Args:
            key: The setting name.
            default: Value returned if the key is absent.

        Returns:
            The stored value or ``default``.
        """
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a setting value and immediately persist it.

        Args:
            key: The setting name.
            value: The value to store. Must be JSON-serializable.
        """
        self._settings[key] = value
        self.save()

    def reset(self) -> None:
        """Reset all settings to defaults and persist."""
        self._settings = dict(self.DEFAULT_SETTINGS)
        self.save()

    def to_dict(self) -> dict[str, Any]:
        """Return a shallow copy of the current settings dictionary."""
        return dict(self._settings)
