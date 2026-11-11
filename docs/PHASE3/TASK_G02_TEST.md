# Task G02: End-to-end regression and playthrough test suite

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: G — Full Integration, Verification & Documentation
- Layer: TEST
- Status: TODO
- Estimate: ~3h
- Depends on: G01
- Blocks: G03
- Covers: AC-26, §12
- Suggested commit: `test(e2e): full regression suite covering Phase 3 end-to-end playthroughs`
- Branch: feature/phase_3_the_shadow

## Objective
Author a comprehensive end-to-end integration and playthrough test suite in `tests/test_phase3_e2e_playthrough.py`, executing complete simulated playthroughs covering all 7 endings, memory fragment collections, Shadow pursuit encounters, and the Endings Gallery tally.

## Non-Goals
- Does not edit production application code.
- Does not modify documentation (handled in G03, G04).

## Context & Constraints
- **Read first:** `screens/game.py`, `screens/ending.py`, `screens/gallery.py`, `game/ending_resolver.py`.
- **Files to create:** `tests/test_phase3_e2e_playthrough.py`.
- **Assertion Target:** All existing tests (263) plus all new Phase 3 tests pass concurrently with 0 failures and 0 warnings.

## Preconditions
- [ ] Tasks A01 through G01 completed and green.
- [ ] Working tree clean on `feature/phase_3_the_shadow`.

## Actionable Steps
1. Create `tests/test_phase3_e2e_playthrough.py`.
2. Construct full-run simulation flows:
   - Playthrough 1: "The Long Walk" (Hall immediate demise -> gallery records 1/7).
   - Playthrough 2: "Meat and Silence" (Kitchen meat taken -> fed to dog -> yard escape -> gallery records 2/7).
   - Playthrough 3: "The Quiet Exit" (Key found -> front door escape -> gallery records 3/7).
   - Playthrough 4: "What the Book Knew" (Book read for 3 turns -> dog name learned -> whistle used -> escape -> gallery records 4/7).
   - Playthrough 5: "The New Shadow" (Exhaust lantern completely -> escape in darkness -> gallery records 5/7).
   - Playthrough 6: "Stay" (Unlock front door -> choose to stay -> gallery records 6/7).
   - Playthrough 7: "Homecoming" (Collect photograph, drawing, and receipt -> escape -> gallery records 7/7).
3. Assert that after Playthrough 7, `EndingsGalleryScreen` displays "DISCOVERED: 7 OF 7" with 0 locked silhouettes remaining.
4. Run full repository pytest suite: `python -m pytest`.

## Test Plan
- **Commands:** `python -m pytest tests/test_phase3_e2e_playthrough.py -v`.
- **Full Suite Run:** `python -m pytest`.

## Definition of Done / Acceptance Criteria
- [ ] All 7 canonical endings proven achievable through end-to-end playthrough tests.
- [ ] Gallery correctly tallies 7 of 7 unlocked endings.
- [ ] Total test count increases cleanly beyond 300+ passing tests with 0 failures.

## Rollback / Undo
Delete `tests/test_phase3_e2e_playthrough.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
