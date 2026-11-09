# Task I01: Save file: serialize the run

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: I — Persistence & Mercy
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: C05, D05, E04
- Blocks: I02
- Covers: AC-20
- Suggested commit: `feat(save): implement run state serialization to single JSON save file`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Implement disk serialization for an active run (`save_game(state, filepath)`), writing `RunState` (room id, oil, composure, inventory, journal, turn count, flags) into a single clean JSON save file following the repo's established `SettingsManager` precedent.

## Non-Goals
- Does not implement multiple save slots or cloud saving (single slot per §9.1 and ASM-9).
- Does not modify main menu "CONTINUE" wiring — that is I02.
- Does not serialize unfinalized transient screen animations.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §9.1 ("Save & Resume: You already have SettingsManager, a proven JSON persistence pattern in this repo. A save file is the same idea with different contents: current room, inventory, lantern, composure, turn count, journal entries, endings seen. One slot is fine"), AC-20 in `EPIC_Phase2_TheHouse_PLAN.md`, ASM-9, RISK-7.
- **Files to create:** `game/save.py`.
- **Files to read, not modify:** `game/state.py` (utilizes `RunState.snapshot()`), `config.py`.
- **Conventions to respect:** Atomic file writing (write to temporary file and replace) to prevent save file corruption on sudden crash or exit. Store save file in a local data path (e.g. `save.json`).
- **Design constraints:**
  - Uses `RunState.snapshot()` as the source of truth for game data.
  - Adds envelope metadata: `save_version: 1`, `timestamp: ISO-8601`, `current_room_title`.
  - Tolerates missing fields gracefully during restoration (backward compatibility).

## Preconditions
- [ ] C05 (Inventory), D05 (Composure), and E04 (Journal) are DONE — state model is fully frozen (RISK-7).
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. Create `game/save.py` defining `SaveManager` class.
2. Define save envelope schema: `version`, `saved_at`, `state` (from `RunState.snapshot()`).
3. Implement `save_to_disk(state: RunState, path: Path = DEFAULT_SAVE_PATH) -> bool`:
   - Serializes payload to JSON string with indentation.
   - Writes to a `.tmp` file and atomically renames to target file.
4. Implement validation of saved JSON schema on write.
5. Provide helper `has_saved_game(path: Path) -> bool` and `delete_saved_game(path: Path) -> bool`.
6. Write unit tests verifying atomic write and schema validity.

## Test Plan
- **Tests to write/update:** `tests/test_save_serialization.py`:
  - `test_save_creates_valid_json` — verifies JSON file created on disk with envelope metadata.
  - `test_atomic_write_prevents_partial_file` — verifies write-temp-and-rename operation.
  - `test_delete_save_removes_file` — verifies clean deletion when run ends.
- **Commands:** `python -m pytest tests/test_save_serialization.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/save.py` serializes full `RunState` into a single JSON save file.
- [ ] Envelope carries version, timestamp, and snapshot data.
- [ ] Writing uses safe atomic temp-and-rename pattern.
- [ ] Helpers identify and delete existing save files cleanly.
- [ ] Automated tests pass cleanly.

## Rollback / Undo
Delete `game/save.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
