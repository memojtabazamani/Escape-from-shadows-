# Task A05: Profile persistence and Endings Gallery tests

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: A — Meta-Progression & The Endings Gallery
- Layer: TEST
- Status: DONE
- Estimate: ~2.5h
- Depends on: A04
- Blocks: B01, G01
- Covers: AC-1, AC-2, AC-3, §9.4
- Suggested commit: `test(gallery): verify full profile persistence and gallery integration`
- Branch: feature/phase_3_the_shadow

## Objective
Assemble a complete test suite verifying cross-run profile persistence, safe atomic file updates, schema compliance, and Endings Gallery UI rendering across all states (0 unlocked, partially unlocked, all 7 unlocked).

## Non-Goals
- Does not test the narrative gameplay triggers of endings (covered in Slice B).
- Does not test memory fragments (covered in Slice C).

## Context & Constraints
- **Read first:** `game/profile.py`, `game/endings.py`, `screens/gallery.py`, `screens/main_menu.py`.
- **Files to create/extend:** `tests/test_profile_gallery_suite.py`.
- **Precedent:** Follows Textual screen testing patterns in `tests/test_journal_ui.py` and `tests/test_save_lifecycle.py`.

## Preconditions
- [x] Tasks A01–A04 complete and passing individually.
- [x] Working tree clean.

## Actionable Steps
1. Create `tests/test_profile_gallery_suite.py`.
2. Test profile lifecycle:
   - Starting with no profile file produces empty set.
   - Calling `unlock_ending("the_quiet_exit")` updates disk.
   - Resetting active game run does NOT delete profile.
   - Deleting run save preserves unlocked endings.
3. Test gallery screen rendering using Textual `Pilot`:
   - Screen displays correct ratio string ("0 OF 7", "4 OF 7", "7 OF 7").
   - Locked cards do not reveal true title names.
   - Unlocked cards reveal accurate titles and summaries.
4. Test menu transition:
   - Selecting "ENDINGS" opens gallery and pressing Escape returns to menu.

## Test Plan
- **Commands:** `python -m pytest tests/test_profile_gallery_suite.py -v`.
- **Assertions:** 100% assertions pass; no unhandled exceptions.

## Definition of Done / Acceptance Criteria
- [x] `tests/test_profile_gallery_suite.py` provides comprehensive coverage of Slice A.
- [x] No regression across the 263 existing tests.
- [x] All new tests pass cleanly with pytest.

## Rollback / Undo
Delete `tests/test_profile_gallery_suite.py`.

## Execution Log
- **Date:** 2026-11-11
- **Agent:** Antigravity (Coding Worker)
- **Branch:** `feature/phase_3_the_shadow`
- **Implemented:** `tests/test_profile_gallery_suite.py` covering multi-run profile lifecycle, savegame isolation, Pilot ratio rendering across discovery counts, masked silhouettes vs revealed titles, and full keyboard menu navigation loop.
- **Review & Hardening:** Added tests for Enter key details expansion, cursor retention on menu return across save states, input sanitization edge cases in `PlayerProfile.from_dict`, and invalid ending ID rejection in `unlock_ending`.
