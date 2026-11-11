# Task C03: "Homecoming" secret ending integration and criteria validation

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: C — The Three Memory Fragments
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: C02, B02
- Blocks: C04
- Covers: AC-10, §2.3, §2.4
- Suggested commit: `feat(ending): wire Homecoming secret ending when all 3 memory fragments collected`
- Branch: feature/phase_3_the_shadow

## Objective
Integrate the secret ending **Homecoming** into the ending resolution engine and screen flow, asserting that a player escaping with all 3 memory fragments held unlocks this highest-tier realization ending.

## Non-Goals
- Does not modify other ending condition checks.
- Does not make memory fragments easier to find.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.3 ("Homecoming: Find all three memory fragments — Secret ending, recontextualizes the house"), `game/ending_resolver.py`.
- **Files to modify:** `game/ending_resolver.py`, `screens/ending.py`.

## Preconditions
- [ ] Task C02 DONE (fragments obtainable in content).
- [ ] Task B02 DONE (`game/ending_resolver.py` available).

## Actionable Steps
1. In `game/ending_resolver.py`, update `resolve_escape_ending()`:
   - If `state.has_all_memory_fragments` is True (or all 3 fragment IDs in `state.held_items` / `state.memory_fragments`), resolve to `"homecoming"`.
   - Ensure `"homecoming"` takes precedence over `"the_quiet_exit"`, `"what_the_book_knew"`, and `"the_new_shadow"`.
2. In `data/content.json`, verify `ending_homecoming` record is defined and wired to `EndingMetadata`.
3. In `screens/ending.py`, verify `ending_id == "homecoming"` displays the dedicated prose and triggers profile unlock.

## Test Plan
- **Tests to write:** `tests/test_homecoming_ending.py`:
  - `test_escaping_with_three_fragments_triggers_homecoming`: Full fragment set yields "homecoming".
  - `test_escaping_with_two_fragments_does_not_trigger_homecoming`: Partial set falls back to book or quiet exit.
  - `test_homecoming_recorded_in_profile`: Asserts "homecoming" is stored in `PlayerProfile`.
- **Commands:** `python -m pytest tests/test_homecoming_ending.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] "Homecoming" ending reliably triggers only when all 3 fragments are obtained.
- [ ] It takes correct precedence over standard victory outcomes.
- [ ] Tests in `tests/test_homecoming_ending.py` pass.

## Rollback / Undo
Revert edits to `game/ending_resolver.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
