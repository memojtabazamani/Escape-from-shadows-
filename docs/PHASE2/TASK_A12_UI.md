# Task A12: Wire `START GAME` and the run lifecycle

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: UI
- Status: TODO
- Estimate: ~2h
- Depends on: A11
- Blocks: A13
- Covers: AC-1, AC-15
- Suggested commit: `feat(menu): wire start game to a real run`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make `START GAME` actually start a game: build a fresh run, push the gameplay screen, and return to the menu cleanly when the run ends.

## Non-Goals
- Does not add a `CONTINUE` option or any save/load — that is I02. This task makes the *new run* path real; the resume path is separate.
- Does not implement difficulty behaviour — that is Slice B. The menu may read the difficulty, but nothing may branch on it yet.
- Does not change the other menu options (`SETTINGS`, `ABOUT`, `EXIT`); they already work.
- Does not implement the journal or the death screen's teaching lines — those are E02 and I03.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §9.1 for the shape of a run's lifecycle and §12's Phase 1 bullet ("`START GAME` only prints a status line. There is no gameplay screen" — the defect this task removes), plus `docs/SUGGEST.md` §0's honest snapshot of where the game stands.
- **Files to modify:** `screens/main_menu.py` — `action_select()`'s `START GAME` branch currently only updates the `#status` label with the difficulty; `index.py` if screen registration is needed.
- **Files to read, not modify:** `screens/game.py`, `screens/death.py`, `screens/ending.py` (A01–A11); `game/state.py` — `RunState.fresh_run()` is the constructor to use; `config.py`'s `SettingsManager` — read via `self.app.config`, as `screens/settings.py` already does.
- **Conventions to respect:** `AGENTS.md` — screens share state via `self.app`; `main_menu.py` already shows the pattern with `self.app.config.get("difficulty", "MEDIUM")` and `self.push_screen(SettingsScreen())`.
- **Design constraints:**
  - The run state must be **owned by the app**, not by the gameplay screen, so every screen reads and mutates one object — §11's "game state object owned by the app (like `self.app.config` already is)". This is also exactly what I01 serialises.
  - **A finished run must not leak into the next.** Starting a second run from the menu must produce a genuinely fresh `RunState`, not a mutated one.
  - Escape from the gameplay screen returns to the menu without leaving a half-run behind.
  - No behaviour may branch on difficulty yet — Slice B owns that, and branching early is exactly the retrofit §11 warns against if done without the seam.
- **Voice:** the menu's status label should stop announcing the difficulty and start acknowledging the run, or say nothing at all. Decide and record.

## Preconditions
- [ ] A01–A11 DONE — the gameplay, death, and ending screens exist and route correctly
- [ ] `RunState.fresh_run()` exists in `game/state.py`
- [ ] `index.py` mounts `MainMenuScreen` and exposes `self.config`
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `action_select()` in `screens/main_menu.py` and `screens/settings.py`'s use of `self.app.config` to see the shared-state pattern.
2. Add the run-state ownership to the app (`index.py`), following `self.app.config`'s precedent, so screens read one object.
3. Change the `START GAME` branch to build a fresh run via `RunState.fresh_run()` and push the gameplay screen.
4. Ensure pressing Escape in the gameplay screen pops back to the menu and discards the run.
5. Ensure starting a second run immediately after the first yields a fresh state — verify by checking the lantern and flags after a second `START GAME`.
6. Decide what the status label says now that the game truly starts, and record the decision.
7. Leave `SETTINGS`, `ABOUT`, and `EXIT` untouched.

## Test Plan
- **Tests to write/update:** new `tests/test_run_lifecycle.py` (to be created):
  - `test_start_game_pushes_the_gameplay_screen` — asserts navigation, using Textual's `run_test()` harness.
  - `test_second_run_starts_from_a_fresh_state` — asserts lantern, flags and visited are reset.
  - `test_escape_from_gameplay_returns_to_the_menu` — asserts the pop and that no run survives it.
  - `test_menu_does_not_branch_on_difficulty` — a guard for §11: asserts no difficulty branch exists in the lifecycle path yet.
- **Commands:** `python -m pytest tests/test_run_lifecycle.py -v`; then `python -m pytest`.
- **Manual verification:** `python index.py`, choose `START GAME`, confirm the game starts; Escape back; start again and confirm the lantern is full and the flags are empty.

## Definition of Done / Acceptance Criteria
- [ ] `START GAME` launches a real run on the gameplay screen
- [ ] The run state is owned by the app and read by every screen through it
- [ ] Escape from the gameplay screen returns to the menu and discards the run
- [ ] A second `START GAME` produces a genuinely fresh state
- [ ] No difficulty branching exists in the lifecycle yet
- [ ] `SETTINGS`, `ABOUT`, and `EXIT` are unchanged
- [ ] The menu status label's new behaviour is decided and recorded
- [ ] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; `START GAME` returns to printing a status line and the game is unreachable from the menu, though every screen and rule still exists and is tested. A13's playtest depends on this wiring, so revert them together.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the status-label decision here -->
