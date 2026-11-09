# Task F03: OLD LIBRARY rework: the three-turn read

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: F01, C05
- Blocks: F05
- Covers: AC-1, AC-4, AC-21, AC-23
- Suggested commit: `feat(content): rework Old Library to feature three-turn Book reading puzzle`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Rework the Old Library content record from Phase 1's single-turn action into §6's three-consecutive-turn read scene: reading the Book burns down the candle and oil across three turns while the door is unmonitored, culminating in discovering the dog's true name and noticing that the door has quietly swung open.

## Non-Goals
- Does not change the multi-turn engine logic — F01 already implemented that mechanism.
- Does not author the Hell Dog scene — Slice G authors the Hell Dog encounter that consumes the dog's name.
- Does not add extra rooms (Cellar or Chapel).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.3 (The Book), §6 (Old Library: "reading it takes three consecutive turns during which you cannot see the door. The candle burns down while you read... you know someone came in, because the door is open now"), AC-4, AC-21, AC-23.
- **Files to modify:** `data/rooms/old_library.json` (or equivalent content record).
- **Files to read, not modify:** `game/multiturn.py`, `game/content_schema.py`.
- **Conventions to respect:** Conforms to `content_schema.py`. Utilizes `start_multiturn` / `advance_multiturn` action schemas.
- **Design constraints:**
  - Reading the Book consumes oil on each turn.
  - On turn 1 of reading: describes opening the thick volume, pages heavy with dust.
  - On turn 2 of reading: describes finding the passage on the guardian beast in the yard (revealing the name / lore).
  - On turn 3 of reading: candle flickers to a stub, shadow deepens, and the chilling realization lands: the study door is now standing ajar.
  - Setting flag: `knows_dog_name` or `read_the_book`.
  - Can take the Book into inventory if an inventory slot is free (heavy item).
  - Prose stays strictly within 20 lines per state (AC-23).

## Preconditions
- [ ] F01 DONE — Multi-turn action engine mechanism available.
- [ ] C05 DONE — Inventory system active.
- [ ] Schema validator passes.

## Actionable Steps
1. Refactor `old_library.json` to link the reading choice to a 3-step multi-turn action.
2. Author dynamic step prose or room state descriptions reflecting the advancing turns and candle burning down.
3. Configure the per-step oil cost (1 oil per turn) and composure drain if interrupted.
4. On step 3 completion, award the `read_the_book` / `knows_dog_name` knowledge flag, record entry in the Journal, and change room state to note the ajar door.
5. Provide a choice to take the Book into inventory if an empty slot is available.
6. Provide choices to inspect the shelves and exit back into The Hall.
7. Validate content and ensure all prose variants remain within the 20-line ceiling.

## Test Plan
- **Tests to write/update:** `tests/test_old_library_rework.py`:
  - `test_library_content_valid` — passes schema validation.
  - `test_book_reading_requires_three_turns` — completing reading takes exactly 3 turns and drains 3 oil total.
  - `test_book_reading_grants_knowledge_flag` — flag is awarded upon completing third turn.
  - `test_book_reading_abort` — stepping away mid-read leaves knowledge unearned but preserves turns spent.
- **Commands:** `python -m pytest tests/test_old_library_rework.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Old Library content uses the multi-turn engine to require 3 turns for reading.
- [ ] Each turn expends lantern oil and updates narration atmospheric tension.
- [ ] Completing the read sets the required knowledge flag and notes the open door.
- [ ] Prose fits within the ≤ 20 line requirement.
- [ ] Automated tests verify the three-turn sequence.

## Rollback / Undo
Revert `old_library.json` to its previous vertical-slice state.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
