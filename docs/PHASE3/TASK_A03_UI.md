# Task A03: Endings Gallery screen (`screens/gallery.py`)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: A — Meta-Progression & The Endings Gallery
- Layer: UI
- Status: DONE
- Estimate: ~3.5h
- Depends on: A02
- Blocks: A04
- Covers: AC-2, §9.4
- Suggested commit: `feat(ui): create Endings Gallery screen with silhouette cards and tally`
- Branch: feature/phase_3_the_shadow

## Objective
Create a dedicated Textual screen `screens/gallery.py` (`EndingsGalleryScreen`) that displays all 7 endings as silhouettes or unlocked entries, displaying the discovery count ("3 of 7 unlocked"), detailed summaries for discovered endings, and cryptic hints for locked ones per §9.4.

## Non-Goals
- Does not wire the Main Menu button (handled in A04).
- Does not render large ASCII art vignettes in the gallery list itself (detailed view or ending screen handles this).
- Does not mutate profile state (read-only view of unlocked endings).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §9.4 ("The Endings Gallery: A screen listing all endings as silhouettes: the ones you got are named, the ones you missed are just counts ('3 of 7'). Achievements without the pop-up gamification — just a quiet record of what you've seen."), `screens/journal.py` (modal/screen layout precedent).
- **Files to create:** `screens/gallery.py`.
- **Files to read:** `game/profile.py`, `game/endings.py`.
- **Styling constraints:** Consistent terminal aesthetic: dark background (`#0d0d0d`), dim grey for locked entries (`#555555`), white/cyan for unlocked entries, amber highlight for tally. Supports Up/Down navigation, Enter for details, Escape to close.

## Preconditions
- [x] Task A01 and A02 DONE (`game/profile.py` and `game/endings.py` ready).
- [x] Clean working tree.

## Actionable Steps
1. Create `screens/gallery.py` inheriting from `textual.screen.Screen`.
2. Implement header zone with title: `ENDINGS GALLERY` and dynamic tally: `DISCOVERED: X OF 7`.
3. In scrollable/cursor-driven list, render each of the 7 endings:
   - If unlocked: Display index, official title, narrative tone, and full summary.
   - If locked: Display index, cryptic silhouette label (e.g. `[ ? ? ? ]`), and hint teaser.
4. Implement keyboard bindings: `up` / `down` to navigate cards, `enter` to view expanded description, `escape` to pop screen.
5. Provide helper factory or constructor accepting optional `PlayerProfile` instance (falling back to `load_profile()`).

## Test Plan
- **Tests to write:** `tests/test_gallery_ui.py`:
  - `test_gallery_renders_all_seven_cards`: Asserts 7 cards are rendered in order.
  - `test_gallery_shows_unlocked_vs_locked_styling`: Asserts unlocked endings display titles while locked show silhouettes.
  - `test_gallery_tally_calculation`: Verifies "X OF 7" reflects the provided profile.
- **Commands:** `python -m pytest tests/test_gallery_ui.py -v`.

## Definition of Done / Acceptance Criteria
- [x] `screens/gallery.py` exists and mounts cleanly without UI errors.
- [x] All 7 endings are listed with correct locked/unlocked visual distinction per §9.4.
- [x] Keyboard navigation (Up, Down, Escape) works seamlessly.
- [x] Tests in `tests/test_gallery_ui.py` pass.

## Rollback / Undo
Delete `screens/gallery.py` and `tests/test_gallery_ui.py`.

## Execution Log
- **Date:** 2026-11-11
- **Agent:** Antigravity (Coding Worker)
- **Branch:** `feature/phase_3_the_shadow`
- **Implemented:** `screens/gallery.py` with `EndingsGalleryScreen`, tally display (`DISCOVERED: X OF 7`), locked silhouette masking (`[ ? ? ? ? ? ? ? ? ]`), unlocked title/summary revelation, cursor navigation with Up/Down/Enter/Escape, and comprehensive unit tests in `tests/test_gallery_ui.py`.
- **Review & Hardening:** Fixed dead code where pressing Enter did not alter details; wired expanded view revealing criteria hints for unlocked endings and exploration prompts for locked ones. Fixed vertical scroll desynchronization on cursor movement and guarded against modulo zero.
