# Task D02: Lit-room barrier and zero-oil breach rules (§2.2, §3.1)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: D — The Shadow Pursuit Engine
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: D01
- Blocks: D04
- Covers: AC-16, AC-17, §2.2, §3.1
- Suggested commit: `feat(shadow): enforce lit-room barrier and zero-oil breach condition`
- Branch: feature/phase_3_the_shadow

## Objective
Enforce the fundamental physical and supernatural laws of the Shadow in `game/shadow.py`: it cannot enter lit rooms as long as the player's lantern has oil, but immediately breaches the player's room when oil drops to zero (§2.2, §3.1).

## Non-Goals
- Does not replace standard zero-oil death/consequence, but enhances it with the Shadow breach narrative.
- Does not change oil consumption rates (regulated by difficulty in `game/lantern.py`).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.2 ("It cannot enter lit rooms — so light is both your resource and your leash"), §3.1 ("At zero oil, the Shadow can reach you. This creates the game's core tension: *understanding the world costs you the safety to explore it.*").
- **Files to modify:** `game/shadow.py`, `game/lantern.py`.
- **Core Rules:**
  1. `can_enter_room(room_id: str, state: RunState) -> bool`:
     - If `state.lantern > 0` and room is lit / held by player -> Returns `False`. The Shadow is repelled to adjacent doorway/shadows.
     - If `state.lantern == 0` -> Returns `True`. Entity breaches barrier directly.
  2. When breached, sets `breach_active = True` and prompts the direct encounter state.

## Preconditions
- [ ] Task D01 DONE (`ShadowTracker` available).
- [ ] `game/lantern.py` rules intact.

## Actionable Steps
1. In `game/shadow.py`, implement `evaluate_light_barrier(tracker: ShadowTracker, state: RunState) -> None`:
   - Checks `state.lantern`:
     - If `> 0`: Shadow remains outside the current room. If proximity is high, state becomes `STALKING` (loitering in dark threshold).
     - If `== 0`: Triggers `tracker.stage = ShadowStage.BREACH`, setting `tracker.breach_active = True`.
2. Provide query helper `is_shadow_in_current_room(tracker: ShadowTracker, state: RunState) -> bool`.
3. Provide query helper `is_shadow_at_threshold(tracker: ShadowTracker, room_id: str) -> bool`.

## Test Plan
- **Tests to write:** `tests/test_shadow_light_barrier.py`:
  - `test_lit_room_blocks_shadow_entry`: While lantern oil > 0, shadow cannot enter player room.
  - `test_zero_oil_triggers_shadow_breach`: When lantern reaches 0, shadow enters BREACH stage.
  - `test_refilling_oil_restores_barrier`: If oil is refilled, breach status resets and shadow is pushed back to threshold.
- **Commands:** `python -m pytest tests/test_shadow_light_barrier.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Light barrier rule strictly blocks Shadow entry when lantern > 0.
- [ ] Zero oil immediately triggers Shadow breach.
- [ ] Tests verify both barrier enforcement and breach transition.

## Rollback / Undo
Revert edits to `game/shadow.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
