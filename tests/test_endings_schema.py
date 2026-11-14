"""Tests for canonical endings schema and registry (Task A02)."""

import pytest

from game.content_schema import SAMPLE_CONTENT, validate_content
from game.endings import (
    CANONICAL_ENDINGS,
    CANONICAL_ENDINGS_LIST,
    TOTAL_CANONICAL_ENDINGS,
    EndingMetadata,
    get_all_canonical_endings,
    get_ending_metadata,
)


def test_canonical_endings_registry_completeness():
    """Asserts exactly 7 canonical endings exist with numbers 1..7 and non-empty metadata."""
    assert TOTAL_CANONICAL_ENDINGS == 7
    assert len(CANONICAL_ENDINGS) == 7
    assert len(CANONICAL_ENDINGS_LIST) == 7

    expected_ids = {
        "the_long_walk",
        "meat_and_silence",
        "the_quiet_exit",
        "what_the_book_knew",
        "the_new_shadow",
        "homecoming",
        "stay",
    }
    assert set(CANONICAL_ENDINGS.keys()) == expected_ids

    numbers = set()
    for ending_id, meta in CANONICAL_ENDINGS.items():
        assert isinstance(meta, EndingMetadata)
        assert meta.id == ending_id
        assert 1 <= meta.number <= 7
        assert meta.title.strip() != ""
        assert meta.tone.strip() != ""
        assert meta.hint.strip() != ""
        assert meta.summary.strip() != ""
        numbers.add(meta.number)

    assert numbers == set(range(1, 8))

    sorted_endings = get_all_canonical_endings()
    assert [e.number for e in sorted_endings] == list(range(1, 8))


def test_schema_validates_endings_section():
    """Content dictionary containing valid endings passes validation."""
    content = dict(SAMPLE_CONTENT)
    content["endings"] = [
        {
            "id": "the_quiet_exit",
            "title": "The Quiet Exit",
            "tone": "Standard win",
            "summary": "You unlatched the front door and walked out.",
        },
        {
            "id": "stay",
            "title": "Stay",
            "prose": "You closed the door and stayed in the dark.",
        },
    ]

    problems = validate_content(content)
    assert problems == []


def test_missing_ending_lookup_returns_none():
    """Lookup of unknown ending ID safely returns None."""
    assert get_ending_metadata("non_existent_ending_id") is None
    assert get_ending_metadata("") is None

    # Valid lookup
    meta = get_ending_metadata("the_quiet_exit")
    assert meta is not None
    assert meta.id == "the_quiet_exit"
    assert meta.title == "The Quiet Exit"


def test_schema_flags_invalid_ending_records():
    """Validator catches duplicate ending IDs, missing title/prose, and malformed types."""
    # 1. Non-list endings
    bad_content_1 = dict(SAMPLE_CONTENT)
    bad_content_1["endings"] = "not a list"
    problems = validate_content(bad_content_1)
    assert any("must be a list of ending records" in p.message for p in problems)

    # 2. Duplicate ID
    bad_content_2 = dict(SAMPLE_CONTENT)
    bad_content_2["endings"] = [
        {"id": "dup", "title": "First", "prose": "Text"},
        {"id": "dup", "title": "Second", "prose": "Text"},
    ]
    problems = validate_content(bad_content_2)
    assert any("duplicate ending id 'dup'" in p.message for p in problems)

    # 3. Missing title or prose
    bad_content_3 = dict(SAMPLE_CONTENT)
    bad_content_3["endings"] = [
        {"id": "incomplete"},
    ]
    problems = validate_content(bad_content_3)
    assert any("ending title must be a non-empty string" in p.message for p in problems)
    assert any("ending prose/summary must be a non-empty string" in p.message for p in problems)
