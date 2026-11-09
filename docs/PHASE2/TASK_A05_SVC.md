# Task A05: Lantern drain rules

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: A03
- Blocks: A06
- Covers: AC-1
- Suggested commit: `feat(lantern): implement the oil drain rules`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Make oil a real, felt cost: entering a room spends it, careful actions spend more of it, and rooms already lit spend less — so the player's curiosity has a price.

## Non-Goals
- Does not implement the zero-oil consequence — that is A06. This task spends oil; A06 decides what happens when there is none.
- Does not author refills — that is F07. §3.1's scarce refills arrive with the kitchen.
- Does not scale drain by difficulty — that is B02. The numbers here are the MEDIUM baseline B02 multiplies.
- Does not render the bar — that is A04, which reads the same state this task writes.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.1 in full — "Your central resource. Every room you enter costs oil. Oil drains **faster** when you take a slow, careful action (searching, reading). Oil drains **slower** in rooms you've already lit... **At zero oil, the Shadow can reach you.** This creates the game's core tension: *understanding the world costs you the safety to explore it.*"
- **Files to create:** `game/lantern.py` (to be created).
- **Files to read, not modify:** `game/state.py` — `spend_lantern(amount) -> int` returns the amount **actually** spent, clamps at zero, and treats a negative amount as zero spend; `has_light()`; `visited` / `has_visited(room_id)`; `advance_turn()`.
- **Conventions to respect:** `AGENTS.md` — shared game state lives in `game/`, screens in `screens/`; `game/effects.py` is the precedent for a small, data-driven module with module-level constants, type hints, and docstrings that explain the contract.
- **Design constraints:**
  - **Drains are constants with names**, defined once at module level like `EFFECT_VERBS` in `content_schema.py` — never magic numbers scattered through the screen.
  - **A revisit costs less than a first visit** (§3.1's "already lit"), and the state to detect a revisit already exists: `RunState.visit()` returns `True` only on the first visit.
  - **A slow, careful action costs more than a step.** The multiplier must be large enough for a player to feel it within a two-room loop, and small enough that a careful run stays possible. State the chosen numbers and the reasoning in the Execution Log.
  - Drain is applied through `RunState.spend_lantern()` so clamping and the "actually spent" return value are never reimplemented.
- **Performance:** drain is arithmetic on one integer — no I/O, no lookups beyond the room id.

## Preconditions
- [ ] A03 DONE — room transitions exist and effects resolve through `resolve_choice`
- [ ] `RunState.spend_lantern()` behaves as documented (verify in `tests/test_state.py`)
- [ ] A04 DONE or in progress, so the drain is observable on screen while developing
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read §3.1 again and write down the three drain situations as named constants: a first visit to a room, a revisit, and a slow/careful action.
2. Create `game/lantern.py` with the constants, a `drain_for_room(state, room_id)` helper that chooses first-visit or revisit, and a `drain_for_action(kind)` helper for careful actions.
3. Return the chosen cost rather than mutating inside the helper, so the caller decides when to spend — this keeps the module testable and keeps `resolve_choice` the single mutation path.
4. Apply the room-entry drain on transition in the screen, using `spend_lantern()`'s return value so the displayed bar matches what was actually spent.
5. Express the book's costly read (A08) and the kitchen's search (F02) through `drain_for_action`, not as bespoke numbers in content.
6. Confirm the revisit discount fires by walking `hall → old_library → hall` and comparing the two `hall` entries.
7. Confirm the bar (A04) and the state agree after every spend, including a spend larger than the remaining oil.

## Test Plan
- **Tests to write/update:** new `tests/test_lantern.py` (to be created):
  - `test_first_visit_costs_more_than_revisit` — asserts the §3.1 discount using a real `RunState`.
  - `test_careful_action_costs_more_than_a_step` — asserts the multiplier's direction and order of magnitude.
  - `test_spend_never_goes_below_zero_and_reports_actual_spend` — asserts the clamped return value when the cost exceeds the remaining oil.
  - `test_drain_is_pure_and_does_not_mutate` — asserts the helpers return a cost without changing the state.
- **Commands:** `python -m pytest tests/test_lantern.py -v`; then `python -m pytest`.
- **Manual verification:** play the two-room loop and confirm the oil visibly drops on entry, drops more on a careful action, and drops less on a revisit.
- **Feeling check (the real test):** after one loop, say out loud how much oil a second loop would cost. If you cannot, the numbers are too small to feel — raise them.

## Definition of Done / Acceptance Criteria
- [ ] `game/lantern.py` exists with named, module-level drain constants
- [ ] Entering a room spends oil; a revisit spends less than a first visit
- [ ] A slow, careful action spends more than a step
- [ ] All spending goes through `RunState.spend_lantern()`; the module is not a second clamp
- [ ] The displayed bar matches the actual spend, including a partial spend at low oil
- [ ] No magic numbers for drain appear in `screens/`
- [ ] `python -m pytest` passes, including the three pre-existing modules
- [ ] Chosen drain values and their reasoning are recorded in the Execution Log

## Rollback / Undo
Revert this task's commit and delete `game/lantern.py`; the game becomes free to explore and the lantern bar (A04) never moves. A06 depends on this task and revert them together. F07's refills are meaningless without drain, so revert those too.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the drain constants and the reasoning for their size here -->
