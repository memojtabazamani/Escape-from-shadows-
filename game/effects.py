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


def check_requirements(
    requirements: list[dict[str, Any]],
    state: RunState,
) -> RequirementResult:
    """Evaluate requirements without touching *state*.

    Returns a RequirementResult where `satisfied` is True only if every
    requirement passes.  `reasons` contains a human-readable message for each
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
        elif predicate == "lantern_above":
            amount = requirement.get("amount")
            if not isinstance(amount, (int, float)):
                raise ValueError(f"lantern_above requirement must have numeric amount, got {amount!r}")
            if state.lantern <= amount:
                reasons.append(f"requires lantern above {amount}")
        else:
            raise ValueError(f"unknown requirement predicate: {predicate!r}")

    return RequirementResult(satisfied=(not reasons), reasons=reasons)


def apply_effects(
    effects: list[dict[str, Any]],
    state: RunState,
) -> EffectResult:
    """Apply effects to *state* all-or-nothing.

    If any effect fails, the original state is restored and the result carries
    the reason.  On success, the returned EffectResult lists the effects that
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
    elif verb == "grant_item":
        item = effect.get("item")
        if not isinstance(item, str):
            raise ValueError(f"grant_item effect must have string item, got {item!r}")
        state.add_item(item)
    elif verb == "set_flag":
        flag = effect.get("flag")
        if not isinstance(flag, str):
            raise ValueError(f"set_flag effect must have string flag, got {flag!r}")
        state.set_flag(flag)
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
