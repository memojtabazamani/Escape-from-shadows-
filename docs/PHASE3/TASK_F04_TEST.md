# Task F04: Dread counter thresholds and presentation rule tests

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: F — Dread Counter & Quiet Horror Presentation
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: F03
- Blocks: G01
- Covers: AC-22, AC-23, AC-24, §3.5, §7.4, §7.5
- Suggested commit: `test(presentation): verify dread counter, color grammar, and quiet horror techniques`
- Branch: feature/phase_3_the_shadow

## Objective
Author an automated test suite in `tests/test_dread_presentation_suite.py` verifying all Slice F mechanics: dread threshold activations at Turns 20 and 30, absolute restriction of red text to Shadow manifestations, and the once-per-run limits on quiet horror techniques.

## Non-Goals
- Does not test content endings (tested in Slice B).
- Does not test save file serialization (tested in Slice G).

## Context & Constraints
- **Read first:** `game/dread.py`, `game/quiet_horror.py`, `screens/game.py`.
- **Files to create:** `tests/test_dread_presentation_suite.py`.

## Preconditions
- [ ] Tasks F01–F03 complete.
- [ ] Working tree clean.

## Actionable Steps
1. Create `tests/test_dread_presentation_suite.py`.
2. Test dread progression:
   - Increment turn counter past 20 and verify rhythm shift flag activates.
   - Increment turn counter past 30 and verify proximity line is returned.
3. Test color grammar lint:
   - Scan all `.py` files in `screens/` and `game/` plus `content.json` for unauthorized red style tags.
4. Test quiet horror limits:
   - Run a simulated 40-turn playthrough; count occurrences of delayed echo, missing line, and prompt hesitation.
   - Assert each occurs exactly 0 or 1 times, never 2+.

## Test Plan
- **Commands:** `python -m pytest tests/test_dread_presentation_suite.py -v`.
- **Assertions:** All dread and presentation assertions pass.

## Definition of Done / Acceptance Criteria
- [ ] Comprehensive test coverage for dread thresholds.
- [ ] Strict enforcement of red color grammar verified.
- [ ] Quiet horror rarity invariants proven by tests.
- [ ] 100% test pass rate.

## Rollback / Undo
Delete `tests/test_dread_presentation_suite.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
