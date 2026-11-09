# Task A07: THE HALL content — hub, two doorways, the stuck front door

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: A06, A04
- Blocks: A09
- Covers: AC-1, AC-2, AC-23
- Suggested commit: `content(hall): build the hall as a hub with two doorways and a stuck front door`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author THE HALL as a hub rather than a corridor: two doorways, a staircase up, and a front door that is visibly, insultingly unlocked-but-stuck.

## Non-Goals
- Does not make the front door yield. §6 says the third attempt works; in this phase the door is described and refuses. **Making it yield is F05**, and the third-attempt counter that persists across runs is F05's to build.
- Does not build the staircase as a walkable room — ASM-13 keeps §6's Stairwell in Phase 3+. The staircase is described.
- Does not author the left doorway's death — that is A09, which adds the choice and its telegraphs to this room.
- Does not author OLD LIBRARY — that is A08.
- Does not build the kitchen or the yard — those are F02 and F04.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6's THE HALL entry in full — "Keep it as the 'safe' tutorial room, but make it a *hub*, not a corridor. Two doors, a staircase up, and a front door that is visibly, insultingly, unlocked-but-stuck. The player will try it three times across two runs. Let the third attempt work." — plus §2.1's premise, §7.4's colour grammar, and §13's "text walls".
- **Files to create:** the content file for this room (to be created), in the JSON-compatible format `game/content_schema.py` defines. Keep the whole content set in one file for the slice, or one file per room — decide once, record it, and keep it consistent for A08 and beyond.
- **Files to read, not modify:** `game/content_schema.py` — the room record shape (`id`, `name`, `prose`, `choices[]`), `start_room`, `validate_content()`, and `SAMPLE_CONTENT` as the format precedent; `game/effects.py` for the verbs available (`spend_oil`, `grant_item`, `set_flag`) and predicates (`has_flag`, `has_item`, `lantern_above`).
- **Conventions to respect:** content as data (§11); the HALL is the configured `start_room`; ids follow the existing short-snake convention (`hall`, `hall_left`, `old_library`).
- **Design constraints:**
  - **≈ 20 usable lines of prose** (§13, ASM-18). If the hall needs more, it is two rooms.
  - **The front door must read as insulting, not as locked.** §6 says *unlocked-but-stuck*: the refusal is physical, not a key check, and the prose must make the player want to try again.
  - **Three attempts across two runs** implies the attempt is *remembered*. Persisting that counter is F05's work; here the door refuses and the refusal is recorded as a flag the way F05 will need it.
  - **The hub teaches the lantern.** §3.1's "already lit" discount is most visible on a room the player returns to, so the hall's return visit should be where they feel it (A05 supplies the rule).
  - **No prose in `screens/`** — AC-22 holds here too.
- **Voice:** dread over gore. The hall is the one room where nothing is wrong yet, which is exactly what should make it unnerving.

## Preconditions
- [ ] A03 DONE — choices render and resolve
- [ ] A05 DONE — the revisit discount exists, so the hub's return visit is meaningful
- [ ] A06 DONE — the oil context the hall introduces is real
- [ ] The content file location and format are decided and recorded
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Decide the content file layout (one file for the set, or one per room) and record the decision in the Execution Log — A08 and the whole of Slice F will follow it.
2. Author the hall's `id`, `name`, and `prose` within the ≈ 20-line budget: a high hall, two doorways, a staircase up, and the front door.
3. Author the front-door choice: it refuses, and its refusal is phrased as *stuck*, not *locked*. Record the attempt as a flag so F05 can count it.
4. Author the staircase as described-but-unreachable content — no destination, or a choice that honestly refuses. It must not imply a walkable room exists.
5. Note the right-hand passage toward the library (A08 supplies the destination room) and the left doorway (A09 supplies its death) — or author the choice stubs here if A09 is not yet started, and say so in the log.
6. Confirm the hall is the `start_room` and that the validator reports a clean content set.
7. Check the colour grammar: nothing in the hall should be red (§7.4).
8. Read the prose aloud at a normal pace; if it takes more than about a minute, cut it.

## Test Plan
- **Tests to write/update:** A13's suite owns content regression, but add the hall's own cases now in `tests/test_content_schema.py`'s style, or a new `tests/test_content_house.py` (to be created):
  - `test_hall_is_the_start_room` — asserts `start_room` resolves to the hall.
  - `test_front_door_refuses_and_records_an_attempt` — asserts the choice does not move the player and sets the attempt flag.
  - `test_hall_prose_fits_the_line_budget` — asserts the prose length against the ≈ 20-line limit (ASM-18).
  - `test_content_validates_clean` — asserts `validate_content()` returns no problems.
- **Commands:** `python -m pytest tests/test_content_house.py -v`; then `python -m pytest`.
- **Manual verification:** start a run in the hall, try the front door, and confirm the prose makes you want to try it again — that reaction is the whole point of §6's note.
- **Reaction check:** if the door reads as "locked", rewrite it as "stuck". A locked door is a key puzzle; a stuck door is an insult.

## Definition of Done / Acceptance Criteria
- [ ] The hall is the configured `start_room` and the content set validates clean
- [ ] The hall is a hub: two doorways and a staircase, not a single corridor
- [ ] The front door refuses in a way that reads as stuck, not locked, and records the attempt
- [ ] The staircase does not imply a walkable room
- [ ] Prose is within the ≈ 20-line budget
- [ ] No prose from this room appears anywhere under `screens/`
- [ ] No red styling is implied or used in this room
- [ ] The content file layout decision is recorded in the Execution Log
- [ ] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; the content set loses its start room and the game cannot begin — `validate_content()` will report a missing start room, which is the correct, loud failure. Revert A08 and A09 alongside it.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the content file layout decision here -->
