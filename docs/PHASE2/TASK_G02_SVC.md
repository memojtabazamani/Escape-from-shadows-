# Task G02: The four solutions: slow, quick, meat, whistle (§4.3)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: G — The Hell Dog
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: G01
- Blocks: G03
- Covers: AC-13, AC-21
- Suggested commit: `feat(content): author the four distinct Hell Dog solutions with respective trade-offs`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the four distinct solutions for resolving the Hell Dog encounter as described in §4.3 (Move slowly, Move quickly, Throw the meat, Blow the whistle), replacing the baseline's coin flip with a rich choice architecture where each option has distinct costs, requirements, and long-term consequences.

## Non-Goals
- Does not author the hidden memory fragment inside the meat (deferred to Phase 3 per ASM-12).
- Does not author the delayed return of the whistled dog (that is G03).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §4.3 ("Choices With No Safe Answer... Example for the OLD YARD Hell Dog"), §6 (Hell Dog reworked), AC-13 and AC-21 in `EPIC_Phase2_TheHouse_PLAN.md`, and RISK-9 (Ensuring solutions don't collapse into duplicates).
- **Files to modify:** `data/rooms/old_yard_dog.json` (or `old_yard.json`).
- **Files to read, not modify:** `game/content_schema.py`.
- **Conventions to respect:** Conforms strictly to schema in `game/content_schema.py`.
- **Design constraints — each solution must have distinct mechanical and narrative effects (RISK-9):**
  1. **Move slowly:** Costs substantial oil and composure; player edges around the kennel carefully; keeps any held weapons clean; dog stays asleep/contained.
  2. **Move quickly:** Sprints across the mud. If composure is high, player slips past by a hair; if low or unlucky, wakes the dog immediately, forcing a brutal struggle or telegraphed escape setback.
  3. **Throw the meat:** Requires `raw_meat` in inventory. Dog devours the meat greedily. Dog survives and remains occupied; player loses the meat item safely.
  4. **Blow the silver whistle:** Requires `silver_whistle` in inventory AND `knows_dog_name` flag. Dog halts, whimpers at its true name, and retreats into the gloom (setting up G03).

## Preconditions
- [ ] G01 DONE — Dog standoff state and freeze mechanic active.
- [ ] Inventory items `raw_meat` and `silver_whistle` defined in Slice C / F.
- [ ] `knows_dog_name` flag set up in F03.

## Actionable Steps
1. Author Solution 1 ("Edge past slowly, step by deliberate step"):
   - Deducts 3 oil, deducts 2 composure, takes 2 turns.
   - Successful bypass, exits yard toward the perimeter kennel shed.
2. Author Solution 2 ("Sprint for the gate gap"):
   - High risk. Checks composure / agility.
   - If successful, bypasses dog with 0 oil cost, but causes noise.
   - If failed, dog lunges, causing damage/setback with clear warning.
3. Author Solution 3 ("Toss the butcher's meat across the yard"):
   - Requirement: `has_item: "raw_meat"`.
   - Effect: removes `raw_meat` from inventory, pacifies dog, allows free passage.
4. Author Solution 4 ("Raise the silver whistle to your lips"):
   - Requirement: `has_item: "silver_whistle"`.
   - Gated by whether the player knows the name (routed through G03).
5. Author Journal entries for each method chosen.
6. Verify line budget across all four outcomes (≤ 20 lines).

## Test Plan
- **Tests to write/update:** `tests/test_hell_dog_solutions.py`:
  - `test_solution_slow_costs_oil_and_composure` — slow bypass deducts oil and composure.
  - `test_solution_meat_consumes_meat_item` — tossing meat removes item and bypasses dog.
  - `test_solution_sprint_triggers_distinct_outcome` — sprint produces distinct consequences.
  - `test_solutions_are_mutually_distinct` — asserts that all four options have different outcome states (RISK-9 guard).
- **Commands:** `python -m pytest tests/test_hell_dog_solutions.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] All four solutions are authored and functional.
- [ ] Requirements (meat, whistle) gate their respective options.
- [ ] Each solution produces observably different costs and journal notes.
- [ ] No two solutions collapse into the same mechanical state.
- [ ] All tests pass cleanly.

## Rollback / Undo
Revert solution choices in yard content.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
