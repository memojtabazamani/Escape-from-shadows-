# Task B02: Render a room from content

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: B — The Screen
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: B01
- Blocks: B03, F02
- Covers: AC-1, AC-9, AC-11
- Suggested commit: `feat(screens): render room name and prose from content data`
- Branch: per GP-3

## Objective
Make the scene zone display a room — its name and its arrival prose — read entirely from a content record, so that from this task on, what a room says lives in data and never in the screen. This is the engine/content split proven visually (AC-9).

## Non-Goals
- Does not render the choices or handle selection (B03).
- Does not render the status meters (B04).
- Does not implement room transitions (B03).
- Does not write the real HALL and LIBRARY prose (Slice D) — this task proves itself against A04's sample content.
- Does not add the typewriter effect (F02, optional).

## Context & Constraints
- **Read first:** `screens/game.py` (B01's zones), `game/content_schema.py` (A04's record shape), A04's sample content set, `docs/SUGGEST.md` §7.1 and §7.4, and §13's "text walls" pitfall.
- **Files to modify:** `screens/game.py` — the scene zone rendering.
- **Files to create:** none expected. If a text-wrapping or layout helper is needed, keep it a pure function in the game screen module so B05 can test it.
- **Files to read, not modify:** `game/state.py`, `game/content_schema.py`.
- **Conventions to respect:** PEP 8; type hints; no logic in `compose()`; Textual markup for styling, not hand-rolled escapes.
- **Design constraints:**
  - Narration is styled dim; the room name is emphasized (§7.4). No red.
  - **No room text may be hardcoded in the screen** — if you find yourself writing a room's name or prose into a Python file under `screens/`, stop: that is the defect this task exists to prevent (AC-9).
  - A room's prose must fit the scene zone without pushing the room name out of view (§13: a terminal screen holds about 20 useful lines; AC-11).
  - Prose is rendered with a documented, consistent wrap width rather than relying on default terminal wrapping, so the layout is predictable.
  - The rendering function is driven by a room identifier plus the content set, not by a hardcoded room.

## Preconditions
- [ ] B01 DONE — the three zones exist
- [ ] A04 DONE — a validated sample content set exists to render
- [ ] The gameplay screen is reachable for manual checks

## Actionable Steps
1. Load A04's sample content set and pick a room to render by identifier.
2. Implement a pure wrapping helper (text plus width to a list of lines) if one does not already exist, and keep it a pure function for B05 to test.
3. Implement the scene rendering: room name, then wrapped arrival prose, styled per §7.4.
4. Implement the capacity rule: if the wrapped prose would exceed the scene zone's line budget, truncate with a clearly marked continuation rather than silently overflowing — and record the budget as a named constant.
5. Drive the render from a room identifier looked up in the content set; add an explicit failure path for an unknown identifier.
6. Verify by rendering at least two different rooms from the sample set and confirming the output changes with the data alone.
7. Check the three zones still hold their shape at a narrow width with a long room description.

## Test Plan
- **Tests to write:** B05 owns the pure helper's tests (wrapping at the boundary, zero width, text longer than the budget) and the content-only proof.
- **Commands:** `python index.py`
- **Expected:** the scene zone shows the selected room's name and prose; a different room identifier produces different text with no code change.
- **Content-only check (AC-9):** edit only the sample content, restart, and confirm the screen reflects the change. Then revert the sample edit.
- **Budget check:** a deliberately over-long sample room truncates with the marked continuation and does not push the room name out of view.

## Definition of Done / Acceptance Criteria
- [ ] Room name and prose render from a content record
- [ ] No room text is hardcoded anywhere under `screens/`
- [ ] Narration is dim, the name is emphasized, and no red is used
- [ ] The wrap width and the scene line budget are named constants
- [ ] Over-long prose truncates visibly instead of overflowing the zone
- [ ] An unknown room identifier produces a clear failure, not a blank screen
- [ ] The content-only check passes
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. The scene zone returns to B01's placeholder text; the zones and the content format are unaffected.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
