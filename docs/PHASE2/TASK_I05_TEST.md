# Task I05: Save/load round-trip and death-screen tests

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: I — Persistence & Mercy
- Layer: TEST
- Status: DONE
- Estimate: ~2.5h
- Depends on: I02, I04
- Blocks: None (Slice I terminal verification / Epic DoD)
- Covers: AC-15, AC-16, AC-20
- Suggested commit: `test(persistence): comprehensive suite for save-load roundtrip and respectful death screen`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the terminal integration test suite for Slice I, verifying that active runs survive application quit and restart with 100% fidelity, that death purges save data safely, and that the death screen delivers cause, lesson, and difficulty-appropriate guidance cleanly.

## Non-Goals
- Does not test cloud persistence or multi-user access.
- Does not test unrelated room content data.

## Context & Constraints
- **Read first:** `EPIC_Phase2_TheHouse_PLAN.md` AC-15, AC-16, AC-20, §9.1, §9.2.
- **Files to create:** `tests/test_persistence_suite.py`.
- **Files to read, not modify:** `game/save.py`, `screens/death.py`, `screens/main_menu.py`, `game/state.py`.
- **Conventions to respect:** Use `pytest` and temporary directories (`tmp_path`) for disk operations so tests do not touch actual user save files.

## Preconditions
- [ ] Tasks I01, I02, I03, and I04 are DONE.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. Create `tests/test_persistence_suite.py`.
2. Write tests for save/load round-trip using `tmp_path`:
   - Initialize complex `RunState` with custom room, oil, composure, inventory items, journal entries, and turn count.
   - Save to disk via `save_to_disk()`.
   - Reconstitute state via `load_from_disk()`.
   - Assert all fields and child data structures match the pre-save state identically (AC-20).
3. Write tests for save lifecycle:
   - Death event invokes `delete_saved_game()` and confirms file absence.
   - Victory event invokes `delete_saved_game()` and confirms file absence.
4. Write tests for Death Screen formatting:
   - Verifies cause string is rendered.
   - Verifies lesson string is rendered (AC-15).
   - Verifies hint is present on EASY and suppressed on MEDIUM and HARD (AC-16).
5. Run full test suite and confirm green.

## Test Plan
- **Commands:** `python -m pytest tests/test_persistence_suite.py -v`.
- **Manual verification:** Run `python index.py`, start game, pick up an item, quit to menu, select Continue, confirm item and room retained. Die intentionally and confirm Continue is removed from menu.

## Definition of Done / Acceptance Criteria
- [ ] Save/load round-trip retains 100% state fidelity with passing automated tests.
- [ ] Save file is purged automatically upon run completion or death.
- [ ] Death screen cause, lesson, and difficulty hint logic are verified by tests.
- [ ] All tests pass without warnings or regressions.

## Rollback / Undo
Delete `tests/test_persistence_suite.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
