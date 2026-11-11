# Task A09: One honest death at the left doorway

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: SVC
- Status: DONE
- Estimate: ~2.5h
- Depends on: A07
- Blocks: A10, A11
- Covers: AC-21, AC-2
- Suggested commit: `content(hall): implement the telegraphed death at the left doorway`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Implement the slice's one honest death: the left doorway in THE HALL kills you, but only after two warnings, and the death itself says what killed you.

## Non-Goals
- Does not build BLOOD KITCHEN as a room — that is F02. In this slice the kitchen is a threshold where a death occurs, matching Phase 1's ASM-3; F02 later turns it into a trade room and this death is revisited then.
- Does not present the death — that is A11. This task produces the death *result*; A11 renders it.
- Does not add a second death. This slice has exactly one.
- Does not implement difficulty-gated mercy for death — that is B03.
- Does not implement the "what you could have done" line — that is I04.

## Context & Constraints
- **Read first:** §4.1 in full — the three-tier model and "death should be *earned by the player*... **An unwarned death is a bug**" — plus §4.2's worked example of a telegraph, §6's BLOOD KITCHEN entry (so the threshold prose is honest about what lies beyond), and §13's first pitfall.
- **Files to modify:** the content file(s) from A07.
- **Files to read, not modify:** `game/content_schema.py` — the `death` tier and `_validate_death_telegraphs`, which **already rejects a death choice with fewer than two telegraphs** (so the count is enforced; the quality is yours); `game/effects.py` for how a terminal result is produced; `screens/game.py` (A03's death-tier placeholder), which must keep routing correctly until A11 replaces it.
- **Conventions to respect:** the tier and its telegraphs live in content, not in code; darkness is the only terminal mechanic here, reused from A06 rather than reinvented.
- **Design constraints — the honesty requirements are the point of this task:**
  - **Two distinct telegraphs, mandatory.** They must be sensory and specific — §4.2's model is "The door to the left is warm. There is a smell, and it is recent." Two variations of "it looks dangerous" do not count as two.
  - **The warnings must be available before the choice**, not delivered as part of the death text. A player must be able to read the room and decide not to go.
  - **The death result must state its cause** in one sentence, as structured data — A11 and E02 both consume it.
  - **The death must be reachable but not accidental.** There must be no path where the death occurs without the player choosing the doorway.
  - **The threshold must not be a fake room.** It is a place you die; the content must not imply you can explore it, or §13's promise about honest choices is broken.
- **Voice:** restraint over gore. The kitchen is described by what is *wrong* with approaching it, not by an inventory of blood (pillar 1).

## Preconditions
- [x] A07 DONE — the left doorway choice exists in the hall
- [x] A03 DONE — the death tier routes through the placeholder and receives a cause
- [x] `validate_content()` enforces the two-telegraph rule
- [x] A05 DONE — the oil context at the doorway is coherent (see step 1)
- [x] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Decide and record whether walking into the doorway costs the room-entry drain before the death lands, and make the behaviour match the recorded decision.
2. Author the destination: a short, final threshold scene that is unmistakably terminal and does not invite exploration.
3. Write the two telegraphs so they are **distinct in kind** — a warmth and a sound, not two smells.
4. Implement the death result as structured data carrying a one-sentence cause.
5. Confirm the Death tier routes through A03's placeholder and that the placeholder receives the cause rather than a generic message.
6. Verify no path reaches the death without the player selecting the doorway — including the front door, the staircase, and a refused choice.
7. Walk it: read the room as a first-timer, decide whether you feel warned, then walk in deliberately and confirm the death states its cause.

## Test Plan
- **Tests to write/update:** extend `tests/test_content_house.py`:
  - `test_left_doorway_has_two_distinct_telegraphs` — asserts two or more telegraphs via the validator's own rule.
  - `test_reaching_the_doorway_produces_a_death_with_a_cause` — asserts the cause is present and is one sentence.
  - `test_death_is_unreachable_without_selecting_the_doorway` — asserts the other choices cannot produce it.
  - `test_run_is_completable_without_the_doorway` — the avoidability check.
- **Commands:** `python -m pytest tests/test_content_house.py -v`; then `python -m pytest`.
- **Manual verification:** run the app and walk the doorway; confirm the room warned you twice before you chose, and that the death names its cause.
- **Honesty observation (the real check):** show the room to someone who has never played. Ask whether they felt warned. If they say no, the telegraphs are too subtle — rewrite them. This observation is what §12's success test ultimately rests on.

## Definition of Done / Acceptance Criteria
- [x] The doorway has at least two telegraphs, distinct in kind, in the §4.2 style
- [x] The warnings are available before the choice, not delivered with the death
- [x] The death result carries a one-sentence cause as structured data
- [x] The death is unreachable without the player selecting the doorway
- [x] The threshold scene does not invite exploration
- [x] The death is avoidable and the run is completable without it
- [x] The doorway's oil behaviour matches the recorded decision
- [x] No engine or screen file changed except where A03's placeholder already lives
- [x] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; the doorway choice remains but no longer kills, which removes AC-21 and leaves the slice without a failure state — revert together with A07's doorway, or the content will no longer match the slice's design. Verify the content set still validates after reverting.

## Execution Log
- **Date:** 2026-11-09
- **Agent:** Antigravity
- **Branch:** feature/phase_2_the_house (No git commit per user instruction)
- **Oil Decision:** Stepping through the left doorway costs standard room-entry drain (`FIRST_VISIT_DRAIN = 10`), simulating crossing the threshold into darkness before the lethal strike lands.
- **Telegraphs:** Two distinct sensory modalities authored on `hall_left`:
  1. Thermal: `"A draft of warm, unnatural air breathes steadily from the dark archway."`
  2. Auditory: `"A wet, rhythmic dripping echoes somewhere just past the threshold, accompanied by the dull scrape of bone on stone."`
- **Structured Death Cause:** `"You stepped blindly past the warned threshold and were butchered in the dark."` (one concise, honest sentence recorded on choice and destination room).
- **Notes:**
  - `left_doorway_death` authored with terminal threshold prose (`"The Threshold of Blood"` with 0 choices) that does not invite exploration.
  - `GameScreen.last_death_cause` captures the structured cause upon selecting a death-tier choice and displays the cause on `#prompt-line`.
  - Added unit and pilot tests in `tests/test_content_house.py` verifying sensory differentiation, single-sentence cause, unreachability from other choices, avoidability, and screen routing.
  - 64 tests passing green.
