import os
import shutil
import tempfile
from pathlib import Path
import pytest
from game.save import DEFAULT_SAVE_PATH


@pytest.fixture(autouse=True)
def cleanup_default_savegame():
    if DEFAULT_SAVE_PATH.exists():
        try:
            DEFAULT_SAVE_PATH.unlink()
        except Exception:
            pass
    yield
    if DEFAULT_SAVE_PATH.exists():
        try:
            DEFAULT_SAVE_PATH.unlink()
        except Exception:
            pass


@pytest.fixture
def tmp_path():
    """Robust tmp_path fixture immune to Windows temp directory locking / WinError 5."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
