# Task F06: The front door key: three routes, two of them traps

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: F05
- Blocks: F08
- Covers: AC-8, AC-21
- Suggested commit: `feat(content): implement three routes to the Front Door Key with two telegraphed traps`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the three distinct acquisition paths for the Front Door Key across the house — where exactly one is genuine and two are telegraphed lethal/harmful traps (§3.3), ensuring players learn to read warnings rather than blindly grabbing keys.

## Non-Goals
- Does not change the core engine or inventory capacity mechanics.
- Does not author unwarned deaths (both trap routes must present two clear warnings before triggering, per AC-21).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.3 ("Front Door Key — obtainable three different ways. Two of them are traps"), §4.1 (Three-tier consequence model), §4.2 (Telegraph, don't announce), AC-8 and AC-21 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `data/rooms/the_hall.json`, `data/rooms/blood_kitchen.json`, `data/rooms/old_library.json`, and item definition files.
- **Files to read, not modify:** `game/content_schema.py`.
- **Conventions to respect:** Maintain declarative triggers, requirements, and effects.
- **Design constraints:**
  - Route 1 (Genuine Key): Discovered through careful search in the Old Library's secret drawer (unlocked by knowledge or clever inspection).
  - Route 2 (Trap A - Blood Kitchen): A tarnished key sitting in a bowl of warm entrails on the kitchen butcher table. Touching it without a tool or ignoring the stench/heat triggers a visceral trap (severe composure scar or fatal ambush if unheeded).
  - Route 3 (Trap B - The Hall Clock/Niche): A gleaming brass key inside a dark grandfather clock in the Hall. Clock gears tick erratically; sticking a hand inside without bracing the pendulum snaps down an iron counterweight (limb injury / setback or fatal trap if ignored).
  - Every trap choice must offer an exit/step-back option and provide two explicit sensory telegraphs.

## Preconditions
- [ ] F05 DONE — Hall hub and rooms are operational.
- [ ] Item schemas support the Front Door Key item.
- [ ] Content schema validator passing.

## Actionable Steps
1. Add the genuine Front Door Key item to the Old Library content with appropriate requirements.
2. Add the Blood Kitchen false/trapped key interaction with two distinct telegraphs:
   - Warning 1: Unnatural warmth and putrid steam rising from the basin.
   - Warning 2: Strange rhythmic pulse under the metal bowl.
   - Consequence if persisted: violent setback or death with clear lesson.
3. Add the Hall Grandfather Clock false/trapped key interaction with two distinct telegraphs:
   - Warning 1: Clock ticks out of sync, pendulum vibrates with high tension.
   - Warning 2: Scent of rusted metal shavings and coiled spring pressure.
   - Consequence if persisted: setback or trap consequence with clear lesson.
4. Update the Front Door choice in The Hall to check for the genuine key (`has_item: "front_door_key"`).
5. Validate content and test each route.

## Test Plan
- **Tests to write/update:** `tests/test_front_door_key_routes.py`:
  - `test_genuine_key_opens_front_door` — acquiring key from Library enables door opening on attempt 3.
  - `test_kitchen_trap_route_telegraphed` — kitchen trap displays both telegraphs before consequence.
  - `test_clock_trap_route_telegraphed` — clock trap displays both telegraphs before consequence.
  - `test_trap_lessons_recorded_in_journal` — if a trap kills the player, journal records why.
- **Commands:** `python -m pytest tests/test_front_door_key_routes.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Three distinct key routes exist across the content files.
- [ ] Exactly one key route is genuine and unlocks the front door.
- [ ] Both trap routes feature at least two clear sensory telegraphs before triggering adverse effects.
- [ ] Reaching a trap consequence records an informative lesson in the journal.
- [ ] All tests pass cleanly.

## Rollback / Undo
Revert key route choices in room content records.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
