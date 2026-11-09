# Task D01: Composure stat, drains, and recovery

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: D — Composure
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: A13, B02
- Blocks: D02, D03
- Covers: AC-9
- Suggested commit: `feat(composure): add the nerve stat with its drains and recovery`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Add composure as the game's second bar: a stat on the run that horror drains, calm and safety restore, and that difficulty scales — with no narration or UI behaviour attached yet.

## Non-Goals
- Does not distort any prose — that is D02, which is deliberately separate so the highest-variance feature in the phase can be reviewed on its own (RISK-4).
- Does not implement the zero-composure walk — that is D03.
- Does not render a bar — that is D04.
- Does not add composure verbs or predicates to the engine beyond what content needs to drain and restore it; if the verb table needs extending, that is C02's verdict being consumed, and record it here.
- Does not author content that drains composure in the new rooms. Slice F authors the rooms; this task provides the mechanism and applies it to A07's and A08's existing rooms so the bar is observable.

## Context & Constraints
- **Read first:** §3.2 in full — the composure rules, the restoration list, and the explicit caveat ASM-6 encodes ("distortion is capped at the last 20% and always carries a tic") — plus ASM-6 itself, §6's room-by-room composure costs, and §4.1's three tiers, since composure loss is the mechanic that makes `scar` mean something.
- **Files to create:** `game/composure.py` (to be created).
- **Files to modify:** `game/state.py` — the new stat, its snapshot/restore fields, and its clamping; `game/effects.py` and `game/content_schema.py` if new verbs are needed (per C02's verdict, which is recorded in the C02 Execution Log — read it before inventing a verb).
- **Files to read, not modify:** `game/lantern.py` — the lantern is the closest precedent for a resource with drains, drains-by-action, and a terminal consequence; **follow its structure rather than inventing a parallel one.** `game/difficulty.py` — B02 defined the composure generosity parameter's units; consume it as defined, do not reinterpret it.
- **Conventions to respect:** `spend_lantern()`'s contract is the house style: clamp internally, **return what actually happened**, never raise on a mundane resource change. Composure operations should mirror it so a reader who knows one knows both.
- **Design constraints — §3.2's caveat is a structural constraint, not a polish note:**
  - **Composure is not health and must not behave like it.** §3.2 and AC-11: zero composure does **not** kill; D03's voluntary walk is what happens instead. Nothing in this task may treat zero as a death, and the module's docstring should say so explicitly — that is the single most likely mistake a future contributor makes here.
  - **Drain is content-authored, not code-authored.** §11: which rooms and choices cost nerve is a content property. The module provides the verbs; the values live in content.
  - **Recovery follows §3.2's list** — confined spaces, light, stillness. Read the list and implement only what it names; inventing extra recovery is how the bar stops mattering.
  - **Distortion is not this task's, and the boundary must be visible.** This task produces the number. D02 reads it to decide whether to distort. Do not add a `distorted` flag or a prose hook here, or the two tasks will overlap and RISK-4's review will have nothing clean to inspect.
  - **The start value is difficulty-derived**, via B02's parameter, and MEDIUM must equal the value A13's playtest balanced against.
  - **Snapshot/restore must carry it**, or I01's save silently loses the bar.
- **Voice:** the module docstring should state the zero-does-not-kill rule in §3.2's own terms, because it is the contract D03 and D04 both rely on.

## Preconditions
- [ ] A13 DONE — the loop is green and its playtest passed
- [ ] B02 DONE — the composure generosity parameter exists with documented units
- [ ] C02's spike verdict is recorded and read, so the verb-extension route is known
- [ ] A07 and A08 DONE — there are at least two rooms to apply a drain to
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `game/lantern.py` end to end; note the clamp, the "actually spent" return, and where the terminal consequence is **not** implemented (A06 holds it) so the same separation holds here.
2. Read §3.2's restoration list and write it down as the module's contract.
3. Read C02's verdict and B02's parameter units before adding any verb.
4. Create `game/composure.py`: the stat's operations — a drain that returns what actually happened, a restore, and a predicate-friendly accessor for the last-20% band that D02 will need.
5. Add the field to `RunState` with clamping, and carry it through `snapshot()`/`restore()` — confirming C01's backward-compatibility rule still holds for a snapshot that predates the field.
6. Add the verbs to `game/effects.py` and mirror them into `game/content_schema.py`.
7. Apply a drain to at least one choice in A07's hall and one in A08's library, using §6's per-room costs, so the bar is observable before Slice F.
8. Apply a recovery opportunity per §3.2's list, so the bar moves both ways and D05 can test the range.
9. Verify the start value honours B02's parameter and that MEDIUM matches the balanced baseline.
10. Confirm nothing yet reads the value for narration — D02's job — and that no code path treats zero as fatal.

## Test Plan
- **Tests to write/update:** new `tests/test_composure_model.py` (to be created):
  - `test_composure_clamps_at_both_ends` — the boundary, mirroring the lantern's.
  - `test_drain_returns_what_actually_happened` — the house-style contract.
  - `test_recovery_follows_the_modeled_list` — asserts the recovery sites are exactly those §3.2 names.
  - `test_zero_composure_does_not_end_the_run` — the AC-11 guard, asserted here so D03 cannot accidentally introduce a death.
  - `test_start_value_honours_the_difficulty_parameter` — the B02 consumption check.
  - `test_snapshot_round_trips_composure` — the I01 dependency.
  - `test_pre_slice_snapshot_restores_with_a_default_composure` — backward compatibility, as C01 established.
- **Commands:** `python -m pytest tests/test_composure_model.py -v`; then `python -m pytest -v`.
- **Manual verification:** play a run that loses nerve and regains it; confirm the number moves both ways and that reaching zero is survivable.
- **Boundary check:** confirm no prose changed — this task must be invisible to the player except through the bar D04 will add.

## Definition of Done / Acceptance Criteria
- [ ] `game/composure.py` exists, structured after `game/lantern.py`'s precedent
- [ ] The stat clamps, drains and restores, and the drain returns what actually happened
- [ ] Zero composure does not end the run — asserted by test and stated in the docstring
- [ ] The start value is difficulty-derived, with MEDIUM matching the balanced baseline
- [ ] Recovery sites are exactly those §3.2 names
- [ ] `snapshot()`/`restore()` carry the field and tolerate a pre-slice snapshot
- [ ] Verbs are added to `effects.py` and mirrored in `content_schema.py`, per C02's verdict
- [ ] At least one drain and one recovery exist in the current content, so the bar is observable
- [ ] No narration distorts and no `distorted` flag exists — D02's boundary is clean
- [ ] `python -m pytest -v` passes, including A13's suite and C01–C05's tests

## Rollback / Undo
Revert this task's commit; the stat disappears along with its content references, so any choice authored with a composure verb becomes invalid and `validate_content()` fails. D02, D03 and D04 all depend on this module — revert the whole slice together.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the verb names chosen (per C02's verdict), the start value, and the drain/recovery sites authored here -->
