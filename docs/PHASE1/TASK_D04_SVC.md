# Task D04: One honest death at the left doorway

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: D — The Two Rooms
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: D01
- Blocks: D05, D06, E01
- Covers: AC-6
- Suggested commit: `content(hall): implement the telegraphed death at the left doorway`
- Branch: per GP-3

## Objective
Implement the slice's one honest death: the left doorway in THE HALL kills you, but only after you have been warned twice, and the death itself says what killed you. This is the direct fix for the baseline's defect, where choosing `l` ended the run with no information and no warning (§4.1, §13).

## Non-Goals
- Does not build BLOOD KITCHEN as a room — the death happens at the threshold (ASM-3); the room is Phase 2.
- Does not implement the death screen's presentation (E01) — this task produces the death *result*; E01 renders it.
- Does not add a second death. Phase 1 has exactly one.
- Does not implement difficulty-gated mercy for death (Phase 2, §5.1).
- Does not implement the "what you could have done" line (Phase 2, §9.2).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §4.1 in full — the three-tier model, and its statement that "death should be *earned by the player*... An unwarned death is a bug" — plus §4.2's worked example, §6's BLOOD KITCHEN entry (what the kitchen is, so the threshold prose is honest about it), and §13's first pitfall.
- **Files to modify:** the content for the doorway and its destination, using the format A04 settled.
- **Files to read, not modify:** `game/effects.py` (tier reporting), `screens/game.py` (B03's Death-tier placeholder). The placeholder must keep working; E01 replaces it.
- **Conventions to respect:** content as data; the Death tier and its telegraphs are expressed in the format, not in code.
- **Design constraints — the honesty requirements are the point of this task:**
  - **Two distinct telegraphs, mandatory** — the validator from A04 already rejects a Death choice with fewer than two, so this is enforced, but the *quality* is on you: they must be sensory and specific (a warmth, a smell, a sound), following §4.2's model. Two variations of "it looks dangerous" do not count as two.
  - **The warnings must be available before the choice**, not delivered as part of the death text. A player must be able to read the room and decide not to go.
  - **The death result must state its cause** in a single sentence that names what happened, so E01 and the player both know why. Produce it as structured data, not as prose buried in the room text.
  - **The death must be reachable but not accidental.** A player who reads the room should be able to avoid it; a player who ignores the warnings should be able to walk into it deliberately. There must be no path where the death occurs without the player having chosen it.
  - **The threshold must not be a fake room.** It is a place you die, and the content must not imply you can explore it — that would break the promise §13 makes about honest choices.
- **Voice:** restraint over gore; the kitchen is described by what is *wrong* with approaching it, not by an inventory of blood (pillar 1).

## Preconditions
- [ ] D01 DONE — the left doorway choice exists with two telegraphs and Death tier
- [ ] A04's format validator is in place and enforces the two-telegraph rule
- [ ] B03's Death-tier placeholder still routes correctly
- [ ] C01 DONE, so the death's oil context is coherent (the doorway costs the entry drain before the death lands, or does not — decide and record which)

## Actionable Steps
1. Decide and record whether walking into the doorway costs the room-entry drain before the death, and make the behavior match the recorded decision.
2. Author the destination: a short, final threshold scene that is unmistakably terminal and does not invite exploration.
3. Confirm the two telegraphs are present on the choice and are distinct in kind, not just in wording.
4. Implement the death result as structured data carrying a one-sentence cause.
5. Confirm the Death tier routes through B03's placeholder, and that the placeholder receives the cause rather than a generic message.
6. Verify no path reaches the death without the player selecting the doorway.
7. Walk the path: read the room as a first-timer, decide whether you feel warned, then walk into it deliberately and confirm the death states its cause.

## Test Plan
- **Tests to write:** D06 adds a case asserting the doorway choice carries two or more distinct telegraphs and Death tier, and that reaching it produces a death result with a non-empty cause.
- **Commands:** run A04's validator; then `python index.py` and walk the doorway.
- **Expected:** the room warns twice before the choice; choosing the doorway ends the run at the threshold with a cause stated; there is no way to die without selecting it.
- **Honesty observation (the real check):** show the room to someone who has never played. Ask whether they felt warned. If they say no, the telegraphs are too subtle — rewrite them. This is the observation §12's success test ultimately depends on.
- **Avoidability check:** confirm a player can complete the run without ever taking this choice.

## Definition of Done / Acceptance Criteria
- [ ] The doorway has at least two telegraphs that are distinct in kind, in the §4.2 style
- [ ] The warning is available before the choice is made, not delivered with the death
- [ ] The death result carries a one-sentence cause as structured data
- [ ] The death is unreachable without the player selecting the doorway
- [ ] The threshold scene does not invite exploration
- [ ] The death is avoidable, and the run is completable without it
- [ ] The oil behavior at the doorway matches the recorded decision
- [ ] No engine or screen file changed except where B03's placeholder already lives

## Rollback / Undo
Revert this task's commit. The doorway choice remains but no longer produces a death, which removes AC-6 and leaves the slice without a failure state — revert together with D01's door tier, or the content will no longer match the slice's design. Verify the content set validates after reverting.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the oil decision and the first-timer honesty observation here -->
