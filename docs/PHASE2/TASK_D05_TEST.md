# Task D05: Composure tests

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: D — Composure
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: D03, D04
- Blocks: F02, F04, I01
- Covers: AC-9, AC-10, AC-11
- Suggested commit: `test(composure): prove the cap, the tic, and the walk`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Close the slice's net on its three promises: composure is visible, distortion never leaves the last fifth and never lies silently, and zero nerve is a walk rather than a death.

## Non-Goals
- Does not repeat D01–D04's per-layer tests; those exist and must be green. This task asserts the slice's cross-cutting behaviour.
- Does not fix what it finds — a distortion leaking above its threshold or a tic missing is a bug in D02, reported under §4.2, not a boundary moved.
- Does not test Slices F–I. F02 and F04 will drain composure in rooms that do not exist yet; their own tests cover that.
- Does not re-litigate the values. Whether the drain is *well tuned* is a playtest judgement, not a test assertion; record observations in the log instead.

## Context & Constraints
- **Read first:** §3.2 in full (this slice's source), ASM-6 (the cap and the tic), RISK-4 in the epic (the highest-variance feature), and AC-10's and AC-11's wording in the coverage matrix — those two ACs are what this file exists to evidence.
- **Files to create:** `tests/test_composure_slice.py` (to be created).
- **Files to modify:** none.
- **Files to read, not modify:** `tests/test_composure_model.py` (D01), `tests/test_distortion.py` (D02), `tests/test_composure_floor.py` (D03), `tests/test_composure_ui.py` (D04); `game/composure.py`, `game/distortion.py`; the content; A13's traversal helper.
- **Conventions to respect:** A13's helper reuse and naming voice. Assertions over **all** rooms, not samples — RISK-4's failure mode is one room that distorts at the wrong threshold, which a sample would miss.
- **Design constraints — three slice-level promises, each asserted exhaustively:**
  - **The cap holds everywhere.** For every room in the content, walk composure from full to empty and assert the transform is the identity above the threshold and tic-bearing below it. Exhaustive, because a per-room exception is exactly the bug.
  - **The tic is never absent.** If any distorted line lacks its marker, the feature has become a lie. This is AC-10's teeth.
  - **Zero is not death.** Assert that reaching the floor produces the walk's terminal state and that no code path routes it to the death screen — and assert the two states are distinguishable in the run state, since I01 depends on that.
- **Voice:** the test names state §3.2's rules as claims, matching A13's style.

## Preconditions
- [ ] D03 and D04 DONE
- [ ] D01's and D02's tests green
- [ ] The content's room set is stable enough to iterate over exhaustively
- [ ] A13's traversal helper is available
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read the four D test modules and list what is already asserted, to avoid duplication.
2. Write `test_no_room_distorts_above_the_threshold` — exhaustive over every room, at several composure values above the band.
3. Write `test_every_distorted_line_in_every_room_carries_a_tic` — exhaustive, at values inside the band.
4. Write `test_choice_sets_are_identical_under_distortion_in_every_room` — ASM-6's boundary, at slice level.
5. Write `test_zero_composure_never_routes_to_the_death_screen` — the AC-11 assertion, over the whole flow.
6. Write `test_walk_and_death_are_distinguishable_in_the_run_state` — the I01 handoff.
7. Write `test_composure_is_visible_and_colour_independent` — the AC-9/§8 guard at slice level.
8. Write `test_a_clean_run_never_sees_distortion_or_the_walk` — the end-to-end avoidance check.
9. Run the suite twice for determinism, and record any tuning observation (too fast, too slow) in the log as a note rather than an assertion.

## Test Plan
- **Tests to write/update:** new `tests/test_composure_slice.py` (to be created) — the eight tests in steps 2–8.
- **Commands:** `python -m pytest tests/test_composure_slice.py -v`; then `python -m pytest -v` twice.
- **Manual verification:** one deliberate drain run and one clean run, confirming both ends of the slice's promise.
- **Negative check (mandatory, given RISK-4):** temporarily remove the tic from one distorted line and confirm step 3 fails, then revert. RISK-4 says this feature is the easiest in the phase to overdo — the equivalent risk is that its guard silently stops guarding.

## Definition of Done / Acceptance Criteria
- [ ] The cap is asserted exhaustively across all rooms, both sides
- [ ] Every distorted line carries a tic, asserted exhaustively
- [ ] Choice sets are identical under distortion in every room
- [ ] Zero composure never routes to the death screen
- [ ] The walk and the death are distinguishable in the run state, asserted for I01
- [ ] Composure information survives the loss of colour
- [ ] A clean run never encounters distortion or the walk
- [ ] The negative check was performed and observed failing before revert
- [ ] Tuning observations are recorded in the log, without being asserted
- [ ] `python -m pytest -v` passes deterministically, including A13's suite and Slices B/C tests

## Rollback / Undo
Revert this task's commit; the slice keeps working but loses its exhaustive guard, and RISK-4 — the phase's highest-variance feature — goes unguarded. F02, F04 and I01 expect this suite green; treat a revert as reopening the slice's verification.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the negative-check result and any tuning observation here -->
