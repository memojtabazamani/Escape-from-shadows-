# Task C05: Inventory tests

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: C — Inventory
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: C03, C04
- Blocks: F03, I01
- Covers: AC-6, AC-7
- Suggested commit: `test(inventory): cover the cap, the drop flow, and item placement`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Close the slice's test net: the cap's boundary, the drop flow's transactionality, item placement, and the rule that no item is ever required to finish the game.

## Non-Goals
- Does not repeat C01's and C02's tests — those exist and must be green. This task covers what they cannot: the slice's behaviour as a whole.
- Does not place the items belonging to unbuilt rooms — F02 and F04 own those placements, and the ledger from C03 records them. This task asserts the *placed* ones and notes the rest.
- Does not fix what it finds. A missing placement is a content bug to report under §4.2, not a test to relax.
- Does not test item *effects* — Slices F and G own them.

## Context & Constraints
- **Read first:** §3.3 in full (this slice's source), ASM-5 (the cap is a real choice), and the C03 ledger naming which item belongs to which room and which placement is deferred to F02/F04.
- **Files to create:** `tests/test_inventory_slice.py` (to be created).
- **Files to modify:** none.
- **Files to read, not modify:** `tests/test_inventory_model.py` (C01), `tests/test_inventory_contract.py` (C02), `tests/test_item_definitions.py` (C03), `tests/test_inventory_ui.py` (C04); `game/state.py`; `game/effects.py`; the content files; `tests/test_vertical_slice.py` (A13) for the traversal-helper pattern this task reuses.
- **Conventions to respect:** A13's traversal helper — reuse it rather than writing a second one, so the reachability claim is computed the same way in both places.
- **Design constraints — the assertions worth having are the ones that catch a design drift:**
  - **The cap is a wall, not a slope.** Assert the exact boundary and assert there is no path around it (no verb, no requirement, no content trick grants a seventh item).
  - **The drop flow is transactional.** Assert that cancel changes *nothing* — not the inventory, not the room, not the turn count, not the oil. A half-applied cancel is the bug this test exists for.
  - **No item is a skeleton key.** The traversal assertion from C03, promoted here to slice level: strip the inventory to empty, traverse the content, and confirm the run is still completable. This is the strongest version of ASM-14's fairness rule and it is worth the computation.
  - **Placement ledger closure.** For every item C03 defined, assert either that it is placed in content or that its placement is recorded in the ledger with an owning task. An item with neither is the silent-drop failure §3.3 is vulnerable to.
- **Voice:** the test names state the slice's promises, in A13's style.

## Preconditions
- [ ] C03 and C04 DONE
- [ ] C01's and C02's tests green
- [ ] A13's traversal helper is available to reuse
- [ ] The C03 ledger is available, listing which placements are deferred
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read A13's traversal helper and the four C tests; list what is already asserted so you do not duplicate it.
2. Write `test_seven_items_cannot_be_held_by_any_route` — the boundary plus the no-way-around check across every verb and requirement.
3. Write `test_cancel_changes_nothing_at_all` — inventory, room, turn count and oil compared before and after.
4. Write `test_run_is_completable_with_an_empty_inventory` — the strongest fairness assertion in the slice.
5. Write `test_every_defined_item_is_placed_or_recorded_as_deferred` — the ledger-closure check.
6. Write `test_items_found_in_their_own_room` — asserts each placed item's grant site matches §3.3's room assignment.
7. Write `test_full_pack_never_blocks_the_ending` — asserts the cap cannot strand a run that needs to finish.
8. Run the whole suite twice to confirm determinism, and record the deferred-item count in the log.

## Test Plan
- **Tests to write/update:** new `tests/test_inventory_slice.py` (to be created) — the seven tests in steps 2–7.
- **Commands:** `python -m pytest tests/test_inventory_slice.py -v`; then `python -m pytest -v` twice.
- **Manual verification:** none beyond A13's playtest pattern; do one by-hand run collecting to the cap and finishing.
- **Negative check:** temporarily allow a seventh item in the model and confirm step 2's test fails, then revert. A cap assertion that cannot fail proves nothing.

## Definition of Done / Acceptance Criteria
- [ ] The cap's boundary is asserted from both sides, with a no-way-around check
- [ ] Cancelling a drop provably changes nothing
- [ ] A run is provably completable with an empty inventory
- [ ] Every defined item is either placed in content or recorded in the ledger with an owning task
- [ ] Every placed item is granted in the room §3.3 assigns it
- [ ] The cap cannot block the ending
- [ ] The traversal claim is computed with A13's helper, not a second implementation
- [ ] The negative check was performed and observed failing before revert
- [ ] The deferred-placement count is recorded in the Execution Log
- [ ] `python -m pytest -v` passes deterministically, including A13's suite and C01–C04's tests

## Rollback / Undo
Revert this task's commit; the inventory keeps working but loses its slice-level net, and F03 and I01 lose a dependency they expect green. Treat a revert as reopening the slice's verification, not as a clean undo.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the deferred-placement count and any content bug found (which becomes its own task) here -->
