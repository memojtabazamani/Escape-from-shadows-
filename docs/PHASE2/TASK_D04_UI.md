# Task D04: Composure bar and the distortion tic

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: D — Composure
- Layer: UI
- Status: DONE
- Estimate: ~3h
- Depends on: D02
- Blocks: D05
- Covers: AC-9, AC-10
- Suggested commit: `feat(ui): show the composure bar and render the distortion tic`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Put composure on screen as a second bar beside the lantern, and give D02's tic a visual form — so the player can see the nerve drain and recognise distorted narration as distorted.

## Non-Goals
- Does not change the drain or recovery values — D01 owns them.
- Does not change the distortion text — D02 owns it. This task *styles* the marker D02 established; if D02's marker proves unstyleable, that is a finding to report, not licence to re-author the text.
- Does not add a fourth zone. §7.1 fixes three zones; the composure bar lives in the status zone beside the lantern, and the inventory (C04) is already there. **Space is now the constraint this task must solve.**
- Does not implement the journal overlay — E03.
- Does not implement H02's pulsing or typewriter effects. Music-driven rhythm is Slice H; this task's styling is static.

## Context & Constraints
- **Read first:** §7.1's three zones and the ~20-line budget, §7.4's colour grammar — **amber for time, light and resources; red only when the Shadow is present** — §3.2's caveat (the tic's *existence* is the information), and §13's text-wall pitfall.
- **Files to modify:** `screens/game.py` — the status zone from A04, which C04 has already extended with the inventory; and the narration rendering path from A02 for the tic.
- **Files to read, not modify:** `game/composure.py` (D01); `game/distortion.py` (D02's marker); `screens/game.py`'s existing bar implementation for the lantern (A04) — **the composure bar must match it visually**, so the two read as two bars of one instrument rather than two features.
- **Conventions to respect:** `AGENTS.md` — thin `compose()`, helpers for rendering, `CSS` class attribute. Keep bar-drawing in a shared helper if A04 did not already factor one out; if it did, reuse it rather than duplicating the drawing code.
- **Design constraints:**
  - **Two bars, three zones, one screen.** The status zone now holds the lantern bar (A04), the turn counter, the low-oil warning, the inventory (C04), and now the composure bar. Confirm the whole thing plus §7.1's ~20 lines of room prose still fits at a narrow width, and solve it by layout — **the prose budget is not this task's to spend** (ASM-18).
  - **Amber for composure.** It is a resource, per §7.4. Red stays reserved for the Shadow — **except** in the walk D03 authored, where the Shadow is present and red is therefore correct. Decide that case explicitly and record it.
  - **The tic must be visible, not decorative.** Its job is to tell the player the narration is unreliable. If the styling is subtle enough to miss, AC-10 is unmet in practice even though D02 is correct in fact. Verify with someone who does not know the feature exists.
  - **The bar must be legible at the values that matter.** The last 20% is the functional region (D02's threshold) and the floor is D03's trigger; both should be distinguishable at a glance, without reading the number.
  - **No bar for a value that isn't changing.** If composure is at full and has never moved, a neutral rendering is better than a bar at maximum shouting for attention. Decide the default state and record it.
  - **Accessibility note for Phase 4:** §8 lists high contrast and colourblind glyphs as Phase 4, but if this task's information is *only* in colour, record that as a Phase 4 dependency rather than shipping a bar that a colourblind player cannot read. Bars and counts carry information without colour; prefer that.
- **Voice:** no new prose. The tic is styling; the bar is a measurement.

## Preconditions
- [ ] D02 DONE — the distortion transform and its marker exist
- [ ] D01 DONE — composure is on the run and moves
- [ ] A04 DONE — the lantern bar exists as the visual precedent
- [ ] C04 DONE — the inventory has already claimed part of the status zone, so the space is known
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read A04's lantern bar and C04's inventory rendering; measure the status zone's current height.
2. Decide the composure bar's placement and rendering so the zone fits within §7.1's budget at a narrow width; record the layout decision.
3. Render the bar in amber, matching the lantern's visual language.
4. Distinguish the last-20% band (D02's threshold) and the floor (D03's trigger) visually — the two states that change behaviour must be readable without arithmetic.
5. Decide and record the full-composure default rendering.
6. Style D02's tic marker in the narration region so it is unmistakable. Record the styling.
7. Verify the tic is not the *only* signal — the text itself is distorted, so the styling is reinforcement, not the whole information.
8. Check the whole screen at a narrow width with a full inventory, a low lantern and a low composure simultaneously — the worst case.
9. Show it to someone who does not know about the feature and ask whether they can tell the text is unreliable, and whether they can see the bar is low.

## Test Plan
- **Tests to write/update:** new `tests/test_composure_ui.py` (to be created):
  - `test_composure_bar_renders_in_the_status_zone` — asserts no fourth zone was added.
  - `test_the_worst_case_screen_fits_one_terminal` — full inventory, low lantern, low composure, at a narrow width.
  - `test_last_twenty_percent_is_visually_distinct` — asserts the functional band is distinguishable.
  - `test_tic_marker_is_rendered_in_narration` — asserts D02's marker reaches the screen.
  - `test_bar_and_text_carry_information_without_colour` — the §8 guard: asserts a non-colour channel exists for both.
  - `test_red_is_absent_except_in_the_walk` — §7.4's reservation, asserted mechanically.
- **Commands:** `python -m pytest tests/test_composure_ui.py -v`; then `python -m pytest -v`.
- **Manual verification:** play into the last 20% and confirm both the bar and the narration tell you, without knowing the feature.
- **Stranger check:** the observation in step 9 is the deliverable's real test. Record both answers verbatim.

## Definition of Done / Acceptance Criteria
- [ ] The composure bar renders in the status zone, matching the lantern's visual language, with no fourth zone
- [ ] The last-20% band and the floor are visually distinguishable without reading a number
- [ ] The full-composure default state is decided and recorded
- [ ] D02's tic marker is rendered in narration and is unmistakable
- [ ] Both the bar and the tic carry information through a non-colour channel
- [ ] Red appears only where the Shadow is present — asserted by test
- [ ] The worst-case screen with a full inventory fits one terminal at a narrow width
- [ ] The room prose budget is unchanged by this task
- [ ] The stranger observation is recorded verbatim in the log
- [ ] `python -m pytest -v` passes, including A13's suite and Slice C/D tests

## Rollback / Undo
Revert this task's commit; composure drains invisibly and the tic loses its styling, so AC-9 and AC-10 are unmet without the underlying rules breaking — the run stays playable but the player is flying blind. D05 depends on this rendering to assert visibility, so revert as a group with D02 if the tic is the problem.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the layout decision, the tic styling, the red-in-the-walk decision, and the stranger's verbatim answers here -->
