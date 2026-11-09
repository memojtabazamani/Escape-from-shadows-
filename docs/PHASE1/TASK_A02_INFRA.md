# Task A02: Resolve the empty `settings_manager.py` stub and sync structure docs

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: A — Prerequisites & Foundation
- Layer: INFRA
- Status: DONE
- Estimate: ~2h
- Depends on: A01
- Blocks: A03
- Covers: AC-10
- Suggested commit: `refactor(game): remove empty settings stub and sync structure docs`
- Branch: per GP-3

## Objective
Remove the contradiction between the documented structure and the real one: `game/settings_manager.py` is an empty stub while the working `SettingsManager` lives in `config.py`. Leave exactly one obvious home for the settings concern, then correct `AGENTS.md`, `README.md`, and `docs/GENERAL_DOC.md` to describe reality.

## Non-Goals
- Does not change `SettingsManager` behavior, file format, or public API — that is Phase 1's *settings* work, already implemented and working.
- Does not add settings keys (that is Phase 2).
- Does not touch `settings.json` contents, and does not un-ignore it.
- Does not restructure anything else in `game/` or `screens/`.

## Context & Constraints
- **Read first:** `config.py` (the real implementation), `game/settings_manager.py` (**currently empty**), `index.py` and `screens/settings.py` (both import `from config import SettingsManager`), `AGENTS.md` §Architecture, `README.md` §Project Structure, `docs/GENERAL_DOC.md` §Project Structure and §Configuration.
- **Files to modify:** `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, plus either `game/settings_manager.py` or `config.py` depending on the decision below.
- **Decision required — pick one and record it in the Epic Change Log:**
  - **(a) Delete the stub** and document `config.py` as the settings home. Fewest moving parts; honest about working code. **Recommended.**
  - **(b) Re-export:** move the class into `game/settings_manager.py` and make `config.py` a thin re-export so existing imports keep working. Choose only if `game/` is meant to own all game logic.
- **Conventions to respect:** PEP 8; type hints; the canonical module keeps the module docstring; **no empty file may remain under any option.**
- **Note:** `.gitignore` currently excludes `settings.json` — confirm it still does after the change.

## Preconditions
- [ ] A01 DONE
- [ ] The decision above is made and recorded
- [ ] The app launches; the settings screen reads and writes `settings.json` correctly

## Actionable Steps
1. Confirm the decision; if it is unmade, stop and ask rather than choosing silently.
2. Apply the chosen option.
3. Search the repo for `SettingsManager`, `settings_manager`, and `from config` imports to confirm every import site still resolves to a real module.
4. Exercise the settings screen end to end: open Settings, cycle difficulty, toggle sound, toggle music, Escape back.
5. Inspect `settings.json` on disk and confirm the values persisted and the file is still gitignored.
6. Update `AGENTS.md` §Architecture file tree and §Common Tasks.
7. Update `README.md` §Project Structure.
8. Update `docs/GENERAL_DOC.md` §Project Structure and §Configuration; drop any "(stub)" annotation that is no longer true.
9. Re-read all three docs against the real tree and fix remaining drift.

## Test Plan
- **Commands:** `python index.py`, then `python -m py_compile index.py config.py screens/*.py game/*.py`
- **Expected:** app launches; Settings opens; each toggle persists; py_compile clean.
- **Import check:** no repo hit points at a removed or empty settings module.
- **Doc check:** the file tree in each of the three docs matches `git ls-files` for `screens/` and `game/` exactly.
- **Manual:** `cat settings.json` after toggling; confirm the file remains listed in `.gitignore`.

## Definition of Done / Acceptance Criteria
- [x] Exactly one module implements `SettingsManager`; no empty stub remains under any name
- [x] No import site is broken
- [x] The settings screen persists changes exactly as before
- [x] `AGENTS.md`, `README.md`, and `docs/GENERAL_DOC.md` structure sections match the real tree
- [x] No "(stub)" annotation remains for a file that is empty or gone
- [x] The decision and its reason are recorded in the Epic Change Log
- [x] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. `settings.json` is untouched and its format is unchanged, so no migration is needed. If option (b) moved the class, the revert restores it to `config.py`.

## Execution Log
- Date: 2026-11-08
- Agent: Claude Code
- Branch: feature/use-settings-into-game (working tree, no commits per GP-3)
- Commit hash: N/A — git commits not authorized
- Notes:
  - Decision: **option (a)** — delete the empty `game/settings_manager.py` stub and keep `SettingsManager` in `config.py`.
  - Deleted `game/settings_manager.py`.
  - Updated structure trees in `AGENTS.md`, `README.md`, and `docs/GENERAL_DOC.md`; removed all `(stub)` / `(currently stubbed)` annotations.
  - Updated `AGENTS.md` "Add a new menu option" to point to `screens/main_menu.py`.
  - Updated py_compile commands in `AGENTS.md` and `README.md` to match current files (`index.py config.py screens/*.py`).
  - Updated `docs/GENERAL_DOC.md` Future Plans so it no longer says "Implement main_menu.py".
  - Verified `python -m py_compile index.py config.py screens/*.py` clean and a 2-second app launch smoke test.
- Deviations: Manual interactive settings-screen walkthrough not performed; `config.py` and `screens/settings.py` were untouched, so persistence behavior is unchanged.
