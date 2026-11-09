# Task B04: Status zone — lantern bar, turn counter, low-oil warning

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: B — The Screen
- Layer: UI
- Status: TODO
- Estimate: ~2.5h
- Depends on: B01
- Blocks: B05
- Covers: AC-1, AC-5
- Suggested commit: `feat(screens): render lantern bar, turn counter, and low-oil warning`
- Branch: per GP-3

## Objective
Give the player a permanent read of the two things that make the run finite — the lantern's oil and the turn count — in the status zone, so that the cost introduced in Slice C is felt rather than guessed.

## Non-Goals
- Does not implement the drain rules (C01) or the zero-oil condition (C02) — this task only displays the value and warns when it is low.
- Does not implement the dread counter's *behavior* from §3.5 (the extra Shadow sentence, the layered rhythm) — the counter is displayed only, and its behavioral consequences are Phase 2+.
- Does not display composure (Phase 2, §3.2).
- Does not display the inventory (Phase 2, §3.3).

## Context & Constraints
- **Read first:** `screens/game.py` (B01's status zone), `docs/SUGGEST.md` §7.1 (the status zone sketch) and §7.4 (amber for time and resource warnings; red reserved for the Shadow), `game/state.py` (A03's bounded lantern scale).
- **Files to modify:** `screens/game.py` — the status zone rendering.
- **Files to create:** none expected; the meter helper should be a module-level pure function so B05 can test it directly.
- **Conventions to respect:** PEP 8; type hints; no logic in `compose()`; a single refresh path rather than scattered partial updates.
- **Design constraints:**
  - The meter helper is a **pure function** of value, maximum, and width, returning display text.
  - Meter width is **fixed** so the layout does not jitter as the value changes.
  - The helper clamps for display, so an out-of-range value cannot produce a malformed bar.
  - **Amber** is used when the lantern is low (§7.4). Define "low" once as a named constant or a named threshold function, because Phase 2's difficulty work will need to change it in one place.
  - The turn counter is displayed with **no** label implying a limit or a consequence (§3.5: "never tell the player the number means anything").
  - No red anywhere.
  - The status zone refreshes from run state on every state change and every room transition.

## Preconditions
- [ ] B01 DONE — the status zone exists as a placeholder
- [ ] A03 DONE — lantern and turn count exist on the run state
- [ ] B03 DONE is **not** required; this task may proceed in parallel, but the refresh must be wired to whatever transition path exists

## Actionable Steps
1. Implement the pure meter helper: value, maximum, and width in; a fixed-width filled/empty bar plus a numeric reading out.
2. Define the low-oil threshold as a single named constant and record its value.
3. Implement status zone rendering: lantern meter and turn counter, arranged per §7.1.
4. Apply amber to the lantern when below the threshold, and confirm no red is introduced.
5. Implement one refresh path that re-renders the status zone from run state, and call it on state change and on room transition.
6. Verify the turn counter advances exactly once per player action, not once per refresh or per render.
7. Verify at ~60 columns that the status zone stays on its own lines and the scene zone is unaffected.

## Test Plan
- **Tests to write:** B05 owns the meter helper's tests (zero, full, mid-range, width of one, out-of-range input) and the threshold boundary test.
- **Commands:** `python index.py`
- **Expected:** the lantern bar and turn counter are visible at all times; they update on each action; the turn counter advances by exactly one per action; the amber warning appears exactly at the threshold.
- **Manual:** drive the lantern value to both extremes through the content samples and confirm the bar renders correctly full and empty.
- **Narrow check:** at ~60 columns the status zone does not collide with the scene zone.

## Definition of Done / Acceptance Criteria
- [ ] The lantern bar and turn counter are always visible during play
- [ ] The meter helper is pure and deterministic, with fixed output width
- [ ] The bar clamps for display at both bounds
- [ ] Low-oil amber appears exactly at a single named threshold
- [ ] No red is used anywhere on the screen
- [ ] The turn counter advances exactly once per action
- [ ] Layout holds at ~60 columns
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. The status zone returns to B01's placeholder; the run state and rendering of rooms and choices are unaffected.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the chosen low-oil threshold here -->
