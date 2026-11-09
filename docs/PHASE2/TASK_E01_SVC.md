# Task E01: Journal model: rooms, deaths, Shadow lines

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: E — The Journal
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: A13
- Blocks: E02, E03
- Covers: AC-12
- Suggested commit: `feat(journal): add journal state model for rooms, deaths, and shadow lines`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Create the in-memory journal model that records player discoveries across a run — rooms visited, causes of death witnessed, and lines spoken by the Shadow — as structured data on `RunState` that survives until death or victory.

## Non-Goals
- Does not automatically write journal entries upon room visits or death events — that is E02.
- Does not render any UI, modal, or overlay screen — that is E03.
- Does not persist journal records across distinct application launches — that belongs to Slice I (Save & Load).
- Does not generate dynamic Shadow taunts or dialogue based on history — that is deferred to Phase 3 (§2.2).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.4 (The Journal as an anti-frustration system), §5.1 (Journal auto-fill differences by difficulty), and AC-12 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to create:** `game/journal.py`.
- **Files to modify:** `game/state.py` (integrate journal container into `RunState`, support snapshot and restore).
- **Files to read, not modify:** `game/state.py`, `game/content_schema.py`.
- **Conventions to respect:** Journal entries should be lightweight dataclasses or typed dictionaries with timestamps/turn counts, category tags (`room`, `death`, `shadow`), and formatted prose strings.
- **Design constraints:**
  - Duplicate entries should be coalesced or deduplicated (e.g. visiting THE HALL three times should not record three identical room notes; it should update first seen / last seen or retain a single clean entry).
  - Must seamlessly serialize and deserialize within `RunState.snapshot()` and `RunState.restore()` without loss or schema distortion.

## Preconditions
- [ ] A13 DONE — the core gameplay loop and state baseline are established and tested.
- [ ] `python -m pytest` passes cleanly.

## Actionable Steps
1. Create `game/journal.py` defining `JournalEntry` and `Journal` dataclasses.
2. Define structured categories: `ROOM_DISCOVERY`, `DEATH_LESSON`, `SHADOW_WHISPER`.
3. Provide methods: `add_room(room_id, title, notes)`, `add_death(cause, lesson)`, `add_shadow_line(line, context)`, `get_entries(category=None)`.
4. Ensure duplicate protection: prevent spamming duplicate room/death entries during backtracking or repeated events.
5. Integrate `journal: Journal` into `RunState` in `game/state.py`, initializing an empty journal on new runs.
6. Update `RunState.snapshot()` and `RunState.restore()` to cleanly round-trip all journal records.

## Test Plan
- **Tests to write/update:** `tests/test_journal_model.py`:
  - `test_journal_initialization_empty` — newly created journal has zero entries.
  - `test_journal_add_distinct_categories` — correctly stores and filters room, death, and shadow entries.
  - `test_journal_deduplication` — repeated additions of the same room update metadata rather than duplicating.
  - `test_journal_state_snapshot_roundtrip` — snapshot and restore faithfully preserve all entries.
- **Commands:** `python -m pytest tests/test_journal_model.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/journal.py` exists with clear type hints, docstrings, and clean data structures.
- [ ] Journal supports room discoveries, death lessons, and Shadow utterances.
- [ ] Deduplication logic prevents bloated lists when navigating back and forth.
- [ ] `RunState.snapshot()` and `RunState.restore()` serialize and deserialize journal data cleanly.
- [ ] `tests/test_journal_model.py` passes with 100% green assertions.

## Rollback / Undo
Delete `game/journal.py` and revert additions to `game/state.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
