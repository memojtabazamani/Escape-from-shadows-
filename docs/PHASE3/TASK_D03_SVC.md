# Task D03: Shadow manifestation text generator: descriptions of absence (§2.2)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: D — The Shadow Pursuit Engine
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: D01
- Blocks: D04, F02
- Covers: AC-18, §2.2
- Suggested commit: `feat(shadow): generate descriptions of absence for Shadow manifestations`
- Branch: feature/phase_3_the_shadow

## Objective
Author the prose generation engine for Shadow manifestations in `game/shadow_prose.py`, adhering strictly to §2.2's rule: "It is never drawn as a sprite — only as a description of what's missing: a doorway with no light behind it, a chair that is now facing the wall."

## Non-Goals
- Does not render ASCII monster sprites.
- Does not inject full dialogue quotes (handled in Slice E).
- Does not format terminal text colors (handled in F02).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.2 ("It is never drawn as a sprite — only as a description of what's missing: a doorway with no light behind it, a chair that is now facing the wall.").
- **Files to create:** `game/shadow_prose.py`.
- **Catalogue of Absence Cues by Stage:**
  - `TRAILING` (the room you just left):
    - "Behind you, the doorway into the previous room has gone entirely black. Even the ambient dust motes have stopped moving."
    - "The sound of your own footsteps echoes from the hallway you just vacated, a half-second too late."
  - `FLANKING` / `STALKING` (thresholds ahead):
    - "The doorframe to your right casts no shadow on the floorboards, though your lantern burns bright."
    - "The high-backed armchair by the corner is facing the wall now. You are certain it was turned toward the fire when you entered."
    - "A draft of icy air presses from the threshold ahead, smelling faintly of cold iron and extinguished tallow."
  - `BREACH` (zero oil):
    - "The wick sputters and drowns in blackened oil. The darkness around you is not an absence of light; it has weight and heat."

## Preconditions
- [ ] Task D01 DONE (`ShadowStage` and `proximity_level` available).
- [ ] Working tree clean.

## Actionable Steps
1. Create `game/shadow_prose.py`.
2. Author curated catalogs of subtle absence descriptions keyed by `ShadowStage` and current room context.
3. Implement `get_shadow_absence_prose(tracker: ShadowTracker, current_room: str) -> Optional[str]`:
   - Returns None if stage is `DORMANT`.
   - Returns a restrained, 1-2 sentence absence description when trailing or stalking.
   - Rotates/samples deterministically to avoid repetitive descriptions.
4. Provide helper `get_threshold_telegraph(tracker: ShadowTracker, door_destination: str) -> Optional[str]` to warn players when the Shadow is lurking just beyond a specific doorway.

## Test Plan
- **Tests to write:** `tests/test_shadow_prose.py`:
  - `test_dormant_stage_returns_no_prose`: Dormant returns None.
  - `test_trailing_stage_returns_absence_prose`: Returns prose describing absence behind player.
  - `test_stalking_stage_returns_threshold_warning`: Warns about altered room details.
  - `test_breach_returns_heavy_darkness_prose`: Zero-oil breach returns definitive cold dark prose.
- **Commands:** `python -m pytest tests/test_shadow_prose.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/shadow_prose.py` generates eerie absence descriptions without sprite references.
- [ ] Conforms to §2.2 horror ethos.
- [ ] Tests pass cleanly.

## Rollback / Undo
Delete `game/shadow_prose.py` and `tests/test_shadow_prose.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
