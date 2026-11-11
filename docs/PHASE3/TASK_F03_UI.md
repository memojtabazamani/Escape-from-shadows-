# Task F03: Quiet horror presentation techniques (delayed echo, missing line, patient prompt)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: F — Dread Counter & Quiet Horror Presentation
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: F02
- Blocks: F04
- Covers: AC-24, §7.5
- Suggested commit: `feat(ui): implement quiet horror presentation techniques with subtle restraint`
- Branch: feature/phase_3_the_shadow

## Objective
Implement the quiet psychological horror techniques detailed in `docs/SUGGEST.md` §7.5: **delayed echo** (repeating an earlier sensory fragment), **the missing line** (subtly omitting the concluding sentence of a room description once), and **the patient prompt** (a single brief hesitation on the prompt line before accepting input).

## Non-Goals
- Never break the terminal layout or cause confusing crashes. §7.5 caveat: "Ambiguity between 'haunting' and 'buggy' destroys trust fast."
- Does not distort mechanical option choices.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §7.5 ("Quiet Horror Techniques: Small tricks that cost little and stick for years... Delayed echo... The missing line... The patient prompt... *Careful:* never break the frame in a way the player can't tell is intentional."), `screens/game.py`.
- **Files to create/modify:** `game/quiet_horror.py`, `screens/game.py`.
- **Frequency Constraints:** Max ONCE per run for each effect. Rarity is what makes them land.

## Preconditions
- [ ] Task F02 DONE.
- [ ] Baseline test suite clean.

## Actionable Steps
1. Create `game/quiet_horror.py`:
   - Dataclass `QuietHorrorTracker` with booleans: `echo_fired`, `missing_line_fired`, `patient_prompt_fired`.
   - Implement `check_delayed_echo(visited_rooms: set[str], turn_count: int) -> Optional[str]`:
     - If turn >= 15 and not fired, returns a sensory echo from a room seen early (e.g. "The faint smell of tallow and raw meat lingers here, though neither is present.").
   - Implement `should_omit_final_line(turn_count: int) -> bool`:
     - On a single specific turn (e.g. turn 25), gently trims the last sentence of the description.
   - Implement `should_hesitate_prompt(turn_count: int) -> bool`:
     - Once per run around turn 22, delays the cursor prompt blinking for 800ms before enabling selection.
2. In `screens/game.py`, connect `QuietHorrorTracker` to `RunState` and apply effects cleanly within the presentation lifecycle.

## Test Plan
- **Tests to write:** `tests/test_quiet_horror.py`:
  - `test_delayed_echo_triggers_at_most_once`: Asserts echo fires only once per run.
  - `test_missing_line_preserves_sentence_integrity`: Trims without malforming text.
  - `test_patient_prompt_does_not_hang_game`: Verifies hesitation completes cleanly and allows input.
- **Commands:** `python -m pytest tests/test_quiet_horror.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Delayed echo, missing line, and patient prompt implemented per §7.5.
- [ ] Capped to at most once per run.
- [ ] No ambiguity between horror effects and UI bugs.
- [ ] Tests pass cleanly.

## Rollback / Undo
Delete `game/quiet_horror.py` and revert edits to `screens/game.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
