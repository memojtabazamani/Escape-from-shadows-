# Task G01: The dog's rule: it only moves when you do (§6)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: G — The Hell Dog
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: F08
- Blocks: G02
- Covers: AC-14
- Suggested commit: `feat(content): implement Hell Dog movement rule where standing still costs oil but keeps safe`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the core behavioral mechanic of the Hell Dog in the Old Yard: the beast only moves when the player moves; standing perfectly still is safe from attack but continuously expends lantern oil, transforming the encounter into a tense turn-based resource-management puzzle.

## Non-Goals
- Does not implement all four distinct bypass/combat solutions yet — that is G02.
- Does not implement the recurring dog consequence or whistle lore dependency — that is G03.
- Does not render ASCII art (ASCII art is reserved for title screen and key encounters, governed by Slice H).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6 ("The Hell Dog, Reworked: ...give it one rule the player can discover: *it only moves when you do.* Standing still is safe and costs oil. This turns the encounter into a resource-management scene instead of a dice roll"), AC-14 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `data/rooms/old_yard_dog.json` (or sub-scene of `old_yard.json`).
- **Files to read, not modify:** `game/content_schema.py`, `game/lantern.py`.
- **Conventions to respect:** Conforms to `content_schema.py`.
- **Design constraints:**
  - Player discovers the rule organically through observation and telegraphing: the dog's glowing eyes fixate on you; when you freeze, its heavy paws stay planted; when you shift, the gravel crunches and the beast edges forward.
  - Choosing "Stand still / Don't move" advances the turn, consumes 1 oil, but results in zero beast advance and decreases composure slightly (the dread of freezing in the dark).
  - Standing still reveals sensory details (chain slack, the scent of burning hair, the dog's collar tag).

## Preconditions
- [ ] F08 DONE — Old Yard content and full-house validation passed.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. In `old_yard.json` (or linked encounter state `old_yard_dog.json`), author the Hell Dog standoff encounter scene.
2. Author choice: "Freeze / Stand perfectly still":
   - Deducts 1 lantern oil.
   - Advances turn counter.
   - Deducts 1 composure.
   - Text explicitly telegraphs: "The beast pauses, black chest heaving. It does not advance. It is waiting for you to move."
3. Author choice: "Take a step" / shift position:
   - Advances the beast closer by one stage (e.g. `dog_distance` stage counter: 3 -> 2 -> 1).
4. Author the discovery note into the Journal upon using the stand-still action ("The Hell Dog only moves when I move").
5. Validate schema and prose length.

## Test Plan
- **Tests to write/update:** `tests/test_hell_dog_rule.py`:
  - `test_standing_still_costs_oil_without_dog_advancing` — choosing freeze drains oil but maintains distance counter.
  - `test_moving_advances_dog_distance` — advancing decreases distance to dog.
  - `test_rule_recorded_in_journal` — freeze action records dog's movement rule in player journal.
- **Commands:** `python -m pytest tests/test_hell_dog_rule.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Hell Dog standoff scene supports the "stand still" action.
- [ ] Standing still consumes lantern oil but prevents the beast from attacking.
- [ ] Discovery is telegraphed clearly in prose and recorded in the Journal.
- [ ] All tests pass cleanly.

## Rollback / Undo
Revert dog encounter choice additions in yard content.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
