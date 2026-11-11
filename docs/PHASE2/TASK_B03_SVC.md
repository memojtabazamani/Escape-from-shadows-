# Task B03: Mercy knobs — restart point and journal auto-fill

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: B — Difficulty as a Real System
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: B02
- Blocks: B06, I04
- Covers: AC-16, AC-17
- Suggested commit: `feat(difficulty): add the restart and journal mercy knobs`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Give difficulty its two mercy mechanisms: where a restart begins, and whether death fills the journal for you — so EASY forgives, HARD does not, and MEDIUM does neither gratuitously.

## Non-Goals
- Does not implement the death screen itself — A11 built it, and **I03 gives it the "what you learned" line.** This task decides *what that line is allowed to say*; I03 renders it, I04 gates the harder hint.
- Does not author the journal model — that is E01. This task defines the mercy *parameter* and the interface E02 calls; it does not store entries.
- Does not implement hints — that is B04, which is about *reaching* an answer; this is about *keeping* one after failure.
- Does not implement save/load — that is Slice I. Restart points are in-memory within a session, not a save file.

## Context & Constraints
- **Read first:** §5.1's mercy bullet and its caveat ("HARD removes safety nets, not fairness"), §9.2's four-part death screen (this task supplies the content of parts two and three), §3.4's journal rules, and §13's "make death a lesson" pillar — pillar 2, "Every death is a lesson," is the design justification for auto-fill existing at all.
- **Files to modify:** `game/difficulty.py` (the mercy parameters); the run-lifecycle path in `index.py` or the gameplay screen's restart handler (A11/A12) for the restart point.
- **Files to read, not modify:** `game/state.py` — `RunState` has no concept of a checkpoint, so the restart point must be expressed as a *fresh run from a recorded room*, not as a state snapshot; `game/effects.py`; `screens/death.py` (A11) — its "Again" action is the hook.
- **Conventions to respect:** the state-lives-in-files discipline the skill applies to plans applies here to runs: the restart point is recorded data on the run, not a hidden screen variable.
- **Design constraints — mercy is where difficulty is easiest to get wrong:**
  - **HARD's mercy is zero, but never negative.** HARD must not remove the journal's *ability* to record (that is E01's job and content-neutral); it removes the *free* recording. A player on HARD can still learn, by paying attention.
  - **The restart point must not skip content.** Restarting at a later room is mercy; restarting *past* the lesson is not. The recorded room must be one the player has actually reached.
  - **Auto-fill must be honest.** If EASY records what killed you, it records the true cause — the same string A11 renders. Auto-fill that records a generic entry is worse than none.
  - **Mercy is a parameter, not a branch at the call site.** The death handler asks the config, it does not ask `if difficulty == "EASY"`. B06 tests this.
  - **Restart must interact correctly with A12's "Back to menu".** A death's two actions now differ: "Again" may resume from the restart point, "Back to menu" discards. Decide and record which, and make sure I02 (save/load) can still assert "a death leaves nothing resumable" — if "Again" creates a resumable point, that must be in-memory only, and say so.
- **Voice:** mercy reads as the house being patient with you, not as a difficulty label. The journal entries EASY fills should read like the Shadow's own summary, since §3.4 already attributes journal lines to it.

## Preconditions
- [ ] B02 DONE — the bar generosity parameters exist, so the config has a mercy group to extend
- [ ] A11 DONE — the death screen exists with its two actions
- [ ] The journal interface from E01 is available, or E01 has not yet started and this task defines the call it will implement
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read A11's death screen and identify the exact hook its "Again" action calls.
2. Add the mercy parameters to `game/difficulty.py`: a restart-point mode and a journal-auto-fill flag, each named for its effect.
3. Define what the restart point *is* — a room id recorded on the run at each first visit, or at designated safe rooms — and record the choice. Prefer the simpler one that cannot skip content.
4. Implement the restart path: "Again" consults the config, and either restarts at the recorded room or at the beginning.
5. Implement the auto-fill call: on death, ask the config; if mercy is on, write the true cause into the journal through E01's interface.
6. Ensure the auto-filled entry uses the same cause string the death screen renders — one source, not two.
7. Decide and record whether "Again" produces anything I02 could resume, and make the answer true.
8. Verify HARD leaves the journal able to record by other means — a player who survived something can still write it down.

## Test Plan
- **Tests to write/update:** new `tests/test_difficulty_mercy.py` (to be created):
  - `test_easy_restarts_at_the_recorded_room_and_hard_restarts_at_the_beginning` — the mercy difference, asserted in both directions.
  - `test_auto_fill_is_off_on_hard_and_on_for_easy` — asserts the parameter is consulted, not assumed.
  - `test_auto_filled_entry_matches_the_death_cause_exactly` — the honesty guard; catches a divergence between the screen and the journal.
  - `test_restart_point_is_always_a_room_the_player_reached` — guards against mercy skipping content.
  - `test_mercy_is_read_from_config_not_branched_on_the_string` — a source-level guard, in the spirit of B01's seam test.
- **Commands:** `python -m pytest tests/test_difficulty_mercy.py -v`; then `python -m pytest -v`.
- **Manual verification:** die on EASY and on HARD; confirm EASY resumes somewhere sensible and HARD returns you to the start, and that only EASY's journal already contains the cause.
- **Content-skip check:** on EASY, restart and confirm you did not arrive somewhere you had never been.

## Definition of Done / Acceptance Criteria
- [x] The config's mercy parameters exist and are read from config, never from a difficulty string
- [x] EASY restarts at a reachable recorded room; HARD restarts at the beginning; MEDIUM's behaviour is decided and recorded
- [x] Journal auto-fill is on for EASY and off for HARD, and the recorded text is the true cause
- [x] The auto-filled text and the death screen's cause come from one source
- [x] The restart point can never be a room the player has not visited
- [x] HARD does not remove the journal's ability to record by other means
- [x] The interaction with "Back to menu" and with I02's "nothing resumable" property is decided and recorded
- [x] `python -m pytest -v` passes, including the three pre-existing modules and A13's suite

## Rollback / Undo
Revert this task's commit; difficulty stops affecting mercy and the death screen's "Again" returns to a plain restart. I04 depends on the "what you could have done" gating this task establishes — revert as a group if I04 has landed.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the restart-point design, MEDIUM's mercy behaviour, and the resumability decision here -->
