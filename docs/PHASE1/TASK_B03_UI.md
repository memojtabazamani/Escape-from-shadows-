# Task B03: Selectable choices and room transition

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: B — The Screen
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: B02
- Blocks: B05, C01, E03
- Covers: AC-1, AC-8, AC-9
- Suggested commit: `feat(screens): add selectable choices and room transitions`
- Branch: per GP-3

## Objective
Let the player actually play: list a room's choices as selectable rows, move the selection with the arrow keys, and on Enter evaluate the choice through the resolver and move to the destination room. This is the moment the slice becomes a game rather than a display.

## Non-Goals
- Does not display the meters (B04).
- Does not implement lantern drain or any cost arithmetic (Slice C) — costs are applied through the resolver, but the *rates* are C01's.
- Does not implement the death or ending screens (Slice E) — both tiers route to clearly marked placeholders.
- Does not keep the baseline's letter-typing as the input method (ASM-7 / §13).
- Does not write real room content (Slice D).

## Context & Constraints
- **Read first:** `screens/game.py` (B01, B02), `game/effects.py` (A05's resolver: requirement check, effect application, tier reporting), `game/state.py`, `docs/SUGGEST.md` §13 ("input friction": selectable options are required; **a mistyped key must never be a death**).
- **Files to modify:** `screens/game.py` — the choice list and the selection action.
- **Files to read, not modify:** `screens/main_menu.py` and `screens/settings.py` — reuse the same selection interaction shape already used there rather than inventing a third pattern.
- **Conventions to respect:** PEP 8; type hints; selection state as a screen attribute updated through helper methods; `BINDINGS` for up/down/enter/escape; the footer already derives from the bindings (B01).
- **Design constraints:**
  - Choices are styled cyan as the player's own options (§7.4). No red.
  - **Order of operations is fixed and must not be reordered:** check requirement → if refused, show the reason and change nothing → if permitted, apply effects → then transition. Applying before checking is a defect.
  - A refused choice must change **no** state — this is exactly what A05's side-effect-free requirement check guarantees, and this task must not bypass it.
  - **Tier routing is explicit:** a Death-tier choice routes to a placeholder for Slice E; a Scar or Setback choice continues normally. Both placeholders must be commented as temporary.
  - Selection must wrap, matching the menu and settings screens' existing behavior.
  - The choice list is generated from the room record; no choice labels are hardcoded in the screen.

## Preconditions
- [ ] B02 DONE — a room renders from content
- [ ] A05 DONE — requirements, effects, and tiers resolve
- [ ] The sample content set contains at least one choice that is permitted and one that is refused, so both paths are observable

## Actionable Steps
1. Implement choice rendering in the status or scene zone: each choice's label, from the room record, styled cyan.
2. Implement selection state and movement with wrap-around, reusing the menu screen's interaction shape.
3. Implement the selection action in the fixed order: resolve the requirement; on refusal, show the reason and stop; on success, apply the effects.
4. Implement the transition: look up the destination room and re-render the scene zone through B02's renderer.
5. Implement tier routing: Scar and Setback continue; Death routes to a clearly commented placeholder.
6. Add a commented placeholder for the ending so Slice D's win has somewhere to land; mark it for E02.
7. Verify a refused choice leaves state untouched, using a snapshot comparison around the attempt.
8. Play several transitions in a row and confirm the screen re-renders correctly each time with no stale choice rows.

## Test Plan
- **Tests to write:** B05 owns the transition-sequencing test (a refused choice applies nothing; a permitted choice applies exactly its effects and lands on the right room).
- **Commands:** `python index.py`
- **Expected:** choices list from content; ↑/↓ move and wrap; Enter on a permitted choice moves rooms and re-renders; Enter on a refused choice shows the reason and changes nothing; Escape returns to the menu.
- **Snapshot check:** capture run state, attempt a refused choice, capture again, confirm the two are identical.
- **Content-only check (AC-9):** add a choice to the sample content only, restart, and confirm it appears in the list and works. Then revert.
- **Manual:** confirm no state changes and no transition occur on a refused choice.

## Definition of Done / Acceptance Criteria
- [ ] Choices render as selectable rows from content, styled cyan
- [ ] Selection moves and wraps; Enter selects
- [ ] The order check → refuse-or-apply → transition is enforced
- [ ] A refused choice provably changes no state
- [ ] Scar and Setback continue; Death routes to a commented placeholder
- [ ] An ending placeholder exists and is commented for E02
- [ ] No choice labels are hardcoded in the screen
- [ ] Typing is never required to make a choice (AC-8)
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. The scene zone still renders a room from B02, but choices are no longer listed or selectable; the sample content and resolver are unaffected.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
