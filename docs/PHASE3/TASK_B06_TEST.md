# Task B06: Ending resolution criteria and transition tests

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: B — The Multiple Endings Spectrum
- Layer: TEST
- Status: DONE
- Estimate: ~2.5h
- Depends on: B04, B05
- Blocks: G01
- Covers: AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-11, AC-12, §2.3
- Suggested commit: `test(endings): comprehensive test suite for all canonical endings resolution`
- Branch: feature/phase_3_the_shadow

## Objective
Author a comprehensive regression test suite in `tests/test_canonical_endings_suite.py` verifying that all 7 canonical endings can be triggered through real gameplay states, resolve correctly, display their ASCII art vignettes, and unlock in the profile.

## Non-Goals
- Does not test memory fragment placement details (covered in Slice C).
- Does not test Shadow pursuit state machine (covered in Slice D).

## Context & Constraints
- **Read first:** `game/ending_resolver.py`, `screens/ending.py`, `game/endings_art.py`, `game/profile.py`.
- **Files to create:** `tests/test_canonical_endings_suite.py`.

## Preconditions
- [x] Tasks B01–B05 complete.
- [x] Working tree clean.

## Actionable Steps
1. Create `tests/test_canonical_endings_suite.py`.
2. Author simulated run states for:
   - "The Long Walk" (Hall fatal state)
   - "Meat and Silence" (dog meat fed, escape flag set)
   - "The Quiet Exit" (key held, default escape)
   - "What the Book Knew" (book read 3 turns, escape)
   - "The New Shadow" (lantern == 0, escape)
   - "Stay" (refusal chosen)
3. Assert `resolve_escape_ending()` or `resolve_terminal_event()` returns the exact expected ID for each scenario.
4. Mount `EndingScreen` for each scenario and assert:
   - ASCII vignette is rendered without exceptions.
   - Profile contains the unlocked ending ID.
   - Prose and title match content records.

## Test Plan
- **Commands:** `python -m pytest tests/test_canonical_endings_suite.py -v`.
- **Assertions:** All ending states resolve deterministically and unlock cleanly.

## Definition of Done / Acceptance Criteria
- [x] All 6 non-secret endings (and resolution foundation for secret ending) fully tested.
- [x] ASCII art and profile unlock verified.
- [x] 100% passing tests.

## Rollback / Undo
Delete `tests/test_canonical_endings_suite.py`.

## Execution Log
- 2026-11-11: Antigravity subagent authored `tests/test_canonical_endings_suite.py` verifying resolution, UI mounting, title/prose matching, ASCII art rendering, and PlayerProfile unlock persistence across all 7 canonical endings. Verified cleanly with 14 assertions across state and async UI test cases.
- 2026-11-11: Added end-to-end `GameScreen` UI integration tests covering zero-oil escape to The New Shadow, Homecoming escape with zero oil, and shadow walk profile isolation (17 tests total).
