# Task F08: Full-house validation: prices, reachability, prose budget

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: TEST
- Status: DONE
- Estimate: ~3h
- Depends on: F06, F07
- Blocks: G01
- Covers: AC-1, AC-21, AC-22, AC-23
- Suggested commit: `test(content): validate full-house graph reachability, prices, and line budgets`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Implement an automated validator and end-to-end test suite for all four house rooms (The Hall, Blood Kitchen, Old Library, Old Yard) that mechanically verifies graph reachability, resource economy (oil and composure costs), two-telegraph death safety, and strict compliance with the 20-line prose budget.

## Non-Goals
- Does not test the Hell Dog encounter mechanics (that is Slice G).
- Does not test save/load disk persistence (that is Slice I).

## Context & Constraints
- **Read first:** `EPIC_Phase2_TheHouse_PLAN.md` AC-1, AC-21, AC-22, AC-23; `docs/SUGGEST.md` §13 ("No text walls: every room fits one screen"), §4.1 (Consequence tiers).
- **Files to create or expand:** `tests/test_house_content_validation.py`.
- **Files to read, not modify:** All room JSON records in `data/rooms/`, `game/content_schema.py`.
- **Conventions to respect:** Mechanically iterate through every room and choice in the content graph. Fail if any room exceeds 20 usable lines, has dead-end inescapable cycles (without intent), has untelegraphed deaths, or broken reference links.

## Preconditions
- [ ] Tasks F01 through F07 are DONE.
- [ ] All four baseline rooms and item routes are authored.

## Actionable Steps
1. Create `tests/test_house_content_validation.py`.
2. Write validation rule: **Graph Reachability & Acyclicity**:
   - Assert that every room is reachable from The Hall.
   - Assert that every room has at least one valid transition back or onward.
3. Write validation rule: **Prose Budget Check** (AC-23):
   - Measure lines of text for every room description and state variation.
   - Assert that line counts do not exceed 20 lines.
4. Write validation rule: **Two-Telegraph Death Rule** (AC-21):
   - Trace all paths leading to a death terminal state.
   - Assert that every fatal node has at least two antecedent warning nodes/messages.
5. Write validation rule: **Resource Economy Feasibility**:
   - Verify that it is mathematically possible to complete the minimum viable run within default starting oil and composure reserves.
6. Verify the Content-Only Proof (AC-22): adding an arbitrary room content record requires zero engine code alterations.

## Test Plan
- **Commands:** `python -m pytest tests/test_house_content_validation.py -v`.
- **Manual verification:** Step through room transitions in the interactive game and inspect screen formatting.

## Definition of Done / Acceptance Criteria
- [ ] All four house rooms validate cleanly against the structural schema.
- [ ] Graph validator confirms 100% room reachability from The Hall.
- [ ] No room or choice prose exceeds 20 usable terminal lines.
- [ ] Every lethal outcome is proven to have at least two preceding telegraphs.
- [ ] Test suite runs completely green.

## Rollback / Undo
Delete `tests/test_house_content_validation.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
