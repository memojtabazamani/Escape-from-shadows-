# Task A11: Death screen and ending screen

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: UI
- Status: TODO
- Estimate: ~3.5h
- Depends on: A09, A10
- Blocks: A12, E02, I03
- Covers: AC-15, AC-21
- Suggested commit: `feat(ui): add the death and ending screens`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Give the run's two terminal states real screens: a death that states its cause and offers retry or menu, and an ending that closes the run properly.

## Non-Goals
- Does not implement the "what you learned" journal line — that is I03, which depends on E02's journal entry.
- Does not implement the greyed-out "what you could have done" line — that is I04; §9.2 binds it to difficulty. Build the frame so **I03 and I04 can add both lines without restructuring**, and say so in the log.
- Does not write journal entries — that is E02. This screen consumes what E02 records.
- Does not implement save/load — that is I01/I02. A11's "Back to menu" must not leave a resumable corpse, and I02 depends on that property holding.
- Does not implement difficulty-gated restart behaviour — that is B03.

## Context & Constraints
- **Read first:** §9.2 in full — "Never show just 'YOU LOSE.'" and its four-part structure — plus §7.3 (ASCII art is reserved for three moments only), §7.4's colour reservation, and §13's input-friction rule.
- **Files to create:** `screens/death.py` and `screens/ending.py` (both to be created).
- **Files to read, not modify:** `screens/game.py` (A03's death-tier placeholder, which these screens replace); `screens/main_menu.py` for the return-to-menu navigation precedent; `game/effects.py`'s `ChoiceResult` for the cause the death carries; `AGENTS.md` for the key conventions.
- **Conventions to respect:** `AGENTS.md` — screen logic in `screens/`, thin `compose()`, delegate rendering to helpers, `CSS` class attribute; Escape back, Enter select.
- **Design constraints:**
  - **The cause is displayed verbatim from structured data.** §9.2's first line is "how you died, in one sentence" — the screen renders it, it does not compose it.
  - **red is reserved** (§7.4: red appears only when the Shadow is present). Decide deliberately whether a death screen qualifies and **record the answer**; if yes, red appears on this screen and nowhere else.
  - **No ASCII art on the death screen.** §7.3 reserves art for the title, the Hell Dog, and each ending. The ending screen may use it; the death screen may not.
  - **"Again" and "Back to menu"** (§9.2 items 4) must both work, and "Back to menu" must leave nothing resumable.
  - Both screens must render correctly from the two room shapes A09 and A10 produce.
- **Voice:** the death screen is a lesson, not a punishment. It should feel like the house explaining itself, briefly.

## Preconditions
- [ ] A09 DONE — the death produces a result carrying a one-sentence cause
- [ ] A10 DONE — the ending produces a terminal result
- [ ] A03 DONE — the death-tier placeholder exists and is the thing being replaced
- [ ] A01's frame and CSS vocabulary are available to reuse
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `ChoiceResult` and the two terminal results A09 and A10 produce; note exactly which field carries the cause.
2. Create `screens/death.py`: render the cause verbatim as the first line, then a placeholder region for I03's "what you learned" and I04's "what you could have done", then the two actions.
3. Create `screens/ending.py`: render the ending's prose and a single clear action back to the menu.
4. Wire "Again" to start a fresh run and "Back to menu" to return, reusing `main_menu.py`'s navigation pattern.
5. Ensure "Back to menu" clears any resumable state — I02 depends on a death leaving nothing to continue.
6. Replace A03's placeholder routing so both terminal tiers land on their real screens.
7. Decide the red question explicitly and record it.
8. Test each screen with a long cause string and a short one, and at a narrow terminal width.

## Test Plan
- **Tests to write/update:** new `tests/test_terminal_screens.py` (to be created):
  - `test_death_screen_shows_the_cause_verbatim` — asserts the rendered text contains the structured cause.
  - `test_death_screen_offers_again_and_menu` — asserts both actions exist and are selectable.
  - `test_back_to_menu_leaves_no_resumable_state` — asserts nothing is left for I02 to continue.
  - `test_ending_screen_shows_the_ending_and_returns` — asserts prose renders and the menu action works.
  - `test_death_screen_uses_no_ascii_art` — guards §7.3's rarity rule mechanically.
- **Commands:** `python -m pytest tests/test_terminal_screens.py -v`; then `python -m pytest`.
- **Manual verification:** die once and finish once; confirm each screen tells you what happened and what you can do next, without a dead end.
- **Readability check:** confirm both screens fit one terminal without scrolling at a narrow width.

## Definition of Done / Acceptance Criteria
- [ ] The death screen states the cause verbatim from structured data, not from screen-authored prose
- [ ] The death screen offers both "Again" and "Back to menu", and both work
- [ ] "Back to menu" after a death leaves nothing resumable
- [ ] The ending screen renders its prose and closes the run cleanly
- [ ] The death screen contains no ASCII art
- [ ] The red-styling question is decided and recorded
- [ ] Both screens fit one terminal at a narrow width
- [ ] The frame accommodates I03's and I04's lines without restructuring
- [ ] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; A03's placeholder routing returns and terminal states are unreadable but non-crashing. A12, E02 and I03 all depend on these screens existing — revert as a group.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the red-styling decision and the frame's reserved regions here -->
