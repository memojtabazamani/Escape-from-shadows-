# Task I02: Load, CONTINUE, and save-slot lifecycle

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: I — Persistence & Mercy
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: I01
- Blocks: I05
- Covers: AC-20
- Suggested commit: `feat(save): wire CONTINUE menu option and manage save lifecycle on exit and death`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Implement save restoration (`load_from_disk()`) and wire the main menu's `CONTINUE` button so that returning players can resume their in-progress run, while ensuring the save file is cleanly purged or archived when the run terminates in death or victory.

## Non-Goals
- Does not create branching save slots.
- Does not allow cheating death by force-quitting during a death screen (save is wiped when lethal state is entered).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §9.1 ("Save & Resume... the 'continue' option on the main menu becomes real"), AC-20 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `screens/main_menu.py`, `index.py`, `screens/game.py`, `screens/death.py`, `game/save.py`.
- **Files to read, not modify:** `game/state.py`.
- **Conventions to respect:** Enable/disable menu options dynamically based on save availability (`has_saved_game()`). Use `RunState.restore(snapshot)` to reconstitute runtime state.
- **Design constraints:**
  - When a valid save exists: Main Menu shows enabled `CONTINUE` option (or highlights it as first option).
  - When no save exists: `CONTINUE` option is disabled or hidden.
  - Selecting `CONTINUE` mounts `GameScreen` with restored `RunState` and current room immediately loaded.
  - Quitting to Main Menu from `GameScreen` automatically saves current state.
  - Reaching a death or escape terminal state immediately purges the active save file.

## Preconditions
- [ ] I01 DONE — Save serialization module is functional.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. Add `load_from_disk(path: Path) -> Optional[RunState]` in `game/save.py`.
2. Update `screens/main_menu.py` to check `has_saved_game()`:
   - If save exists, render `CONTINUE` option.
   - Bind `action_select` on `CONTINUE` to load state and push `GameScreen(state=restored_state)`.
3. In `screens/game.py`, when player presses `Escape` or selects "Save and Quit to Menu":
   - Invoke `save_to_disk(state)`.
   - Pop screen back to Main Menu.
4. In `screens/death.py` and `screens/ending.py`, ensure `delete_saved_game()` is called so dead runs cannot be resumed.
5. Write unit and integration tests verifying the full lifecycle.

## Test Plan
- **Tests to write/update:** `tests/test_save_lifecycle.py`:
  - `test_continue_enabled_when_save_file_present` — menu detects save and enables continue.
  - `test_load_restores_identical_state` — loaded state matches exact snapshot prior to quit.
  - `test_death_deletes_save_file` — entering fatal outcome deletes active save file.
- **Commands:** `python -m pytest tests/test_save_lifecycle.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `CONTINUE` menu option is visible and active only when a valid save file exists.
- [ ] Selecting `CONTINUE` resumes the run at the exact room with all items, stats, and turns preserved.
- [ ] Exiting to menu saves progress.
- [ ] Death or victory deletes the active save file.
- [ ] All tests pass cleanly.

## Rollback / Undo
Revert `screens/main_menu.py` continue handlers and save calls.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
