# Task H04: Presentation toggle tests

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: H — Sound & Music Made Real
- Layer: TEST
- Status: DONE
- Estimate: ~2.5h
- Depends on: H01, H03
- Blocks: None (Slice H terminal verification)
- Covers: AC-18, AC-19, AC-24
- Suggested commit: `test(presentation): tests for Sound and Music toggles producing observable differences`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author an automated test suite verifying that toggling `Sound` and `Music` in `config.py` produces verifiable, observable behavioral differences in the presentation layer (AC-18, AC-19, AC-24), proving that the settings no longer lie.

## Non-Goals
- Does not test gameplay logic or room content correctness.
- Does not test hardware audio device drivers.

## Context & Constraints
- **Read first:** `EPIC_Phase2_TheHouse_PLAN.md` AC-18, AC-19, AC-24 ("No setting lies: every menu toggle changes observable behaviour").
- **Files to create:** `tests/test_presentation_toggles.py`.
- **Files to read, not modify:** `game/sound.py`, `screens/game.py`, `config.py`.
- **Conventions to respect:** Use `pytest` to assert differences under both configuration states.

## Preconditions
- [ ] H01 and H03 are DONE.
- [ ] Working tree clean and existing tests green.

## Actionable Steps
1. Create `tests/test_presentation_toggles.py`.
2. Write tests for `Sound` toggle:
   - When `sound=True`, invoking sound cues emits system bell.
   - When `sound=False`, invoking sound cues emits zero bells.
   - Asserts the game remains 100% playable and non-crashing with sound disabled.
3. Write tests for `Music` toggle:
   - When `music=True`, typewriter animation timer is registered.
   - When `music=False`, prose is delivered in a single immediate assignment with zero timers.
4. Verify that neither toggle breaks room transitions or player input responsiveness.
5. Execute full test suite and confirm 100% green.

## Test Plan
- **Commands:** `python -m pytest tests/test_presentation_toggles.py -v`.
- **Manual verification:** Run `python index.py`, go to Settings, toggle Sound and Music OFF, start game and verify instant prose and silence; toggle ON and verify typewriter and bell.

## Definition of Done / Acceptance Criteria
- [ ] Test verifies Sound toggle creates an observable audio difference.
- [ ] Test verifies Music toggle creates an observable animation difference.
- [ ] Zero settings lie: every setting toggle is proven to change runtime behavior (AC-24).
- [ ] All tests pass cleanly.

## Rollback / Undo
Delete `tests/test_presentation_toggles.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
