# Task E02: Ending screen

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: E — Honest Endings on Screen
- Layer: UI
- Status: TODO
- Estimate: ~2h
- Depends on: D05
- Blocks: E03
- Covers: AC-7
- Suggested commit: `feat(screens): add the ending screen`
- Branch: per GP-3

## Objective
Render the slice's one ending: the player leaves through the front door, and the screen tells them what they are leaving with. This replaces B03's commented ending placeholder and is the last thing a first-time player sees — so it is what they will judge the whole game by.

## Non-Goals
- Does not implement the ending *condition* (D05) — this task renders the result D05 produces.
- Does not implement multiple endings or variants by what the player understood (§2.3) — Phase 3.
- Does not implement the journal recap, statistics, run summary, or "what you missed" (§3.4, §9.2) — Phase 2.
- Does not implement the `Stay` ending or the memory fragments (§6) — Phase 3.
- Does not implement a credits roll, a score, a timer display, or a shareable result.
- Does not persist anything: the run ends and nothing is written.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.3's *The Quiet Exit* (the standard win: leaving through the front door — note that its tone, not its full text, is the target), §3.3 (what the BOOK's knowledge meant), §7.3 (the loop's closing beat), and `screens/game.py` (B03's commented ending placeholder, which this task replaces).
- **Files to create:** `screens/ending.py`.
- **Files to modify:** `screens/game.py` — replace the commented ending placeholder with a push of the real screen; remove the placeholder comment.
- **Files to read, not modify:** `game/effects.py` (the ending result D05 produces), `game/state.py`, `screens/death.py` (E01) — the two screens should feel like siblings, so mirror its structure and interaction shape rather than inventing a different one.
- **Conventions to respect:** PEP 8; type hints; `Screen` subclass; CSS in the class attribute; `BINDINGS` rendered into the footer; `self.app` for shared state.
- **Design constraints:**
  - **The result is structured data, not prose.** D05 supplies at minimum whether the book was read (and so whether the player understood what they escaped). The screen chooses the words; the result supplies the facts. Do not hardcode a single fixed ending paragraph that ignores the result.
  - **Phase 1 has one ending, but the ending must already respect its result.** If the result says the book was read, that must colour the text. This is a two-branch difference, not a variant system — Phase 3 expands it, and this task must leave the seam where it will expand rather than closing it off.
  - **Do not overstate.** §4.1's discipline applies to victory too: the ending must not claim the player solved something they did not, and must not promise a Phase 2 mechanic such as the Shadow or the journal. A player who finishes must not expect a feature that is not there.
  - **No red** (§7.4).
  - **The tone is quiet, not triumphant.** The baseline's win text ends the story with a shrug; §2.3's *Quiet Exit* is the model. Restraint.
  - **The screen must offer a way out:** back to the main menu, and optionally a fresh run. Neither may require typing (AC-8). Escape must dismiss.
  - The ending is terminal — there is no "return to the room" and no way back into a run that has ended.

## Preconditions
- [ ] D05 DONE — an ending result carrying at least the book-read state is produced
- [ ] B03's ending placeholder exists and is commented for replacement
- [ ] E01 DONE or in progress — the sibling screen's structure is settled, so the two do not diverge
- [ ] The app launches and the menu and settings screens still work

## Actionable Steps
1. Record the shape of D05's ending result and confirm the placeholder receives it.
2. Decide and record the screen's two text branches (book read / book not read) and the actions offered.
3. Create `screens/ending.py` with the screen class, its `CSS`, and its `BINDINGS`, mirroring E01's structure.
4. Render the branch selected by the result; do not render a fixed paragraph regardless of the result.
5. Implement the actions — back to the main menu, and a fresh run if offered — in the footer from the bindings.
6. Replace B03's commented ending placeholder in `screens/game.py` with the push of this screen, and delete the placeholder comment.
7. If a fresh run is offered, reuse E03's fresh-run construction path; do not duplicate construction logic.
8. Verify both branches by playing the game twice: once winning after reading the book, once by the shortest route that still wins if one exists; if the second is not reachable in Phase 1, record that and verify the branch's text by observation rather than by play.
9. Verify at ~60 columns that the ending text and the available actions remain visible.

## Test Plan
- **Tests to write:** E04's end-to-end checklist covers this screen, including the winning path. A screen test asserting the rendered text changes with the result belongs in E04; do not duplicate B05's harness here.
- **Commands:** `python index.py`, then play the winning path.
- **Expected:** the ending screen appears after the front door yields; its text reflects the result; the offered actions work; Escape dismisses; nothing claims a feature Phase 1 lacks.
- **Both-branches check (required):** render the screen with the book-read result and with the book-not-read result, and confirm the text differs and both read as complete endings rather than as an unfinished one.
- **No-promises check:** read the text against the README's phase notes and confirm it does not imply the Shadow, the journal, a save system, or any other deferred feature.
- **Placeholder check:** confirm no commented ending placeholder remains in `screens/game.py`.
- **Syntax check:** `python -m py_compile index.py screens/*.py`

## Definition of Done / Acceptance Criteria
- [ ] `screens/ending.py` exists and renders text selected by D05's structured result
- [ ] Both result branches are implemented and both read as complete endings
- [ ] The text makes no claim about a feature Phase 1 does not have
- [ ] A way back to the main menu is offered; no typing is required (AC-8)
- [ ] The ending is terminal — no route back into the ended run
- [ ] No red anywhere on the screen (§7.4)
- [ ] The screen is dismissible with Escape
- [ ] The ending placeholder in `screens/game.py` is replaced, with its comment removed
- [ ] Layout holds at ~60 columns
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. `screens/ending.py` is removed and the front door's win again routes to B03's placeholder; the ending result from D05 remains produced but unrendered. Verify the game still launches and the winning path does not crash.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the text-branch decision and the no-promises check here -->
