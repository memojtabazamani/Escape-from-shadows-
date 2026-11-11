# Task D01: Shadow state model and pursuit state machine (`game/shadow.py`)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: D — The Shadow Pursuit Engine
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: GP-1
- Blocks: D02, D03, E02
- Covers: AC-15, §2.2
- Suggested commit: `feat(shadow): implement Shadow state model and pursuit state machine`
- Branch: feature/phase_3_the_shadow

## Objective
Implement `game/shadow.py` defining the `ShadowTracker` state machine that models the Shadow's position and pursuit stages relative to the player, executing the learning rule: "it appears in the room you just left, then the room you're about to enter, then the room you *considered* entering" (§2.2).

## Non-Goals
- Does not render UI widgets or styling directly (handled in D04, F02).
- Does not generate player history dialogue (handled in Slice E).
- Does not draw ASCII sprites (forbidden by §2.2).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.2 ("The Shadow as a Named Antagonist: It cannot enter lit rooms... It learns: it appears in the room you just left, then the room you're about to enter, then the room you *considered* entering... It is never drawn as a sprite — only as a description of what's missing").
- **Files to create:** `game/shadow.py`.
- **Files to modify:** `game/state.py`.
- **Pursuit Stages:**
  - `DORMANT` (early turns)
  - `TRAILING` (occupying the room the player just left)
  - `FLANKING` (anticipating player's next move, lingering at thresholds)
  - `STALKING` (occupying an adjacent room the player considered entering)
  - `BREACH` (zero oil or forced darkness: entity breaches into player's room)

## Preconditions
- [ ] Baseline test suite is green.
- [ ] `RunState` model available in `game/state.py`.

## Actionable Steps
1. Create `game/shadow.py` with enum `ShadowStage` and dataclass `ShadowTracker`:
   - `stage`: `ShadowStage` (default `DORMANT`)
   - `last_known_room`: Optional[str] (the room player vacated)
   - `stalking_room`: Optional[str] (room player considered or is moving toward)
   - `proximity_level`: int (0 to 3)
   - `breach_active`: bool
2. Implement transition logic:
   - On room change `record_movement(from_room: str, to_room: str, considered_rooms: list[str])`:
     - Sets `last_known_room = from_room`.
     - Sets stage to `TRAILING`.
     - If player visits a room previously considered, elevates to `FLANKING` / `STALKING`.
3. In `game/state.py`, add `shadow: ShadowTracker = field(default_factory=ShadowTracker)` to `RunState`, ensuring clean JSON snapshot/restore serialization.

## Test Plan
- **Tests to write:** `tests/test_shadow_state.py`:
  - `test_shadow_initial_stage_dormant`: Fresh tracker starts dormant.
  - `test_movement_sets_trailing_stage`: Moving from room A to B places Shadow trailing in room A.
  - `test_repeated_movement_elevates_proximity`: Continued transitions advance proximity level.
  - `test_snapshot_restore_shadow_state`: State machine serializes and restores faithfully.
- **Commands:** `python -m pytest tests/test_shadow_state.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/shadow.py` defines `ShadowTracker` and pursuit state machine cleanly.
- [ ] Learning rule accurately tracks room left and rooms considered.
- [ ] `RunState` serializes and restores Shadow state seamlessly.
- [ ] Tests pass cleanly.

## Rollback / Undo
Delete `game/shadow.py` and revert additions to `game/state.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
