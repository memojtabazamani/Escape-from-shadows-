# Task C03: Lantern rule tests

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: C — The Cost
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: C02
- Blocks: D01, D02
- Covers: AC-4, AC-5
- Suggested commit: `test(game): cover lantern drain, re-entry discount, and zero-oil handling`
- Branch: per GP-3

## Objective
Pin down the cost mechanic with tests, so that the slice's central tension is verifiable and so that Phase 2's difficulty scaling (§5.1) has a specification to change deliberately rather than a behavior to guess at.

## Non-Goals
- Does not implement new behavior — it tests C01 and C02.
- Does not test room content or its prose (D06 validates content).
- Does not test the amber meter's rendering (B05 covers the pure helper and the threshold).
- Does not test difficulty scaling — that is Phase 2 and does not exist yet.

## Context & Constraints
- **Read first:** `game/lantern.py`, `game/state.py`, the drain wiring in `screens/game.py`, and the existing test setup from A06/B05.
- **Files to create:** a lantern test module under the project's test root.
- **Files to modify:** the test runner configuration only if a new path needs registering.
- **Conventions to respect:** follow A06's and B05's structure; deterministic; no terminal dependence; no reliance on authored content.
- **Required coverage — drain:**
  - First entry to a room drains exactly the recorded first-entry rate
  - Re-entry to a lit room drains exactly the recorded re-entry rate
  - The re-entry rate is **strictly less** than the first-entry rate — assert the inequality itself, not just the two values
  - A slow or careful action drains exactly the recorded rate
  - Drain applied through the effect vocabulary produces the same result as the direct rule, so there is one source of truth
- **Required coverage — bounds:**
  - The lantern never falls below zero, including when a drain larger than the remaining oil is applied
  - The lantern never exceeds its maximum, including when a refill effect is applied
  - The boundary assertion in the drain path holds rather than being incidentally satisfied
- **Required coverage — zero oil (C02's decision):**
  - The zero predicate flips exactly at zero, not at one and not below zero
  - The outcome cannot fire before the required warnings have been delivered
  - Under option (a): once oil is zero, the winning path is unreachable, asserted by resolving the relevant choice and observing the refusal
  - Under option (b): the outcome resolves to the death path with its telegraphs attached
- **Required coverage — balance (a guard, not a style check):**
  - The recorded turns-to-empty from a full lantern equals what the rule table actually produces, so a future rate change cannot silently invalidate the documented balance target

## Preconditions
- [ ] C01 and C02 DONE
- [ ] The recorded drain rates and the balance target are available from C01's Execution Log
- [ ] A06's and B05's test suites pass before this task starts

## Actionable Steps
1. Record the pre-task baseline: run the existing suite and confirm it passes.
2. Write the drain tests, including the strict-inequality assertion for re-entry.
3. Write the bounds tests, including the oversized-drain and oversized-refill cases.
4. Write the zero-oil tests matching whichever option C02 chose.
5. Write the balance guard test comparing the documented turns-to-empty against what the rule table produces.
6. Run the whole suite (A06 + B05 + C03) and confirm it passes.
7. If a test exposes a defect in C01 or C02, fix it only if in scope; otherwise raise a follow-up and stop.

## Test Plan
- **Commands:** the project's test command from GP-2, plus `python -m py_compile` on changed files.
- **Expected:** all listed cases pass; the combined suite passes twice consecutively; runtime stays well under a minute.
- **Manual — mutation check:** temporarily set the re-entry rate equal to the first-entry rate and confirm the inequality test fails, then restore. This proves the test is load-bearing.
- **Manual — balance check:** temporarily scale every rate by two and confirm the balance guard fails, then restore.

## Definition of Done / Acceptance Criteria
- [ ] Every case in the four coverage lists exists as a named test
- [ ] The re-entry discount is asserted as an inequality, not as two literals
- [ ] Bounds are tested in both directions with oversized inputs
- [ ] The zero-oil behavior is tested against C02's recorded decision
- [ ] The balance guard test ties the documented turns-to-empty to the real rate table
- [ ] The combined suite passes twice in a row
- [ ] No test depends on authored content, wall-clock time, terminal size, or network
- [ ] No production file changed, or any change is a genuine in-scope fix logged in the Execution Log

## Rollback / Undo
Delete the added lantern test module. Production behavior is unaffected.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
