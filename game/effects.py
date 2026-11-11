"""Effect and requirement resolver.

This module answers two questions about a choice:

1. *May the player take it?* — by evaluating requirement predicates against a
   `RunState` without changing it.
2. *What happens when they do?* — by applying the choice's declared effects to
   that same `RunState`.

Every operation is data-driven: no room names, no choice names, and no special
cases.  Unknown verbs and predicates raise rather than silently failing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from game.state import RunState


@dataclass
class RequirementResult:
    """Outcome of evaluating a list of requirements."""

    satisfied: bool
    reasons: list[str]


@dataclass
class EffectResult:
    """Outcome of applying a list of effects."""

    success: bool
    applied: list[dict[str, Any]]
    reason: str = ""


@dataclass
class ChoiceResult:
    """Outcome of resolving a choice against a run state."""

    destination: str
    tier: str
    applied: list[dict[str, Any]]
    refused: bool
    reason: str = ""


# Valid effect verbs and the keys they require.
EFFECT_VERBS: dict[str, dict[str, set[str]]] = {
    "spend_oil": {"required": {"amount"}, "optional": set()},
    "spend_composure": {"required": {"amount"}, "optional": set()},
    "restore_composure": {"required": {"amount"}, "optional": set()},
    "grant_item": {"required": {"item"}, "optional": set()},
    "drop_item": {"required": {"item"}, "optional": set()},
    "spend_item": {"required": {"item"}, "optional": set()},
    "set_flag": {"required": {"flag"}, "optional": set()},
    "start_multiturn": {
        "required": {"action_id", "total_steps"},
        "optional": {"step_costs", "completion_effects", "cancel_effects"},
    },
    "advance_multiturn": {"required": set(), "optional": {"action_id"}},
    "cancel_multiturn": {"required": set(), "optional": {"action_id"}},
    "restore_oil": {"required": set(), "optional": {"amount"}},
}

# Valid requirement predicates and the keys they require.
REQUIREMENT_PREDICATES: dict[str, dict[str, set[str]]] = {
    "has_flag": {"required": {"flag"}, "optional": set()},
    "has_item": {"required": {"item"}, "optional": set()},
    "lacks_item": {"required": {"item"}, "optional": set()},
    "has_free_slot": {"required": set(), "optional": set()},
    "inventory_under": {"required": {"count"}, "optional": set()},
    "lantern_above": {"required": {"amount"}, "optional": set()},
    "composure_above": {"required": {"amount"}, "optional": set()},
    "composure_under": {"required": {"amount"}, "optional": set()},
    "has_active_multiturn": {"required": set(), "optional": {"action_id"}},
    "no_active_multiturn": {"required": set(), "optional": {"action_id"}},
    "multiturn_step_is": {"required": {"step"}, "optional": {"action_id"}},
}


def check_requirements(
    requirements: list[dict[str, Any]],
    state: RunState,
) -> RequirementResult:
    """Evaluate requirements without touching *state*.

    Returns a RequirementResult where `satisfied` is True only if every
    requirement passes. `reasons` contains a human-readable message for each
    failing requirement.
    """
    reasons: list[str] = []

    for requirement in requirements:
        predicate = requirement.get("predicate")
        if predicate == "has_flag":
            flag = requirement.get("flag")
            if not state.has_flag(flag):
                reasons.append(f"requires flag '{flag}'")
        elif predicate == "has_item":
            item = requirement.get("item")
            if not state.has_item(item):
                reasons.append(f"requires item '{item}'")
        elif predicate == "lacks_item":
            item = requirement.get("item")
            if state.has_item(item):
                reasons.append(f"already holding item '{item}'")
        elif predicate == "has_free_slot":
            if not state.can_add_item():
                reasons.append("pack is full (6/6 slots filled); drop an item to make room")
        elif predicate == "inventory_under":
            count = requirement.get("count")
            if not isinstance(count, (int, float)):
                raise ValueError(f"inventory_under requirement must have numeric count, got {count!r}")
            if len(state.held_items) >= int(count):
                reasons.append(f"requires fewer than {int(count)} items in pack")
        elif predicate == "lantern_above":
            amount = requirement.get("amount")
            if not isinstance(amount, (int, float)):
                raise ValueError(f"lantern_above requirement must have numeric amount, got {amount!r}")
            if state.lantern <= amount:
                reasons.append(f"requires lantern above {amount}")
        elif predicate == "composure_above":
            amount = requirement.get("amount")
            if not isinstance(amount, (int, float)):
                raise ValueError(f"composure_above requirement must have numeric amount, got {amount!r}")
            if state.composure <= int(amount):
                reasons.append(f"requires composure above {amount}")
        elif predicate == "composure_under":
            amount = requirement.get("amount")
            if not isinstance(amount, (int, float)):
                raise ValueError(f"composure_under requirement must have numeric amount, got {amount!r}")
            if state.composure >= int(amount):
                reasons.append(f"requires composure under {amount}")
        elif predicate == "has_active_multiturn":
            action_id = requirement.get("action_id")
            if not state.has_active_multiturn(action_id):
                reasons.append(f"requires ongoing action '{action_id or 'any'}'")
        elif predicate == "no_active_multiturn":
            action_id = requirement.get("action_id")
            if state.has_active_multiturn(action_id):
                reasons.append(f"conflicts with ongoing action '{action_id or 'any'}'")
        elif predicate == "multiturn_step_is":
            target_step = int(requirement.get("step", 0))
            action_id = requirement.get("action_id")
            if not state.active_action:
                reasons.append("no active multi-turn action")
            elif action_id and state.active_action.action_id != action_id:
                reasons.append(f"active action is '{state.active_action.action_id}', expected '{action_id}'")
            elif state.active_action.current_step != target_step:
                reasons.append(f"action at step {state.active_action.current_step}, requires step {target_step}")
        else:
            raise ValueError(f"unknown requirement predicate: {predicate!r}")

    return RequirementResult(satisfied=(not reasons), reasons=reasons)


def apply_effects(
    effects: list[dict[str, Any]],
    state: RunState,
) -> EffectResult:
    """Apply effects to *state* all-or-nothing.

    If any effect fails, the original state is restored and the result carries
    the reason. On success, the returned EffectResult lists the effects that
    were actually applied.
    """
    snapshot = state.snapshot()
    applied: list[dict[str, Any]] = []

    try:
        for effect in effects:
            _apply_one(effect, state)
            applied.append(effect)
    except Exception as exc:
        state.restore(snapshot)
        return EffectResult(success=False, applied=[], reason=str(exc))

    return EffectResult(success=True, applied=applied)


def _apply_one(effect: dict[str, Any], state: RunState) -> None:
    verb = effect.get("verb")

    if verb == "spend_oil":
        amount = effect.get("amount")
        if not isinstance(amount, (int, float)):
            raise ValueError(f"spend_oil effect must have numeric amount, got {amount!r}")
        state.spend_lantern(int(amount))
    elif verb == "spend_composure":
        amount = effect.get("amount")
        if not isinstance(amount, (int, float)):
            raise ValueError(f"spend_composure effect must have numeric amount, got {amount!r}")
        state.spend_composure(int(amount))
    elif verb == "restore_composure":
        amount = effect.get("amount")
        if not isinstance(amount, (int, float)):
            raise ValueError(f"restore_composure effect must have numeric amount, got {amount!r}")
        state.restore_composure(int(amount))
    elif verb == "grant_item":
        item = effect.get("item")
        if not isinstance(item, str):
            raise ValueError(f"grant_item effect must have string item, got {item!r}")
        if not state.add_item(item):
            raise ValueError(f"Inventory full: cannot carry '{item}' (6/6 slots filled)")
    elif verb == "drop_item":
        item = effect.get("item")
        if not isinstance(item, str):
            raise ValueError(f"drop_item effect must have string item, got {item!r}")
        if not state.drop_item(item):
            raise ValueError(f"drop_item failed: '{item}' is not held in inventory")
    elif verb == "spend_item":
        item = effect.get("item")
        if not isinstance(item, str):
            raise ValueError(f"spend_item effect must have string item, got {item!r}")
        if not state.remove_item(item):
            raise ValueError(f"spend_item failed: '{item}' is not held in inventory")
    elif verb == "set_flag":
        flag = effect.get("flag")
        if not isinstance(flag, str):
            raise ValueError(f"set_flag effect must have string flag, got {flag!r}")
        state.set_flag(flag)
    elif verb == "start_multiturn":
        action_id = effect.get("action_id")
        if not isinstance(action_id, str):
            raise ValueError(f"start_multiturn effect must have string action_id, got {action_id!r}")
        total_steps = effect.get("total_steps")
        if not isinstance(total_steps, int) or total_steps <= 0:
            raise ValueError(f"start_multiturn effect must have positive int total_steps, got {total_steps!r}")
        step_costs = list(effect.get("step_costs", []))
        completion_effects = list(effect.get("completion_effects", []))
        cancel_effects = list(effect.get("cancel_effects", []))
        state.start_multiturn(
            action_id=action_id,
            total_steps=total_steps,
            step_costs=step_costs,
            completion_effects=completion_effects,
            cancel_effects=cancel_effects,
        )
    elif verb == "advance_multiturn":
        completed, pending_effects = state.advance_multiturn()
        for pending_effect in pending_effects:
            _apply_one(pending_effect, state)
    elif verb == "cancel_multiturn":
        cancel_effects = state.cancel_multiturn()
        for cancel_effect in cancel_effects:
            _apply_one(cancel_effect, state)
    elif verb == "restore_oil":
        amount = effect.get("amount", 100)
        if not isinstance(amount, (int, float)):
            raise ValueError(f"restore_oil effect must have numeric amount, got {amount!r}")
        state.restore_lantern(int(amount))
    else:
        raise ValueError(f"unknown effect verb: {verb!r}")


def resolve_choice(
    choice: dict[str, Any],
    state: RunState,
) -> ChoiceResult:
    """Resolve a choice: check requirements, then apply effects.

    The returned `ChoiceResult` always carries the destination and tier.
    `refused` is True when a requirement was not satisfied; no effect is applied
    in that case.  Unknown verbs or predicates raise.
    """
    destination = choice.get("destination", "")
    tier = choice.get("tier", "scar")

    requirement_result = check_requirements(choice.get("requirements", []), state)
    if not requirement_result.satisfied:
        return ChoiceResult(
            destination=destination,
            tier=tier,
            applied=[],
            refused=True,
            reason="; ".join(requirement_result.reasons),
        )

    effect_result = apply_effects(choice.get("effects", []), state)
    if not effect_result.success:
        return ChoiceResult(
            destination=destination,
            tier=tier,
            applied=[],
            refused=True,
            reason=effect_result.reason,
        )

    return ChoiceResult(
        destination=destination,
        tier=tier,
        applied=effect_result.applied,
        refused=False,
    )
