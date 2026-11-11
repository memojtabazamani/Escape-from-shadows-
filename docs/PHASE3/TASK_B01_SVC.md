# Task B01: Content authoring for the 7 canonical endings in `data/content.json`

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: B — The Multiple Endings Spectrum
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: A02
- Blocks: B02, B03
- Covers: AC-4, AC-5, AC-6, AC-7, AC-8, AC-9, AC-10, AC-11, §2.3
- Suggested commit: `feat(content): author narrative prose for all 7 canonical endings`
- Branch: feature/phase_3_the_shadow

## Objective
Author the high-atmosphere narrative prose and room/destination records for all 7 canonical endings in `data/content.json` per `docs/SUGGEST.md` §2.3, adhering strictly to the 20-line prose budget and tone table.

## Non-Goals
- Does not implement condition checking engine (handled in B02).
- Does not create ASCII art artboards (handled in B03).
- Does not alter existing intermediate rooms unless linking exit endpoints.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.3 (The 7 Endings table and tones):
  1. `the_long_walk` — Die in first room / Hall. Failure, but the shadow respects you.
  2. `meat_and_silence` — Feed Hell Dog and escape. Ugly survival.
  3. `the_quiet_exit` — Leave through front door with key. Standard win.
  4. `what_the_book_knew` — Read the book *and* escape. Best "true" ending.
  5. `the_new_shadow` — Escape with lantern empty. Something came with you.
  6. `homecoming` — Collect all 3 memory fragments and escape. Recontextualizes the house.
  7. `stay` — Refuse to leave at the final door. Player chooses the house.
- **Files to modify:** `data/content.json`.
- **Constraint:** Each ending must fit a single terminal screen without scrolling (prose budget <= 20 lines).

## Preconditions
- [ ] Task A02 DONE (endings schema defined).
- [ ] Working tree clean and content schema validator passing.

## Actionable Steps
1. In `data/content.json`, add an `endings` dictionary or terminal room definitions for each of the 7 endings:
   - `the_long_walk`: "You fell where you first stood. The darkness steps over you gently. It does not gloat. You were brave enough to open your eyes."
   - `meat_and_silence`: "The cold bone grease coats your palms. Behind you, wet mastication fills the yard. You survived, but the sound will never leave your ears."
   - `the_quiet_exit`: "The iron key turns with a dry snap. The night air hits your lungs like ice. You walk down the gravel drive and do not look back."
   - `what_the_book_knew`: "The lock yields to your whispered word. The house cannot hold what has read its marrow. You step out under stars you finally understand."
   - `the_new_shadow`: "The door opened into total blackness. You ran until your feet hit grass. The lantern was dead. You cast two shadows in the moonlight."
   - `homecoming`: "The photograph. The child's hand. The date stamped tomorrow. This was never a prison; it was a home you abandoned. The front door dissolves into dawn."
   - `stay`: "The night outside is vast, cold, and empty. You reach out and pull the iron door shut from the inside. The lock clicks. You are home."
2. Define metadata on each ending: `id`, `name`, `tone`, `prose`, `terminal_type: "victory" | "death" | "choice"`.
3. Validate `data/content.json` against `game/content_schema.py`.

## Test Plan
- **Tests to write:** `tests/test_endings_content.py`:
  - `test_all_seven_endings_present_in_content`: Asserts all 7 canonical IDs exist in content.
  - `test_endings_prose_budget_under_limit`: Asserts no ending prose exceeds 20 lines.
  - `test_endings_schema_validation`: Validates content file through `validate_content()`.
- **Commands:** `python -m pytest tests/test_endings_content.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] All 7 endings authored with prose matching the philosophical tone in §2.3.
- [ ] Content conforms to `content_schema.py`.
- [ ] All prose fits the terminal budget.
- [ ] Tests pass cleanly.

## Rollback / Undo
Revert additions to `data/content.json`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
