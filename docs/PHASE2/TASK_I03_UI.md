# Task I03: Death screen with the "what you learned" line (§9.2)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: I — Persistence & Mercy
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: A11, E02
- Blocks: I04
- Covers: AC-15
- Suggested commit: `feat(ui): display cause of death and what you learned on the death screen`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Upgrade the Death Screen (`screens/death.py`) from a simple generic failure screen to §9.2's respectful death presentation, displaying: (1) exactly how you died in one clear sentence, and (2) what you learned from this demise (auto-extracted from the death lesson registered in the Journal).

## Non-Goals
- Does not render the difficulty-gated "what you could have done" hint line (that is I04).
- Does not alter font styling outside the established Textual gothic theme.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §9.2 ("Death Screen That Respects the Player: Never show just 'YOU LOSE.' Show: 1. How you died, in one sentence. 2. What you learned (auto-journal entry)... 4. 'Again' and 'Back to menu'"), Design Pillar 2 ("Every death is a lesson"), AC-15 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `screens/death.py`.
- **Files to read, not modify:** `game/journal.py`, `game/state.py`.
- **Conventions to respect:** Maintain clean Textual widget layout with clear visual hierarchy:
  - Header: Somber title ("THE SHADOWS TAKE YOU")
  - Cause of death: Highlighted in Amber or Dim Grey
  - Lesson learned: Highlighted in White or Cyan ("Lesson: ...")
  - Action buttons: "Try Again" (launches new run) and "Return to Menu"
- **Design constraints:**
  - Must never blame or mock the player; tone is respectful and somber.
  - If no explicit lesson was set, fallback to a sensible room-derived lesson ("The darkness here was absolute; heed the oil reserve").

## Preconditions
- [ ] A11 DONE — Initial death screen skeleton exists.
- [ ] E02 DONE — Death causes and lessons are logged into the Journal.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. In `screens/death.py`, accept `cause: str` and `lesson: str` parameters in the screen constructor.
2. Update the Textual layout with dedicated labels:
   - `#death-cause`: displays "How you died: <cause>"
   - `#death-lesson`: displays "What you learned: <lesson>"
3. Update "Try Again" button action to trigger a fresh run directly.
4. Update "Main Menu" button action to return to the title screen.
5. Apply styling adhering to §7.4 color grammar (dim grey for narrative, white for interactives).

## Test Plan
- **Tests to write/update:** `tests/test_death_screen_ui.py`:
  - `test_death_screen_renders_cause_and_lesson` — mounts screen and asserts cause and lesson widgets contain passed text strings.
  - `test_death_screen_buttons_present` — asserts 'Again' and 'Menu' action buttons exist and are focusable.
- **Commands:** `python -m pytest tests/test_death_screen_ui.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Death screen prominently displays the single-sentence cause of death.
- [ ] Death screen prominently displays the lesson learned.
- [ ] Buttons allow quick restart or returning to the main menu.
- [ ] Automated tests verify cause and lesson rendering.

## Rollback / Undo
Revert widget updates in `screens/death.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
