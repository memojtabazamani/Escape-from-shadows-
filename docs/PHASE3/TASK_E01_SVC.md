# Task E01: Player choice and action history tracking in `RunState`

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: E — Player History & Shadow Voice
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: GP-1
- Blocks: E02
- Covers: AC-19, §2.2
- Suggested commit: `feat(state): track significant player choices and narrative tags in RunState`
- Branch: feature/phase_3_the_shadow

## Objective
Extend `RunState` in `game/state.py` to record a structured chronology of significant narrative choices and actions made by the player (e.g. `took_cleaver`, `read_book_turn_1`, `chose_hall_left`, `stood_still_before_dog`, `examined_mirror`, `searched_floorboard`), providing the raw historical substrate needed by the Shadow dialogue engine (§2.2).

## Non-Goals
- Does not generate the second-person prose (handled in E02).
- Does not play audio bell cues (handled in E03).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.2 ("It speaks in the second person, and its dialogue is drawn from the player's own earlier choices. ('You went left in the hall. I remember.')"), `game/state.py`.
- **Files to modify:** `game/state.py`, `game/effects.py`.
- **Precedent:** Follows existing `visited`, `flags`, and `held_items` tracking patterns.

## Preconditions
- [ ] Baseline test suite clean.
- [ ] `RunState` model operational.

## Actionable Steps
1. In `game/state.py`:
   - Add field `choice_history: list[dict[str, Any]] = field(default_factory=list)` to `RunState`.
   - Each entry records: `{"turn": int, "choice_id": str, "action_tag": str, "room": str}`.
   - Add helper method `record_choice(choice_id: str, action_tag: str, room: str) -> None`:
     - Appends formatted entry to `choice_history`.
     - Caps history to the most recent 50 significant events to prevent unbounded growth.
   - Update `snapshot()` to serialize `choice_history`.
   - Update `restore(data)` to restore `choice_history` with empty list default.
2. In `game/effects.py`, in `resolve_choice()`:
   - When resolving choices with an `action_tag` or significant ID, automatically invoke `state.record_choice()`.

## Test Plan
- **Tests to write:** `tests/test_choice_history.py`:
  - `test_record_choice_appends_to_history`: Verifies choices are logged with turn and room.
  - `test_history_capped_at_fifty`: Verifies history cap prevents memory bloat.
  - `test_snapshot_restore_preserves_history`: Round-trip serialization preserves exact chronological order.
  - `test_effects_resolution_logs_choice`: Resolving choice in `effects.py` triggers logging.
- **Commands:** `python -m pytest tests/test_choice_history.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `RunState` records player choice history with turn, room, and action tags.
- [ ] Snapshot and restore serialize history without errors.
- [ ] Existing save file compatibility is preserved.
- [ ] Tests pass cleanly.

## Rollback / Undo
Revert additions to `game/state.py` and `game/effects.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
