# Task E03: Journal screen, keybound overlay

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: E — The Journal
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: E01
- Blocks: E04
- Covers: AC-12
- Suggested commit: `feat(ui): add journal modal overlay screen bound to key 'j'`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Create a Textual screen (`screens/journal.py`) accessible via a keybind (such as `j` or `J`) during gameplay that displays recorded room discoveries, deaths witnessed, and Shadow whispers in an atmospheric, readable journal notebook.

## Non-Goals
- Does not modify room content or gameplay turn mechanics.
- Opening/closing the journal does not advance turn counters or drain lantern oil (it is a pause-safe reading overlay).
- Does not edit or delete entries (journal is strictly append/read-only).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.4, §7.1 (Screen layout and footer key hints), §7.4 (Color grammar).
- **Files to create:** `screens/journal.py`.
- **Files to modify:** `screens/game.py` (bind `j` to push `JournalScreen`, update footer key hints).
- **Files to read, not modify:** `game/journal.py`, `screens/game.py`.
- **Conventions to respect:** Inherit from `textual.screen.ModalScreen` or `textual.screen.Screen`. Follow Textual CSS styling conventions established in `screens/game.py` and `screens/settings.py`. Use Dim Grey for narration and White for titles.
- **Design constraints:**
  - Navigable with Up/Down arrow keys and dismissible with `Escape` or `j`.
  - Must display an empty-state message if no discoveries have been logged yet ("The pages are blank...").
  - Must remain responsive and clean even with dozens of entries.

## Preconditions
- [ ] E01 DONE — Journal data structure is accessible on `RunState`.
- [ ] A01 DONE — Gameplay screen handles input bindings.
- [ ] `python -m pytest` passes cleanly.

## Actionable Steps
1. Create `screens/journal.py` subclassing `Screen` or `ModalScreen`.
2. Define a clean Textual layout: Title header ("THE JOURNAL"), category tabs or sectioned scrollable body, and footer ("Press [Escape] or [J] to return").
3. Compose widgets showing categorized journal entries:
   - Visited rooms (Room titles + discovery summaries)
   - Lessons learned from past demises
   - Captured Shadow whispers
4. Style the screen using Textual CSS adhering to the dark gothic palette (consistent with `game.py`).
5. In `screens/game.py`, bind the `j` key to push `JournalScreen`.
6. Add `[J] Journal` hint to the footer zone in `screens/game.py`.

## Test Plan
- **Tests to write/update:** `tests/test_journal_ui.py`:
  - `test_journal_screen_mounts_cleanly` — instantiating `JournalScreen` with populated entries renders without widget errors.
  - `test_journal_screen_empty_state` — mounting `JournalScreen` with an empty journal renders the graceful blank-pages message.
  - `test_journal_keybind_registered` — verifying action handler exists on `GameScreen`.
- **Manual verification:** Run `python index.py`, start game, press `j` to view journal, verify sections, press `Escape` to resume seamlessly.

## Definition of Done / Acceptance Criteria
- [ ] Pressing `j` in gameplay opens the journal overlay.
- [ ] Pressing `Escape` or `j` returns seamlessly to the exact game state without advancing the turn counter.
- [ ] Recorded room notes, death lessons, and Shadow whispers are cleanly separated and easy to read.
- [ ] Footer in gameplay displays the `[J] Journal` key hint.
- [ ] Textual styling matches the project's color palette.

## Rollback / Undo
Delete `screens/journal.py` and revert keybinding additions in `screens/game.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
