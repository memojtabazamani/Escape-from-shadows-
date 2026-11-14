"""Tests for canonical endings content in data/content.json (Task B01)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.endings import CANONICAL_ENDINGS


@pytest.fixture
def content():
    path = Path("data/content.json")
    assert path.exists(), "data/content.json must exist"
    return load_content(path)


def test_all_seven_endings_present_in_content(content):
    """AC-4: Asserts all 7 canonical IDs exist in data/content.json."""
    assert "endings" in content, "content must contain an 'endings' key"
    endings = content["endings"]
    assert isinstance(endings, list)

    endings_by_id = {e["id"]: e for e in endings if isinstance(e, dict) and "id" in e}
    for canon_id in CANONICAL_ENDINGS.keys():
        assert canon_id in endings_by_id, f"Missing canonical ending '{canon_id}' in content.json"
        ending = endings_by_id[canon_id]
        assert ending.get("title"), f"Ending '{canon_id}' must have a non-empty title"
        assert ending.get("prose"), f"Ending '{canon_id}' must have a non-empty prose"
        assert ending.get("tone"), f"Ending '{canon_id}' must have a non-empty tone"
        assert ending.get("terminal_type") in ("victory", "death", "choice")


def test_endings_prose_budget_under_limit(content):
    """Each ending prose must fit a single terminal screen without scrolling (<= 20 lines)."""
    endings = content.get("endings", [])
    for ending in endings:
        prose = ending.get("prose", "")
        lines = prose.split("\n")
        assert len(lines) <= 20, f"Ending '{ending.get('id')}' prose exceeds 20 lines ({len(lines)})"
        assert len(lines) >= 1


def test_endings_schema_validation(content):
    """Validates entire content file through validate_content()."""
    problems = validate_content(content)
    assert problems == [], f"Validation problems found: {[str(p) for p in problems]}"
