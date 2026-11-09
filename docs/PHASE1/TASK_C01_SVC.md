# Task C01: Lantern drain rules

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: C — The Cost
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: B03
- Blocks: C02, D01, D02
- Covers: AC-4
- Suggested commit: `feat(game): implement lantern oil drain rules`
- Branch: per GP-3

## Objective
Make oil the cost of doing anything: entering a room drains the lantern, re-entering a room you have already lit drains less, and a careful or slow action drains more. This is the mechanic that creates the slice's tension — understanding the world costs you the light to explore it (§3.1).

## Non-Goals
- Does not implement the zero-oil consequence (C02) — this task only makes the value fall.
- Does not decide where refills come from; refills are content, applied through A05's vocabulary.
- Does not implement the Shadow reaching you at zero oil (§3.1) — the Shadow is Phase 3 (§2.2). Phase 1's zero-oil behavior is C02's honest, telegraphed outcome.
- Does not implement difficulty scaling — Phase 2 (§5.1) — but every rate must live in **one named table** so it can be scaled there.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.1 (drain faster on slow or careful actions; drain slower in already-lit rooms), `game/state.py` (the bounded lantern scale and the visited-room record from A03), `game/effects.py` (how costs are applied declaratively).
- **Files to create:** `game/lantern.py` — the drain rules as a small, pure, testable module.
- **Files to modify:** `screens/game.py` — invoke the drain at the documented moments.
- **Files to read, not modify:** `game/content_schema.py` — if content must be able to mark an action as slow or careful, confirm the format already expresses it. If it does not, stop and raise a format change as a follow-up rather than adding a parallel mechanism.
- **Conventions to respect:** PEP 8; type hints; standard library only; pure functions where possible; **no room or choice referenced by name** (AC-9).
- **Design constraints:**
  - Every rate is a named constant or one named table — no magic numbers at call sites.
  - Drain is in whole units so the meter stays predictable and the rule stays testable.
  - Entering an already-visited room costs **strictly less** than the first entry; this must be verifiable, not merely intended.
  - "Already lit" is read from A03's visited-room record, never from a UI cache.
  - The lantern must never go below zero; **assert** the clamp at the drain boundary rather than trusting it.
  - Zero oil must be reachable in a normal run but not trivially: compute and record the expected turns-to-empty as a comment so playtesting can check the balance.

## Preconditions
- [ ] B03 DONE — choices apply effects and transition between rooms
- [ ] A03's lantern range and visited-room record are documented and stable
- [ ] The drain values are chosen and recorded in the Execution Log

## Actionable Steps
1. Choose and record the rates: first entry to a room, re-entry to a lit room, and a slow or careful action. Give each a one-line rationale.
2. Compute and record the turns-to-empty from a full lantern along the intended Phase 1 path — this is the balance target.
3. Create `game/lantern.py` with the pure drain functions and the named rate table.
4. Wire the drain into the gameplay screen: on room entry, and on any action the content marks as slow or careful.
5. Confirm the visited-room record is updated on entry so the reduced re-entry rate applies from the second visit onward.
6. Assert the clamp at the drain boundary rather than assuming A03 enforces it.
7. Play a sample run and compare turns-to-empty against the recorded target; adjust rates if the cost is punishing or negligible, and log the change.

## Test Plan
- **Tests to write:** C03 owns them. C03 must cover: first-entry drain, reduced re-entry drain, the strict inequality between the two, slow-action drain, that the lantern never falls below zero, and that drain applies through the effect vocabulary rather than a special path.
- **Commands:** `python index.py`
- **Expected:** the lantern falls as rooms are entered and careful actions taken; a second visit to the same room costs visibly less; a full lantern lasts approximately the recorded number of turns.
- **Manual:** play until the lantern empties and confirm the bar bottoms out cleanly with no negative reading and no crash.
- **Syntax check:** `python -m py_compile index.py screens/*.py game/*.py`

## Definition of Done / Acceptance Criteria
- [ ] Drain occurs on room entry and on slow or careful actions
- [ ] A previously lit room costs strictly less to re-enter
- [ ] All rates live in one named table with no magic numbers at call sites
- [ ] The lantern never reads below zero, with an assertion at the boundary
- [ ] Turns-to-empty matches the recorded target, or the deviation is logged with its reason
- [ ] No room or choice is referenced by name (AC-9)
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. The lantern stops changing, returning the game to a cost-free traversal as in B03. No persisted data is affected.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the drain rates and the balance target here -->
