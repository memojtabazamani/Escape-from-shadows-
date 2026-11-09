# Task A03: Selectable choices, requirement gating, room transition

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: A02
- Blocks: A05, A08
- Covers: AC-1, AC-22
- Suggested commit: `feat(ui): add selectable choices and room transitions`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Let the player pick a choice with the keyboard, resolve it through the existing effect resolver, and move to the destination room — with selectable options only, never typed letters.

## Non-Goals
- Does not implement lantern drain — A05 owns the oil rules; this task only applies whatever effects the resolver returns.
- Does not author the HALL or the LIBRARY content — those are A07 and A08.
- Does not build the death or ending screens — that is A11. A death-tier destination is reachable here and routed, but its presentation is A11's.
- Does not implement HARD's expiring choices — that is B05.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §13 — "**Input friction.** Requiring players to type letters is a fine retro flourish, but pair it with selectable options — **a mistyped key should never be a death**" — plus §4.1's three-tier consequence model (`Scar`, `Setback`, `Death`) and §11's "conditionals become requirements".
- **Files to modify:** `screens/game.py` (from A01/A02).
- **Files to read, not modify:** `game/effects.py` — `resolve_choice(choice, state) -> ChoiceResult(destination, tier, applied, refused, reason)`, and its `check_requirements` / `apply_effects` halves; `game/content_schema.py` for the choice record shape (`id`, `label`, `destination`, `tier`, `telegraphs`, `requirements`, `effects`); `game/state.py`.
- **Conventions to respect:** `AGENTS.md` key conventions — ↑/↓ navigate, Enter select, Escape back — and the `main_menu.py` precedent for a cursor-driven list with a render helper.
- **Design constraints:**
  - **Selectable only.** Arrow keys move a cursor, Enter selects. Typed letters may be accepted as an *additional* affordance but must never be the only way, and a wrong key must never kill.
  - **Requirements are gates, not warnings.** A refused choice stays visible with its reason (the resolver's `reason` string, e.g. `requires item 'book'`) and does nothing when chosen. It must never end the run.
  - **Telegraphs are shown before the choice**, per §4.2 — the warning belongs to the room, not to the consequence. Rendering them here is what makes A09's death honest.
  - Effects are applied through `resolve_choice`; the screen must not mutate the run state directly.
- **Voice:** choice labels are the player's own actions, in cyan (§7.4), phrased as things the player does.

## Preconditions
- [ ] A02 DONE — rooms render from content and a room-lookup helper exists
- [ ] `game/effects.py` exposes `resolve_choice` with the `ChoiceResult` contract
- [ ] The content set validates clean via `validate_content()`
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `resolve_choice` and `ChoiceResult` in `game/effects.py`; note that `refused` is True when a requirement failed and that no effect is applied in that case.
2. Render each choice in the room as a selectable line, using the `main_menu.py` cursor pattern (index, `render_*` helper, `update_*` helper).
3. Render each choice's `telegraphs` in the scene zone before the choice list, so warnings precede the decision.
4. On Enter, call `resolve_choice(choice, state)`.
5. If `refused`, display `reason` in the status zone and stay in the room — do not move, do not end the run.
6. If not refused, update the run's current room to `ChoiceResult.destination`, record the visit, advance the turn, and re-render.
7. Route the three tiers: `scar` and `setback` continue play; `death` moves to the death path placeholder. A11 replaces the placeholder with the real screen.
8. Confirm a room with zero choices renders without a cursor and does not accept Enter as a transition.
9. Walk the SAMPLE_CONTENT graph by hand: `hall` → `old_library` → `hall`, and `hall` → the death destination.

## Test Plan
- **Tests to write/update:** extend `tests/test_game_screen.py`:
  - `test_arrow_keys_move_the_choice_cursor` — asserts selection changes and wraps.
  - `test_selecting_a_choice_moves_to_its_destination` — asserts the rendered room matches the choice's `destination`.
  - `test_refused_choice_shows_reason_and_does_not_move` — uses a choice with an unsatisfied requirement; asserts the room is unchanged and a reason is shown.
  - `test_unselectable_choice_never_ends_the_run` — asserts a refused choice leaves the run alive.
- **Commands:** `python -m pytest tests/test_game_screen.py -v`; then `python -m pytest`.
- **Manual verification:** navigate with the arrow keys only and complete a two-room loop without typing a single letter. Then press a wrong letter and confirm nothing happens.

## Definition of Done / Acceptance Criteria
- [ ] Every choice is selectable with the keyboard; no action requires typing
- [ ] A mistyped key cannot cause a transition, an effect, or a death
- [ ] Telegraphs render before the choice is offered
- [ ] A refused choice displays its reason and leaves the run state untouched
- [ ] Effects are applied only through `resolve_choice`, never by the screen directly
- [ ] Room transitions update the run state's current room and turn count
- [ ] A room with no choices renders and does not accept Enter as a transition
- [ ] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; the screen renders rooms (A02) but the player cannot move. A05, A08 and the rest of Slices C–G all assume transitions exist — revert together with A02 or not at all.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
