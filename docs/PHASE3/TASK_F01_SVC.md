# Task F01: Dread turn thresholds (Turn 20 rhythm shift, Turn 30 proximity sentence)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: F — Dread Counter & Quiet Horror Presentation
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: D04
- Blocks: F02, F04
- Covers: AC-22, §3.5
- Suggested commit: `feat(dread): implement dread thresholds at turn 20 and turn 30`
- Branch: feature/phase_3_the_shadow

## Objective
Implement dread threshold triggers in `game/dread.py` and `screens/game.py` based on `RunState.turn_count`, without ever showing the turn threshold to the player (§3.5): around Turn 20, presentation rhythm gains an ominous layer, and around Turn 30, room descriptions gain an extra sentence describing the Shadow's proximity.

## Non-Goals
- Never tell the player the turn number means anything or show a countdown timer (forbidden by §3.5).
- Does not modify difficulty-specific choice countdown timers on Hard (handled in Phase 2 Task B05).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.5 ("Dread Counter: A simple turn counter that the player can *see*, but with no stated limit. Around turn 20, the music (if on) gains a second layer. Around turn 30, room descriptions get one extra sentence describing the Shadow's position. *Never tell the player the number means anything.* They'll figure it out and start optimizing — which is the fun.").
- **Files to create:** `game/dread.py`.
- **Files to modify:** `screens/game.py`.

## Preconditions
- [ ] Task D04 DONE (Shadow integrated with game screen).
- [ ] `RunState.turn_count` increments on player actions.

## Actionable Steps
1. Create `game/dread.py`.
2. Define dread constants:
   - `DREAD_RHYTHM_TURN = 20`
   - `DREAD_PROXIMITY_TURN = 30`
3. Implement `get_dread_proximity_sentence(turn_count: int, room_id: str) -> Optional[str]`:
   - If `turn_count >= 30`: returns a chilling one-sentence observation of the Shadow's physical proximity (e.g. "The shadow cast by the doorway is leaning into the room, stretching toward your heels.").
   - Otherwise returns None.
4. Implement `should_shift_rhythm(turn_count: int) -> bool`:
   - Returns True if `turn_count >= 20`.
5. In `screens/game.py`:
   - At Turn >= 20, if Music setting is ON, deepen the border pulsing interval or darken background CSS shade slightly.
   - At Turn >= 30, append the dread proximity sentence to `#scene-text`.

## Test Plan
- **Tests to write:** `tests/test_dread_thresholds.py`:
  - `test_turn_below_twenty_has_no_dread_effects`: Turns 1-19 produce no dread modifications.
  - `test_turn_twenty_triggers_rhythm_shift`: Turn 20 flags rhythm shift.
  - `test_turn_thirty_injects_proximity_sentence`: Turn 30 appends proximity observation.
- **Commands:** `python -m pytest tests/test_dread_thresholds.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Dread thresholds at Turn 20 and 30 trigger accurately.
- [ ] No explicit numerical warnings or countdowns exposed to the player.
- [ ] Tests pass cleanly.

## Rollback / Undo
Delete `game/dread.py` and revert edits to `screens/game.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
