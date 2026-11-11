# Task B04: Hints — the Shadow's taunts double as hints on EASY

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: B — Difficulty as a Real System
- Layer: SVC
- Status: DONE
- Estimate: ~2.5h
- Depends on: B02
- Blocks: B06
- Covers: AC-16
- Suggested commit: `feat(difficulty): make the shadow hint on easy`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make EASY give information: when the player is stuck, the Shadow speaks, and what it says is a usable hint disguised as a taunt — while MEDIUM and HARD stay silent.

## Non-Goals
- Does not build the Shadow as an entity — ASM-11: no pursuit, no presence rules, no history-drawn dialogue. **It speaks and is gone.** That is the whole implementation.
- Does not write the journal's Shadow-line log — that is E01/E02; this task produces lines, E02 records them.
- Does not implement the Shadow's Phase 3 taunt system or its learning pattern (§2.2) — Phase 3.
- Does not implement the HARD pressure mechanics — that is B05.
- Does not add a "hint" command or a keybinding. The hint arrives as narration; §13's puzzle-integrity note means a player must not be able to *ask* for the answer on HARD.

## Context & Constraints
- **Read first:** §5.1's information bullet, §2.2 for the Shadow's voice (this is the only place its character is defined before Phase 3), §4.2's "telegraph, don't announce" — a hint must *point*, never *state* — and §13's puzzles-without-solutions note plus pillar 2.
- **Files to create/modify:** `game/hints.py` (to be created) or the hint logic in `game/difficulty.py` if it stays small enough to be one concern; the content or a small data table of hint lines.
- **Files to read, not modify:** `screens/game.py`'s narration region (A02) — a hint is narration and should use the existing channel rather than a new widget; `game/state.py` — the "stuck" signal needs a home on the run; `game/effects.py`.
- **Conventions to respect:** content-as-data (§11) — the hint lines are data keyed to a room or a stuck-condition, not prose inside a screen. Whatever records the Shadow's lines must be the same store E02 writes the journal from.
- **Design constraints — a hint that solves the puzzle is a failure:**
  - **Point, don't state.** The §4.2 model applies. "You have not looked behind the shelves" is a hint; "go to the library and read the book" is a walkthrough.
  - **Nothing may be named that the player has not already encountered.** A hint cannot reference a room the player has never seen — that leaks content and breaks the discovery the game is about.
  - **A stuck trigger must be real.** Decide and record what "stuck" means — N turns in one room, N refused choices, N revisits. It must be impossible for the hint to fire during ordinary competent play, or EASY becomes a narrator that talks over the game.
  - **EASY only.** MEDIUM and HARD produce no hints at all. This is the information axis of §5.1 and is asserted by B06.
  - **The hint must be usable.** "Point don't state" is not licence to be cryptic: the player must be able to act on it. Test it by asking whether someone could follow it.
  - **The Shadow's voice is earned.** It speaks rarely. If a hint fires often, the character is spent before Phase 3 uses it.
- **Voice:** the Shadow's lines are second-person and unpleasant — it addresses you, it knows what you did, and it is amused. Read §2.2 for register. It should be *right* and *disliked*.

## Preconditions
- [ ] B02 DONE — the difficulty config has an information group
- [ ] A02 DONE — narration renders and has a channel a hint can use
- [ ] A07, A08, A09, A10 DONE — there are rooms and puzzles worth hinting about
- [ ] The content set's room and choice ids are stable, so hints can key to them
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Decide and record the stuck trigger, and where it is counted on the run.
2. Create the hint data: one or more lines per room or per blocked condition, keyed by id, following the content record style.
3. Write the hint selection: pick the line whose condition currently holds, preferring the most-recently-relevant one; do not repeat an already-delivered hint.
4. Gate the whole path on the config's information parameter.
5. Route the delivered line through A02's narration channel, in whatever style §7.4 assigns to the Shadow (decide and record — the color-grammar rule reserves red for the Shadow's presence, so this needs an explicit call).
6. Record each delivered line wherever E02 will look for the journal, using the same store.
7. Walk EASY into every room and every refusal; confirm the hint fires where expected and **never** during a competent run.
8. Ask of each hint: could a stuck player act on this? Rewrite any that only sound meaningful.

## Test Plan
- **Tests to write/update:** new `tests/test_difficulty_hints.py` (to be created):
  - `test_hints_fire_on_easy_and_never_on_medium_or_hard` — the axis check, asserted across all three.
  - `test_a_hint_is_not_delivered_twice` — guards against repetition fatigue.
  - `test_hints_only_reference_encountered_content` — asserts no hint names an unseen room or item.
  - `test_hint_does_not_fire_during_a_competent_run` — the trigger check; drives a clean route and asserts silence.
  - `test_delivered_hints_are_recorded_for_the_journal` — the E02 handoff, asserted as an interface.
- **Commands:** `python -m pytest tests/test_difficulty_hints.py -v`; then `python -m pytest -v`.
- **Manual verification:** play EASY deliberately badly — refuse everything, dawdle — and confirm a hint arrives and is followable. Then play EASY well and confirm silence.
- **Usability check (the real one):** hand a hint to someone who is stuck and watch whether they act on it. A hint that requires interpretation has failed, whichever pillar it cites.

## Definition of Done / Acceptance Criteria
- [x] A stuck trigger exists, is recorded, and cannot fire during a competent run
- [x] Hints are content data keyed by room or condition, not prose in a screen
- [x] Hints fire on EASY only, asserted across all three difficulties
- [x] No hint is delivered twice in a run
- [x] No hint references content the player has not encountered
- [x] Each hint is actionable — verified by observation, not by reading
- [x] Delivered lines are recorded in the store E02 uses for the journal
- [x] The rendering style for the Shadow's lines is decided and consistent with §7.4
- [x] No Shadow entity, pursuit rule, or presence mechanic was introduced
- [x] `python -m pytest -v` passes, including the three pre-existing modules and A13's suite

## Rollback / Undo
Revert this task's commit; EASY loses its information advantage and difficulty differs only in generosity, which is a coherent state but leaves AC-16 half-satisfied. B06 depends on this task's behaviour, so revert as a group.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the stuck trigger, the rendering-style decision, and the usability observation here -->
