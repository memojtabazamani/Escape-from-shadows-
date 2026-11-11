"""Unit and integration tests for multi-turn action support (Task F01)."""

from game.effects import apply_effects, check_requirements, resolve_choice
from game.multiturn import MultiTurnAction
from game.state import RunState


def test_multiturn_action_lifecycle():
    """Advances step by step, applies incremental costs, triggers completion effects at target step."""
    state = RunState.fresh_run()
    initial_lantern = state.lantern

    action = state.start_multiturn(
        action_id="read_book",
        total_steps=3,
        step_costs=[{"verb": "spend_oil", "amount": 2}],
        completion_effects=[{"verb": "set_flag", "flag": "read_the_book"}],
    )

    assert state.has_active_multiturn("read_book")
    assert not state.has_flag("read_the_book")
    assert state.active_action.current_step == 0

    # Step 1
    completed, costs = state.advance_multiturn()
    assert not completed
    assert costs == [{"verb": "spend_oil", "amount": 2}]
    assert state.active_action.current_step == 1
    apply_effects(costs, state)
    assert state.lantern == initial_lantern - 2

    # Step 2
    completed, costs = state.advance_multiturn()
    assert not completed
    assert state.active_action.current_step == 2
    apply_effects(costs, state)
    assert state.lantern == initial_lantern - 4

    # Step 3 (completion)
    completed, completion_effects = state.advance_multiturn()
    assert completed
    assert completion_effects == [{"verb": "set_flag", "flag": "read_the_book"}]
    assert state.active_action is None
    assert not state.has_active_multiturn()

    apply_effects(completion_effects, state)
    assert state.has_flag("read_the_book")


def test_multiturn_interruption():
    """Cancelling resets active action without triggering completion effects."""
    state = RunState.fresh_run()
    state.start_multiturn(
        action_id="read_book",
        total_steps=3,
        step_costs=[{"verb": "spend_oil", "amount": 1}],
        completion_effects=[{"verb": "set_flag", "flag": "read_the_book"}],
        cancel_effects=[{"verb": "spend_composure", "amount": 5}],
    )

    state.advance_multiturn()
    assert state.active_action.current_step == 1
    assert state.has_active_multiturn("read_book")

    cancel_effects = state.cancel_multiturn()
    assert state.active_action is None
    assert not state.has_active_multiturn()
    assert cancel_effects == [{"verb": "spend_composure", "amount": 5}]

    apply_effects(cancel_effects, state)
    assert not state.has_flag("read_the_book")
    assert state.composure == 95


def test_multiturn_snapshot_persistence():
    """Action in progress round-trips through state snapshot correctly."""
    state = RunState.fresh_run()
    state.start_multiturn(
        action_id="read_book",
        total_steps=3,
        step_costs=[{"verb": "spend_oil", "amount": 1}],
        completion_effects=[{"verb": "set_flag", "flag": "read_the_book"}],
    )
    state.advance_multiturn()
    assert state.active_action.current_step == 1

    snap = state.snapshot()
    restored = RunState.fresh_run()
    restored.restore(snap)

    assert restored.active_action is not None
    assert restored.active_action.action_id == "read_book"
    assert restored.active_action.total_steps == 3
    assert restored.active_action.current_step == 1
    assert restored.active_action.step_costs == [{"verb": "spend_oil", "amount": 1}]
    assert restored.active_action.completion_effects == [{"verb": "set_flag", "flag": "read_the_book"}]


def test_multiturn_declarative_effects_and_predicates():
    """Tests declarative start_multiturn, advance_multiturn, cancel_multiturn, and predicates."""
    state = RunState.fresh_run()

    # Predicate: no_active_multiturn passes initially
    req = check_requirements([{"predicate": "no_active_multiturn"}], state)
    assert req.satisfied

    # Start multi-turn via apply_effects
    start_fx = [
        {
            "verb": "start_multiturn",
            "action_id": "pick_lock",
            "total_steps": 2,
            "step_costs": [{"verb": "spend_oil", "amount": 3}],
            "completion_effects": [{"verb": "set_flag", "flag": "door_unlocked"}],
        }
    ]
    res = apply_effects(start_fx, state)
    assert res.success
    assert state.has_active_multiturn("pick_lock")

    # Predicate: has_active_multiturn passes
    req = check_requirements([{"predicate": "has_active_multiturn", "action_id": "pick_lock"}], state)
    assert req.satisfied

    # Step check
    req = check_requirements([{"predicate": "multiturn_step_is", "step": 0}], state)
    assert req.satisfied

    # Advance 1
    adv_fx = [{"verb": "advance_multiturn"}]
    res = apply_effects(adv_fx, state)
    assert res.success
    assert state.lantern == 97
    assert state.active_action.current_step == 1

    req = check_requirements([{"predicate": "multiturn_step_is", "step": 1}], state)
    assert req.satisfied

    # Advance 2 (completes)
    res = apply_effects(adv_fx, state)
    assert res.success
    assert state.active_action is None
    assert state.has_flag("door_unlocked")
