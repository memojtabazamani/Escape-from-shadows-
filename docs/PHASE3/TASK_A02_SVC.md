# Task A02: Endings metadata schema and registry

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: A — Meta-Progression & The Endings Gallery
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: A01
- Blocks: A03, B01
- Covers: AC-2, AC-4, §2.3, §9.4
- Suggested commit: `feat(endings): define canonical endings schema and static registry`
- Branch: feature/phase_3_the_shadow

## Objective
Define the structured metadata schema for canonical endings in `game/endings.py` and integrate endings validation into `game/content_schema.py`, establishing the canonical 7-ending catalog with metadata (ID, title, hint/silhouette description, criteria description).

## Non-Goals
- Does not render UI or Textual widgets (handled in A03).
- Does not author the full narrative ending prose blocks in `content.json` (handled in B01).
- Does not create ending resolution conditions logic (handled in B02).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.3 (Multiple Endings table: The Long Walk, Meat and Silence, The Quiet Exit, What the Book Knew, The New Shadow, Homecoming, Stay), §9.4 ("The Endings Gallery"), `game/content_schema.py`.
- **Files to create:** `game/endings.py`.
- **Files to modify:** `game/content_schema.py`.
- **Conventions to respect:** Dataclass structures; pure data; typed dictionaries; strict schema validation.

## Preconditions
- [ ] Task A01 DONE (`game/profile.py` exists and is tested).
- [ ] Existing schema tests pass cleanly.

## Actionable Steps
1. In `game/endings.py`, define dataclass `EndingMetadata`:
   - `id`: str (canonical identifier, e.g. `the_long_walk`, `meat_and_silence`, etc.)
   - `number`: int (1 to 7)
   - `title`: str (official display name)
   - `tone`: str (narrative classification per §2.3)
   - `hint`: str (cryptic teaser shown when locked in the Gallery)
   - `summary`: str (brief description displayed once unlocked)
2. Define `CANONICAL_ENDINGS: dict[str, EndingMetadata]` registering all 7 endings from §2.3.
3. In `game/content_schema.py`, add schema validation rules for the `endings` section in content JSON.
4. Provide lookup helper `get_ending_metadata(ending_id: str) -> Optional[EndingMetadata]`.

## Test Plan
- **Tests to write:** `tests/test_endings_schema.py`:
  - `test_canonical_endings_registry_completeness`: Asserts exactly 7 canonical endings exist with numbers 1..7.
  - `test_schema_validates_endings_section`: Validates content dictionary containing endings entries.
  - `test_missing_ending_lookup_returns_none`: Asserts unknown ending queries return safe `None`.
- **Commands:** `python -m pytest tests/test_endings_schema.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/endings.py` defines all 7 canonical endings with correct IDs and metadata per §2.3.
- [ ] `game/content_schema.py` validates endings data without breaking existing room/item validations.
- [ ] Schema tests pass with 100% success.

## Rollback / Undo
Revert modifications to `game/content_schema.py` and delete `game/endings.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
