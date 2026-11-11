# Task E04: Player history recording and Shadow dialogue tests

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: E — Player History & Shadow Voice
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: E03
- Blocks: G01
- Covers: AC-19, AC-20, AC-21, §2.2, §3.4
- Suggested commit: `test(shadow): test history tracking, whisper generation, and journal recording`
- Branch: feature/phase_3_the_shadow

## Objective
Author a targeted automated test suite in `tests/test_shadow_voice_suite.py` asserting that player choices are faithfully logged across gameplay, that the dialogue engine generates responsive second-person whispers, and that bell cues and journal entries fire accurately.

## Non-Goals
- Does not test visual color grammar (covered in Slice F).
- Does not test ending resolution (covered in Slice B).

## Context & Constraints
- **Read first:** `game/state.py`, `game/shadow_dialogue.py`, `game/journal.py`, `screens/game.py`.
- **Files to create:** `tests/test_shadow_voice_suite.py`.

## Preconditions
- [ ] Tasks E01–E03 complete.
- [ ] Working tree clean.

## Actionable Steps
1. Create `tests/test_shadow_voice_suite.py`.
2. Test choice logging:
   - Perform sequential choices in a simulated run.
   - Assert `state.choice_history` contains expected action tags and timestamps.
3. Test dialogue generation:
   - Provide historical actions and verify dialogue reflects those specific deeds.
   - Verify second-person perspective invariant ("You ...").
4. Test journal and sound integration:
   - Verify whisper logs to `Journal.whispers`.
   - Verify `play_cue` invoked without exceptions even when sound setting is False.

## Test Plan
- **Commands:** `python -m pytest tests/test_shadow_voice_suite.py -v`.
- **Assertions:** All voice generation and journal recording tests pass.

## Definition of Done / Acceptance Criteria
- [ ] Full coverage of history tracking and Shadow voice mechanics.
- [ ] Invariants verified: second-person only, journal logging, sound safe.
- [ ] 100% test pass rate.

## Rollback / Undo
Delete `tests/test_shadow_voice_suite.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
