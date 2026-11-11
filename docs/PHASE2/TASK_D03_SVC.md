# Task D03: Zero composure — the voluntary walk into the Shadow

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: D — Composure
- Layer: SVC
- Status: DONE
- Estimate: ~2.5h
- Depends on: D01
- Blocks: D05
- Covers: AC-11
- Suggested commit: `content(composure): let zero nerve end in a walk, not a death`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make zero composure end the run the way §3.2 says it does: the player walks into the Shadow, deliberately — a third terminal state that is neither the doorway death nor the front-door ending.

## Non-Goals
- Does not make the Shadow a pursuing entity — ASM-11: no pursuit, no presence rules, no lit-room rule. It is waiting, and you go to it.
- Does not treat zero as a death. AC-11's whole point is that it is not: it produces its own terminal state with its own meaning, and the death screen's cause must not be repurposed for it (though it may share presentation if that reads honestly — decide and record).
- Does not implement the death screen's teaching lines — I03/I04. If this terminal state uses A11's screen, the integration surface is A11's, and any addition belongs to I03.
- Does not write the ending's prose consequences for other endings, or add to §2.3's spread — ASM-10, ASM-17.
- Does not drain composure to zero as a punishment. §4.1's tiers govern *choices*; this is a resource reaching its floor, and it must not double as a fourth tier.

## Context & Constraints
- **Read first:** §3.2's zero-composure rule and why it is a walk rather than a death, §2.2 for the Shadow's characterization (this is its one appearance in the phase, so it must land), §2.3's ending table for tone, and ASM-17 — "only **the front door** produces an *escape* ending in Phase 2; the other terminal states are the death screen and the zero-composure walk."
- **Files to modify:** the content file(s) for the hall (or wherever the walk is triggered), and the content schema if a third terminal kind needs declaring.
- **Files to read, not modify:** `game/content_schema.py` — `TIERS = {"scar", "setback", "death"}` is the existing taxonomy, and a terminal *walk* is not a death tier. **Decide whether this is a new terminal kind, a room with no choices, or a death-tier entry with different meaning, and record the decision** — it is the task's central design call and the schema's shape is what makes it visible. `game/composure.py` (D01); `screens/death.py` and `screens/ending.py` (A11) — one of them must render this, and which one is part of the decision.
- **Conventions to respect:** content-as-data (§11) — the trigger threshold and the walk's prose are content, not code. The composure floor is code (D01's clamp); what happens at it is content.
- **Design constraints:**
  - **It must be voluntary in the fiction.** The player walks. That is not a euphemism for a scripted death — the prose and the player's framing must make it a choice made in a state where choosing well is no longer possible. §3.2's design intent is that it lands differently from dying, and it will only do so if the writing commits.
  - **It must be reachable but not cheap.** Reaching zero should take sustained bad decisions, so it is a real state a careless player discovers and a careful one never sees. Record how many rooms of drain it takes at MEDIUM.
  - **It must be telegraphed like everything else.** §4.1's honesty generalises, and AC-21's spirit applies: a player should feel the bar approaching its floor and know what waits there. The drop is visible (D04's bar); what the floor *means* should be foreshadowed in prose, and the Shadow's hints (B04) may carry it.
  - **It must not be reachable by accident in the first rooms.** A player who has barely started should not be able to stumble into it; check the minimum-room count.
  - **Snapshot/restore must not lose the state**, and I01 must be able to tell a walk-terminated run from a death-terminated one.
- **Voice:** the Shadow finally speaks at length. §2.2's register. It should be the phase's best-written passage, because it is the one time the antagonist is on stage.

## Preconditions
- [ ] D01 DONE — composure exists with a floor and drains
- [ ] A11 DONE — the terminal screens exist, so the walk has somewhere to land
- [ ] The terminal-kind decision is made and recorded before implementation
- [ ] GP-7 confirmed — ASM-11 and ASM-13: no Shadow pursuit, no new rooms
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `game/content_schema.py`'s terminal handling and decide the walk's representation; record the decision and its reasoning.
2. Author the walk's prose per §2.2's register, within the room budget.
3. Implement the trigger: at the composure floor, the run enters the walk's terminal state, reachable from the content's structure rather than from a hardcoded room.
4. Wire presentation to whichever of A11's screens the decision chose, and record which — including how it is distinguished from the doorway death on screen.
5. Decide and record whether the walk carries telegraphs, and if so what they are.
6. Measure the minimum rooms of drain required to reach zero at MEDIUM and at HARD; record both.
7. Confirm the run is fully completable without ever reaching zero.
8. Walk it: from full composure, drain to the floor, and confirm the arrival reads as a walk rather than a punishment.
9. Confirm I01 will be able to distinguish this terminal state from a death — record what field carries it.

## Test Plan
- **Tests to write/update:** new `tests/test_composure_floor.py` (to be created):
  - `test_zero_composure_enters_the_walk_and_not_the_death_screen` — the AC-11 assertion, distinguishing the two terminal states.
  - `test_the_walk_is_unreachable_in_the_first_rooms` — asserts a minimum-room floor.
  - `test_the_walk_is_reachable_by_sustained_drain` — asserts it is not dead content.
  - `test_run_is_completable_without_reaching_zero` — the avoidability check.
  - `test_terminal_kind_is_recorded_distinguishably` — the I01 handoff.
  - `test_walk_prose_fits_the_room_budget` — ASM-18.
- **Commands:** `python -m pytest tests/test_composure_floor.py -v`; then `python -m pytest -v`.
- **Manual verification:** drain deliberately and read the arrival; then finish a clean run and confirm you never saw it.
- **Read-aloud check:** the Shadow's passage is the phase's best prose or it is a problem. Read it aloud and record the judgement.

## Definition of Done / Acceptance Criteria
- [ ] The walk is a distinct terminal state, not a death — asserted by test and distinguishable in the saved run state
- [ ] The terminal representation is decided, recorded, and consistent with `TIERS` or its documented extension
- [ ] The walk's prose is authored in §2.2's register and fits the room budget
- [ ] It is reachable only after sustained drain; the minimum-room count is measured at MEDIUM and HARD and recorded
- [ ] The run remains completable without ever reaching zero
- [ ] The telegraphing decision is made and recorded
- [ ] The Shadow does not pursue, appear elsewhere, or gain presence rules
- [ ] The screen it lands on is recorded, along with how it differs from the doorway death
- [ ] `python -m pytest -v` passes, including A13's suite and Slice C/D tests

## Rollback / Undo
Revert this task's commit; zero composure returns to being merely a very low number with no consequence, which leaves AC-11 unmet and §3.2's most distinctive rule unimplemented. D05 depends on this behaviour — revert as a group.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the terminal representation decision, the presentation decision, the telegraph decision, and the minimum-room measurements here -->
