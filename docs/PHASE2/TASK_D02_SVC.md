# Task D02: Unreliable narration, capped at 20% and always signalled

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: D — Composure
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: D01
- Blocks: D04
- Covers: AC-10
- Suggested commit: `feat(composure): distort narration only in the last fifth, and always visibly`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make low composure change how the room reads — but only in the last 20% of the bar, and never without a visible tic that tells the player the narration has become unreliable.

## Non-Goals
- Does not write the distorted prose. §3.2's rule is that distortion alters the *description*, not the room; the distortion is a transformation applied to authored prose, and **authoring a second version of every room's prose is explicitly not the design.** Decide the transformation, implement it, and record the decision.
- Does not render it — D04 puts it on screen. This task produces the transformed text.
- Does not touch the exits' existence (ASM-6): distortion may change how a door is described, never whether it is there. This is the one hard boundary of the feature.
- Does not distort the status or footer zones (§7.1) — the bar is a measurement; distorting the instrument is a different, worse idea.
- Does not implement the zero-composure walk — D03.

## Context & Constraints
- **Read first:** §3.2 in full, especially its caveat, and ASM-6 verbatim: "**Composure distortion is capped at the last 20% of the bar and always carries a tic** (italic, stutter, repeated word)... Distortion never affects the *existence* of an exit, only its description." Then RISK-4 in the epic: "**Unreliable narration is the highest-variance feature in the phase** — wonderful once, infuriating when overdone."
- **Files to create:** `game/distortion.py` (to be created), or an addition to `game/composure.py` if it stays under the file budget — decide and record.
- **Files to modify:** the narration path that A02 established, so transformed text has one entry point rather than being applied at each call site.
- **Files to read, not modify:** `game/composure.py` (D01's last-20% accessor, built for this); `screens/game.py` (A02's prose rendering — the transform should be applied *before* rendering, so the screen keeps rendering plain text and one module owns the distortion); `game/state.py`.
- **Conventions to respect:** keep the transform a **pure function of (text, composure band) → text**, so it is trivially testable and cannot mutate state. A pure function is also the only shape that makes the "always carries a tic" rule assertable.
- **Design constraints — the tic is the whole feature:**
  - **The tic is mandatory, on every distorted line.** Not on the first one, not sometimes. §3.2's caveat exists so the player can tell hallucination from fact; a distortion without a tic is a lie the player cannot detect, which inverts the design's honesty pillar.
  - **Distortion is bounded to the last 20%.** Above that threshold the transform is the identity function, exactly. Assert this at the boundary, both sides.
  - **The transform must be reversible in the player's mind.** Distortion should read as *your* perception slipping — a repeated word, a stutter, a colour change in the description — not as prose that is simply different. The player must be able to discount it.
  - **No exit may be removed, added, or renamed.** Only its description may change. Assertable: the set of choice ids and destinations is identical before and after transformation. This is the assertion that keeps D02 from becoming a bug factory.
  - **Deterministic.** The same text and band produce the same output, or tests cannot assert it and the player cannot learn it. If variety is wanted, seed it from the run, not from the clock.
  - **Distortion must not fight readability.** §13's text-wall pitfall plus §8's accessibility concern: if a player cannot parse a distorted sentence, they cannot act on the tic. It should be noticeable and understandable, not corrupted.
- **Voice:** distortion is *your* mind, not the Shadow's. Keep it in the narration register (§7.4, dim grey) unless D04's styling decides otherwise — and if a colour is used, record the call, since §7.4 reserves red.

## Preconditions
- [ ] D01 DONE — the stat exists with its last-20% accessor
- [ ] A02 DONE — narration has a single rendering entry point to hook
- [ ] The content's room prose is authored and stable, since the transform operates on real text
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read §3.2's caveat and ASM-6 again, and read D01's last-20% accessor to see what it exposes.
2. Decide the transform: which device (repetition, stutter, or a small set), how many tics, and how the tic is marked. Record the decision.
3. Implement it as a pure function with the composure band as an input, returning text unchanged above the threshold.
4. Make the tic's presence assertable — a detectable marker the tests and D04 can both look for. Record what that marker is.
5. Wire it into A02's single narration entry point; do not apply it at call sites.
6. Prove the exits are untouched: transform every room's prose and compare the choice sets.
7. Prove determinism: transform the same text twice and compare.
8. Read a distorted room as a player would; if a sentence no longer makes sense, soften the device.
9. Confirm the status and footer zones are unaffected.

## Test Plan
- **Tests to write/update:** new `tests/test_distortion.py` (to be created):
  - `test_above_the_threshold_transformation_is_identity` — the cap's upper side.
  - `test_below_the_threshold_every_line_carries_a_tic` — the cap's lower side plus the mandatory tic, checked over **every** room in the content, not a sample.
  - `test_transform_never_changes_the_choice_set` — ASM-6's hard boundary, asserted over all rooms.
  - `test_transform_is_deterministic` — same input, same output.
  - `test_transform_is_pure` — asserts no state mutation, by comparing the run before and after.
  - `test_distorted_text_remains_parseable` — a length and word-count sanity bound, guarding the text-wall pitfall.
- **Commands:** `python -m pytest tests/test_distortion.py -v`; then `python -m pytest -v`.
- **Manual verification:** drive composure into the last fifth and read a room you know well; confirm you can tell it is distorted *and* still know what the room contains.
- **Overdone check (RISK-4's review):** read the distorted prose for three consecutive rooms. If it is annoying by the third, reduce the frequency or the intensity — that judgement is the deliverable's real test, and the result belongs in the log.

## Definition of Done / Acceptance Criteria
- [ ] The transformation is a pure, deterministic function of text and composure band
- [ ] Above the last-20% threshold the output is byte-identical to the input
- [ ] Every distorted line carries a detectable tic, asserted across all content
- [ ] No choice id, destination, or exit is added, removed or renamed by distortion
- [ ] The tic's marker is recorded, so D04 can style it and tests can find it
- [ ] Distortion is applied at one entry point, not at call sites
- [ ] The status and footer zones are never distorted
- [ ] Distorted text remains parseable — bounded length and word count
- [ ] The three-consecutive-rooms readability judgement is recorded in the log
- [ ] `python -m pytest -v` passes, including A13's suite and C/D tests so far

## Rollback / Undo
Revert this task's commit; narration returns to plain text at every composure level and AC-10 is unmet, but the run is fully playable and the bar still drains. This is the safest single-task revert in the slice, which is why D02 is separable from D01 and D04.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the transform's device, the tic marker, and the three-room readability judgement here -->
