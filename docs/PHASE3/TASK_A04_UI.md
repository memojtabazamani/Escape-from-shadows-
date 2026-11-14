# Task A04: Wire Main Menu with `ENDINGS` navigation option

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: A — Meta-Progression & The Endings Gallery
- Layer: UI
- Status: DONE
- Estimate: ~2h
- Depends on: A03
- Blocks: A05
- Covers: AC-3, §9.4
- Suggested commit: `feat(menu): add ENDINGS gallery navigation option to main menu`
- Branch: feature/phase_3_the_shadow

## Objective
Expose the `ENDINGS` gallery option on `screens/main_menu.py` (`MainMenuScreen`), enabling players to open the `EndingsGalleryScreen` directly from the main game hub.

## Non-Goals
- Does not alter existing `CONTINUE`, `START GAME`, `SETTINGS`, or `EXIT` workflows.
- Does not modify styling or layout of other screens.

## Context & Constraints
- **Read first:** `screens/main_menu.py` (menu list, `refresh_options()`, `action_select()`).
- **Files to modify:** `screens/main_menu.py`.
- **Precedent:** Follows the pattern established for `SETTINGS` and `CONTINUE`.

## Preconditions
- [x] Task A03 DONE (`EndingsGalleryScreen` available in `screens/gallery.py`).
- [x] Working tree clean.

## Actionable Steps
1. In `screens/main_menu.py`, import `EndingsGalleryScreen` from `screens.gallery`.
2. Update `self.options` list in both `__init__()` and `refresh_options()` to include `"ENDINGS"`:
   - With save: `["CONTINUE", "START GAME", "ENDINGS", "SETTINGS", "ABOUT", "EXIT"]`
   - Without save: `["START GAME", "ENDINGS", "SETTINGS", "ABOUT", "EXIT"]`
3. In `action_select()`, add condition `elif selected_option == "ENDINGS":`:
   - Push `EndingsGalleryScreen()` onto the screen stack via `self.app.push_screen(EndingsGalleryScreen())`.
4. Ensure cursor position logic maintains bounds on option array refresh.

## Test Plan
- **Tests to write/update:** `tests/test_main_menu_gallery.py`:
  - `test_main_menu_includes_endings_option`: Asserts "ENDINGS" is present in options list.
  - `test_selecting_endings_pushes_gallery_screen`: Asserts selecting "ENDINGS" pushes `EndingsGalleryScreen`.
- **Commands:** `python -m pytest tests/test_main_menu_gallery.py -v`.

## Definition of Done / Acceptance Criteria
- [x] Main menu displays "ENDINGS" in its menu list.
- [x] Selecting "ENDINGS" cleanly pushes `EndingsGalleryScreen`.
- [x] Returning with Escape returns to Main Menu without state corruption.
- [x] Tests pass cleanly.

## Rollback / Undo
Revert edits to `screens/main_menu.py`.

## Execution Log
- **Date:** 2026-11-11
- **Agent:** Antigravity (Coding Worker)
- **Branch:** `feature/phase_3_the_shadow`
- **Implemented:** Added `EndingsGalleryScreen` import to `screens/main_menu.py`, added `"ENDINGS"` entry to `self.options` in both `__init__()` and `refresh_options()`, wired `elif selected_option == "ENDINGS":` in `action_select()`, and created `tests/test_main_menu_gallery.py`.
- **Review & Hardening:** Fixed cursor reset bug where returning to main menu with a save file forcibly reset cursor index to 0 (CONTINUE) instead of preserving the player's selected option. Added regression test for cursor retention.
