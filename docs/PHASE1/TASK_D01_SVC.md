# Task D01: THE HALL content — hub, left doorway, front door

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: D — The Two Rooms
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: C03, B05
- Blocks: D04, D05, D06
- Covers: AC-2, AC-11
- Suggested commit: `content(hall): author the hall as the slice's hub room`
- Branch: per GP-3

## Objective
Author THE HALL as the slice's hub: the room the player starts in, the room they return to, the room with a left doorway that is telegraphed as dangerous, and a front door that visibly refuses to open. This room carries the slice's first impressions and its two most important promises (§6).

## Non-Goals
- Does not build BLOOD KITCHEN as a room — the left doorway is a *threshold* in Phase 1 (ASM-3); the kitchen room is Phase 2.
- Does not implement the death (D04) or the ending (D05) — this task authors the choices and destinations; those tasks implement the outcomes.
- Does not author the OLD LIBRARY (D02) or the BOOK (D03).
- Does not add engine features; if the room needs something the format cannot express, stop and raise a format change.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6's THE HALL entry (a hub, not a corridor; two doors, a staircase, and a front door that is "visibly, insultingly, unlocked-but-stuck"), §4.2 (telegraph, don't announce — including its worked example, which is written for a doorway), §4.1 (the three-tier model), §2.1 (the premise), and §7.4 (color as grammar).
- **Files to create/modify:** the content files for THE HALL (per the format A04 settled) and the start-room declaration.
- **Files to read, not modify:** `game/content_schema.py` (the vocabulary), and D01's sibling tasks are not yet written, so stub destinations must be declared in a way that validates.
- **Conventions to respect:** content is data, never code; every new item or flag referenced must be declared in the content set or the validator will (correctly) reject it.
- **Content requirements — mandatory:**
  - **Prose budget:** the arrival description fits the scene line budget from B02 at ~60 columns, with no continuation marker (AC-11). If it does not fit, cut it — §13: "if a room needs 40 lines, it's two rooms."
  - **A left doorway** whose choice carries **at least two distinct telegraphs** in the §4.2 style — sensory and recent, not an announcement of danger. Its tier is Death (the outcome itself belongs to D04).
  - **A front door** that does not open yet and whose refusal is honest and memorable; it becomes the ending's door in D05. Its tier is Scar, and it must be re-attemptable.
  - **One route to the OLD LIBRARY**, so the player can find the BOOK.
  - **A staircase, described but not climbable in Phase 1** (§6 places it in the hall). Its choice must be an honest Scar-tier refusal, not a dead end that reads as a bug.
  - **The low-oil telegraph variant** required by C02, so the zero-oil warning has a home here.
- **Voice:** the premise from §2.1 — a house that is not yours, and not outside. Restraint over gore (design pillar 1). No red is involved; the hall is lit.

## Preconditions
- [ ] C03 and B05 DONE — the cost rules and screen behaviors are settled and tested
- [ ] A04's format is frozen and its validator passes on the existing content set
- [ ] C02's low-oil telegraph requirement is read and understood

## Actionable Steps
1. Read §6's HALL entry and §4.2's example; write the room's beats on paper before authoring: arrival, the left doorway, the front door, the library route, the staircase.
2. Declare THE HALL as the start room and author its arrival prose within the scene line budget.
3. Author the left doorway choice with two distinct telegraphs and Death tier, pointing at the destination D04 will implement (declare the destination in a way that validates).
4. Author the front door choice with an honest refusal, Scar tier, and re-attemptability; leave a clear content-level hook for D05 to make it yield.
5. Author the route to the OLD LIBRARY (D02 authors that room; this task declares the choice and destination).
6. Author the staircase as an honest Scar-tier refusal.
7. Author the low-oil telegraph variant required by C02.
8. Validate the content set and confirm every declared destination, item, and flag resolves.
9. Render the room at ~60 columns and confirm the prose fits with no continuation marker and the room name stays visible.

## Test Plan
- **Tests to write:** D06 validates the content set and both terminal paths. This task's own check is the validator plus a render check.
- **Commands:** run A04's validator over the content set; then `python index.py` and walk into THE HALL.
- **Expected:** the room validates clean; prose fits the budget at ~60 columns; both doors and the library route appear as selectable choices; the staircase and front door refuse honestly rather than crashing or dead-ending.
- **Telegraph check:** read the left doorway's telegraphs as a first-time player. If you would not feel warned, rewrite them. Two *distinct* warnings, not the same warning twice.
- **Syntax/validation check:** no code added; confirm `python -m py_compile` is unaffected and the validator exits clean.

## Definition of Done / Acceptance Criteria
- [ ] THE HALL validates and is the declared start room
- [ ] Arrival prose fits the scene budget at ~60 columns with no continuation marker
- [ ] The left doorway carries at least two distinct §4.2-style telegraphs and Death tier
- [ ] The front door refuses honestly, is re-attemptable, is Scar tier, and has a content-level hook for D05
- [ ] A route to the OLD LIBRARY exists
- [ ] The staircase is an honest Scar-tier refusal, not a silent dead end
- [ ] The low-oil telegraph variant required by C02 exists
- [ ] No engine or screen file changed to accommodate the content (AC-9)

## Rollback / Undo
Revert this task's commit — the content file returns to its previous state. If THE HALL is the declared start room and is removed, the start-room declaration must be restored with it, or the game will fail to start; verify the revert leaves a startable content set.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
