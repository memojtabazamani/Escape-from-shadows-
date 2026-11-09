# Task D03: The BOOK — a costly read that grants knowledge

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: D — The Two Rooms
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: D02
- Blocks: D05, D06
- Covers: AC-3
- Suggested commit: `content(book): make reading the book cost oil and grant knowledge`
- Branch: per GP-3

## Objective
Make the BOOK the slice's hinge: reading it costs a serious amount of oil and sets a knowledge flag, and that flag is the only way the front door will ever open. This is how the slice teaches that information is a purchase, and it is what makes the second visit to THE HALL mean something.

## Non-Goals
- Does not implement §6's three consecutive turns of reading — ASM-5 defers it to Phase 2.
- Does not implement the ending itself (D05) — this task sets the flag; D05 consumes it.
- Does not create a general knowledge or codex system; one flag, read by one door, per Phase 1's scope.
- Does not add engine features. If the format cannot express "cost oil and set a flag", that is an A04 defect — raise it, do not work around it.
- Does not make the BOOK a six-slot inventory item — ASM-6 defers the inventory to Phase 2. The BOOK is read in place.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.3 (the BOOK is "the single best source of information in the game, and it's heavy, slow to read, and *watched*"), §6's OLD LIBRARY entry, §4.3 (knowledge as a gate: the whistle "only works if you know its name" — the same pattern, in miniature), and §11 on requirements as conditions.
- **Files to modify:** the OLD LIBRARY content file (D02's), plus the item declaration if the BOOK needs one.
- **Files to read, not modify:** `game/effects.py` (the effect vocabulary), `game/state.py` (flags). No engine change is expected — if one is needed, raise it.
- **Conventions to respect:** the cost and the flag are declared as **content data**, using the same effect vocabulary as every other choice. No special-casing the BOOK in code.
- **Design constraints:**
  - The oil cost is **material** — it must be a meaningful fraction of a full lantern, enough that a player who reads carelessly can lose the run. Record the fraction and its rationale.
  - Reading is **repeatable but not free**: a second read must not be a way to farm nothing, and must not be a trap that punishes a player for a misclick. Decide the behavior (the flag is idempotent; the oil cost is charged only once, or is charged again) and record the decision.
  - The knowledge flag has **exactly one consumer** in Phase 1: the front door (D05). Record that contract explicitly so D05 and this task cannot drift.
  - The BOOK must be readable **only with light** — at zero oil the read is refused, which is what makes C02's option (a) close the winning path. Coordinate with C02's recorded decision; if C02 chose option (b), the read still requires oil above zero, and say so.
  - The read's outcome should be **legible**: the player must be able to tell that they now know something, without being told what it is for. Show, don't explain.

## Preconditions
- [ ] D02 DONE — the BOOK exists as an interactable with its cost recorded
- [ ] D02's BOOK identifier matches the one used here
- [ ] C02's zero-oil decision is recorded, since it determines this task's refusal behavior
- [ ] The effect vocabulary can express cost-and-flag without a new verb (expected); if not, raise an A04 follow-up first

## Actionable Steps
1. Confirm the BOOK's identifier with D02 and record it.
2. Choose the oil cost as a fraction of a full lantern, with a one-line rationale, and record both.
3. Decide the repeat-read behavior and record the decision.
4. Author the read as content: cost oil, set the knowledge flag, and render an outcome that conveys "you know something now" without naming the front door.
5. Implement the zero-oil refusal so the read is impossible without light.
6. Record the flag's single consumer contract for D05 in the Execution Log and in the content's own comment or metadata where the format allows.
7. Verify the flag is idempotent — reading twice does not produce two flags or any other duplicated state.
8. Play the path: enter the library, read the book, and confirm the oil cost lands and the flag is set.

## Test Plan
- **Tests to write:** D06 covers content validation and reachability. The read's cost-and-flag behavior is observable through the existing resolver tests (A06) since it uses the same vocabulary; D06 should add one case asserting that reading sets the flag and charges the oil exactly once.
- **Commands:** run A04's validator; then `python index.py` and walk the library path.
- **Expected:** reading the book visibly costs oil and reports an outcome; the flag is set exactly once; a second read does not duplicate state; at zero oil the read is refused.
- **Contract check:** confirm the flag's name here is character-for-character the one D05 expects.
- **Balance check:** confirm the cost is a material fraction of the lantern and that reading it does not automatically end the run for a careful player.

## Definition of Done / Acceptance Criteria
- [ ] Reading the BOOK costs a material, recorded fraction of the lantern
- [ ] Reading sets exactly one knowledge flag, idempotently
- [ ] The repeat-read behavior is decided and recorded
- [ ] The read is refused at zero oil
- [ ] The flag's name matches D05's expectation exactly, and the contract is recorded
- [ ] The cost and flag are declared in content data, with no BOOK special-casing in code
- [ ] The outcome is legible without explaining what the knowledge is for
- [ ] No engine or screen file changed (AC-9)

## Rollback / Undo
Revert this task's commit. The BOOK remains present and interactive but reading it has no cost and sets no flag, which closes the winning path — so revert together with D05's door condition, or the ending becomes unreachable. Verify reachability after reverting.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the cost fraction, the repeat-read decision, and the flag contract here -->
