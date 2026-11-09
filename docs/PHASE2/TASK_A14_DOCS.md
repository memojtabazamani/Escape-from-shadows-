# Task A14: Re-sync the docs and mark `docs/PHASE1/` superseded

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: DOCS
- Status: TODO
- Estimate: ~1.5h
- Depends on: A13
- Blocks: None
- Covers: AC-24, AC-22
- Suggested commit: `docs: re-sync project docs and mark phase 1 tasks superseded`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make every prose document describe the game that now exists, and resolve RISK-1 by marking `docs/PHASE1/` as superseded so two folders stop describing the same unbuilt work.

## Non-Goals
- Does not modify `docs/SUGGEST.md` beyond **§0 only** — the blueprint is the design source; §0 is its snapshot of reality and is the only section that claims things about the current build.
- Does not rewrite `docs/PHASE1/`'s plans. It adds a superseded banner and a pointer; **deleting or rewriting them is GP-4's decision and this task implements only the outcome the owner chose.**
- Does not document Slices B–I — they do not exist yet. Documenting planned features as if built is the exact failure §0 exists to prevent.
- Does not add screenshots or ASCII mockups.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` **§0 "Where the Game Stands Today"**, §12's Phase 2 bullet, and §13's "no setting lies" pitfall that AC-24 encodes. Also read `docs/PHASE1/README.md`'s "Deliberately Not In This Phase" section — it defers several items into Phase 2, and some of those deferrals are now themselves out of date.
- **Files to modify:**
  - `AGENTS.md` — the architecture tree and "How to Run" must name `screens/game.py`, `screens/death.py`, `screens/ending.py`, `game/lantern.py`, and the content files, since they now exist.
  - `README.md` — the feature description must match what the game does now.
  - `docs/GENERAL_DOC.md` — the user-facing and developer sections must match.
  - `docs/SUGGEST.md` — **§0 only**.
  - `docs/PHASE1/*.md` — superseded banner per GP-4's answer.
- **Files to read, not modify:** the whole Phase 1 folder, to determine what its banner should say.
- **Conventions to respect:** `AGENTS.md` is loaded into every agent session — its accuracy matters more than its polish. Keep its existing section structure and tone; this is a re-sync, not a rewrite. Match `docs/PHASE1/README.md`'s banner idiom if it has one.
- **Design constraints:**
  - **Every claim must be verifiable by opening a file.** If a doc says a screen exists, `ls screens/` must show it. This is AC-24's spirit applied to prose: no setting, and no document, may lie.
  - **GP-4 gates the Phase 1 banner.** Ask if unanswered. If the owner chose "leave as historical record", add a dated note rather than a superseded banner — do not decide for them.
  - §0 must state plainly that Slices B–I of Phase 2 are **not built**, so the next session does not repeat the discovery this epic opened with.
- **Voice:** plain and accurate. The project's docs are unusually honest about their own state — §0's whole purpose — and this task is that honesty brought up to date.

## Preconditions
- [ ] A13 DONE — the loop works and the playtest verdict is recorded, so the docs describe something real
- [ ] GP-4 answered — the owner has decided whether Phase 1 tasks are marked superseded
- [ ] File listing of `screens/`, `game/`, `tests/`, and the content files available, to verify every claim
- [ ] The pending deletion of `docs/PHASE2/PHASE2_USE_SETTINGS_INTO_GAME.md` resolved or explicitly left alone (per the epic's Git Policy, it is not this epic's business)

## Actionable Steps
1. List `screens/`, `game/`, `tests/`, and the content files, and write down what actually exists.
2. Update `AGENTS.md`'s architecture tree to match that listing, and confirm "How to Run" is still correct.
3. Update `AGENTS.md`'s Controls table if the gameplay screen added keys beyond the Phase 1 set.
4. Update `README.md`'s description to match the playable game.
5. Update `docs/GENERAL_DOC.md` in both its user and developer sections.
6. Rewrite `docs/SUGGEST.md` **§0** to state exactly what exists and what does not, naming Slices B–I as unbuilt.
7. Apply GP-4's decision to `docs/PHASE1/` — banner or dated note — with a pointer to `docs/PHASE2/` as the live record.
8. Re-read each changed document once, checking every claim against a file listing.

## Test Plan
- **Tests to write/update:** none — this is a DOCS task. Its verification is a claim audit, not a test run.
- **Commands:** `ls screens game tests`; `python -m pytest` (confirm nothing regressed and no doc change broke an import path); `python index.py` (confirm the app still starts).
- **Manual verification:** open each changed document and check it against a fresh directory listing. For every named file, confirm it exists.
- **Claim audit (the real check):** read §0 aloud as if to a new contributor. Does any sentence describe something that is not there? That sentence is the bug.

## Definition of Done / Acceptance Criteria
- [ ] `AGENTS.md`'s tree, run instructions, and controls match the repository
- [ ] `README.md` describes the game that exists
- [ ] `docs/GENERAL_DOC.md` is accurate in both sections
- [ ] `docs/SUGGEST.md` **§0** states plainly what exists and that Slices B–I are unbuilt
- [ ] `docs/PHASE1/` carries GP-4's decision and points to this folder as the live record
- [ ] Every file named in a changed doc exists — verified against a listing, not from memory
- [ ] No document claims a Phase 2 feature is built
- [ ] No file outside the declared list was modified, and `docs/SUGGEST.md` is untouched outside §0
- [ ] `python -m pytest` still green; `python index.py` still starts

## Rollback / Undo
Revert this task's commit; documentation returns to describing the pre-Slice-A state, which is a milder inaccurate rather than a broken build. RISK-1 reopens, so revert only if the superseded banner itself caused a problem.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record GP-4's answer and the exact files whose claims were audited -->
