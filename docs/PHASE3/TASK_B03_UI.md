# Task B03: ASCII art vignettes for all endings (§7.3)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: B — The Multiple Endings Spectrum
- Layer: UI
- Status: DONE
- Estimate: ~3h
- Depends on: B01
- Blocks: B04
- Covers: AC-12, §7.3
- Suggested commit: `feat(art): design minimalist ASCII vignettes for each canonical ending`
- Branch: feature/phase_3_the_shadow

## Objective
Author clean, evocative, minimalist ASCII art vignettes (<= 8 lines high, <= 60 chars wide) in `game/endings_art.py` for each of the 7 canonical endings, fulfilling the §7.3 design principle: "Reserve ASCII art for three moments only: the title screen, the Hell Dog, and each ending. Rarity is what makes it land."

## Non-Goals
- Does not create animated ASCII art or color sequences.
- Does not add ASCII art to standard room descriptions (forbidden by §7.3).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §7.3 ("ASCII Art: Reserve ASCII art for three moments only... A dog rendered in forty characters is scarier than a paragraph describing one."), `screens/ending.py`.
- **Files to create:** `game/endings_art.py`.
- **Formatting constraints:** Max width 60 columns, max height 8 lines. Pure ASCII characters (no wide Unicode emojis that break monospace terminal layouts). Minimalist and evocative.

## Preconditions
- [x] Canonical ending IDs established in Task A02/B01.
- [x] Clean working tree.

## Actionable Steps
1. Create `game/endings_art.py`.
2. Author distinct ASCII vignettes for each canonical ending:
   - `the_long_walk`: Stone floor threshold and a fading silhouette.
   - `meat_and_silence`: Chained collar slack on gravel beside bone.
   - `the_quiet_exit`: Heavy iron gate slightly open to a starless horizon.
   - `what_the_book_knew`: The open black grimoire with an unblinking eye glyph.
   - `the_new_shadow`: Twin long shadows cast against an empty wall.
   - `homecoming`: A small framed photograph with a light beam across it.
   - `stay`: Heavy door bolted from inside with key turned in the lock.
3. Expose lookup function `get_ending_ascii(ending_id: str) -> str`.
4. Provide fallback marker string if an unknown ending is queried.

## Test Plan
- **Tests to write:** `tests/test_endings_art.py`:
  - `test_all_endings_have_ascii_art`: Verifies each of the 7 IDs returns a non-empty art string.
  - `test_ascii_dimensions_within_budget`: Verifies every art string has width <= 60 and height <= 8 lines.
  - `test_unknown_ending_returns_fallback`: Returns a safe default marker.
- **Commands:** `python -m pytest tests/test_endings_art.py -v`.

## Definition of Done / Acceptance Criteria
- [x] `game/endings_art.py` contains 7 unique ASCII vignettes.
- [x] Dimensions conform strictly to terminal constraints (<= 60 cols, <= 8 rows).
- [x] Tests verify all dimensions and lookup safety.

## Rollback / Undo
Delete `game/endings_art.py` and `tests/test_endings_art.py`.

## Execution Log
- 2026-11-11: Antigravity subagent authored 7 pure ASCII art vignettes in `game/endings_art.py` with `get_ending_ascii()`, strictly capped to <= 8 lines high and <= 60 cols wide.
- Verified with `tests/test_endings_art.py`: 3/3 tests passing.
