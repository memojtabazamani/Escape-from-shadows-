# Task D02: OLD LIBRARY content — the BOOK, the shelf, the watching

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: D — The Two Rooms
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: C03, B05
- Blocks: D03, D06
- Covers: AC-2, AC-11
- Suggested commit: `content(library): author the old library and the book`
- Branch: per GP-3

## Objective
Author the OLD LIBRARY: the slice's information room, where the best item in the game sits and where reading it costs you the ability to watch the door (§6). This room is where the slice teaches that knowledge has a price.

## Non-Goals
- Does not implement the BOOK's mechanics — its cost, its knowledge flag, and what it unlocks are D03.
- Does not implement §6's **three consecutive turns** of reading. ASM-5 defers that to Phase 2, because it needs multi-turn action machinery; Phase 1's read is a single costly action.
- Does not author THE HALL (D01) or the ending (D05).
- Does not add engine features.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6's OLD LIBRARY entry (the information room; the BOOK is the best item and reading it is dangerous; the candle burns down; "you know someone came in, because the door is open now"), §3.3 (the BOOK: "heavy, slow to read, and *watched*"), §3.1 (light as both resource and leash), and §7.4.
- **Files to create/modify:** the content file for the OLD LIBRARY.
- **Files to read, not modify:** `game/content_schema.py`. D01 declares the route in; this task declares the room and its own choices.
- **Conventions to respect:** content as data; every referenced item and flag declared; the validator must pass.
- **Content requirements — mandatory:**
  - **Prose budget:** arrival prose fits the scene line budget at ~60 columns with no continuation marker (AC-11).
  - **The BOOK** is present as an interactable; its choice records **the full oil cost** D03 will apply, and its tier must reflect that cost (a Setback or Scar, not a Death).
  - **A shelf** — one flavour interactable that yields nothing mechanical, so the room is not a single-button corridor and so the player learns that not every interaction is a transaction. It must be honest about yielding nothing, or be subtly informative; it must not pretend to matter.
  - **The door** — the room's tension. Per §6, the door is what you cannot watch while reading. Express this with a telegraph that the choice itself is a commitment, so the player understands what they are giving up.
  - **The watching** — the room must carry the §6 beat that *someone has been here*. This is atmosphere, not a mechanic, and it must not promise a mechanic Phase 1 does not have.
- **Voice:** restraint over gore; the horror is between the lines (pillar 1). No red — red is reserved for the Shadow (§7.4) and the Shadow does not appear in Phase 1 (§12 defers it to Phase 3).

## Preconditions
- [ ] C03 and B05 DONE
- [ ] A04's validator passes on the existing content set
- [ ] D01 DONE is **not required** — this task may run in parallel; but the route in must exist before D06's reachability check, so coordinate the destination identifier with D01

## Actionable Steps
1. Coordinate the room identifier with D01 so the hall's route matches this room's identity.
2. Author the arrival prose within the scene line budget; include the §6 "someone has been here" beat.
3. Author the BOOK as an interactable, recording the oil cost D03 will apply and a non-Death tier, plus the telegraph that reading is a commitment.
4. Author the shelf as an honest non-mechanical interaction.
5. Author the door beat and any accompanying choice, ensuring it does not promise a mechanic that does not exist.
6. Declare the BOOK's item identity consistently with whatever D03 defines — agree the identifier before writing both, so the content and the mechanics cannot drift.
7. Validate the content set; confirm every destination, item, and flag resolves.
8. Render at ~60 columns and confirm the prose fits with the room name visible.

## Test Plan
- **Tests to write:** D06 validates the content set and checks both terminal paths are reachable. This task's own check is the validator plus a render check.
- **Commands:** run A04's validator; then `python index.py` and walk from THE HALL into the LIBRARY.
- **Expected:** the room validates clean; prose fits at ~60 columns; the BOOK, the shelf, and the door are selectable; the BOOK's oil cost is recorded in its choice data; no choice crashes or dead-ends.
- **Honesty check:** read the shelf's and the door's text as a first-time player. Confirm the shelf does not promise a reward it will not give, and the door does not promise a mechanic the slice lacks.
- **Consistency check:** the BOOK's item identifier here matches the one D03 implements.

## Definition of Done / Acceptance Criteria
- [ ] THE OLD LIBRARY validates and is reachable from THE HALL
- [ ] Arrival prose fits the scene budget at ~60 columns with no continuation marker
- [ ] The BOOK is present with its oil cost recorded in content data and a non-Death tier
- [ ] The shelf is an honest non-mechanical interaction
- [ ] The "someone has been here" beat is present
- [ ] No text promises a mechanic Phase 1 does not have
- [ ] No red is used anywhere in the room
- [ ] The BOOK's identifier matches D03's
- [ ] No engine or screen file changed to accommodate the content (AC-9)

## Rollback / Undo
Revert this task's commit. THE HALL's route into the library would then point at a missing room, so the content set would fail validation — revert together with D01's route, or replace the destination. Verify the set validates after reverting.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
