# Task B04: Ending screen upgrade with ASCII art, profile unlocking, and gallery link

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: B — The Multiple Endings Spectrum
- Layer: UI
- Status: DONE
- Estimate: ~3h
- Depends on: B02, B03
- Blocks: B06
- Covers: AC-1, AC-4, AC-12, §2.3, §7.3, §9.4
- Suggested commit: `feat(ui): upgrade EndingScreen with ASCII vignettes, profile unlock, and gallery link`
- Branch: feature/phase_3_the_shadow

## Objective
Upgrade `screens/ending.py` (`EndingScreen`) to render the ending's dedicated ASCII art vignette (§7.3), record the unlocked ending permanently into `PlayerProfile` via `unlock_ending()`, and provide an option to jump directly to the Endings Gallery.

## Non-Goals
- Does not modify death screen layout (`screens/death.py`).
- Does not change game over run-reset mechanics (save is still purged on ending).

## Context & Constraints
- **Read first:** `screens/ending.py` (current layout), `game/endings_art.py`, `game/profile.py`.
- **Files to modify:** `screens/ending.py`.
- **Precedent:** `EndingScreen` currently renders `ENDING_MARKER`, `title`, `prose`, and options `["AGAIN", "BACK TO MENU"]`.

## Preconditions
- [x] Task B02 and B03 DONE (`ending_resolver.py` and `endings_art.py` available).
- [x] Profile unlock API available (`game.profile.unlock_ending`).

## Actionable Steps
1. In `screens/ending.py`, import `get_ending_ascii` and `unlock_ending`.
2. Accept `ending_id: str` in `EndingScreen.__init__()`.
3. In `on_mount()`, automatically call `unlock_ending(self.ending_id)` to permanently persist the accomplishment across runs.
4. Add ASCII art Static widget between the ending marker and the title:
   - Render `get_ending_ascii(self.ending_id)` in dim cyan/grey.
5. Add `"VIEW GALLERY"` to `self.options`:
   - `["AGAIN", "BACK TO MENU", "VIEW GALLERY"]`
6. In `action_select()`, handle `"VIEW GALLERY"` by pushing `EndingsGalleryScreen`.

## Test Plan
- **Tests to write/update:** `tests/test_ending_screen_upgrades.py`:
  - `test_ending_mount_unlocks_profile_ending`: Mounting ending screen calls `unlock_ending()`.
  - `test_ending_screen_renders_ascii_art`: Screen contains the ASCII art widget.
  - `test_gallery_option_navigation`: Selecting "VIEW GALLERY" pushes `EndingsGalleryScreen`.
- **Commands:** `python -m pytest tests/test_ending_screen_upgrades.py -v`.

## Definition of Done / Acceptance Criteria
- [x] EndingScreen displays ASCII vignette cleanly.
- [x] Profile records unlocked ending immediately upon mounting ending screen.
- [x] "VIEW GALLERY" option is available and navigates properly.
- [x] Tests pass cleanly.

## Rollback / Undo
Revert modifications to `screens/ending.py`.

## Execution Log
- 2026-11-11: Antigravity subagent upgraded `screens/ending.py` with ASCII art display, auto profile unlocking via `unlock_ending()`, escape recording via `record_escape()`, and "VIEW GALLERY" modal navigation.
- Verified with `tests/test_ending_screen_upgrades.py` (3/3 passing) and `tests/test_terminal_screens.py` (9/9 passing).
