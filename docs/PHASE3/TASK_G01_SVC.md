# Task G01: Content schema validation and save backward compatibility audit

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: G — Full Integration, Verification & Documentation
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: B06, C04, D05, E04, F04
- Blocks: G02
- Covers: AC-25, §11
- Suggested commit: `chore(schema): audit content validation and save backward compatibility`
- Branch: feature/phase_3_the_shadow

## Objective
Execute a rigorous audit of the content schema validator in `game/content_schema.py` and serialization in `game/save.py`, ensuring all new Phase 3 constructs (endings, fragments, shadow state, history) validate cleanly and that saves created prior to Phase 3 load without errors or data loss.

## Non-Goals
- Does not modify gameplay logic or prose.
- Does not change persistence schema version unless strictly required.

## Context & Constraints
- **Read first:** `game/content_schema.py`, `game/save.py`, `game/state.py`.
- **Backward Compatibility Invariant:** A JSON save file produced in Phase 2 must load seamlessly into Phase 3's `RunState`, initializing `shadow`, `memory_fragments`, and `choice_history` to valid default values.

## Preconditions
- [ ] Slices A through F complete.
- [ ] Working tree clean.

## Actionable Steps
1. Run schema validation across `data/content.json` using `validate_content()`.
2. Verify all new predicates (`has_memory_fragment`, `shadow_state_is`, etc.) and verbs (`advance_shadow`, etc.) are recognized by `effects.py` and `content_schema.py`.
3. Audit `game/save.py` save/load roundtrips:
   - Construct Phase 2 legacy JSON save payload (without Phase 3 fields).
   - Assert `load_from_disk()` restores a valid `RunState` with default Phase 3 structures.
   - Assert saving the restored run serializes the updated fields cleanly.
4. Verify `data/profile.json` and `data/save.json` operate independently without cross-file locks or corruption.

## Test Plan
- **Tests to write:** `tests/test_phase3_schema_and_compat.py`:
  - `test_content_json_fully_validates_under_phase3`: Content schema passes with 0 errors.
  - `test_legacy_phase2_save_deserialization`: Phase 2 save payload loads cleanly.
  - `test_profile_and_save_isolation`: Deleting run save preserves profile.
- **Commands:** `python -m pytest tests/test_phase3_schema_and_compat.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] All Phase 3 content passes `validate_content()`.
- [ ] Backward compatibility with Phase 2 save files is 100% verified.
- [ ] Profile and save file isolation proven.
- [ ] Tests pass cleanly.

## Rollback / Undo
Revert any schema or compat adjustments in `game/content_schema.py` or `game/save.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
