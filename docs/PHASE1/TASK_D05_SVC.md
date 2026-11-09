# Task D05: One honest ending at the front door

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: D — The Two Rooms
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: D03, D04
- Blocks: D06, E02
- Covers: AC-3, AC-7
- Suggested commit: `content(hall): make the front door open once the book is known`
- Branch: per GP-3

## Objective
Implement the slice's one ending: the HALL's front door — the door that has refused you all run — opens once you hold the BOOK's knowledge. This closes the loop the slice is built on: the cost you paid in the library is what buys your way out of the hall, and the second visit to the HALL means something (design pillar 3).

## Non-Goals
- Does not implement the ending's presentation (E02) — this task produces the ending *result*; E02 renders it.
- Does not implement multiple endings, or ending variants by what the player understood (§2.3) — Phase 3.
- Does not implement §6's memory fragments or the `Stay` ending — Phase 3.
- Does not make the ending require the death or the reading order beyond the one flag.
- Does not add engine features.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6's THE HALL entry (the front door is "visibly, insultingly, unlocked-but-stuck" and "always visible and never reachable until the end"), §3.3 (the BOOK's knowledge as a gate), §4.3 (the same knowledge-gate pattern), and §2.3's *The Quiet Exit* (the standard win: leave through the front door).
- **Files to modify:** the front door's choice in THE HALL content (D01's file).
- **Files to read, not modify:** `game/effects.py` (requirements), `game/state.py` (flags), `screens/game.py` (B03's ending placeholder).
- **Conventions to respect:** the gate is a **requirement** on the choice, expressed in content data — the same mechanism A04 built for gating. No front-door special-casing in code.
- **Design constraints — mandatory:**
  - The gate's requirement is **exactly the flag D03 sets**, character for character. Confirm against D03's recorded contract.
  - **The refusal before the flag must be honest and consistent.** The player will attempt this door early; the refusal must be the same door every time, and must not read as a bug. §13: "choices that don't matter" train players to stop reading — a door that silently changes behavior would do worse.
  - **The refusal should hint without instructing.** After the player has the knowledge, the door should feel like it *changed* rather than like a key was inserted. The difference between "you now have the key" and "the door no longer resists you" is the difference between a mechanic and a story.
  - **The ending result must be structured data** carrying what the player leaves with — at minimum, whether they read the book — so E02 and Phase 3's ending variants can use it. Do not bake prose into the result.
  - **The ending must be reachable and the death avoidable**: a careful player can finish without dying. Confirm this explicitly.
  - **Zero oil must not leave a stuck state.** Under C02's option (a), a player who runs out of light before reading the book cannot win — the loss must be honest and legible, not a silent dead end. Verify the combination of C02's decision and this task's gate produces an understandable state, not a soft-lock.
- **Voice:** §6 calls the door "insultingly unlocked-but-stuck." The ending should feel like the house finally allowing it, not like a puzzle solved.

## Preconditions
- [ ] D03 DONE — the knowledge flag exists, with its contract recorded
- [ ] D04 DONE — the death is implemented, so "avoidable" is meaningful
- [ ] D01 DONE — the front door choice exists with its refusal and content-level hook
- [ ] C02's decision is recorded, so the zero-oil interaction can be verified
- [ ] B03's ending placeholder still routes correctly

## Actionable Steps
1. Confirm the knowledge flag's exact name against D03's recorded contract.
2. Convert the front door's refusal into a `requires` requirement on the flag, using the existing vocabulary.
3. Author the refusal text so it reads identically every time before the flag is set, and does not suggest a hidden trigger.
4. Author the post-flag outcome so the door feels changed rather than unlocked.
5. Produce the ending result as structured data carrying at least the book-read state.
6. Route the result through B03's ending placeholder, confirming the placeholder receives the structured result rather than a generic message.
7. Verify reachability: from a fresh run, win without dying.
8. Verify avoidability and honesty: from a fresh run, confirm the death can be skipped, and confirm that running out of oil before reading produces a legible lost state rather than a soft-lock.

## Test Plan
- **Tests to write:** D06 adds cases asserting the door is refused without the flag, permitted with it, and that the ending result carries the book-read state. The zero-oil soft-lock check belongs to D06 as an explicit reachability case.
- **Commands:** run A04's validator; then `python index.py` and play the full winning path.
- **Expected:** the door refuses before the flag and gives way after it; the ending result is produced; the run is completable without dying; a zero-oil run is legibly lost rather than stuck.
- **Consistency check:** attempt the door early and confirm the refusal is identical on repeat attempts — a player must be able to trust the door they are told about.
- **Contract check:** confirm the flag name matches D03 exactly.

## Definition of Done / Acceptance Criteria
- [ ] The gate is a content requirement on the flag D03 sets, with names matching exactly
- [ ] The refusal is identical on every pre-flag attempt and does not read as a bug
- [ ] The post-flag outcome reads as the door changing, not as a key being used
- [ ] The ending result is structured data carrying the book-read state
- [ ] The full run is completable without dying
- [ ] The death remains avoidable
- [ ] The zero-oil interaction produces a legible loss or a legible closed path, never a soft-lock
- [ ] No front-door special-casing in code; the gate uses the requirement vocabulary

## Rollback / Undo
Revert this task's commit. The front door returns to refusing unconditionally, which makes the slice unwinnable — revert together with D03's read, or restore a temporary win condition. Verify the content set validates and the run remains completable or clearly interrupted after reverting.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the flag contract confirmation and the reachability results here -->
