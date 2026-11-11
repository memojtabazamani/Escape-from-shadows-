# Task F05: THE HALL rework: hub, staircase, the yielding front door

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: F02, F03, F04
- Blocks: F06
- Covers: AC-1, AC-2, AC-7, AC-23
- Suggested commit: `feat(content): rework The Hall as true four-way manor hub with stuck front door`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Rework The Hall content record (`the_hall.json`) into the true manor hub that connects all four rooms (Blood Kitchen, Old Library, Old Yard) plus the staircase and the front door — where the heavy front door is visibly stuck, resists early attempts, and yields on the third attempt once properly unlocked or forced.

## Non-Goals
- Does not author the walkable staircase rooms (The Stairwell / Nursery are Phase 3+ per ASM-13); the staircase is described as ominous and blocked.
- Does not author the three key routes — that is F06.
- Does not author ending screen rendering — that is A11 / Slice E.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6 (The Hall: "hub, not a corridor. Two doors, a staircase up, and a front door that is visibly, insultingly, unlocked-but-stuck. The player will try it three times across two runs. Let the third attempt work"), AC-1, AC-2, AC-7, AC-23.
- **Files to modify:** `data/rooms/the_hall.json`.
- **Files to read, not modify:** `game/content_schema.py`.
- **Conventions to respect:** Conforms strictly to schema in `game/content_schema.py`.
- **Design constraints:**
  - The Hall acts as the central crossroad linking:
    - West door: Blood Kitchen
    - East door: Old Library
    - Back door: Old Yard
    - Upward: Ominous grand staircase (descending draft, unlit, currently inaccessible)
    - South: The massive Front Door
  - First attempt on the Front Door: iron latch shudders, wood groans, door does not budge; player notes the binding lock.
  - Second attempt: door gives an inch, revealing rusted iron deadbolts; costs composure and turn.
  - Third attempt (with prerequisite key or knowledge): latch gives way with a sharp crack, opening the path to escape.
  - Matchbox item can be searched and found on the hall table (§3.3).
  - All room descriptions remain within the 20-line ceiling (AC-23).

## Preconditions
- [ ] F02 (Kitchen), F03 (Library), F04 (Yard) content files exist.
- [ ] Content schema validator passing.

## Actionable Steps
1. Refactor `the_hall.json` to feature navigation links to all three wings (Kitchen, Library, Yard).
2. Author the Matchbox item on the side table (consumable item granting one lantern relight).
3. Implement the three-attempt counter or state progression on the Front Door interaction (`door_attempts` flag or state counter).
4. Author descriptive text for the staircase: winding into suffocating darkness above.
5. Author the front door resistance and final release when prerequisites are met.
6. Verify line budget across all state variants (≤ 20 lines).

## Test Plan
- **Tests to write/update:** `tests/test_the_hall_hub.py`:
  - `test_the_hall_links_all_rooms` — choices lead to Blood Kitchen, Old Library, and Old Yard.
  - `test_front_door_attempts_progression` — attempts 1 and 2 fail with descriptive tension; attempt 3 succeeds when prerequisites met.
  - `test_matchbox_obtainable` — matchbox can be picked up into inventory.
  - `test_the_hall_prose_budget` — lines are under 20.
- **Commands:** `python -m pytest tests/test_the_hall_hub.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] The Hall connects cleanly to Blood Kitchen, Old Library, and Old Yard.
- [ ] Front door exhibits the three-attempt yielding mechanic.
- [ ] Matchbox item is obtainable from the hall table.
- [ ] Prose conforms to the ≤ 20 line ceiling.
- [ ] All tests pass cleanly.

## Rollback / Undo
Revert changes to `the_hall.json`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
