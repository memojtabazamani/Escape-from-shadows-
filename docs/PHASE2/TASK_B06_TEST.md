# Task B06: Difficulty behaviour tests

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: B — Difficulty as a Real System
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: B03, B04, B05
- Blocks: None
- Covers: AC-16, AC-17, AC-24
- Suggested commit: `test(difficulty): prove difficulty changes outcomes without gating content`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Prove the two claims §5.1 makes and the epic's Definition of Done repeats: difficulty **does** change observable outcomes on all three settings, and difficulty **never** gates content.

## Non-Goals
- Does not write the per-feature tests — B02, B03, B04 and B05 each own theirs and must be green already. This task writes the **cross-cutting** assertions that no single feature task can make.
- Does not fix what it finds. If a difficulty gates content, that is a **design bug in B02–B05** — report it under §4.2 rather than loosening the assertion. RISK-5 exists precisely because this test is the kind that gets weakened to pass.
- Does not test Slices C–I; those arrive later with their own tests.
- Does not add coverage tooling.

## Context & Constraints
- **Read first:** §5.1 in full — both the rule and the caveat, which are the two assertions this task encodes — plus RISK-5 in the epic ("Difficulty becomes a difficulty-flavoured story branch... because it is easier to gate content than to tune mercy") and ASM-14. Also re-read §13's "no setting lies" pitfall, which AC-24 turns into the third assertion here.
- **Files to create:** `tests/test_difficulty_invariants.py` (to be created).
- **Files to modify:** none.
- **Files to read, not modify:** `tests/test_difficulty_config.py` (B01), `tests/test_difficulty_bars.py` (B02), `tests/test_difficulty_mercy.py` (B03), `tests/test_difficulty_hints.py` (B04), `tests/test_difficulty_pressure.py` (B05); `game/difficulty.py`; the content set; `tests/test_vertical_slice.py` (A13) — its content-only proof is a sibling of the reachability proof written here.
- **Conventions to respect:** the existing `tests/` style and A13's naming voice — test names read as claims about the game.
- **Design constraints — three invariants, and the third is the one that is usually forgotten:**
  - **Invariant 1 — reachability is difficulty-independent.** The set of reachable rooms, obtainable items, and available solutions is *identical* on EASY, MEDIUM and HARD. Compute the sets from the content by traversal rather than by hand, so adding a room later cannot silently break the claim.
  - **Invariant 2 — outcomes are difficulty-dependent.** Something observable differs on each setting: at minimum the starting oil, the mercy behaviour, the hint presence, and the pressure cue. A difficulty that changes nothing is a setting that lies.
  - **Invariant 3 — MEDIUM is the identity.** MEDIUM's numbers equal the pre-Slice-B values, so the baseline the rest of the phases balance against has not moved. This is easy to lose across four B tasks and is the reason this assertion lives here, once.
  - Use the same traversal helper for all three difficulties, so a bug in the helper cannot make the invariant pass.
- **Voice:** these tests are the epic's argument with itself — the place where "difficulty is real" and "difficulty is fair" are checked in the same file.

## Preconditions
- [ ] B03, B04, B05 DONE
- [ ] B01's and B02's tests green
- [ ] The content set is stable — its room, item and solution ids are settled for this slice
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `game/difficulty.py` and the four B test modules; list every parameter and every behaviour already asserted.
2. Write the traversal helper: given a content set and a config, compute the reachable room ids, obtainable item ids, and available solution ids.
3. Write `test_reachable_content_is_identical_on_easy_medium_and_hard` — Invariant 1.
4. Write `test_every_difficulty_changes_something_observable` — Invariant 2, listing the four observable axes explicitly.
5. Write `test_medium_is_the_identity_config` — Invariant 3, comparing MEDIUM against the recorded pre-slice numbers.
6. Write `test_no_parameter_carries_a_content_identifier` — the ASM-14 structural guard, so a future field cannot smuggle a gate in.
7. Write `test_every_setting_toggle_has_an_observable_effect` — AC-24's seed for this slice. `sound` and `music` are still inert at this point; assert what is true now and mark the remaining two as the H04 handoff in a comment.
8. Run the whole suite. **If Invariant 1 fails, stop and report** — do not adjust the traversal to make it pass.

## Test Plan
- **Tests to write/update:** new `tests/test_difficulty_invariants.py` (to be created) — the six tests in steps 3–7.
- **Commands:** `python -m pytest tests/test_difficulty_invariants.py -v`; then `python -m pytest -v`.
- **Manual verification:** none needed beyond watching the suite; the assertions cover the claims. Do run `python -m pytest` twice to confirm determinism.
- **Negative check (worth doing once):** temporarily make EASY grant an extra item, confirm Invariant 1 fails loudly, then revert. A test that cannot fail is not a test, and this is the one assertion whose failure mode is invisible.

## Definition of Done / Acceptance Criteria
- [ ] The three invariants are asserted, each by a named test
- [ ] Reachability is computed by traversal from the content, not hardcoded
- [ ] MEDIUM is proven identical to the pre-slice baseline
- [ ] The no-content-identifier guard exists and passes
- [ ] AC-24's status for this slice is asserted, with the `sound`/`music` handoff to H04 marked
- [ ] The negative check was performed and Invariant 1 was observed failing before being reverted
- [ ] No product file changed by this task
- [ ] The suite is deterministic across repeated runs
- [ ] `python -m pytest -v` passes, including the three pre-existing modules and A13's suite

## Rollback / Undo
Revert this task's commit; difficulty continues to work but the fairness claim loses its mechanical guard, which reopens RISK-5. Slice B's AC-16 and AC-17 lose their evidence, so treat a revert as reopening the slice rather than as a clean undo.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the negative-check result and any fairness bug found (which becomes its own task, not a silent fix) here -->
