# Task D04: Shadow pursuit integration into gameplay room loop

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: D — The Shadow Pursuit Engine
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: D02, D03
- Blocks: D05, E03, F01
- Covers: AC-15, AC-16, AC-17, §2.2, §3.1
- Suggested commit: `feat(game): integrate Shadow pursuit state machine into room transition loop`
- Branch: feature/phase_3_the_shadow

## Objective
Wire the Shadow pursuit engine into `screens/game.py` and `game/effects.py`, updating the Shadow's position on every room transition and choice evaluation, and appending absence telegraphs to the scene zone when appropriate.

## Non-Goals
- Does not inject history-driven second-person dialogue yet (handled in Slice E).
- Does not implement Turn 20/30 dread counter hooks yet (handled in Slice F).

## Context & Constraints
- **Read first:** `screens/game.py` (`transition_to_room()`, `resolve_selected_choice()`), `game/shadow.py`, `game/shadow_prose.py`.
- **Files to modify:** `screens/game.py`, `game/effects.py`.
- **Precedent:** Follows how `drain_for_room()` and `distort_narration()` are integrated into `GameScreen`.

## Preconditions
- [ ] Tasks D01, D02, D03 DONE.
- [ ] Baseline test suite clean.

## Actionable Steps
1. In `screens/game.py`, in `transition_to_room(destination)`:
   - Call `state.shadow.record_movement(from_room=previous_room, to_room=destination, considered_rooms=...)`.
   - Call `evaluate_light_barrier(state.shadow, state)`.
2. In `render_room()`:
   - Query `absence_prose = get_shadow_absence_prose(state.shadow, state.current_room)`.
   - If present, append to `#scene-telegraphs` or `#scene-text`.
3. In `render_choices()`:
   - For choices that enter unlit or stalked rooms, query `get_threshold_telegraph()` to hint at the Shadow's lurking presence.
4. If `state.shadow.breach_active`:
   - Trigger the zero-oil confrontation / transition immediately.

## Test Plan
- **Tests to write:** `tests/test_shadow_room_integration.py`:
  - `test_room_transition_updates_shadow_tracker`: Moving between rooms updates tracker on state.
  - `test_absence_prose_appended_to_scene`: When stalking, absence prose appears in scene zone.
  - `test_threshold_warning_in_choices`: Choices leading toward Shadow include warning cues.
- **Commands:** `python -m pytest tests/test_shadow_room_integration.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Every room transition updates Shadow pursuit tracking.
- [ ] Absence cues and threshold warnings display reliably in the UI.
- [ ] Tests pass cleanly with no regression.

## Rollback / Undo
Revert modifications to `screens/game.py` and `game/effects.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
