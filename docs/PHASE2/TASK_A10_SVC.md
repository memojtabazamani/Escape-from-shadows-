# Task A10: One honest ending at the front door

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: A08, A09
- Blocks: A11
- Covers: AC-1, AC-2
- Suggested commit: `content(hall): make the front door yield once the book is known`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make THE HALL's front door yield once the player holds the BOOK's knowledge, producing the slice's one honest ending and making the second visit to the hall mean something.

## Non-Goals
- Does not implement the third-attempt counter — that is F05. This ending is gated by **knowledge**, not by attempt count; F05 later reconciles the two and decides which governs.
- Does not implement the multiple-ending spread or an endings gallery — ASM-10 and §2.3 keep those in Phase 3.
- Does not present the ending — that is A11. This task produces the ending *result*.
- Does not author the knowledge flag — that is A08; this task reads it.
- Does not add a key requirement — §3.3's front-door key with its three routes is F06.

## Context & Constraints
- **Read first:** Phase 1's ASM-4 (`docs/PHASE1/EPIC_Phase1_VerticalSlice_PLAN.md`) for the reasoning behind this scope call — "**The 'one honest ending' is the HALL's front door yielding once the BOOK's knowledge is held.** This reuses both Phase 1 rooms, makes the second visit to the HALL meaningful (design pillar 3, 'choices echo')" — plus §6's front-door note, §2.3's ending table for tone, and §11's "conditionals become requirements".
- **Files to modify:** the content file(s) from A07.
- **Files to read, not modify:** `game/effects.py` — the `has_flag` predicate is the requirement mechanism; `game/content_schema.py` for the requirement record shape; the knowledge flag name recorded by A08.
- **Conventions to respect:** content as data — the gate is a `requirements` entry on the choice, not a branch in the loop; the ending is a room the door leads to, consistent with A09's threshold pattern.
- **Design constraints:**
  - **The gate is knowledge, expressed as `has_flag`.** No new predicate is invented here; C02 owns engine-contract extension.
  - **The door must refuse informatively before the flag is held** — a refusal that names the reason, in the manner A03 already supports, so the player learns there is something to learn.
  - **≈ 20 usable lines** for the ending's prose (§13).
  - **Pillar 3 holds:** the ending must be *better* because the player already saw the hall and the library, not merely later.
  - **Tone** follows §2.3's "standard win" register — an exit, not a triumph.
- **Voice:** the ending is quiet. §12's Phase 1 does not ask for spectacle, and §7.3 reserves ASCII art for three moments, none of which this is.

## Preconditions
- [ ] A08 DONE — the knowledge flag exists and its name is recorded
- [ ] A09 DONE — the death path exists, so the run has both terminal states
- [ ] A07 DONE — the front door choice exists and refuses
- [ ] A03 DONE — `has_flag` requirements render as informative refusals
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read A08's recorded flag name and add a `has_flag` requirement to the front-door choice.
2. Author the refusal the player sees *without* the flag: it must name the reason (via the resolver's `reason`) and must not read as a locked door, to stay consistent with A07's "stuck" framing.
3. Author the destination room: the ending's prose, within the ≈ 20-line budget, in §2.3's "standard win" register.
4. Make the ending terminal in the same way A09's death is — a result the screen routes on, not a room with choices.
5. Decide what the run does after the ending (return to menu, offer a new run) and record it; A11 renders both branches, so the decision must exist as data first.
6. Confirm the walk: hall → library → read → hall → front door yields, and hall → front door without reading refuses with a reason.
7. Confirm the ending is reachable without ever taking A09's death — the two terminal states must be independent.

## Test Plan
- **Tests to write/update:** extend `tests/test_content_house.py`:
  - `test_front_door_refuses_without_the_knowledge_flag` — asserts the refusal carries a reason and does not move the player.
  - `test_front_door_yields_with_the_knowledge_flag` — asserts the destination is reached once the flag is set.
  - `test_ending_prose_fits_the_line_budget` — asserts the ≈ 20-line limit.
  - `test_both_terminal_states_are_reachable_independently` — asserts the ending and the death can each be reached without the other.
- **Commands:** `python -m pytest tests/test_content_house.py -v`; then `python -m pytest`.
- **Manual verification:** complete a full run twice — once reading the book, once not — and confirm the difference is knowledge, not luck.
- **Echo check (pillar 3):** the second visit to the hall should feel different from the first. If it does not, the ending is gated but not *earned* — add a line of prose that acknowledges the return.

## Definition of Done / Acceptance Criteria
- [ ] The front door refuses without the flag, naming the reason, and moves nobody
- [ ] The front door yields with the flag, reaching a terminal ending state
- [ ] The gate uses the existing `has_flag` predicate; no new engine predicate was added
- [ ] Both terminal states are independently reachable
- [ ] The run's post-ending behaviour is decided and recorded as data
- [ ] Ending prose is within the ≈ 20-line budget
- [ ] The second visit to the hall reads differently from the first
- [ ] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; the front door refuses forever and the slice has no win state, leaving AC-1's "playable end to end" unsatisfied. Revert A09 alongside it or the slice has a death with no counterpart.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the post-ending decision here -->
