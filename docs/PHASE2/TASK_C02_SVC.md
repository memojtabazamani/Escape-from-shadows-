# Task C02: Inventory requirements and effect verbs

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: C — Inventory
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h (includes a **60-minute time-boxed spike**)
- Depends on: C01
- Blocks: C03, C04
- Covers: AC-6, AC-7
- Suggested commit: `feat(engine): extend the effect contract for slot-capped inventory`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Extend the engine's verb and predicate tables so content can express the new inventory reality — a full pack, a dropped item, a required free slot — and record the RISK-3 verdict on whether the existing contract still fits.

## Non-Goals
- Does not add composure verbs or predicates — that is D01, which consumes this task's verdict.
- Does not add multi-turn or turn-counter support — that is F01, the other RISK-3 consumer.
- Does not author any content that uses the new verbs — C03 and Slice F do.
- Does not author item definitions — C03.
- Does not touch the screen; the refusal text a player sees comes from the resolver's `reason`, as A03 already implemented.

## Context & Constraints
- **Read first:** §11's "conditionals become requirements" and its effect/requirement model, §3.3 for what inventory verbs the design actually needs, and RISK-3 in the epic — which names this task as one of the two places the extension's fit is decided, and prescribes a **60-minute bounded spike** at its head.
- **Files to modify:** `game/effects.py` — `EFFECT_VERBS`, `REQUIREMENT_PREDICATES`, and the dispatch paths, whose current behaviour is to **raise** on an unknown verb or predicate; `game/content_schema.py` — `EFFECT_VERBS` and `REQUIREMENT_PREDICATES` are mirrored there, and the validator must accept the new names or `load_content()` will reject content C03 authors.
- **Files to read, not modify:** `game/state.py` (C01's new operations — the verbs are thin wrappers over them); `game/effects.py`'s all-or-nothing `apply_effects` and its snapshot-restore on failure, which the new verbs must respect: a `drop_item` that succeeds followed by a `spend_oil` that fails must roll back together.
- **Conventions to respect:** the existing verb naming — `spend_oil`, `grant_item`, `set_flag` are all lower-case verb-first. Match it. The unknown-verb **raise** is deliberate and must stay: silent acceptance of a typo is how content quietly stops working.
- **Design constraints — the spike is the point:**
  - **Run the spike first, write it down.** Time-box to 60 minutes: does the existing verb/predicate table extend cleanly for inventory, or does it need a small condition/effect expression layer? Record the verdict and the reasoning in the Execution Log **before** implementing, because D01, F01, F06 and G02 all inherit this decision.
  - **The recommendation is to extend, not to redesign.** The table's shape is sound; a rewrite is only justified if extension genuinely cannot express a required case, and that claim needs a concrete example in the log.
  - **New verbs must be all-or-nothing with their neighbours.** `apply_effects` already restores a snapshot on failure; confirm the new verbs participate.
  - **A failed requirement is a gate, never a death** (§4.1). A full pack refusing an item must produce a gate with a reason, in the shape A03 already renders.
  - **The refusal must be actionable.** "Your pack is full" is a gate; C04's flow turns it into "drop one to take this". The reason text should make the shape of the fix clear without naming the screen.
  - **Keep the tables mirrored.** `effects.py` and `content_schema.py` both hold these sets today; if they can be sourced from one place instead, that is a worthwhile small refactor *only if* it does not exceed this task's file budget — otherwise record it as a follow-up.
- **Voice:** the new names should read like the old ones, so the table stays scannable.

## Preconditions
- [ ] C01 DONE — the slot-capped model and its operations exist
- [ ] `game/effects.py` and `game/content_schema.py` verb/predicate sets are in sync
- [ ] The spike's 60 minutes are budgeted and the verdict will be recorded before implementation
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. **Spike (≤60 min).** Enumerate every inventory conditional §3.3 and §6 require: has a free slot, holds a specific item, holds at most N of a kind, and an item was dropped in this room. For each, decide whether the existing predicate table expresses it and write the verdict down.
2. If extension suffices, add the new predicates and verbs with the existing naming style; if it does not, stop and present the case for an expression layer as a plan change (§9) rather than implementing it unilaterally.
3. Implement the verbs as thin wrappers over C01's operations, so the cap's rule lives in one place.
4. Verify `apply_effects`'s rollback covers the new verbs — construct a two-effect case where the second fails and assert the first is undone.
5. Mirror the new names into `game/content_schema.py` so `validate_content()` accepts them, and confirm the validator still rejects an unknown name.
6. Confirm the unknown-verb raise is intact.
7. Produce a gate, not an error, when a full pack refuses a grant, and check the reason reads actionably.
8. Record the verdict in the Execution Log — **do not touch `docs/SUGGEST.md`.** The blueprint stays as written; D01, F01, F06 and G02 read the log for this decision.

## Test Plan
- **Tests to write/update:** new `tests/test_inventory_contract.py` (to be created):
  - `test_each_new_predicate_resolves_correctly` — one case per predicate, satisfied and unsatisfied.
  - `test_full_pack_refuses_a_grant_with_a_reason` — asserts a gate, not an exception, and that the text is non-empty.
  - `test_new_verbs_roll_back_with_their_neighbours` — the all-or-nothing check.
  - `test_unknown_verb_still_raises` — asserts the deliberate raise was not softened.
  - `test_validator_accepts_the_new_names_and_rejects_unknown_ones` — the mirror check in both directions.
- **Commands:** `python -m pytest tests/test_inventory_contract.py -v`; then `python -m pytest -v`.
- **Manual verification:** exercise a full-pack refusal through the gameplay screen and confirm the screen shows a gate with a readable reason rather than a traceback.
- **Verdict write-down:** the spike's conclusion belongs in the log in one paragraph, with the concrete case (if any) that forced the decision.

## Definition of Done / Acceptance Criteria
- [ ] The 60-minute spike ran and its verdict is recorded before implementation
- [ ] New predicates and verbs exist, named in the existing style
- [ ] `effects.py` and `content_schema.py` agree on the new names, and the validator rejects unknown ones
- [ ] The unknown-verb raise is intact
- [ ] A full pack produces a requirement gate with an actionable reason, never an exception
- [ ] New verbs participate in `apply_effects`' all-or-nothing rollback, asserted by test
- [ ] No change to `game/state.py`'s public contract beyond what C01 already established
- [ ] The verdict is recorded so D01, F01, F06 and G02 can consume it
- [ ] `python -m pytest -v` passes, including A13's suite and C01's tests

## Rollback / Undo
Revert this task's commit; content using the new verbs becomes invalid and `validate_content()` fails loudly on load, which is the correct failure. Because the new names are mirrored in two files, revert both together or the validator and the resolver will disagree.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; THE SPIKE VERDICT IS MANDATORY HERE — extend or redesign, the evidence, and the implication for D01/F01/F06/G02 -->
