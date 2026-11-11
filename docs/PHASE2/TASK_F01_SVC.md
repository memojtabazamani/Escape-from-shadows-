# Task F01: Multi-turn action support in the engine

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: SVC
- Status: DONE
- Estimate: ~3.5h
- Depends on: A13
- Blocks: F03
- Covers: AC-4, AC-22
- Suggested commit: `feat(engine): add multi-turn action tracking to engine state`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Extend the game state and choice resolution engine to support multi-turn activities (such as reading the Book across consecutive turns) where choosing to continue an activity progresses an ongoing action counter, drains per-turn costs, and checks for completion or interruption.

## Non-Goals
- Does not author the Library room prose or Book scene — that is F03.
- Does not write UI animations or timer loops — multi-turn actions are strictly turn-based player choices ("continue reading", "step away").
- Does not modify room transitions or unrelated room choices.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6 (The Old Library: "reading it takes three consecutive turns during which you cannot see the door... you know someone came in, because the door is open now"), §11 (Architecture suggestions: engine vs content), AC-4 and AC-22 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to create:** `game/multiturn.py`.
- **Files to modify:** `game/state.py` (add active multi-turn action state, serialize in snapshots), `game/effects.py`, `game/content_schema.py`.
- **Files to read, not modify:** `game/effects.py`, `game/state.py`.
- **Conventions to respect:** Maintain declarative effect and requirement schemas. A multi-turn action should specify `required_turns`, `current_turn`, `action_id`, and on-step effects (e.g. oil drain) versus on-complete effects (e.g. knowledge flag).
- **Design constraints:**
  - Player must be allowed to interrupt or abandon the action before completion, returning to the standard room options (with spent turns still counted).
  - Snapshot/restore must persist active multi-turn progress.

## Preconditions
- [ ] A13 DONE — baseline loop and tests passing.
- [ ] Working tree clean and existing tests green.

## Actionable Steps
1. Create `game/multiturn.py` defining `MultiTurnAction` dataclass (`action_id`, `total_steps`, `current_step`, `step_costs`, `completion_effects`, `cancel_effects`).
2. Update `RunState` in `game/state.py` with an optional `active_action: Optional[MultiTurnAction] = None`.
3. Add helper methods to advance or cancel the ongoing action, applying the per-step resource costs (such as lantern oil drain).
4. Update `RunState.snapshot()` and `RunState.restore()` to cleanly serialize multi-turn action state.
5. Extend `game/effects.py` and `game/content_schema.py` to support `start_multiturn` and `advance_multiturn` effects declaratively.
6. Write unit tests ensuring state progression, resource deduction per step, and completion triggers.

## Test Plan
- **Tests to write/update:** `tests/test_multiturn.py`:
  - `test_multiturn_action_lifecycle` — advances step by step, applies incremental costs, triggers completion effects at target step.
  - `test_multiturn_interruption` — cancelling resets active action without triggering final completion effects.
  - `test_multiturn_snapshot_persistence` — action in progress round-trips through state snapshot correctly.
- **Commands:** `python -m pytest tests/test_multiturn.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/multiturn.py` exists with clear type annotations and clean encapsulation.
- [ ] Engine can initiate, advance, and finalize multi-turn actions via declarative effects.
- [ ] Mid-action interruption correctly cleans up state.
- [ ] Snapshot/restore fully preserves active multi-turn state.
- [ ] All unit tests pass cleanly.

## Rollback / Undo
Delete `game/multiturn.py` and revert additions to `game/state.py`, `game/effects.py`, and `game/content_schema.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
