# Task C04: Memory fragment trade-offs and Homecoming path tests

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: C — The Three Memory Fragments
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: C03
- Blocks: G01
- Covers: AC-10, AC-13, AC-14, §2.4
- Suggested commit: `test(fragments): test full memory fragment collection and Homecoming path`
- Branch: feature/phase_3_the_shadow

## Objective
Author an automated test suite verifying the complete memory fragment lifecycle: obtaining each fragment through its room trade-off, inventory slot constraints, journal recording, and the successful resolution of the secret Homecoming ending.

## Non-Goals
- Does not test Shadow movement (covered in Slice D).
- Does not test visual rhythm (covered in Slice F).

## Context & Constraints
- **Read first:** `game/state.py`, `game/ending_resolver.py`, `data/content.json`.
- **Files to create:** `tests/test_memory_fragments_suite.py`.

## Preconditions
- [ ] Tasks C01–C03 complete.
- [ ] Baseline test suite clean.

## Actionable Steps
1. Create `tests/test_memory_fragments_suite.py`.
2. Test full collection flow:
   - Acquire Photograph in Hall.
   - Acquire Drawing in Kitchen.
   - Acquire Receipt in Library.
   - Verify inventory handles 3 fragment items alongside key/tools within the 6-slot limit.
3. Test failure to preserve:
   - Test dropping a fragment to make room for another item.
   - Test the dog meat dilemma (losing the drawing when feeding the dog).
4. Test Homecoming resolution:
   - Run reaches exit with 3 fragments held -> Homecoming ending triggered and unlocked in profile.

## Test Plan
- **Commands:** `python -m pytest tests/test_memory_fragments_suite.py -v`.
- **Assertions:** All lifecycle steps pass with zero failures.

## Definition of Done / Acceptance Criteria
- [ ] End-to-end testing of memory fragments and Homecoming ending.
- [ ] Inventory cap compatibility verified.
- [ ] 100% test pass rate.

## Rollback / Undo
Delete `tests/test_memory_fragments_suite.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
