# Task A02: Render a room from content records

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: UI
- Status: DONE
- Estimate: ~3h
- Depends on: A01
- Blocks: A03, H02
- Covers: AC-22, AC-1
- Suggested commit: `feat(ui): render rooms from content records`
- Branch: feature/phase_2_the_house

## Objective
Render a room's name and prose into A01's scene zone by reading a content record, proving §11's engine-versus-content split: no room text lives in `screens/`.

## Non-Goals
- Does not implement choices or room transitions — that is A03.
- Does not draw the lantern bar — that is A04.
- Does not author the real rooms. It renders whatever the current content set contains, including `SAMPLE_CONTENT`; THE HALL and OLD LIBRARY are A07 and A08.
- Does not implement the typewriter reveal — that is H02, which animates the text this task renders.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §11 — "The engine knows how to *walk a story graph*... The content is *data*... This is the single highest-leverage structural change available" — plus §7.1 for the scene zone and §13 for the "text walls" limit.
- **Files to modify:** `screens/game.py` (from A01).
- **Files to read, not modify:** `game/content_schema.py` — the record shape (`id`, `name`, `prose`, `choices[]`), `load_content(path)`, `validate_content(content)`, and `SAMPLE_CONTENT`, which is the fixture this task renders; `game/state.py` for the run's location, if A12 has not yet supplied one.
- **Conventions to respect:** `AGENTS.md` — screen logic in `screens/`, shared game state in `game/`, avoid heavy logic in `compose()`; delegate rendering to a helper method, exactly as `screens/main_menu.py` delegates to `render_menu()`.
- **Design constraints:**
  - **The content-only proof is this task's reason to exist.** A reviewer must be able to add a room by editing content and see it, without touching `screens/`.
  - Room prose is displayed as the content provides it; the screen formats, it does not author.
  - Unknown or missing room ids must fail loudly in development and degrade safely for the player — never render a blank screen with no explanation.
  - ≈ 20 usable lines in the scene zone (§13).
- **Voice:** render, do not embellish. The screen's job is to be a window, not a writer.

## Preconditions
- [ ] A01 DONE — `screens/game.py` exists with an addressable scene zone
- [ ] `game/content_schema.py` is in place with `load_content()` and `validate_content()`
- [ ] A content file or `SAMPLE_CONTENT` is available as the render source
- [ ] `python -m pytest` is green before starting (baseline recorded)

## Actionable Steps
1. Read `SAMPLE_CONTENT` in `game/content_schema.py` and note the exact keys a room record carries.
2. Add a content-loading step to the gameplay screen — loading once at screen construction, not per frame, and not inside `compose()`.
3. Validate the loaded content with `validate_content()` at load time and surface any problems during development rather than at play time.
4. Add a helper that renders a room record's `name` and `prose` into the scene zone, following `render_menu()`'s precedent in `main_menu.py`.
5. Add the room-lookup helper the transition (A03) will call: given a room id, return the record or fail clearly.
6. Render the start room (`start_room`) on mount so the screen shows something real.
7. Keep the current room id in the run's state, not in the widget, so A03 and I01 can move and save it.
8. Confirm by inspection that no prose string from a room record appears anywhere under `screens/`.

## Test Plan
- **Tests to write/update:** extend `tests/test_game_screen.py` (to be created by A01):
  - `test_screen_renders_room_name_and_prose` — asserts both appear in the scene zone for a known room.
  - `test_unknown_room_id_fails_loudly` — asserts a missing room id raises or reports, rather than rendering empty.
  - `test_no_room_prose_hardcoded_in_screens` — the content-only proof: scans `screens/` for any room `prose` string from the content set.
- **Commands:** `python -m pytest tests/test_game_screen.py -v`; then `python -m pytest`.
- **Manual verification:** swap a room's `prose` in the content file, restart, and confirm the change appears with no code edit. That observation *is* AC-22.

## Definition of Done / Acceptance Criteria
- [x] A room's name and prose render from content, with no prose duplicated in `screens/`
- [x] Changing a room's prose in the content file changes the screen with no code edit
- [x] Content is loaded once, not per frame, and never inside `compose()`
- [x] An unknown room id fails loudly in development rather than rendering an empty scene
- [x] The current room id lives in the run state, not in a widget attribute
- [x] `python -m pytest` passes, including the three pre-existing modules
- [x] No file changed outside `screens/game.py`, `game/state.py`, and the screen test module

## Rollback / Undo
Revert this task's commit; the screen returns to A01's empty frame. A03 and H02 both depend on this rendering path, so reverting it alone breaks them — revert together.

## Execution Log
- 2026-11-09: Implemented content record rendering in `screens/game.py`. `GameScreen` loads and validates content once upon initialization. Current room is tracked on `RunState.current_room`. Unknown room lookups raise `KeyError`. Added unit tests in `tests/test_game_screen.py` verifying rendering, error handling, and scanning `screens/` to guarantee no hardcoded prose. All 32 tests pass.
