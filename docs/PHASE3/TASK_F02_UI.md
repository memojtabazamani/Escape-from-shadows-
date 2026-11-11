# Task F02: Visual grammar: strict Red color rule (`#e63946`) for Shadow presence (§7.4)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: F — Dread Counter & Quiet Horror Presentation
- Layer: UI
- Status: TODO
- Estimate: ~2.5h
- Depends on: F01, D03
- Blocks: F03
- Covers: AC-23, §7.4
- Suggested commit: `style(grammar): enforce strict red color rule exclusively for Shadow presence`
- Branch: feature/phase_3_the_shadow

## Objective
Enforce the visual grammar law established in `docs/SUGGEST.md` §7.4: "Red: ONLY when the Shadow is present. If red appears exactly four times in a whole playthrough, it will terrify people." Ensure no general gore or status text uses red, confining red styling (`#e63946` / `[red]`) strictly to Shadow manifestation moments.

## Non-Goals
- Does not change other color assignments (Dim grey = description, White = interactable, Cyan = actions, Amber = light/resources).
- Does not add red to the Blood Kitchen title or descriptions.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §7.4 ("Color as Grammar: Don't color for decoration — color for *meaning*... Red: *ONLY* when the Shadow is present."), `screens/game.py`.
- **Files to modify:** `screens/game.py`, `screens/death.py`, `data/content.json`.
- **Audit Requirement:** Scan existing CSS and markup templates across screens to confirm red (`#ff0000`, `#e63946`, `[red]`) is not used for health, inventory, or room titles.

## Preconditions
- [ ] Task F01 DONE.
- [ ] Working tree clean.

## Actionable Steps
1. Audit `screens/game.py`, `screens/death.py`, and `screens/main_menu.py` for any stray red markup.
2. In `screens/game.py`:
   - Define semantic styling class `.shadow-manifestation { color: #e63946; text-style: bold; }`.
   - Apply red markup ONLY to:
     1. Shadow whispers generated from history.
     2. Zero-oil Shadow breach warnings.
     3. Direct threshold absence text when the Shadow is actively blocking an unlit passage.
3. Author a test lint ensuring non-shadow prose in `data/content.json` does not contain `[red]` tags.

## Test Plan
- **Tests to write:** `tests/test_color_grammar.py`:
  - `test_content_json_has_no_illegal_red_tags`: Asserts standard room prose never uses `[red]`.
  - `test_shadow_whispers_use_shadow_red`: Verifies Shadow whispers format with `#e63946`.
  - `test_status_zone_uses_amber_not_red_for_low_oil`: Low oil remains Amber (`#d4a373`), not red.
- **Commands:** `python -m pytest tests/test_color_grammar.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Red color is exclusively restricted to Shadow moments per §7.4.
- [ ] Low-oil warnings remain amber per visual grammar table.
- [ ] Color grammar lint test passes.

## Rollback / Undo
Revert CSS and markup changes.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
