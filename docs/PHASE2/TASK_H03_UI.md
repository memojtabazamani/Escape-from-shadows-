# Task H03: Instant text and reduce-motion path (§5.3, §8)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: H — Sound & Music Made Real
- Layer: UI
- Status: TODO
- Estimate: ~2.5h
- Depends on: H02
- Blocks: H04
- Covers: AC-19, AC-24
- Suggested commit: `feat(ui): implement instant-text and flat-layout path when music is disabled`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Ensure that turning the persisted `Music` setting OFF acts as a full "Reduce Motion & Instant Text" mode (§5.3, §8): narrative text appears instantaneously with zero delays, border pulsing is completely disabled, and layout remains flat, static, and accessibility-friendly.

## Non-Goals
- Does not change game content or difficulty numbers.
- Does not alter font sizes or terminal emulator settings.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §5.3 ("Music OFF: text appears instantly, layout is static and flat. That makes the toggle a genuine presentation choice, and it doubles as an accessibility option for players who need instant text"), §8 (Accessibility & Comfort), AC-19 and AC-24 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `screens/game.py`.
- **Files to read, not modify:** `config.py`.
- **Conventions to respect:** The instant path must be immediate and branchless; when `music == False`, no timers or async animations should ever be instantiated.
- **Design constraints:**
  - When `music == False`:
    - Zero typewriter delay (the entire prose is mounted/updated in one frame).
    - Zero CSS pulsing animations or interval timers.
    - All choices are immediately selectable without waiting.
  - Toggling `Music` in Settings screen takes effect immediately on returning to gameplay.

## Preconditions
- [ ] H02 DONE — Typewriter and pulsing live in `screens/game.py`.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. In `screens/game.py`, ensure prose rendering checks `self.app.config.get("music", True)`.
2. When `music is False`:
   - Directly set prose widget text immediately.
   - Do not schedule interval timers or border transitions.
   - Remove any animated CSS classes from container widgets.
3. Verify that rapid navigation between rooms remains instantaneous and completely flicker-free.
4. Ensure switching Music in Settings updates the active behavior upon resuming the game screen.

## Test Plan
- **Tests to write/update:** `tests/test_instant_text_accessibility.py`:
  - `test_instant_text_when_music_disabled` — verifies prose is fully rendered on first render tick when music is False.
  - `test_no_timers_created_when_music_disabled` — verifies zero timer objects created when music is False.
- **Commands:** `python -m pytest tests/test_instant_text_accessibility.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Music OFF immediately produces instant prose delivery.
- [ ] Zero animations, pulse intervals, or delays exist when Music is OFF.
- [ ] Serves as a full reduce-motion / screen-reader friendly accessibility mode.
- [ ] Automated tests verify instantaneous text update.

## Rollback / Undo
Revert instant-text branch in `screens/game.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
