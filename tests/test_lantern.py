import pytest
from game.state import RunState
from game.lantern import (
    FIRST_VISIT_DRAIN,
    REVISIT_DRAIN,
    CAREFUL_ACTION_DRAIN,
    STEP_ACTION_DRAIN,
    drain_for_room,
    drain_for_action,
)
from screens.game import GameScreen
from tests.test_game_screen import GameScreenTestApp


def test_first_visit_costs_more_than_revisit():
    state = RunState.fresh_run()
    room_id = "old_library"

    first_cost = drain_for_room(state, room_id)
    assert first_cost == FIRST_VISIT_DRAIN
    assert first_cost == 10

    state.visit(room_id)
    revisit_cost = drain_for_room(state, room_id)
    assert revisit_cost == REVISIT_DRAIN
    assert revisit_cost == 5

    assert first_cost > revisit_cost


def test_careful_action_costs_more_than_a_step():
    careful_cost = drain_for_action("careful")
    read_cost = drain_for_action("read")
    search_cost = drain_for_action("search")
    step_cost = drain_for_action("step")

    assert careful_cost == CAREFUL_ACTION_DRAIN
    assert read_cost == CAREFUL_ACTION_DRAIN
    assert search_cost == CAREFUL_ACTION_DRAIN
    assert step_cost == STEP_ACTION_DRAIN
    assert careful_cost > step_cost
    assert careful_cost >= 2 * step_cost


def test_spend_never_goes_below_zero_and_reports_actual_spend():
    state = RunState.fresh_run()
    state.lantern = 7

    cost = drain_for_room(state, "new_room")
    assert cost == 10

    actual_spent = state.spend_lantern(cost)
    assert actual_spent == 7
    assert state.lantern == 0
    assert state.has_light() is False


def test_drain_is_pure_and_does_not_mutate():
    state = RunState.fresh_run()
    initial_lantern = state.lantern
    initial_visited = set(state.visited)

    cost = drain_for_room(state, "unknown_chamber")
    assert cost == FIRST_VISIT_DRAIN
    assert state.lantern == initial_lantern
    assert state.visited == initial_visited

    action_cost = drain_for_action("careful")
    assert action_cost == CAREFUL_ACTION_DRAIN
    assert state.lantern == initial_lantern


@pytest.mark.anyio
async def test_game_screen_applies_oil_drain_on_room_transition():
    app = GameScreenTestApp()
    async with app.run_test() as pilot:
        screen = pilot.app.screen
        assert isinstance(screen, GameScreen)
        assert screen.state.lantern == 100

        # Move to "old_library" (first visit -> -10)
        await pilot.press("down")
        await pilot.press("enter")
        assert screen.state.current_room == "old_library"
        assert screen.state.lantern == 90

        # Return to "hall" (already visited on mount -> -5)
        # In old_library, choices are:
        # 0: library_read (costs 30 oil from effects, destination: old_library)
        # 1: library_return (destination: hall)
        await pilot.press("down")
        await pilot.press("enter")
        assert screen.state.current_room == "hall"
        assert screen.state.lantern == 85


from game.lantern import (
    LOW_OIL_WARNING_THRESHOLD,
    is_low_oil,
    is_zero_oil,
    get_zero_oil_consequence,
)
from game.content_schema import validate_content


def test_first_warning_fires_above_zero():
    assert LOW_OIL_WARNING_THRESHOLD > 0
    assert LOW_OIL_WARNING_THRESHOLD == 30

    state = RunState.fresh_run()
    state.lantern = 30
    assert is_low_oil(state) is True
    assert is_zero_oil(state) is False

    state.lantern = 31
    assert is_low_oil(state) is False


def test_zero_oil_produces_a_death_result_with_a_cause():
    consequence = get_zero_oil_consequence()
    assert consequence["tier"] == "death"
    assert isinstance(consequence["cause"], str)
    assert len(consequence["cause"].strip()) > 0
    assert consequence["cause"].endswith(".")
    assert "Shadow" in consequence["cause"]
    assert isinstance(consequence["lesson"], str)
    assert len(consequence["lesson"].strip()) > 0


def test_zero_oil_choice_has_two_distinct_telegraphs():
    consequence = get_zero_oil_consequence()
    telegraphs = consequence["telegraphs"]
    assert len(telegraphs) >= 2
    assert telegraphs[0] != telegraphs[1]
    # Sensory differentiation: visual vs thermal/auditory
    assert any("flame" in t or "edges" in t for t in telegraphs)
    assert any("draft" in t or "freezing" in t for t in telegraphs)


def test_warnings_precede_the_choice_and_validator_enforces_it():
    # Construct a content set with a zero-oil death choice containing the two telegraphs
    consequence = get_zero_oil_consequence()
    valid_content = {
        "start_room": "dim_hall",
        "rooms": [
            {
                "id": "dim_hall",
                "name": "Dim Hall",
                "prose": "The lantern is dying.",
                "choices": [
                    {
                        "id": "step_into_dark",
                        "label": "Step forward blindly into the pitch",
                        "destination": "shadow_void",
                        "tier": "death",
                        "telegraphs": consequence["telegraphs"],
                    }
                ],
            },
            {
                "id": "shadow_void",
                "name": "The Void",
                "prose": consequence["cause"],
                "choices": [],
            },
        ],
    }

    # Passes validation with two telegraphs
    assert validate_content(valid_content) == []

    # Removing one telegraph MUST cause validate_content to fail (enforcing the rule)
    invalid_content = {
        "start_room": "dim_hall",
        "rooms": [
            {
                "id": "dim_hall",
                "name": "Dim Hall",
                "prose": "The lantern is dying.",
                "choices": [
                    {
                        "id": "step_into_dark",
                        "label": "Step forward blindly into the pitch",
                        "destination": "shadow_void",
                        "tier": "death",
                        "telegraphs": [consequence["telegraphs"][0]],  # Only 1 telegraph!
                    }
                ],
            },
            {
                "id": "shadow_void",
                "name": "The Void",
                "prose": consequence["cause"],
                "choices": [],
            },
        ],
    }
    problems = validate_content(invalid_content)
    assert len(problems) > 0
    assert any("at least two telegraphs" in p.message for p in problems)
