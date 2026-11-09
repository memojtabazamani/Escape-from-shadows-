# Task A01: Move main menu logic into `screens/main_menu.py`

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: A — Prerequisites & Foundation
- Layer: INFRA
- Status: DONE
- Estimate: ~2h
- Depends on: GP-1, GP-2, GP-3, GP-4, GP-5, GP-6
- Blocks: A02, E03
- Covers: AC-10
- Suggested commit: `refactor(screens): extract main menu from app into its own screen`
- Branch: per GP-3

## Objective
Extract the menu currently living inside the `TerminalGame` app in `index.py` into a dedicated screen class in `screens/main_menu.py`, so `index.py` becomes a thin entry point and the layout matches what `AGENTS.md` and `docs/GENERAL_DOC.md` already claim.

## Non-Goals
- Does not change menu wording, order, styling, or key bindings — a pure move.
- Does not implement `START GAME` gameplay (that is E03, via B01–B03).
- Does not touch `screens/settings.py` or resolve the `game/settings_manager.py` stub (that is A02).
- Does not add tests (A06 covers logic; the menu is verified manually here).

## Context & Constraints
- **Read first:** `index.py` (whole file), `screens/settings.py` (the structural precedent — class-level `BINDINGS` and `CSS`, `compose()`, `render_menu()`, `update_menu()`, `action_*` methods), `AGENTS.md` §Architecture and §Common Tasks.
- **Files to modify:** `index.py` — reduce to app class and entry point.
- **Files to create:** `screens/main_menu.py`.
- **Files to read, not modify:** `config.py` — the `self.app.config` pattern the moved menu must keep using.
- **Conventions to respect:** PEP 8; type hints; screens inherit from `textual.screen.Screen`; CSS in a `CSS` class attribute; `self.app` for shared state; no heavy logic in `compose()`.
- **Do not** add dependencies or alter the visual design.

## Preconditions
- [ ] GP-1..GP-6 answered and recorded in the Epic plan
- [ ] `python index.py` launches and the menu responds to ↑/↓/Enter/Escape
- [ ] Baseline captured: the exact current behavior of all four menu options

## Actionable Steps
1. Record baseline: launch the app and note what each of the four options does today (including that `START GAME` only updates a status label).
2. Create `screens/main_menu.py` with a screen class inheriting from `textual.screen.Screen`.
3. Move into it, unchanged: the `options` list, the `selected` index, the `BINDINGS` (up/down/enter/escape), and the menu-related CSS (`#panel`, `#title`, `#subtitle`, `#menu`, `#status`).
4. Move the behavior methods too: `compose()`, `render_menu()`, `update_menu()`, `action_move_up()`, `action_move_down()`, `action_select()`.
5. Decide which class owns the shared `Screen` background rule so it is not defined twice, and record the decision.
6. In `index.py`, keep `TerminalGame` with `self.config = SettingsManager()` and an `on_mount` that pushes the menu screen; delete the duplicated menu code and CSS.
7. Keep `SETTINGS` → `self.push_screen(SettingsScreen())`, `EXIT` → `self.app.exit()`, and `ABOUT` → status update, matching today's behavior exactly.
8. Add a brief comment or docstring in `index.py` stating it is the entry point only.
9. Launch the app and walk every menu option.

## Test Plan
- **Commands:** `python index.py`
- **Expected:** the menu looks identical to the recorded baseline; ↑/↓ move and wrap; Enter on `SETTINGS` opens settings; Escape there returns to the menu; Enter on `EXIT` quits; `ABOUT` and `START GAME` update the status line as before.
- **Syntax check:** `python -m py_compile index.py screens/*.py` — clean.
- **Regression:** search the repo for any import of the old symbol locations before deleting them; there should be none left dangling.

## Definition of Done / Acceptance Criteria
- [x] `screens/main_menu.py` contains the menu screen
- [x] `index.py` contains no menu rendering, menu CSS, or menu bindings
- [x] All four options behave identically to the recorded baseline
- [x] `python index.py` starts with no errors or new warnings
- [x] `python -m py_compile index.py screens/*.py` clean
- [x] No unrelated files changed; no debug output left behind

## Rollback / Undo
Revert this task's commit. The change is behavior-preserving, so nothing else needs repair.

## Execution Log
- Date: 2026-11-08
- Agent: Claude Code
- Branch: feature/use-settings-into-game (working tree, no commits per GP-3)
- Commit hash: N/A — git commits not authorized
- Notes:
  - Moved menu logic, options, bindings, and screen-specific CSS into `screens/main_menu.py`.
  - Kept the app-level `Screen` background and `#panel/#title/#subtitle` rules in `index.py` so `SettingsScreen` continues to inherit them (it has no panel/title rules of its own).
  - `MainMenuScreen` adds only the `#menu` and `#status` rules that are specific to it.
  - Verified `python -m py_compile index.py screens/*.py` and a 2-second launch smoke test.
- Deviations: None
