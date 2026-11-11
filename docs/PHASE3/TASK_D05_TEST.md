# Task D05: Shadow pursuit mechanics and movement rule tests

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: D — The Shadow Pursuit Engine
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: D04
- Blocks: G01
- Covers: AC-15, AC-16, AC-17, AC-18, §2.2, §3.1
- Suggested commit: `test(shadow): comprehensive test suite for Shadow pursuit and movement rules`
- Branch: feature/phase_3_the_shadow

## Objective
Author a comprehensive test suite in `tests/test_shadow_pursuit_suite.py` asserting that the Shadow entity follows all core rules: stage progression, lit-room barrier enforcement, absence-based description rendering, and zero-oil room breach.

## Non-Goals
- Does not test player history dialogue (covered in Slice E).
- Does not test dread turn counter (covered in Slice F).

## Context & Constraints
- **Read first:** `game/shadow.py`, `game/shadow_prose.py`, `screens/game.py`.
- **Files to create:** `tests/test_shadow_pursuit_suite.py`.

## Preconditions
- [ ] Tasks D01–D04 complete.
- [ ] Working tree clean.

## Actionable Steps
1. Create `tests/test_shadow_pursuit_suite.py`.
2. Test stage progression:
   - DORMANT -> TRAILING (on first room transition).
   - TRAILING -> FLANKING (on repeated movement).
   - FLANKING -> STALKING (when lingering near visited room).
3. Test lit-room barrier:
   - Verify `can_enter_room()` returns False whenever lantern > 0.
   - Verify `can_enter_room()` returns True when lantern == 0.
4. Test absence prose:
   - Assert no sprite or visual character strings exist in absence descriptions.
   - Assert all descriptions focus on missing elements, cold spots, or altered furniture.
5. Test UI integration:
   - Simulate 3 turns of room navigation in `GameScreen` and verify tracker updates.

## Test Plan
- **Commands:** `python -m pytest tests/test_shadow_pursuit_suite.py -v`.
- **Assertions:** All rules pass with zero failures.

## Definition of Done / Acceptance Criteria
- [ ] All Shadow pursuit rules covered by automated tests.
- [ ] Lit-room barrier and breach mechanics verified.
- [ ] 100% test pass rate.

## Rollback / Undo
Delete `tests/test_shadow_pursuit_suite.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
