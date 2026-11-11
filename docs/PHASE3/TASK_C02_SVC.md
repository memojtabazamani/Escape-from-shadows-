# Task C02: House room content placement and acquisition trade-offs (§2.4, §4.3)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: C — The Three Memory Fragments
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: C01
- Blocks: C03
- Covers: AC-13, AC-14, §2.4, §4.3
- Suggested commit: `feat(content): place memory fragments behind room trade-offs`
- Branch: feature/phase_3_the_shadow

## Objective
Place the three memory fragments into the house rooms (`hall`, `blood_kitchen`, `old_library`) behind deliberate exploration trade-offs in `data/content.json`, such as composure expenditures, search turns, or sacrifices (including the §4.3 option 3 meat sacrifice dilemma).

## Non-Goals
- Does not change the core 4-room layout or add unapproved rooms.
- Does not bypass the 6-slot inventory cap (fragments require free slots or drop-to-take).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.4, §4.3 ("Throw the meat (only with the kitchen item) — the dog lives, you lose the meat *and* a memory fragment you didn't notice was in it").
- **Room Placements & Trade-offs:**
  1. `old_photograph` (The Hall): Found by prying the floorboard near the grandfather clock. Costs: 1 lantern oil, 5 composure (the dust and grinding sound summons a cold chill).
  2. `child_drawing` (The Blood Kitchen): Tucked inside the frozen carcass / meat drawer. Taking it requires handling the gore (costs 8 composure). Furthermore, if the player throws the raw meat to the Hell Dog in the yard, authoring branches reflect that the drawing was lost inside the meat!
  3. `dated_receipt` (The Old Library): Found while inspecting the high shadowed shelves instead of reading the lectern tome. Costs: 1 search turn (draining 10 oil).
- **Files to modify:** `data/content.json`.

## Preconditions
- [ ] Task C01 DONE (items and schema predicates available).
- [ ] `data/content.json` passes schema validator.

## Actionable Steps
1. In `data/content.json`, add the 3 item definitions under `"items"`.
2. In `hall`, author a choice to inspect the loose floorboard under the dead clock, yielding `old_photograph` and recording fragment into `RunState`.
3. In `blood_kitchen`, author a search choice at the cold hook, yielding `child_drawing` at a composure cost.
4. In `old_yard`, update the throw-meat choice to check if `child_drawing` was held; if held, remove it or note in prose that it was thrown with the meat.
5. In `old_library`, author a search choice on the upper dust stacks, yielding `dated_receipt` at an oil cost.
6. Validate all choices against `game/content_schema.py`.

## Test Plan
- **Tests to write:** `tests/test_fragment_tradeoffs.py`:
  - `test_photograph_acquisition_costs_oil_and_composure`: Inspecting floorboard costs resources and yields photograph.
  - `test_drawing_acquisition_costs_composure`: Kitchen search drains composure and yields drawing.
  - `test_receipt_acquisition_costs_oil`: Library search consumes oil and grants receipt.
  - `test_throwing_meat_with_drawing_sacrifices_drawing`: Validates the §4.3 dilemma.
- **Commands:** `python -m pytest tests/test_fragment_tradeoffs.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] All three memory fragments are obtainable in the manor via distinct trade-offs.
- [ ] The §4.3 meat dilemma is faithfully represented.
- [ ] Content schema validation passes cleanly.

## Rollback / Undo
Revert choice and item additions in `data/content.json`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
