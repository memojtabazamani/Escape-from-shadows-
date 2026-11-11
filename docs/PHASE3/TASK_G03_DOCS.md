# Task G03: Documentation synchronization (`AGENTS.md`, `README.md`, `GENERAL_DOC.md`, `SUGGEST.md` §0)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: G — Full Integration, Verification & Documentation
- Layer: DOCS
- Status: TODO
- Estimate: ~2h
- Depends on: G02
- Blocks: G04
- Covers: §11, §12
- Suggested commit: `docs: synchronize system architecture docs with Phase 3 deliverables`
- Branch: feature/phase_3_the_shadow

## Objective
Update all central documentation files (`AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, and `docs/SUGGEST.md` §0) to reflect the completed state of Phase 3, documenting the Shadow engine, history dialogue, multiple endings spread, endings gallery, and memory fragments.

## Non-Goals
- Does not edit implementation code or test files.
- Does not modify planning documents in `docs/PHASE1/` or `docs/PHASE2/`.

## Context & Constraints
- **Read first:** `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, `docs/SUGGEST.md` §0.
- **Files to modify:** `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, `docs/SUGGEST.md`.
- **Precedent:** Follows how Phase 2 documented its snapshot in `SUGGEST.md` §0 and updated the file tree in `AGENTS.md`.

## Preconditions
- [ ] Task G02 DONE (full test suite green).
- [ ] Working tree clean.

## Actionable Steps
1. In `AGENTS.md`:
   - Update architecture tree to include `game/profile.py`, `game/endings.py`, `game/endings_art.py`, `game/shadow.py`, `game/shadow_dialogue.py`, `screens/gallery.py`.
   - Update test suite count reference.
2. In `docs/SUGGEST.md` §0:
   - Update "Where the Game Stands Today" snapshot to mark Phase 3 as 100% built and verified with its key systems listed.
3. In `docs/GENERAL_DOC.md`:
   - Add documentation sections describing the Shadow pursuit rules, second-person dialogue, the 7 canonical endings, and the Endings Gallery.
4. In `README.md`:
   - Highlight the new features in gameplay description and control hints.

## Test Plan
- **Verification:**
  - Verify all markdown links resolve correctly.
  - Review diff to ensure no unrelated files or sections were touched.
- **Commands:** `python -m py_compile index.py config.py screens/*.py game/*.py`.

## Definition of Done / Acceptance Criteria
- [ ] All four core documentation files reflect Phase 3 completion.
- [ ] File tree in `AGENTS.md` matches the actual repository structure.
- [ ] `SUGGEST.md` §0 accurately reports Phase 3 as completed.

## Rollback / Undo
Revert documentation edits.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
