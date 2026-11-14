# Task B05: "The Long Walk" and "Stay" narrative branch integration

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: B — The Multiple Endings Spectrum
- Layer: SVC
- Status: DONE
- Estimate: ~2.5h
- Depends on: B02
- Blocks: B06
- Covers: AC-5, AC-11, §2.3
- Suggested commit: `feat(content): wire The Long Walk and Stay narrative branches into room flow`
- Branch: feature/phase_3_the_shadow

## Objective
Integrate the two philosophical non-standard endings from `docs/SUGGEST.md` §2.3 into the game graph: "The Long Walk" (die in the Hall early) and "Stay" (refuse to leave at the final unlocked door).

## Non-Goals
- Does not change the standard front door key solution logic.
- Does not modify Hell Dog encounters.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.3:
  - *The Long Walk*: "Die in the first room — Failure, but the shadow respects you."
  - *Stay*: "Refuse to leave at the final door — The player chooses the house."
- **Files to modify:** `data/content.json`, `screens/game.py`.
- **Precedent:** In `data/content.json`, the front door exit choice in `hall` (`hall_front_door`) currently transitions to `front_door_escape`. We will add a choice at the threshold to turn back / refuse exit, and wire the early Hall demise to recognize `the_long_walk`.

## Preconditions
- [x] Task B02 DONE (`ending_resolver.py` ready).
- [x] Baseline tests passing.

## Actionable Steps
1. In `data/content.json`, at the front door exit threshold scene (`front_door_escape` or sub-choice), author a choice:
   - "Turn away from the night air and bolt the door from the inside" (refusal).
   - Destination: `ending_stay` (triggers `Stay` ending).
2. In `screens/game.py` (or death resolution in `screens/death.py`), when a fatal choice is taken in the first room (`hall`) on turn count <= 3:
   - Route to `the_long_walk` ending instead of a generic death screen, or offer an explicit "Accept the dark / Walk into the shadow" option that triggers `The Long Walk`.
3. Validate all choice requirements and effects in `content_schema.py`.

## Test Plan
- **Tests to write:** `tests/test_long_walk_and_stay.py`:
  - `test_early_hall_demise_triggers_the_long_walk`: Asserts early hall fatality routes to `the_long_walk`.
  - `test_front_door_refusal_triggers_stay`: Asserts choosing to bolt the door triggers `stay`.
- **Commands:** `python -m pytest tests/test_long_walk_and_stay.py -v`.

## Definition of Done / Acceptance Criteria
- [x] Both "The Long Walk" and "Stay" endings are accessible via natural narrative choices.
- [x] Choices are telegraphed fairly.
- [x] Tests pass cleanly with 0 errors.

## Rollback / Undo
Revert choice additions in `data/content.json` and `screens/game.py`.

## Execution Log
- 2026-11-11: Antigravity subagent wired "Stay" (`ending_stay`, `hall_front_door_stay`) and "The Long Walk" (`ending_long_walk`, `hall_accept_dark`, early hall death hook in `screens/death.py`) into content and screens.
- Verified with `tests/test_long_walk_and_stay.py`: 3/3 tests passing.
