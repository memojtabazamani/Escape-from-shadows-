# Task A04: Status zone — lantern bar, turn counter, low-oil warning

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: UI
- Status: TODO
- Estimate: ~2.5h
- Depends on: A01
- Blocks: A07
- Covers: AC-1, AC-9
- Suggested commit: `feat(ui): show the lantern bar, turn counter, and low-oil warning`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Fill A01's status zone with the two facts the player must always see: how much oil is left, rendered as a bar, and how many turns have passed — plus an amber warning as the oil runs low.

## Non-Goals
- Does not implement the oil-drain rules — that is A05. This task draws the value, it does not change it.
- Does not implement the zero-oil consequence — that is A06.
- Does not draw the composure bar — that is D04. It reserves the space (§7.1's layout shows both bars) but leaves the second one empty.
- Does not implement §3.5's dread-counter escalation (music layers, extra sentences). That is a Phase 3+ idea; only the visible, unexplained counter belongs here.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §7.1 — the status zone in the layout diagram, `LANTERN ██████░░░░  COMPOSURE ████████░░` — §7.4's rule that **amber always means time, light, and resource warnings**, and §3.5 in full, especially "**Never tell the player the number means anything.**"
- **Files to modify:** `screens/game.py` (from A01).
- **Files to read, not modify:** `game/state.py` — `lantern` (int, 0–100, clamped; `has_light()` returns True while any oil remains), `turn_count` (`advance_turn()`).
- **Conventions to respect:** `AGENTS.md` — delegate rendering to helper methods, keep `compose()` thin, style via the `CSS` class attribute.
- **Design constraints:**
  - The lantern is rendered as a **bar of filled and empty blocks**, per §7.1's diagram — ten cells is the intended reading, and the scale in `RunState` is 0–100, so the bar quantises.
  - The turn counter is **visible but unexplained** (§3.5). No label saying "danger", no colour change implying a threshold. The player is meant to work it out.
  - The low-oil warning uses **amber** (§7.4). Red is reserved for the Shadow and must not appear here.
  - The bar must redraw on every state change without a full-screen flicker.
- **Voice:** the status zone is instrumentation; it should read like part of the room, not like a debug overlay.

## Preconditions
- [ ] A01 DONE — the status zone container exists with a stable id
- [ ] `game/state.py` exposes `lantern` and `turn_count` with the documented ranges
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Add a helper that converts the 0–100 lantern value into a ten-cell block bar, rounding consistently and clamping at both ends.
2. Render the bar into the status zone next to a label, matching §7.1's shape.
3. Render the turn counter in the status zone, following §3.5's depiction: visible, unlabelled, unexplained.
4. Add the amber low-oil warning, keyed to a named threshold with a clear rationale. Record the threshold in the Execution Log so A05's drain tests can reference it.
5. Reserve the second bar's position for the composure zone so D04 can fill it without moving the layout.
6. Wire a refresh so both values redraw whenever the run state changes (transition, effect, turn).
7. Confirm the zone renders correctly at lantern 100, at 0, and at exactly the warning threshold.
8. Confirm no red styling is used and that the counter carries no explanatory text.

## Test Plan
- **Tests to write/update:** extend `tests/test_game_screen.py`:
  - `test_lantern_bar_reflects_state_value` — asserts the filled-cell count for a set of lantern values, including 0 and 100.
  - `test_status_zone_shows_turn_count` — asserts the counter renders and increments after a turn.
  - `test_low_oil_warning_uses_amber_not_red` — asserts the warning's style name, guarding §7.4's red reservation.
  - `test_turn_counter_has_no_explanatory_label` — asserts §3.5's "never tell the player" rule mechanically.
- **Commands:** `python -m pytest tests/test_game_screen.py -v`; then `python -m pytest`.
- **Manual verification:** run the app, move between rooms, and confirm the counter rises and the bar falls in step. Confirm the warning appears without any label announcing it means anything.
- **Boundary check:** set the lantern to the warning threshold and to one below it, and confirm the warning's behaviour is exactly as recorded.

## Definition of Done / Acceptance Criteria
- [ ] The lantern renders as a block bar that tracks the state value, clamped at 0 and 100
- [ ] The turn counter is visible and carries no explanatory label
- [ ] The low-oil warning uses amber, never red
- [ ] The composure bar's position is reserved but empty
- [ ] Both values refresh on state change without a full-screen flicker
- [ ] `python -m pytest` passes, including the three pre-existing modules
- [ ] The warning threshold is recorded in the Execution Log
- [ ] No file changed outside `screens/game.py` and the screen test module

## Rollback / Undo
Revert this task's commit; the status zone returns to A01's empty frame. A07 depends on the status zone being meaningful (it is where the HALL's oil context first becomes visible), so revert it before A07 or not at all.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the chosen warning threshold and its rationale here -->
