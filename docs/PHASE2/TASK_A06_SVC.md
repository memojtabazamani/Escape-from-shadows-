# Task A06: Zero-oil condition and its honest consequence

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: SVC
- Status: DONE
- Estimate: ~2.5h
- Depends on: A05
- Blocks: A07
- Covers: AC-1, AC-21
- Suggested commit: `feat(lantern): implement the zero-oil consequence`
- Branch: feature/phase_2_the_house

## Objective
Make running out of oil mean something: at zero, the Shadow can reach the player — but only after two warnings, so the loss is a decision the player made, not a trap.

## Non-Goals
- Does not implement the Shadow as a pursuing entity — ASM-11 and §2.2 keep that in Phase 3. The Shadow's *reach* here is a terminal consequence of an empty lantern, not an AI.
- Does not implement the death screen's presentation — that is A11; this task produces the consequence, A11 renders it.
- Does not implement difficulty-gated mercy for this consequence — that is B03.
- Does not implement composure (§3.2). A full-lantern, zero-composure walk is D03's, and it is a *different* state — see D03's Non-Goals.

## Context & Constraints
- **Read first:** §3.1's closing line — "**At zero oil, the Shadow can reach you**" — and then §4.1 and §13 together: "Death should be *earned by the player*: they saw the blood on the kitchen threshold, they heard the thing breathing, and they walked in anyway. **That death is a story. An unwarned death is a bug.**"
- **Files to create:** `game/lantern.py` gains the zero-oil check (from A05), plus a small threshold constant.
- **Files to read, not modify:** `game/content_schema.py` — the `death` tier and its **validator-enforced two-telegraph rule** (`_validate_death_telegraphs`) is the mechanism this task's honesty requirement must use; `game/effects.py` for how a death result is produced; `game/state.py` for `has_light()`.
- **Conventions to respect:** the honesty requirement is expressed **in content**, not in code — the warnings are telegraphs on a choice, per §4.2.
- **Design constraints:**
  - **Two distinct telegraphs, mandatory and non-negotiable.** The validator rejects a death choice with fewer than two, so the *count* is enforced; the *quality* is on this task. Two restatements of "it is dark" do not count (§4.2's model wants a warmth, a smell, a sound).
  - **The warnings must be available before the choice**, not delivered as part of the consequence.
  - **The consequence must state its cause** in one sentence, as structured data — A11 and E02 both consume it.
  - **The first warning must arrive while oil remains**, so the player has a turn in which to act. A warning at exactly zero is not a warning.
- **Voice:** restraint. The Shadow is described by what is *missing* (§2.2) — a doorway with no light behind it — not by what it looks like.

## Preconditions
- [ ] A05 DONE — drain exists and the lantern reaches zero through play
- [ ] A04 DONE — the amber low-oil warning renders, so the first warning is visible
- [ ] A03 DONE — choices, telegraphs, and requirement gating render
- [ ] `validate_content()` is in place and enforces the two-telegraph rule
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Define the low-oil threshold that triggers the **first** warning, above zero, and record it (it should agree with A04's amber threshold — if it does not, reconcile them and say so in the log).
2. Author the first warning in content: a telegraph on the relevant choice or a room state line, delivered while oil remains.
3. Author the second, distinct warning: different in *kind* from the first (§4.2), not in wording.
4. Author the zero-oil consequence as a `death`-tier path with its cause as structured data.
5. Route it through the same path A03 already reserves for the death tier — do not add a second terminal mechanism.
6. Confirm the validator passes with exactly the telegraphs you wrote, and that removing one makes validation fail (that is the rule working).
7. Walk it: spend the lantern down by playing, and confirm a first-timer has a turn in which to change course after the first warning.

## Test Plan
- **Tests to write/update:** extend `tests/test_lantern.py`:
  - `test_first_warning_fires_above_zero` — asserts the warning threshold is strictly greater than zero.
  - `test_zero_oil_produces_a_death_result_with_a_cause` — asserts the consequence carries a non-empty one-sentence cause.
  - `test_zero_oil_choice_has_two_distinct_telegraphs` — asserts the count via the validator's own rule.
  - `test_warnings_precede_the_choice` — asserts both telegraphs are available before the terminal step.
- **Commands:** `python -m pytest tests/test_lantern.py -v`; then `python -m pytest`.
- **Manual verification:** drain the lantern to zero by playing and confirm you were warned twice, and that you could name what warned you.
- **Honesty observation (the real check):** show the zero-oil sequence to someone who has not played. Ask whether they felt warned. If they say no, the telegraphs are too subtle — rewrite them.

## Definition of Done / Acceptance Criteria
- [x] The first warning fires while oil remains, so the player has a turn to act
- [x] Two telegraphs, distinct in kind, following §4.2's sensory model
- [x] The warnings are available before the choice, not delivered with the consequence
- [x] The consequence carries a one-sentence cause as structured data
- [x] Removing one telegraph makes `validate_content()` fail
- [x] No second terminal mechanism was added; it reuses A03's death-tier routing
- [x] The consequence is avoidable: a player who heeds the warnings completes the run
- [x] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; the lantern can reach zero and nothing happens — the game loses its clock. A07 depends on this consequence existing (the HALL's oil context), so revert them together.

## Execution Log
- 2026-11-09: Implemented zero-oil consequence data and helpers in `game/lantern.py`. Warning threshold set to 30 (firing above zero, giving the player multiple turns to adapt). Two distinct sensory telegraphs authored (visual sputtering vs freezing draft/presence). Tests in `tests/test_lantern.py` verify that `validate_content()` strictly enforces the two-telegraph rule, that warnings fire above zero, and that cause data is structured. All 49 tests pass.
