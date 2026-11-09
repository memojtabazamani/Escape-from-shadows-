# Task G04: Hell Dog tests: four solutions, distinct outcomes

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: G — The Hell Dog
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: G03
- Blocks: None (Slice G terminal verification)
- Covers: AC-13, AC-14
- Suggested commit: `test(dog): comprehensive test suite for Hell Dog puzzle solutions and mechanics`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Provide an exhaustive automated test suite for the Hell Dog encounter in the Old Yard, verifying that the freeze rule behaves predictably, all four solutions execute correctly with appropriate requirements and costs, and no two solutions produce identical end states.

## Non-Goals
- Does not test unrelated room transitions or non-dog choices.
- Does not test save/load serialization of dog state (covered in Slice I).

## Context & Constraints
- **Read first:** `EPIC_Phase2_TheHouse_PLAN.md` AC-13, AC-14, RISK-9.
- **Files to create:** `tests/test_hell_dog_suite.py`.
- **Files to read, not modify:** `data/rooms/old_yard_dog.json`, `data/rooms/old_yard.json`, `game/content_schema.py`.
- **Conventions to respect:** Use `pytest`. Test behavioral outcomes, inventory deductions, composure and oil changes, and state flags.

## Preconditions
- [ ] G01, G02, and G03 are DONE.
- [ ] Working tree clean and existing tests green.

## Actionable Steps
1. Create `tests/test_hell_dog_suite.py`.
2. Write unit and integration tests for:
   - Freeze rule: standing still consumes oil, leaves dog in place, advances turns safely.
   - Solution 1 (Slow): costs lantern oil and composure, yields clean passage.
   - Solution 2 (Sprint): tests composure threshold, yields noise / risk outcome.
   - Solution 3 (Meat): requires meat item, consumes meat item from inventory, leaves dog fed.
   - Solution 4 (Whistle): requires whistle item; without book knowledge fails; with book knowledge pacifies dog and sets `dog_whistled_away`.
   - Delayed return: verifies `dog_whistled_away` triggers the climax encounter at the front door.
3. Assert distinctness: verify that the resulting game state sets for each of the four solutions are pairwise non-identical (AC-13, RISK-9).
4. Run full test suite and confirm green.

## Test Plan
- **Commands:** `python -m pytest tests/test_hell_dog_suite.py -v`.
- **Manual verification:** Run the game interactively, test each of the four choices in the Old Yard, verify differing journal notes and inventory changes.

## Definition of Done / Acceptance Criteria
- [ ] All four solutions have passing automated tests.
- [ ] Freeze rule is verified by test.
- [ ] Distinctness assertion confirms no two solutions collapse into the same outcome.
- [ ] Front door reappearance is verified by test.
- [ ] 100% of dog suite tests pass cleanly.

## Rollback / Undo
Delete `tests/test_hell_dog_suite.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
