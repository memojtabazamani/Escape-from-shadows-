# Task E04: Journal tests

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: E — The Journal
- Layer: TEST
- Status: DONE
- Estimate: ~2.5h
- Depends on: E02, E03
- Blocks: F02, F04, I01
- Covers: AC-12
- Suggested commit: `test(journal): end-to-end unit and integration tests for journal system`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Provide comprehensive test coverage across the entire Journal slice (data model, automatic event triggers, snapshot serialization, and UI overlay rendering) to ensure zero regressions and unblock Slices F and I.

## Non-Goals
- Does not test persistence to disk across app reboots — that is I05.
- Does not test full content rooms from Slice F (Blood Kitchen, Old Yard) — it verifies journal behavior with available rooms and mock events.

## Context & Constraints
- **Read first:** `EPIC_Phase2_TheHouse_PLAN.md` AC-12, `docs/SUGGEST.md` §3.4.
- **Files to create or expand:** `tests/test_journal_suite.py` (or consolidate existing journal test files).
- **Files to read, not modify:** `game/journal.py`, `game/state.py`, `screens/game.py`, `screens/journal.py`.
- **Conventions to respect:** Use `pytest` and `textual.pilot` (for async UI testing if feasible) or mock screen harness. Assert behavioral outcomes without brittle UI coupling.

## Preconditions
- [ ] E01, E02, and E03 DONE.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. Create `tests/test_journal_suite.py`.
2. Write unit tests for `Journal` collection methods:
   - Category filtering (`ROOM_DISCOVERY`, `DEATH_LESSON`, `SHADOW_WHISPER`).
   - Deduplication handling and idempotency.
   - Snapshot serialization and restoration integrity.
3. Write integration tests for event hooking:
   - Navigating between rooms registers room entries.
   - Dying logs the corresponding lesson into the journal.
4. Write UI mount tests:
   - `JournalScreen` mounts and displays entries properly.
   - Empty state renders gracefully.
   - Keybind opens and closes without corrupting active game state.
5. Execute full test suite and confirm 100% green pass rate.

## Test Plan
- **Commands:**
  - `python -m pytest tests/test_journal_suite.py -v`
  - `python -m pytest -v`
- **Manual verification:** Run `python index.py`, trigger a room transition and check the journal, trigger a death, restart run, and verify behavior.

## Definition of Done / Acceptance Criteria
- [ ] All journal unit and integration tests pass without warnings or errors.
- [ ] Snapshot round-trip maintains 100% data fidelity.
- [ ] Re-entering rooms does not produce redundant duplicate logs.
- [ ] All tests run cleanly in `pytest`.

## Rollback / Undo
Delete `tests/test_journal_suite.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
