# Task E02: Journal writes on room entry and on death

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: E — The Journal
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: E01, A11
- Blocks: E04, I03
- Covers: AC-12, AC-15
- Suggested commit: `feat(journal): record discoveries on room entry and lessons on death`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Hook the journal into room transition events and death triggers so that entering a new room records the discovery, hearing a Shadow taunt logs the whisper, and suffering a fatal end logs the specific death lesson into the player's journal.

## Non-Goals
- Does not render the journal UI overlay or notebook screen — that is E03.
- Does not modify death screen layout or buttons — that is A11 and I03.
- Does not author the four reworked rooms' prose — that is Slice F.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.4, §9.2 (Death screen that teaches), and AC-12 & AC-15 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `screens/game.py` (hook room entry), `game/effects.py` (hook death effect or shadow line logging), `game/content_schema.py` (ensure room schema supports optional `journal_note` or defaults to room title/summary).
- **Files to read, not modify:** `game/journal.py`, `game/state.py`, `screens/death.py`.
- **Conventions to respect:** Hooking logic must happen through engine effect resolution or explicit screen transition dispatchers, keeping presentation code decoupled from data storage.
- **Design constraints:**
  - Room discovery must be logged on first entry without spamming logs on subsequent returns.
  - Death lessons must extract the telegraphed reason for failure (`lesson` field in death outcome) so that dying immediately instructs the player on what they should have heeded.

## Preconditions
- [ ] E01 DONE — Journal model is in place on `RunState`.
- [ ] A11 DONE — Death screen trigger is wired into the game loop.
- [ ] `python -m pytest` passes cleanly.

## Actionable Steps
1. Add optional `journal_note` / `discovery_text` fields to room schemas in `game/content_schema.py` (with safe fallbacks to room name/first sentence).
2. Update room navigation in `screens/game.py` to invoke `state.journal.add_room(...)` whenever entering an unrecorded room.
3. In `game/effects.py` or the death resolution handler, capture the fatal choice's cause and lesson and invoke `state.journal.add_death(cause, lesson)`.
4. Provide a mechanism for dialogue effects or room events to log Shadow whispers via `state.journal.add_shadow_line(...)`.
5. Verify that difficulty settings (from Slice B if present, or baseline) respect the auto-fill contract (EASY fills immediately, HARD only notes verified player actions).

## Test Plan
- **Tests to write/update:** `tests/test_journal_events.py`:
  - `test_room_entry_logs_journal_record` — navigating to a new room registers a room entry.
  - `test_revisiting_room_does_not_duplicate_entry` — re-entering does not add redundant entries.
  - `test_death_trigger_records_lesson` — executing a lethal action logs the lesson into journal before transitioning to death screen.
- **Commands:** `python -m pytest tests/test_journal_events.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Entering any room automatically logs a journal entry if not previously recorded.
- [ ] Triggering a death condition captures the specific lesson into the journal.
- [ ] Shadow lines encountered are cleanly captured into the journal.
- [ ] All journal events function cleanly without slowing down room transitions.
- [ ] Automated tests verify both room logging and death recording behavior.

## Rollback / Undo
Revert changes to `screens/game.py`, `game/effects.py`, and `game/content_schema.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
