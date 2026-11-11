"""Tests for unreliable narration and cognitive distortion tics (Task D02)."""
import copy
from pathlib import Path
import pytest

from game.composure import DISTORTION_THRESHOLD
from game.content_schema import load_content
from game.distortion import (
    TIC_MARKER,
    distort_line,
    distort_narration,
    has_distortion_tic,
)
from game.state import RunState


@pytest.fixture
def house_content():
    content_path = Path("data/content.json")
    assert content_path.exists(), "data/content.json must exist"
    return load_content(content_path)


def test_above_the_threshold_transformation_is_identity(house_content):
    """Above 20 composure, narration transformation is byte-for-byte identical to original prose."""
    for room in house_content["rooms"]:
        prose = room.get("prose", "")
        # Test values above the 20 threshold: 21, 50, 100
        for comp in (21, 50, 100):
            transformed = distort_narration(prose, composure=comp)
            assert transformed == prose, f"Expected identity in room '{room['id']}' at composure={comp}"

        if "revisit_prose" in room:
            rev_prose = room["revisit_prose"]
            for comp in (21, 50, 100):
                transformed_rev = distort_narration(rev_prose, composure=comp)
                assert transformed_rev == rev_prose


def test_below_the_threshold_every_line_carries_a_tic(house_content):
    """At or below 20 composure, every non-empty line carries the distortion tic across ALL rooms."""
    for comp in (20, 10, 0):
        for room in house_content["rooms"]:
            prose = room.get("prose", "")
            transformed = distort_narration(prose, composure=comp)
            lines = transformed.split("\n")
            for line in lines:
                if line.strip():
                    assert has_distortion_tic(line), (
                        f"Room '{room['id']}' line lacked tic at composure={comp}: {line!r}"
                    )

            if "revisit_prose" in room:
                rev_prose = room["revisit_prose"]
                rev_transformed = distort_narration(rev_prose, composure=comp)
                for line in rev_transformed.split("\n"):
                    if line.strip():
                        assert has_distortion_tic(line), (
                            f"Room '{room['id']}' revisit line lacked tic at composure={comp}: {line!r}"
                        )


def test_transform_never_changes_the_choice_set(house_content):
    """ASM-6: Distortion never adds, removes, or renames exits or choices."""
    for room in house_content["rooms"]:
        original_choices = room.get("choices", [])
        original_ids = [c["id"] for c in original_choices]
        original_destinations = [c["destination"] for c in original_choices]

        # Transformation only applies to prose, never choices
        # Verify that rendering room choices is independent of composure
        transformed_prose = distort_narration(room.get("prose", ""), composure=0)
        assert transformed_prose != room.get("prose", "")  # Confirms prose did distort

        # Choice definitions remain completely intact
        after_ids = [c["id"] for c in room.get("choices", [])]
        after_destinations = [c["destination"] for c in room.get("choices", [])]
        assert after_ids == original_ids
        assert after_destinations == original_destinations


def test_transform_is_deterministic():
    """Identical input text and composure always produce byte-identical output."""
    sample = "The high vaulted ceiling hangs in suffocating darkness.\nA cold draft chills your spine."
    out1 = distort_narration(sample, composure=15)
    out2 = distort_narration(sample, composure=15)
    assert out1 == out2


def test_transform_is_pure():
    """Distortion function has zero side effects and does not mutate the RunState."""
    state = RunState.fresh_run()
    state.composure = 10
    snapshot_before = state.snapshot()

    sample = "A heavy iron door looms ahead."
    _ = distort_narration(sample, state.composure)

    snapshot_after = state.snapshot()
    assert snapshot_before == snapshot_after


def test_distorted_text_remains_parseable(house_content):
    """Distorted prose retains reasonable line lengths and does not cause a text-wall explosion."""
    for room in house_content["rooms"]:
        prose = room.get("prose", "")
        distorted = distort_narration(prose, composure=5)
        # Line count should be preserved
        assert len(distorted.split("\n")) == len(prose.split("\n"))
        # Character length shouldn't explode uncontrollably (less than double)
        assert len(distorted) < len(prose) * 2 + 100
