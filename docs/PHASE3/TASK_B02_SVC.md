# Task B02: Ending resolution engine (`game/ending_resolver.py`)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: B — The Multiple Endings Spectrum
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: B01
- Blocks: B04, B05, B06, C03
- Covers: AC-4, AC-6, AC-7, AC-8, AC-9, §2.3
- Suggested commit: `feat(engine): implement ending resolution evaluator based on run state`
- Branch: feature/phase_3_the_shadow

## Objective
Implement an ending resolution engine in `game/ending_resolver.py` that inspects the player's final `RunState` and context to determine precisely which of the 7 canonical endings should trigger upon reaching terminal events.

## Non-Goals
- Does not modify screens directly (handled in B04).
- Does not alter memory fragment collection logic (handled in Slice C).
- Does not author ending text (already completed in B01).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.3 (Resolution hierarchy).
- **Files to create:** `game/ending_resolver.py`.
- **Files to read:** `game/state.py`, `game/endings.py`.
- **Precedence Hierarchy:**
  When escaping through the front door / yard exit:
  1. If player has all 3 memory fragments (`has_all_memory_fragments`) -> `homecoming` (Secret / highest precedence).
  2. If player escaped with `lantern == 0` -> `the_new_shadow`.
  3. If player has read The Book (`has_flag("read_the_book")` / 3-turn read) -> `what_the_book_knew`.
  4. If player pacified dog with meat and slipped past (`has_flag("fed_dog_meat")` and not tamed with whistle) -> `meat_and_silence`.
  5. Default successful exit with key -> `the_quiet_exit`.
  For choice branches:
  - If player explicitly chooses not to leave at the open door -> `stay`.
  - If player dies within their first room visit in the Hall -> `the_long_walk`.

## Preconditions
- [ ] Task B01 DONE (`data/content.json` has ending records).
- [ ] `RunState` model is accessible.

## Actionable Steps
1. Create `game/ending_resolver.py`.
2. Implement `resolve_escape_ending(state: RunState) -> str`:
   - Checks memory fragments (3/3) -> `"homecoming"`.
   - Checks `state.lantern <= 0` -> `"the_new_shadow"`.
   - Checks `state.flags` for `"read_the_book"` -> `"what_the_book_knew"`.
   - Checks `state.flags` for `"fed_dog_meat"` and `"dog_distracted"` -> `"meat_and_silence"`.
   - Otherwise -> `"the_quiet_exit"`.
3. Implement `resolve_terminal_event(state: RunState, trigger: str) -> str`:
   - Handles `"door_escape"` via `resolve_escape_ending`.
   - Handles `"refuse_exit"` -> `"stay"`.
   - Handles `"hall_death"` when `state.turn_count <= 3` and `len(state.visited) <= 1` -> `"the_long_walk"`.
4. Provide unit tests asserting every precedence branch.

## Test Plan
- **Tests to write:** `tests/test_ending_resolver.py`:
  - `test_resolve_quiet_exit_by_default`: Standard exit resolves to "the_quiet_exit".
  - `test_resolve_what_the_book_knew`: Having read book resolves to "what_the_book_knew".
  - `test_resolve_the_new_shadow_zero_oil`: Escaping with 0 oil resolves to "the_new_shadow".
  - `test_resolve_meat_and_silence`: Escaping after feeding meat resolves to "meat_and_silence".
  - `test_resolve_homecoming_precedence`: 3 memory fragments supersedes book and zero oil.
  - `test_resolve_stay_choice`: Refusing exit resolves to "stay".
- **Commands:** `python -m pytest tests/test_ending_resolver.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/ending_resolver.py` cleanly maps `RunState` conditions to ending IDs.
- [ ] Precedence order is strictly enforced without ambiguity.
- [ ] 100% test coverage on all resolution branches.

## Rollback / Undo
Delete `game/ending_resolver.py` and `tests/test_ending_resolver.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
