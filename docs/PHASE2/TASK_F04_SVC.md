# Task F04: OLD YARD: rain, mud, the wall, the doghouse (§6)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: D05, E04
- Blocks: F05
- Covers: AC-1, AC-5, AC-7, AC-21, AC-23
- Suggested commit: `feat(content): author Old Yard content with doghouse, wall, and silver whistle`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the Old Yard content record (`old_yard.json`), establishing the exterior atmosphere (rain, mud, insurmountable wall, chained doghouse) where the player discovers that survival and escape are distinct goals, and where the Silver Whistle can be discovered.

## Non-Goals
- Does not author the full Hell Dog encounter combat/puzzle resolution — that is Slice G.
- Does not allow climbing the stone wall to bypass the front door (the wall is impassable).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.3 (Silver Whistle), §6 (Old Yard: "closest thing to outside — rain, mud, a wall too high to climb, a doghouse. This is where the game teaches you that escape and survival are different goals"), AC-1, AC-5, AC-7, AC-21, AC-23.
- **Files to create/modify:** `data/rooms/old_yard.json`.
- **Files to read, not modify:** `game/content_schema.py`.
- **Conventions to respect:** Conforms strictly to schema in `game/content_schema.py`.
- **Design constraints:**
  - Establishes sensory dread: cold rain drenching the lantern (rain threatens oil), sucking mud slowing movement, chain clinking near the doghouse.
  - The stone perimeter wall is too slick and tall to climb (attempting costs composure and a turn).
  - The Silver Whistle is nestled near the yard shed/kennel perimeter and can be collected into inventory.
  - Approaches to the doghouse telegraph the resting beast (setting up Slice G).
  - Prose stays under the 20-line ceiling (AC-23).

## Preconditions
- [ ] D05 DONE — Composure mechanics live.
- [ ] E04 DONE — Journal mechanics live.
- [ ] Content schema validator passing.

## Actionable Steps
1. Create `old_yard.json` with room title, atmospheric prose, and ambient details.
2. Author choices:
   - Search the muddy perimeter (finds the Silver Whistle, adds to inventory if slot free).
   - Inspect the outer wall (reveals escape is impossible here; costs composure/time).
   - Approach the kennel/doghouse (telegraphs the Hell Dog, transitions to the encounter state in Slice G).
   - Return through the back threshold to The Hall.
3. Hook entry into Journal ("The Old Yard — cold rain, mud, and a wall that offers no escape").
4. Validate schema and line budgets.

## Test Plan
- **Tests to write/update:** `tests/test_old_yard_content.py`:
  - `test_old_yard_schema_valid` — passes schema validation.
  - `test_silver_whistle_obtainable` — whistle can be added to inventory.
  - `test_wall_cannot_be_climbed` — attempting wall climb does not escape and applies cost.
  - `test_old_yard_prose_budget` — lines are under 20.
- **Commands:** `python -m pytest tests/test_old_yard_content.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Old Yard content record exists and validates cleanly against schema.
- [ ] Silver Whistle item can be found and stored in inventory.
- [ ] Narration clearly establishes that the yard is not an escape route.
- [ ] Prose conforms to the ≤ 20 line ceiling.
- [ ] All unit and validation tests pass.

## Rollback / Undo
Delete `old_yard.json`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
