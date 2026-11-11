# Task A01: Gameplay screen skeleton with the three zones

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: UI
- Status: DONE
- Estimate: ~3h
- Depends on: GP-2, GP-3
- Blocks: A02, A04
- Covers: AC-1, AC-23
- Suggested commit: `feat(ui): add the gameplay screen skeleton with three zones`
- Branch: feature/phase_2_the_house

## Objective
Create the gameplay screen with §7.1's three fixed zones — scene, status, footer — as an empty but structurally complete frame that later tasks fill with a room, a lantern bar, and a prompt.

## Non-Goals
- Does not render any room content — that is A02.
- Does not add choices or transitions — that is A03.
- Does not draw the lantern bar or turn counter — that is A04.
- Does not wire `START GAME` to the screen — that is A12. Nothing reaches this screen from the menu yet.
- Does not implement the typewriter reveal — that is H02.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §7.1 in full — the three zones, the worked layout, and the reason for them ("Stable layout means the player's eye never hunts") — plus §7.4's colour grammar table and §13's "text walls" pitfall (a terminal screen holds about 20 useful lines).
- **Files to create:** `screens/game.py` (to be created).
- **Files to read, not modify:** `screens/settings.py` and `screens/main_menu.py` — the Textual structure precedent in this repo (`Screen` subclass, `CSS` class attribute, `compose()` yielding widgets, `BINDINGS`); `AGENTS.md` for conventions.
- **Conventions to respect:** `AGENTS.md` — keep screen logic in `screens/`, avoid heavy logic inside `compose()`, style through the `CSS` class attribute, use type hints where practical.
- **Design constraints:**
  - **Three zones, fixed.** The scene zone never scrolls within a room, so the player's eye never has to hunt for the status line.
  - **The scene zone holds ≈ 20 usable lines** (§13). Anything longer is two rooms.
  - **Colour is grammar, not decoration** (§7.4): dim grey for description, white for interactables, cyan for the player's own actions, amber for time/light/resources, and **red only when the Shadow is present**. If red is used here at all, it is a bug.
  - The screen must not assume a wide terminal — §7.1's layout has to survive a narrow window.
- **Voice:** the empty frame should already feel like the game — restrained, dim, quiet.

## Preconditions
- [ ] GP-2 done: `python -m pytest` passes the three existing test modules (`test_state.py`, `test_effects.py`, `test_content_schema.py`) and `python index.py` starts
- [ ] GP-3 answered: the git policy is confirmed, or commits are explicitly skipped for this task
- [ ] `screens/settings.py` has been read and its structure is understood

## Actionable Steps
1. Read `screens/settings.py` and mirror its structure: a `Screen` subclass, a `CSS` class attribute, a thin `compose()`.
2. Create `screens/game.py` with the three zones as distinct containers carrying stable ids — one for the scene text, one for status, one for the prompt and key hints — matching §7.1's layout.
3. Give the status zone the §7.1 shape from the start (lantern on the left, composure on the right, prompt beneath) so A04 and D04 have somewhere to write. Leave the values blank.
4. Put the key hints in the footer zone (`AGENTS.md`'s conventions: ↑/↓ navigate, Enter select, Escape back).
5. Apply §7.4's colour vocabulary as a small set of named styles in the `CSS`, so later tasks reuse them rather than inventing their own.
6. Keep `compose()` declarative — no room lookups, no state reads, no branching.
7. Resize the terminal narrow and confirm nothing clips or wraps into illegibility.

## Test Plan
- **Tests to write/update:** new `tests/test_game_screen.py` (to be created):
  - `test_game_screen_mounts_with_three_zones` — asserts the scene, status, and footer zones all exist after mount, using Textual's `run_test()` harness.
  - `test_footer_lists_key_hints` — asserts the footer names the navigation keys.
- **Commands:** `python -m pytest tests/test_game_screen.py -v` — all green; then `python -m pytest` — the three existing modules still pass.
- **Manual verification:** `python index.py`, confirm the app still starts and the menu is unaffected. The gameplay screen is not yet reachable from the menu, which is expected until A12 — verify it mounts via the test harness or a temporary push during development, not by shipping a temporary menu entry.
- **Narrow-terminal check:** resize to roughly the width of the §7.1 diagram and confirm the frame still reads.

## Definition of Done / Acceptance Criteria
- [x] `screens/game.py` exists with three distinct, addressable zones matching §7.1
- [x] The footer zone names the key hints
- [x] `compose()` contains no game-state reads and no branching logic
- [x] No red styling is introduced anywhere
- [x] The frame renders legibly at narrow terminal widths
- [x] `python -m pytest` passes, including the three pre-existing modules
- [x] No file outside `screens/game.py` and the new test module has changed
- [x] No new warnings or TODOs left behind

## Rollback / Undo
Delete `screens/game.py` and `tests/test_game_screen.py`. Nothing references the screen yet, so nothing else breaks. Reverting only this task leaves A02, A03 and A04 with no surface to build on; revert them together or not at all.

## Execution Log
- 2026-11-09: Implemented `screens/game.py` with three zones (`#scene-zone`, `#status-zone`, `#footer-zone`). Added `tests/test_game_screen.py` verifying zone mounting and footer bindings. All 29 unit tests pass cleanly. Preconditions and DoD verified.
