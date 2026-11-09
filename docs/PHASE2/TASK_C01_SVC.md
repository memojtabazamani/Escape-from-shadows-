# Task C01: Six-slot inventory in `RunState`

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: C — Inventory
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: A13
- Blocks: C02
- Covers: AC-6
- Suggested commit: `feat(inventory): add the six-slot inventory to the run state`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Replace `RunState`'s uncapped `held_items` set with a six-slot inventory that refuses a seventh item and supports an explicit drop.

## Non-Goals
- Does not add the drop-to-take *flow* — that is C04's screen work. This task provides the model and the operations; C04 provides the ergonomics.
- Does not add requirements or effect verbs for inventory — that is C02.
- Does not author item definitions — that is C03. This task treats items as opaque ids.
- Does not display anything — that is C04.
- Does not change `spend_lantern`, `advance_turn`, or any non-inventory field.

## Context & Constraints
- **Read first:** §3.3 in full — the six-slot cap and the six candidate items — plus ASM-5 ("**Six slots is a hard cap.** A seventh item requires dropping one; the drop is a real choice, not a silent swap") and RISK-3, since this is the first place the Phase 1 contract is extended under load.
- **Files to modify:** `game/state.py` — `held_items: set[str]` with its docstring citing ASM-6; replace it with a slot-capped structure and update the docstring to cite the new rule.
- **Files to read, not modify:** `game/state.py`'s `snapshot()`/`restore()` — **both must carry the new shape**, and `restore()` must tolerate a snapshot written by the old code, or I01's save file becomes a migration problem the moment it lands. `game/effects.py`'s `grant_item` verb — it calls into the state and must keep working; its failure path matters now that grant can legitimately fail for a new reason. `tests/` — the Phase 1 tests that assert on `held_items` will need updating, and **updating them is in scope**; deleting them is not.
- **Conventions to respect:** `game/state.py`'s docstring style states contracts explicitly ("This contract is what Phase 2's save/load will build on top of") — keep that voice, because the next agent reads it. `spend_lantern()` establishes the pattern of **returning what actually happened** rather than raising; match it for the add operation.
- **Design constraints:**
  - **The cap is real and the failure is not silent.** Adding a seventh item returns a result the caller must handle; there is no automatic eviction. ASM-5's "drop is a real choice" means the *player* chooses, and C04's flow depends on the model refusing cleanly.
  - **Backward-compatible restore.** `restore()` on a snapshot with a list or set of items must load them up to the cap and report any dropped, rather than raising. A save from before this task must not become unloadable.
  - **Order matters for display.** A six-slot inventory shown to a player needs a stable order; a `set` has none. Decide the structure with C04's rendering in mind — a list or an ordered mapping — and record the decision.
  - **Do not change the meaning of `held_items` for existing content.** A02–A10's content grants items via `grant_item`; if any existing content grants a seventh item, the run will now refuse and a previously-passing test will fail. Find out before writing the code, and if the baseline content exceeds six, that is a **content bug to report**, not a reason to raise the cap.
- **Voice:** the docstring should say why six — §3.3's reason, in one clause — so the number does not look arbitrary to a future reader.

## Preconditions
- [ ] A13 DONE — the loop is green and the playtest passed
- [ ] The existing content set grants at most six items in any single run — **verify before starting**
- [ ] `game/state.py`'s tests are green as a baseline
- [ ] The structural decision (list vs ordered mapping) is made, for C04's benefit
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `game/state.py` in full, including `snapshot()`, `restore()`, and the ASM-6 docstring.
2. Grep the content set for item grants and confirm no reachable run exceeds six; record the count.
3. Replace `held_items` with the chosen slot-capped structure and add the operations: an add that returns what happened, a drop, a test for membership, and a count of free slots.
4. Update `snapshot()` to serialise the new shape and `restore()` to accept **both** the old and new shapes, reporting anything dropped.
5. Keep `has_item` semantics identical so `game/effects.py`'s predicate continues to work unchanged.
6. Confirm `grant_item`'s failure path is reachable and produces a truthful reason rather than a silent no-op.
7. Update the Phase 1 tests that assert on `held_items`; keep their intent, change their shape.
8. Write the new tests and run the whole suite.

## Test Plan
- **Tests to write/update:** extend the existing state tests, plus new `tests/test_inventory_model.py` (to be created):
  - `test_a_sixth_item_fits_and_a_seventh_is_refused` — the boundary, both sides.
  - `test_drop_frees_exactly_one_slot` — asserts no off-by-one in either operation.
  - `test_restore_accepts_a_pre_slice_snapshot_and_reports_drops` — the backward-compatibility guard.
  - `test_snapshot_round_trips_the_new_shape` — asserts `snapshot()` → `restore()` is lossless, which I01 will depend on.
  - `test_grant_item_reports_a_truthful_reason_when_full` — asserts the failure is not silent.
  - `test_has_item_and_lantern_behaviour_are_unchanged` — asserts no collateral change to the rest of the contract.
- **Commands:** `python -m pytest tests/test_inventory_model.py -v`; then `python -m pytest -v`.
- **Manual verification:** play a run that collects items to the cap and confirm nothing is silently lost; confirm the game still plays normally with fewer than six.
- **Capacity audit:** confirm the content set never *needs* more than six simultaneously — if it does, report it and propose which item is redundant, rather than raising ASM-5's cap.

## Definition of Done / Acceptance Criteria
- [ ] `held_items` is replaced by a slot-capped structure with stable ordering, and the choice is recorded
- [ ] A sixth item fits; a seventh is refused with a truthful reason and no silent eviction
- [ ] Drop frees exactly one slot
- [ ] `snapshot()`/`restore()` handle the new shape and tolerate a pre-slice snapshot, reporting drops
- [ ] `has_item` semantics are unchanged, so `game/effects.py` needs no modification
- [ ] The `restore()` path never raises on a well-formed but older snapshot
- [ ] The docstring states the cap and cites §3.3's reason
- [ ] Existing state tests are updated in shape, not weakened in intent
- [ ] `python -m pytest -v` passes, including A13's suite

## Rollback / Undo
Revert this task's commit; the inventory returns to an uncapped set and AC-6 is unmet. C02, C03, C04 and C05 all build on this model, so revert the whole slice together — a partially reverted slice would leave content referencing operations that no longer exist.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the structural decision, the capacity audit result, and the maximum items the content actually requires here -->
