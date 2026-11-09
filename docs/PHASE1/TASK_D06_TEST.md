# Task D06: Content validation and both terminal paths reachable

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: D — The Two Rooms
- Layer: TEST
- Status: TODO
- Estimate: ~3h
- Depends on: D05
- Blocks: E01, E02, E04
- Covers: AC-2, AC-6, AC-7, AC-11
- Suggested commit: `test(content): validate the slice content and both terminal paths`
- Branch: per GP-3

## Objective
Prove the slice's content is sound and that the game it describes is actually completable: the content set validates, both terminal paths (the death and the ending) are reachable, no room is unreachable, and the death is avoidable. This is the gate that says the slice is a game rather than a set of rooms.

## Non-Goals
- Does not implement or alter content — it verifies it. Content fixes needed to pass belong in D01–D05, so if this task finds a content defect, stop and report it rather than editing content here.
- Does not test screen behavior (B05) or the cost rules (C03).
- Does not perform the human playtest (E04) — this is automated reachability, not a player's experience.
- Does not test the death and ending *screens* (E01, E02).

## Context & Constraints
- **Read first:** the authored content from D01–D05, `game/content_schema.py` (the validator), `game/effects.py` (resolution), `game/state.py`, and the test structure from A06/B05/C03.
- **Files to create:** a content and reachability test module under the project's test root.
- **Files to modify:** the test runner configuration only if a new path needs registering.
- **Conventions to respect:** follow the established test structure; deterministic; no terminal dependence; the content *is* real here, unlike B05's fixture-based tests — this is the one place tests read the authored set.
- **Required coverage — validation:**
  - The whole authored content set validates clean through A04's validator
  - Every choice destination resolves to a room that exists
  - Every referenced item and flag is declared
  - Every Death-tier choice carries at least two telegraphs
  - No duplicate identifiers
- **Required coverage — reachability (the important half):**
  - The start room is THE HALL and it is reachable from a fresh run by definition
  - THE OLD LIBRARY is reachable from THE HALL
  - **The death is reachable** — a path exists from the start that selects the left doorway
  - **The ending is reachable** — a path exists from the start that reads the BOOK and then opens the front door
  - **The ending is reachable without the death** — the winning path does not transit the Death-tier choice
  - **The death is avoidable** — a path exists from the start to the ending that never selects the left doorway
  - Every room in the content set is reachable from the start room
  - No room leads only to itself (a self-loop with no exit is a dead end)
- **Required coverage — the zero-oil interaction:**
  - Under C02's recorded decision, the reachability walk confirms a zero-oil run is legibly lost or closes the winning path, and never soft-locks. This is the case most likely to be missed by inspection.
- **Required coverage — prose budget (AC-11):**
  - Every room's arrival prose fits the scene line budget at the reference width, with no continuation marker, using the pure wrapping helper from B02

## Preconditions
- [ ] D01–D05 DONE — all content authored
- [ ] The recorded decisions from C02 (zero-oil), D03 (repeat read, flag name), and D04 (oil at the doorway) are available
- [ ] The suites from A06, B05, and C03 pass before this task starts

## Actionable Steps
1. Record the pre-task baseline: run the existing suites and confirm everything passes.
2. Write the validation tests over the real authored content set.
3. Implement a reachability walk over the content graph — a simple graph traversal from the start room, not a simulation of play — and assert the reachability cases listed above, including the death-without-ending and ending-without-death separations.
4. Write the avoidability case explicitly: a path from start to ending exists that never selects the Death-tier choice.
5. Write the dead-end case: no room's only exit leads to itself.
6. Write the zero-oil interaction case per C02's decision.
7. Write the prose-budget case over every room using B02's wrapping helper.
8. Run the whole suite; if a content defect is found, stop and report it for D01–D05 rather than editing content here.

## Test Plan
- **Commands:** the project's test command from GP-2, plus `python -m py_compile` on changed files.
- **Expected:** all listed cases pass; the full suite (A06 + B05 + C03 + D06) passes twice consecutively; runtime stays well under a minute.
- **Manual — mutation checks (two, both required):**
  - Remove a telegraph from the doorway's choice and confirm the validation test fails; restore.
  - Make the front door's requirement reference a misspelled flag and confirm the ending-reachability test fails; restore. This proves the reachability walk is real and not vacuously passing.
- **Soft-lock check:** deliberately set the starting lantern to zero and confirm the zero-oil case reports a legible lost state rather than hanging or passing silently.

## Definition of Done / Acceptance Criteria
- [ ] The authored content set validates clean
- [ ] Both the death and the ending are proven reachable from the start
- [ ] The ending is proven reachable without the death, and the death avoidable
- [ ] Every room is reachable; no room is a self-loop dead end
- [ ] The zero-oil interaction is proven to avoid a soft-lock
- [ ] Every room's prose fits the scene budget at the reference width
- [ ] Both mutation checks fail as expected, then pass after restoration
- [ ] The combined suite passes twice in a row
- [ ] No content edited in this task; any defect found is reported for D01–D05

## Rollback / Undo
Delete the added test module. Content and production code are unaffected.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the mutation-check results here -->
