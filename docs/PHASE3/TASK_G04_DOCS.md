# Task G04: Phase 3 completion report and Handoff to Phase 4

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: G — Full Integration, Verification & Documentation
- Layer: DOCS
- Status: TODO
- Estimate: ~1.5h
- Depends on: G03
- Blocks: None
- Covers: §12
- Suggested commit: `docs: author Phase 3 completion report and handoff specifications for Phase 4`
- Branch: feature/phase_3_the_shadow

## Objective
Author the formal Phase 3 Completion Report and Handoff Specification for Phase 4 ("The Fantastic"), recording the final verification evidence, total test counts, and outlining the clear boundaries for New Game Plus, the seven new rooms, and selected fantastic ideas in Phase 4.

## Non-Goals
- Does not begin Phase 4 implementation.
- Does not write code.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §10 ("Fantastic Ideas"), §12 ("Roadmap: Phase 4 — The Fantastic"), `docs/PHASE3/EPIC_Phase3_TheShadow_PLAN.md`.
- **Files to create:** `docs/PHASE3/PHASE3_COMPLETION_REPORT.md`.
- **Precedent:** Follows the handoff pattern established at the conclusion of Phase 2 in `EPIC_Phase2_TheHouse_PLAN.md`.

## Preconditions
- [ ] Task G03 complete.
- [ ] Working tree clean and all tests green.

## Actionable Steps
1. Create `docs/PHASE3/PHASE3_COMPLETION_REPORT.md`.
2. Summarize key achievements:
   - The Shadow as an active antagonist (lit-room rule, zero-oil breach, absence prose).
   - Dynamic second-person dialogue drawn from player history with audio cues and journal logging.
   - All 7 canonical endings fully implemented and verified.
   - Dedicated Endings Gallery accessible from Main Menu with cross-run profile persistence.
   - Three memory fragments and secret Homecoming ending.
   - Dread thresholds (Turn 20/30) and strict red text visual grammar.
3. Record test evidence: total test count, coverage summary, and execution timings.
4. Detail Phase 4 Handoff:
   - New Game Plus (§9.3) building on `PlayerProfile.unlocked_endings`.
   - Expansion with new rooms from §6 (Stairwell, Nursery, Mirror Room, Cellar, Chapel).
   - Selection of 2–3 Fantastic Ideas from §10.
   - Final accessibility pass (§8).

## Test Plan
- **Verification:**
  - Verify all markdown links are valid.
  - Review that all AC-1 through AC-26 are confirmed completed.

## Definition of Done / Acceptance Criteria
- [ ] `docs/PHASE3/PHASE3_COMPLETION_REPORT.md` written and complete.
- [ ] Phase 4 boundaries clearly defined.
- [ ] Ready for user review and approval.

## Rollback / Undo
Delete `docs/PHASE3/PHASE3_COMPLETION_REPORT.md`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
