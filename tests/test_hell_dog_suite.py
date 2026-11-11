"""Exhaustive integration test suite for the Hell Dog encounter (Task G04)."""

from pathlib import Path
import pytest
from game.content_schema import load_content, validate_content
from game.effects import resolve_choice
from game.state import RunState


@pytest.fixture
def content():
    return load_content(Path("data/content.json"))


def test_dog_encounter_schema_validates(content):
    problems = validate_content(content)
    assert problems == [], f"Validation problems found: {[str(p) for p in problems]}"


def test_all_four_solutions_execute_with_distinct_outcomes(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    choices = {c["id"]: c for c in kennel["choices"]}

    outcomes = {}

    # 1. Slow
    s1 = RunState.fresh_run()
    resolve_choice(choices["dog_slow"], s1)
    outcomes["slow"] = (s1.lantern, s1.composure, tuple(sorted(s1.flags)))

    # 2. Sprint
    s2 = RunState.fresh_run()
    s2.composure = 60
    resolve_choice(choices["dog_sprint"], s2)
    outcomes["sprint"] = (s2.lantern, s2.composure, tuple(sorted(s2.flags)))

    # 3. Meat
    s3 = RunState.fresh_run()
    s3.set_flag("has_meat")
    resolve_choice(choices["dog_feed_meat"], s3)
    outcomes["meat"] = (s3.lantern, s3.composure, tuple(sorted(s3.flags)))

    # 4. Whistle
    s4 = RunState.fresh_run()
    s4.add_item("silver_whistle")
    s4.set_flag("knows_dog_name")
    resolve_choice(choices["dog_whistle_named"], s4)
    outcomes["whistle"] = (s4.lantern, s4.composure, tuple(sorted(s4.flags)))

    # Verify that all 4 outcome profiles are unique
    assert len(set(outcomes.values())) == 4, f"Outcomes collapsed: {outcomes}"


def test_dog_freeze_rule_safe_oil_drain(content):
    kennel = next(r for r in content["rooms"] if r["id"] == "yard_doghouse_encounter")
    freeze_choice = next(c for c in kennel["choices"] if c["id"] == "dog_freeze")

    state = RunState.fresh_run()
    init_oil = state.lantern
    res = resolve_choice(freeze_choice, state)
    assert res.refused is False
    assert state.lantern == init_oil - 1
    assert state.has_flag("knows_dog_freezes")
