# Task B01: Gameplay screen skeleton with the three zones

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: B — The Screen
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: A05
- Blocks: B02, B04, E03
- Covers: AC-1
- Suggested commit: `feat(screens): add gameplay screen with scene, status, and footer zones`
- Branch: per GP-3

## Objective
Create the gameplay screen and its three fixed zones — a scene area, a status area, and a footer of key hints — per SUGGEST.md §7.1. This task builds the stage; the next three tasks put a room, choices, and meters on it.

## Non-Goals
- Does not render room content (B02).
- Does not implement choice selection or transitions (B03).
- Does not render the meters (B04) — the status zone exists as a placeholder this task.
- Does not implement lantern rules (Slice C) or content (Slice D).
- Does not wire the main menu to launch it (E03).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §7.1 (the three-zone sketch and the rule that the scene must not scroll away within a room) and §7.4 (color as grammar: dim for narration, cyan for the player's own options, **red reserved for the Shadow** and therefore unused in Phase 1).
- **Files to create:** `screens/game.py`.
- **Files to modify:** `index.py` — only enough to reach the screen for manual verification; the real wiring is E03.
- **Files to read, not modify:** `screens/main_menu.py` and `screens/settings.py` for structure precedent (`BINDINGS`, class-level `CSS`, `compose()`, `action_*`).
- **Conventions to respect:** PEP 8; type hints; `Screen` subclass; CSS in the class attribute; no heavy logic in `compose()`; `self.app` for shared state.
- **Design constraints:**
  - Three zones must be visually distinct and hold their shape at narrow terminal widths.
  - The scene zone keeps its room name visible even when the prose is long; if content overflows, the room name must not be what scrolls away.
  - The footer lists the available keys, driven by the screen's own `BINDINGS` rather than a hand-written list.
  - No red anywhere (§7.4).
  - The screen must be reachable and dismissible (Escape returns), so the rest of the slice can be developed against it.

## Preconditions
- [ ] A05 DONE
- [ ] A01 DONE (a menu screen exists to navigate from)
- [ ] The app launches and the settings screen still works

## Actionable Steps
1. Decide and record the zone proportions and the CSS identifiers for each zone.
2. Create `screens/game.py` with the screen class, its `CSS`, and its `BINDINGS`.
3. Implement `compose()` to yield the three zones in order: scene, status, footer.
4. Put placeholder text in each zone so the layout is visible before B02–B04 fill it.
5. Add the footer rendering from the screen's own bindings, so it cannot drift from the real keys.
6. Add a temporary entry point so the screen can be opened for manual checks, clearly commented as temporary and marked for replacement by E03.
7. Verify at a normal width and at a narrow width (~60 columns) that the three zones stay intact and distinguishable.
8. Verify Escape returns cleanly to the menu with no leftover state.

## Test Plan
- **Commands:** `python index.py`
- **Expected:** the gameplay screen opens; all three zones are visible and distinct; the footer lists the real keys; Escape returns to the menu.
- **Narrow-width check:** at ~60 columns the zone boundaries remain clear and the scene name stays visible.
- **Syntax check:** `python -m py_compile index.py screens/*.py`
- **Manual:** confirm no red appears on the screen (§7.4).

## Definition of Done / Acceptance Criteria
- [ ] `screens/game.py` exists with three visually distinct zones
- [ ] The scene zone preserves the room name under long prose
- [ ] The footer is generated from the screen's bindings
- [ ] No red is used anywhere on the screen
- [ ] Layout holds at ~60 columns
- [ ] Escape returns to the menu cleanly
- [ ] The temporary entry point is clearly commented as temporary
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. The gameplay screen is removed and the temporary entry point disappears; the menu and settings screens are untouched.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
