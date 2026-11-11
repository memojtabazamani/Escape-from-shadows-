# Task A01: Profile persistence model for unlocked endings

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: A — Meta-Progression & The Endings Gallery
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: GP-1, GP-2
- Blocks: A02
- Covers: AC-1, §9.4
- Suggested commit: `feat(profile): create cross-run profile persistence for unlocked endings`
- Branch: feature/phase_3_the_shadow

## Objective
Implement a persistent meta-progression profile manager (`game/profile.py`) that stores and tracks permanently unlocked endings across independent game runs, ensuring that game over or victory purges single-run state without wiping discovered endings.

## Non-Goals
- Does not build the Gallery UI widget or screen (handled in A03).
- Does not modify existing in-run save/load logic in `game/save.py` beyond guaranteeing isolation from the profile file.
- Does not author the endings narrative content (handled in B01).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §9.4 ("The Endings Gallery"), `game/save.py` (atomic write patterns), `config.py` (JSON persistence pattern).
- **Files to create:** `game/profile.py`.
- **Files to read, not modify:** `game/save.py`, `config.py`.
- **Conventions to respect:** Atomic writing via temporary files with `.replace()` to prevent corruption; JSON format; clean exception fallback; type annotations with `from __future__ import annotations`.
- **Storage path:** `data/profile.json` (or OS-appropriate platform directory matching `config.py` / `save.py`).

## Preconditions
- [ ] Baseline test suite is green (263/263 passing).
- [ ] Working tree is clean on `feature/phase_3_the_shadow`.

## Actionable Steps
1. Create `game/profile.py` with dataclass `PlayerProfile` tracking `unlocked_endings: set[str]`, `total_escapes: int`, and `total_deaths: int`.
2. Implement `save_profile(profile: PlayerProfile, path: Path | None = None) -> bool` using atomic write semantics (writing to `.tmp` and atomic rename).
3. Implement `load_profile(path: Path | None = None) -> PlayerProfile` with graceful fallback to an empty default profile if file is missing or malformed.
4. Implement helper `unlock_ending(ending_id: str, path: Path | None = None) -> bool` that idempotently adds an ending ID and persists the update.
5. Provide helper `get_unlocked_endings() -> set[str]`.

## Test Plan
- **Tests to write:** `tests/test_profile_persistence.py`:
  - `test_default_profile_when_file_absent`: Loading without an existing file returns an empty profile.
  - `test_atomic_save_and_load_roundtrip`: Unlocking an ending persists and restores correctly.
  - `test_idempotent_unlock`: Unlocking the same ending multiple times does not create duplicates.
  - `test_corrupt_profile_fallback`: Malformed JSON recovers safely to a clean default profile.
- **Commands:** `python -m pytest tests/test_profile_persistence.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `PlayerProfile` model and serialization functions exist in `game/profile.py`.
- [ ] Atomic file writes ensure zero risk of corrupted profile files on crash.
- [ ] Profile state is completely isolated from single-run `save.json`.
- [ ] All unit tests pass cleanly.

## Rollback / Undo
Delete `game/profile.py` and `tests/test_profile_persistence.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
