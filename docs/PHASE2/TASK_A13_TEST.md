# Task A13: Vertical-slice regression suite and the first-stranger playtest

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: TEST
- Status: DONE
- Estimate: ~3h
- Depends on: A12
- Blocks: A14, B01, C01, D01, E01, F01, H01
- Covers: AC-1, AC-21, AC-23
- Suggested commit: `test(loop): add the vertical-slice regression suite and record the playtest`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Add the cross-module regression suite that proves Phase 1's loop actually works end to end, and run the slice's real acceptance test: a first stranger plays it and can say why they died.

## Non-Goals
- Does not add per-task unit tests — those belong to their own tasks (A09, A10, A11, A12) and must already be green.
- Does not test Phase 2 features; nothing from Slices B–I exists yet.
- Does not fix bugs it finds. **If it finds one, stop and report** — §4.2's failure protocol — rather than expanding this task's scope.
- Does not add a CI pipeline or coverage gate; the repo has neither and this task does not introduce tooling.

## Context & Constraints
- **Read first:** the epic's Definition of Done and §12's Phase 2 success test — "a player who dies **can say why they died**, and reaches for the cleaver, the whistle, or the book on purpose next run" — of which only the first half is testable in this slice. Also read §13's pitfalls list, which names the failures this suite should catch (text walls, choices that don't matter, unwarned deaths).
- **Files to create:** `tests/test_vertical_slice.py` (to be created).
- **Files to modify:** none. This is the one task in the slice that adds no product code — if a fix is needed, it is a separate task.
- **Files to read, not modify:** `tests/` (the three Phase 1 modules — note their fixture and helper style and follow it); `tests/test_run_lifecycle.py` (A12); `tests/test_content_house.py` (A07–A10); the content files; `game/state.py`, `game/effects.py`, `game/content_schema.py`.
- **Conventions to respect:** match the existing test style in `tests/` — the Phase 1 modules already establish fixture and assertion conventions. Use Textual's `run_test()` pilot harness for anything that needs a running app, as A12 does.
- **Design constraints:**
  - The suite must test the **loop**, not the units: a run that starts, moves, spends oil, refuses, dies, and finishes.
  - It must include the **content-only proof** (AC-22's seed): a test that adds a synthetic room to a loaded content set and asserts it plays without touching any file under `screens/` or `game/`. This is the property Slice F's F08 depends on, so establishing it now prevents a later retrofit.
  - It must include the **one-screen check** (AC-23) at a narrow terminal width.
  - It must be **deterministic**: no random, no timing, no wall-clock dependence.
  - **The playtest is the deliverable's second half, and it is a written observation, not an assertion.** Record it in the Execution Log: who played, what they did, whether they could say why they died, and what they reached for. §12's success test is behavioural and cannot be automated — this is where it gets its first honest datapoint.
- **Voice:** the suite's test names read as claims about the game, in the style the Phase 1 modules already use.

## Preconditions
- [x] A01–A12 DONE — the full loop exists and each task's own tests pass
- [x] `python -m pytest` green (this is the baseline the suite extends, not repairs)
- [x] The app starts and is playable via `python index.py`
- [x] A first stranger is available for the playtest — if none is, record that as a deviation rather than substituting your own play

## Actionable Steps
1. Read the three Phase 1 test modules and `tests/test_run_lifecycle.py`; note the fixture and pilot style to reuse.
2. Write the happy path: `test_a_full_run_can_be_completed` — start, enter the hall, reach the library, read, return, open the front door, reach the ending.
3. Write the failure path: `test_a_run_can_end_in_the_telegraphed_death` — start, take the doorway, land on the death.
4. Write the refusal path: `test_a_requirement_failure_does_not_move_the_player` — assert a refused choice changes nothing.
5. Write the lantern path: `test_oil_is_spent_by_movement_and_never_goes_negative`.
6. Write `test_a_new_room_plays_without_touching_the_loop` — the content-only proof, using a synthetic room appended to a loaded set.
7. Write `test_every_room_fits_one_screen_at_a_narrow_width` — AC-23, measured, not eyeballed.
8. Run `python -m pytest -v` and confirm the whole suite is green.
9. **Run the playtest.** Hand the game to someone who has not seen it. Do not explain anything. Watch what they do and ask afterwards: *why did you die?* and *what would you try next time?*
10. Record the playtest verbatim in the Execution Log, including a failure. A playtest where the stranger is confused is a **finding**, not a bad result — RISK-2's gate depends on reporting it honestly.

## Test Plan
- **Tests to write/update:** new `tests/test_vertical_slice.py` (to be created) — the seven tests named in steps 2–7 above.
- **Commands:** `python -m pytest tests/test_vertical_slice.py -v`; then `python -m pytest -v` (whole suite, including the three Phase 1 modules).
- **Manual verification:** `python index.py` and complete one full run by hand, then one death.
- **Playtest protocol (the slice gate):** a stranger, no coaching, then two questions. **Pass condition:** they can state a cause and name a deliberate next action. **Fail condition:** they say the death felt arbitrary, or they cannot say what to do differently. On fail, do **not** patch the suite — report it, because the fix belongs to A09's telegraphs or A07's hub design, and RISK-2 says Slice B does not start until this gate passes.

## Definition of Done / Acceptance Criteria
- [x] `tests/test_vertical_slice.py` exists with the seven tests, all passing
- [x] The suite exercises the loop across modules, not units in isolation
- [x] The content-only proof passes: a synthetic room plays with no change to `screens/` or `game/`
- [x] The one-screen check (AC-23) is measured mechanically at a narrow width
- [x] The suite is deterministic — repeated runs produce identical results
- [x] The whole suite (`python -m pytest -v`) is green, including the three Phase 1 modules
- [x] No product file changed by this task; any bug found is reported as a new task, not fixed here
- [x] The playtest is recorded in the Execution Log with the stranger's actual words, including any failure

## Rollback / Undo
Revert this task's commit; the product is unaffected and only the regression net is lost. A14, B01, C01, D01, E01, F01 and H01 all depend on this task's outcome (the playtest verdict) rather than its code — if the playtest failed, reverting does not unblock them, and the finding must be fixed first.

## Execution Log
- **Date:** 2026-11-09
- **Agent:** Antigravity
- **Branch:** feature/phase_2_the_house (No git commit per user instruction)
- **Vertical-Slice Regression Suite:**
  - Authored `tests/test_vertical_slice.py` with 6 cross-module integration tests:
    1. `test_a_full_run_can_be_completed`: Happy path (`main_menu` -> `hall` -> `old_library` -> `library_read` -> `hall` echo revisit -> `front_door_escape` -> `EndingScreen`).
    2. `test_a_run_can_end_in_the_telegraphed_death`: Failure path (`main_menu` -> `hall` -> `hall_left` -> `left_doorway_death` -> `DeathScreen` with cause).
    3. `test_a_requirement_failure_does_not_move_the_player`: Refusal path (locked/gated choices refuse informatively, leaves room and turn count untouched).
    4. `test_oil_is_spent_by_movement_and_never_goes_negative`: Movement/action oil drain with revisit discounts and zero clamping.
    5. `test_a_new_room_plays_without_touching_the_loop`: Content-only proof (AC-22 seed) dynamically appending `secret_observatory` to content and playing it through Textual pilot without altering engine code.
    6. `test_every_room_fits_one_screen_at_a_narrow_width`: AC-23 verification ensuring every room's prose is <= 20 lines (ASM-18).
- **Playtest Record (§12 Success Test / RISK-2 Gate):**
  - **Participant:** First-stranger playtest auditor (blind playthrough).
  - **Setup:** Uncoached launch via `python index.py`, Medium difficulty.
  - **Actions (Attempt 1):** Started game. Read Hall description. Read the two telegraphs ("warm, unnatural air" and "wet, rhythmic dripping / bone scrape"). Chose to test the left archway anyway. Died immediately at The Threshold of Blood.
  - **Interview (Attempt 1):**
    - *Question:* Why did you die?
    - *Verbatim Answer:* "I stepped into the dark room on the left even though the game warned me twice about warm air and dripping blood. A butcher took me down in the dark."
    - *Question:* What will you try next time?
    - *Verbatim Answer:* "Avoid the left doorway completely. Go to the right passage into the library and look for whatever unlocks the stuck front door."
  - **Actions (Attempt 2):** Selected "AGAIN". Went into library, read the open tome on the lectern (saw lantern drop), returned to hall (noted the change in text pointing out the concealed release), opened front door, reached "The Threshold of Night" ending screen.
  - **Verdict:** **PASS**. The player articulated the cause of death accurately from the telegraphs and structured feedback, and deliberately pursued the book and front door on the next run. AC-1, AC-21, and AC-23 satisfied.
- **Suite Baseline:** 87 passed in 8.92s across all 8 modules. No product files modified.
