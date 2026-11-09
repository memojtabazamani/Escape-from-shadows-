# Task B02: Lantern and composure generosity by difficulty

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: B — Difficulty as a Real System
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: B01
- Blocks: B03, B04, D01
- Covers: AC-16
- Suggested commit: `feat(difficulty): scale the lantern and composure by difficulty`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make the two bars respond to difficulty: EASY gives more light and steadier nerve, HARD gives less of both, and MEDIUM stays exactly as shipped.

## Non-Goals
- Does not implement mercy (restart points, journal auto-fill) — that is B03, and it is a *restart* concern, not a bar concern.
- Does not implement hints — that is B04.
- Does not implement HARD's expiring choices — that is B05.
- Does not create the composure stat. **D01 does that.** This task only defines what composure's generosity parameter *means*, so D01 can consume it on day one rather than retrofitting the seam — the same bullet-dodging §11 recommends.
- Does not touch the lantern's *rules* (A05's drain, A06's zero-oil consequence) — only the starting amounts and the rate at which those rules bite.

## Context & Constraints
- **Read first:** §5.1's full text and its worked table of what each difficulty does to the lantern; §3.1 (oil is the clock, and the game is balanced around it) and §3.2 (composure's restoration list). Then read A05's recorded drain numbers and A06's zero-oil behaviour, because MEDIUM must not disturb either.
- **Files to modify:** `game/lantern.py` (A05/A06); `game/difficulty.py`'s parameter values.
- **Files to read, not modify:** `game/state.py` — `RunState.lantern` defaults to 100 and is clamped 0–100, and `spend_lantern()` returns the amount *actually* spent; a generosity parameter must compose with that clamp rather than fight it. `game/effects.py` — `lantern_above` is the only lantern predicate today, so a generosity change is felt through existing requirement thresholds. `screens/game.py` (A04) — the bar renders from `RunState`, so it needs no change, but verify it does not cache.
- **Conventions to respect:** the Phase 1 style for numeric contracts — `game/state.py`'s docstrings state ranges and clamping explicitly. Follow that.
- **Design constraints — the §5.1 caveat is the hard part of this task:**
  - **Generosity, not content.** Changing the starting oil must never change *which* rooms are reachable or *which* solutions exist. If a lower starting amount can strand a player who has no alternative route, the parameter is wrong — §5.1's "HARD removes safety nets, never fairness" is a design constraint, not a slogan, and B06 tests it.
  - **Bounded and monotonic.** EASY ≥ MEDIUM ≥ HARD on both bars, with MEDIUM exactly today's numbers. Monotonicity is what makes "EASY is easier" a true statement rather than a coincidence.
  - **Applied once, at run start.** Generosity is an initial condition, not a per-turn multiplier — a per-turn multiplier would silently change every drain number A05 chose and every threshold the content sets.
  - **The zero-oil consequence is unchanged on every difficulty.** A06's honest consequence still lands; difficulty decides how long it takes to get there, not whether it exists. Otherwise HARD acquires a *new* failure mode, which is unfairness.
  - **Do not scale the composure drain in D01's territory** — only the parameter's meaning. The drain itself lands with the stat.
- **Voice:** keep A05's and A06's comments intact; add difficulty's effect as a labelled line, not a rewrite.

## Preconditions
- [ ] B01 DONE — `DifficultyConfig` exists and MEDIUM reproduces pre-slice behaviour
- [ ] A05 and A06 DONE — lantern rules and the zero-oil consequence exist and are tested
- [ ] GP-6 partly answered — at least the lantern generosity values are confirmed; if not, use placeholders and record them as pending
- [ ] A13's regression suite is green, so a behaviour change is detectable
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `game/lantern.py` and note every place a starting amount or threshold is read.
2. Confirm MEDIUM's parameter values equal A05's shipped numbers exactly; adjust B01's placeholders if they drifted.
3. Apply generosity at run start only — in the `RunState` construction path, not inside a drain function.
4. Make sure the derived value still respects `RunState`'s 0–100 clamp and that `spend_lantern()`'s "actually spent" return stays truthful when the lantern is nearly empty.
5. Define the composure generosity parameter's meaning and units in `game/difficulty.py` so D01 can read it without reinterpretation; document the units where D01 will look.
6. Verify the EASY ≥ MEDIUM ≥ HARD ordering holds in the actual numbers.
7. Walk HARD and confirm no room became unreachable and no requirement became unsatisfiable — this is the fairness check, and it is manual because it is about design, not arithmetic.
8. Re-run A13's suite and confirm MEDIUM is unchanged.

## Test Plan
- **Tests to write/update:** new `tests/test_difficulty_bars.py` (to be created):
  - `test_easy_medium_hard_are_monotonic_on_both_bars` — asserts the ordering, so a future edit cannot invert it silently.
  - `test_medium_matches_the_shipped_defaults` — the baseline-stability guard, re-asserted at this layer.
  - `test_generosity_is_applied_at_run_start_only` — asserts a drain's amount is identical across difficulties.
  - `test_zero_oil_consequence_is_reachable_on_every_difficulty` — guards the "no new failure mode" rule in the other direction: HARD must still be *finishable*, and MEDIUM's path must still be *pressuring*.
  - `test_generosity_does_not_change_requirement_satisfiability` — asserts that for every content requirement threshold, a player with the difficulty's starting oil plus the available refills can still satisfy it.
- **Commands:** `python -m pytest tests/test_difficulty_bars.py -v`; then `python -m pytest -v`.
- **Manual verification:** play the same route on EASY and HARD; confirm the only difference is how much light you have, and that both reach the same rooms, the same items, and the same ending.
- **Fairness walk (the design check):** on HARD, ask of every requirement you encounter — *is there another way?* If any answer is no, a parameter is too tight and the value is wrong, not the design.

## Definition of Done / Acceptance Criteria
- [ ] Both bars respond to difficulty and MEDIUM is byte-identical in behaviour to before
- [ ] EASY ≥ MEDIUM ≥ HARD holds on both bars, asserted by test
- [ ] Generosity is applied once at run start, never per-turn
- [ ] Composure's parameter is defined with units, ready for D01 to consume
- [ ] The zero-oil consequence exists on all three difficulties and no difficulty adds a failure mode
- [ ] Every room, item and solution remains reachable on HARD — verified by playing, not by argument
- [ ] The 0–100 clamp and `spend_lantern()`'s return value remain correct at low oil
- [ ] A06's comments and behaviour are preserved
- [ ] `python -m pytest -v` passes, including the three pre-existing modules and A13's suite

## Rollback / Undo
Revert this task's commit; all three difficulties behave identically again and B01's seam becomes inert, which is a safe state. D01 depends on the composure parameter's definition, so if D01 has landed, revert as a group or D01 will read a missing field.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the actual parameter values, GP-6 confirmations, and the HARD fairness walk result here -->
