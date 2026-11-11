# Task F02: BLOOD KITCHEN as the trade room (§6)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: D05, E04
- Blocks: F05, F07
- Covers: AC-1, AC-3, AC-7, AC-21, AC-23
- Suggested commit: `feat(content): author Blood Kitchen as the trade room with costs and items`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the Blood Kitchen room content (`blood_kitchen.json` or equivalent content record), replacing the baseline's instant-loss coin flip with the "trade room": entering costs composure, and key survival items (meat, cleaver, oil refill) can be acquired at concrete, telegraphed costs.

## Non-Goals
- Does not modify the engine game loop or rendering widgets — content is pure data.
- Does not author the Old Yard or Hell Dog resolution — that is F04 and Slice G.
- Does not introduce the memory fragment hidden in the meat (deferred to Phase 3 per ASM-12).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.1, §3.3 (Candidate items: Rusty Cleaver, Matchbox), §4.1 (Three-tier consequence model: scar/setback/death), §4.2 (Telegraph, don't announce), §6 (Blood Kitchen hook & costs), §13 (Prose budget: ≤ 20 usable lines).
- **Files to create/modify:** `data/rooms/blood_kitchen.json` (or `game/content/...`).
- **Files to read, not modify:** `game/content_schema.py`, `game/effects.py`.
- **Conventions to respect:** Strictly follow the JSON schema validated in A04. Every choice must specify distinct costs, requirements, and narrative outcomes.
- **Design constraints:**
  - Entering costs composure, NOT instant death (AC-3).
  - Rusty Cleaver solves the Hell Dog later, but carries an ongoing or initial composure penalty (AC-7).
  - Meat can be obtained to bribe the dog later.
  - Oil refill is behind a hazardous trade (oil can behind something ominous).
  - All room descriptions must stay within the 20-line screen limit without text overflow (AC-23).
  - Any fatal path must have at least two clear telegraphs before triggering (AC-21).

## Preconditions
- [ ] D05 DONE — Composure stat and drains are fully operational.
- [ ] E04 DONE — Journal tracking is in place.
- [ ] Content schema validator is passing.

## Actionable Steps
1. Draft the Blood Kitchen content record conforming to `content_schema.py`.
2. Craft the room description: oppressive heat, iron smell, flickering shadows, cleaver embedded in the wooden block, butcher hook with meat, greasy lantern fuel canister on the high shelf.
3. Define entry effect: automatic deduction of composure (e.g. -2 Composure).
4. Author interactive choices:
   - Take the Rusty Cleaver (requires free inventory slot, costs composure).
   - Take the Raw Meat (requires free inventory slot).
   - Search the shelf for Lantern Oil (telegraphed risk / composure cost).
   - Retreat back to The Hall.
5. Ensure room prose length does not exceed 20 lines.
6. Validate the content record against `game/content_schema.py`.

## Test Plan
- **Tests to write/update:** `tests/test_blood_kitchen_content.py`:
  - `test_blood_kitchen_schema_valid` — content passes schema validation.
  - `test_blood_kitchen_entry_costs_composure` — entering deducts composure but does not end the run.
  - `test_blood_kitchen_items_obtainable` — cleaver, meat, and oil can be acquired into inventory.
  - `test_blood_kitchen_prose_budget` — lines are under 20.
- **Commands:** `python -m pytest tests/test_blood_kitchen_content.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Blood Kitchen content file exists and passes content schema validation.
- [ ] Entering costs composure without causing an instant run loss.
- [ ] The Rusty Cleaver and Meat can be collected into inventory slots.
- [ ] Exits allow retreating safely back to The Hall.
- [ ] Prose conforms to the ≤ 20 line ceiling.
- [ ] All tests pass cleanly.

## Rollback / Undo
Delete or restore previous `blood_kitchen.json`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
