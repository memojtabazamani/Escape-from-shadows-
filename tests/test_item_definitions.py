"""Tests for item definitions as content (Task C03)."""

from game.content_schema import load_content, validate_content

EXPECTED_ITEM_IDS = {
    "matchbox",
    "rusty_cleaver",
    "the_book",
    "silver_whistle",
    "dogs_tooth",
    "front_door_key",
}


def test_all_six_items_have_definitions():
    content = load_content("data/content.json")
    items = content.get("items", [])
    item_ids = {it["id"] for it in items}

    assert EXPECTED_ITEM_IDS.issubset(item_ids)
    assert len(item_ids) == 6


def test_every_grant_item_reference_resolves():
    content = load_content("data/content.json")
    problems = validate_content(content)
    # Referential integrity check from validator should find zero problems
    assert not any("grant_item" in str(p) for p in problems)


def test_item_ids_are_unique_and_stable():
    content = load_content("data/content.json")
    items = content.get("items", [])
    raw_ids = [it["id"] for it in items]

    assert len(raw_ids) == len(set(raw_ids))
    for expected_id in EXPECTED_ITEM_IDS:
        assert expected_id in raw_ids


def test_every_item_description_states_a_cost_or_risk():
    content = load_content("data/content.json")
    items = content.get("items", [])

    cost_indicators = [
        "shadow",
        "drains",
        "slow",
        "watched",
        "echoes",
        "stench",
        "death",
        "trap",
        "danger",
        "risk",
        "reek",
    ]

    for it in items:
        desc = it.get("description", "").lower()
        assert len(desc) > 10
        # Every item description must hint at a cost or risk (§3.3)
        assert any(ind in desc for ind in cost_indicators), f"Item '{it['id']}' missing cost/risk indicator"


def test_no_item_is_required_for_basic_traversal():
    content = load_content("data/content.json")
    # In baseline content, moving between hall and old_library must not require any item
    hall = next(r for r in content["rooms"] if r["id"] == "hall")
    library_choice = next(c for c in hall["choices"] if c.get("destination") == "old_library")

    reqs = library_choice.get("requirements", [])
    assert not any(r.get("predicate") == "has_item" for r in reqs)
