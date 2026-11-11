# Task H02: Visual rhythm: typewriter and pulsing tied to Music (§5.3, §7.2)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: H — Sound & Music Made Real
- Layer: UI
- Status: DONE
- Estimate: ~3h
- Depends on: A02
- Blocks: H03
- Covers: AC-19, AC-24
- Suggested commit: `feat(ui): implement visual rhythm typewriter reveal and border pulsing tied to music setting`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Implement "Visual Rhythm" for the terminal game governed by the persisted `Music` setting (§5.3): when Music is ON, room narrative text types out smoothly character-by-character (typewriter reveal with any-key skip) and screen borders pulse subtly on a slow heartbeat cadence.

## Non-Goals
- Does not play audio synthesizers or MIDI music.
- Does not block user input: pressing any key or Enter immediately completes the typewriter reveal.
- Does not implement instant-text or reduce-motion bypass — that is H03.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §5.3 ("Music: There's no audio pipeline in a plain terminal — so define 'music' as visual rhythm: Music ON: text types out character by character, panel borders pulse on a slow beat..."), §7.2 (Typewriter text), AC-19 and AC-24 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `screens/game.py`.
- **Files to read, not modify:** `config.py` (`SettingsManager`).
- **Conventions to respect:** Use Textual's timer APIs (`set_interval`, `set_timer`) and CSS classes for pulsing effects. Respect Textual's reactive rendering model.
- **Design constraints:**
  - Typewriter reveal must feel natural, eerie, and responsive (~15-25ms per character).
  - Any keypress during typewriter immediately finishes the line and unlocks choices.
  - Slow rhythmic border pulse (e.g. oscillating between two subtle gothic border colors or opacity levels).
  - Controlled 100% by `self.app.config.get("music", True)`.

## Preconditions
- [ ] A02 DONE — Room prose rendering path established in `screens/game.py`.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. In `screens/game.py`, add typewriter reveal logic to the scene prose widget.
2. If `self.app.config.get("music", True)` is True:
   - Stream text into the description widget via a recurring timer.
   - If player presses any key or navigates, immediately cancel timer and display full text.
3. Add a CSS heartbeat class to the scene panel that toggles subtle border tint on a 1.5s interval.
4. Clean up active timers on screen unmount to prevent leaks.
5. Provide manual verification in interactive run.

## Test Plan
- **Tests to write/update:** `tests/test_visual_rhythm.py`:
  - `test_typewriter_active_when_music_enabled` — verifies timer is initiated when music is True.
  - `test_typewriter_skip_on_keypress` — verifies full text immediately visible upon key press event.
  - `test_timer_cleanup_on_unmount` — verifies zero orphaned timers on screen dismiss.
- **Commands:** `python -m pytest tests/test_visual_rhythm.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Typewriter prose reveal operates smoothly when Music is ON.
- [ ] Pressing any key instantaneously reveals all text.
- [ ] Border pulsing provides an atmospheric visual rhythm.
- [ ] All timers clean up cleanly on unmount.
- [ ] Automated tests pass cleanly.

## Rollback / Undo
Revert typewriter and animation timers in `screens/game.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
