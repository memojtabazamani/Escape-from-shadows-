"""Tests for ASCII art vignettes across all canonical endings (Task B03)."""

import pytest
from game.endings import CANONICAL_ENDINGS
from game.endings_art import (
    ASCII_FALLBACK,
    MAX_ASCII_HEIGHT,
    MAX_ASCII_WIDTH,
    get_ending_ascii,
)


def test_all_endings_have_ascii_art():
    """AC-12: Every canonical ending has a dedicated, non-empty ASCII art vignette."""
    for ending_id in CANONICAL_ENDINGS.keys():
        art = get_ending_ascii(ending_id)
        assert art, f"Ending '{ending_id}' returned empty ASCII art"
        assert art != ASCII_FALLBACK, f"Ending '{ending_id}' returned fallback art instead of dedicated vignette"
        # Pure ASCII check
        assert all(ord(ch) < 128 for ch in art), f"Ending '{ending_id}' contains non-ASCII characters"


def test_ascii_dimensions_within_budget():
    """§7.3: Every vignette conforms to the <= 8 rows and <= 60 columns budget."""
    for ending_id in CANONICAL_ENDINGS.keys():
        art = get_ending_ascii(ending_id)
        lines = art.split("\n")
        assert len(lines) <= MAX_ASCII_HEIGHT, (
            f"Ending '{ending_id}' art has {len(lines)} lines, exceeding max {MAX_ASCII_HEIGHT}"
        )
        for line_num, line in enumerate(lines, 1):
            assert len(line) <= MAX_ASCII_WIDTH, (
                f"Ending '{ending_id}' line {line_num} has length {len(line)}, exceeding max {MAX_ASCII_WIDTH}: {line!r}"
            )


def test_unknown_ending_returns_fallback():
    """Unknown or empty ending IDs safely return fallback marker within constraints."""
    for bad_id in ("unknown_id", "", "   ", None):
        art = get_ending_ascii(bad_id)
        assert art == ASCII_FALLBACK
        lines = art.split("\n")
        assert len(lines) <= MAX_ASCII_HEIGHT
        for line in lines:
            assert len(line) <= MAX_ASCII_WIDTH


def test_shadow_walk_has_ascii_art():
    """Voluntary shadow walk returns its dedicated minimalist ASCII vignette within constraints."""
    art = get_ending_ascii("shadow_walk")
    assert art != ASCII_FALLBACK
    assert all(ord(ch) < 128 for ch in art)
    lines = art.split("\n")
    assert len(lines) <= MAX_ASCII_HEIGHT
    for line in lines:
        assert len(line) <= MAX_ASCII_WIDTH
