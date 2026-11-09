# Task C04: Inventory display and the drop-to-take flow

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: C — Inventory
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: C02
- Blocks: C05
- Covers: AC-6
- Suggested commit: `feat(ui): show the inventory and make dropping a deliberate choice`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Show the player what they carry, and when a seventh item is offered, make dropping one a real decision rather than a silent swap.

## Non-Goals
- Does not change the six-slot cap or the model's refusal behaviour — that is C01, and this task must respect it rather than work around it.
- Does not build a separate inventory screen. §7.1's three zones put the inventory in the status zone; the journal (E03) is the keybound overlay precedent, and if a full-screen view proves necessary, that is a change to §7.1's zone design and belongs to the Change Protocol.
- Does not implement the composure bar's slot in the status zone — that is D04. Build the display so D04 can add a bar beside it.
- Does not implement any item's *use*. Items are carried, described and dropped here; Slices F and G give them effects.

## Context & Constraints
- **Read first:** §3.3's "the cap forces a real choice" and §7.1's three-zone layout with its ~20 usable lines, §7.4's colour grammar (white for interactables, amber for resources), and §13's input-friction pitfall, which the drop flow is most likely to trip.
- **Files to modify:** `screens/game.py` — the status zone built in A04, and the choice-resolution path from A03 where a full-pack gate appears.
- **Files to read, not modify:** `game/state.py` (C01's operations and their stable ordering); `game/effects.py` (C02's gate and its reason text); `screens/game.py`'s existing zone structure — **the inventory goes inside the status zone, not in a new region.**
- **Conventions to respect:** `AGENTS.md` — thin `compose()`, rendering delegated to helpers, `CSS` class attribute; `screens/main_menu.py`'s and `screens/settings.py`'s key-handling idiom for a selectable list.
- **Design constraints — the drop must feel like a choice and must not become a modal trap:**
  - **The player initiates the drop.** The model refuses a seventh item (C01); this screen responds to that refusal with an offer to drop, it does not auto-evict. ASM-5's whole point.
  - **Cancellable, always.** A drop prompt the player cannot back out of is the input-friction pitfall. Escape backs out and the item stays where it was — un-taken — rather than half-taken.
  - **Zero new lines in the room's budget.** The status zone has a fixed height; the inventory must render within it. Confirm the room prose still fits §7.1's ~20 lines with a full pack.
  - **A full pack must be visible before it matters.** A player should be able to see six of six slots are used before meeting the seventh item, not discover it at the refusal.
  - **Colour per §7.4:** item names are interactables (white); the capacity indicator is a resource (amber). Do not use red — it is reserved for the Shadow's presence.
  - **Empty is a state.** Zero items must render as something deliberate ("you are carrying nothing"), not as an empty box.
- **Voice:** item names verbatim from C03's definitions; the capacity indicator terse — a count, or a counted graphic. The room's prose is not this task's to write.

## Preconditions
- [ ] C02 DONE — the full-pack gate and its reason exist
- [ ] C01 DONE — the model has stable ordering and a free-slot count
- [ ] A04 DONE — the status zone exists with room for the inventory
- [ ] A03 DONE — the choice path, where a refusal appears, exists
- [ ] C03 DONE, or at least its ids known, so real item names can render
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read A04's status zone and A03's refusal path; decide where the inventory and the capacity indicator sit within the existing zone.
2. Render the inventory list from the model's stable order, with names in the interactables style and the capacity in the resource style.
3. Render the empty state deliberately.
4. Render a full pack distinctly, so the state is legible before the refusal happens.
5. When `apply_effects` or `check_requirements` returns a full-pack gate, present a drop prompt naming the item on offer and the items held.
6. Implement the drop: choose one, confirm, and the flow retries the original action.
7. Implement cancel: Escape backs out with nothing changed — nothing taken, nothing dropped.
8. Verify the room prose plus a full inventory still fits one screen at a narrow width (§7.1, AC-23), and adjust the layout rather than the writing if it does not.
9. Walk: collect to six, meet a seventh, drop one, take the new one, cancel once mid-flow.

## Test Plan
- **Tests to write/update:** new `tests/test_inventory_ui.py` (to be created):
  - `test_inventory_renders_in_the_status_zone` — asserts no new region was added to §7.1's layout.
  - `test_empty_inventory_renders_a_deliberate_state` — guards against an empty box.
  - `test_full_pack_is_visible_before_a_refusal` — asserts the warning precedes the gate.
  - `test_drop_then_take_completes_the_original_action` — the happy path of the flow.
  - `test_cancel_leaves_state_completely_unchanged` — the transactional check; nothing taken, nothing dropped.
  - `test_room_plus_full_inventory_fits_one_screen` — AC-23 at a narrow width.
- **Commands:** `python -m pytest tests/test_inventory_ui.py -v`; then `python -m pytest -v`.
- **Manual verification:** run the flow by hand, including cancel, and confirm the state is exactly as it was.
- **Friction check:** time how many keystrokes a drop-to-take costs. If it is more than a handful, the flow is the problem, not the player.

## Definition of Done / Acceptance Criteria
- [ ] The inventory renders inside the status zone, with no new region and no new screen
- [ ] Capacity is visible before a refusal can occur
- [ ] A full pack presents a cancellable drop prompt naming both the offered item and those held
- [ ] Confirming a drop retries the original action and completes it
- [ ] Escape cancels with nothing taken and nothing dropped — asserted, not assumed
- [ ] The empty inventory renders a deliberate state
- [ ] Colours follow §7.4: interactables white, capacity amber, no red
- [ ] A room with a full inventory still fits one screen at a narrow width
- [ ] No item's effect is implemented here — items are carried and dropped only
- [ ] `python -m pytest -v` passes, including A13's suite and C01–C03's tests

## Rollback / Undo
Revert this task's commit; the inventory stops being visible and a full pack refuses without an offer to drop, so a player can be stuck with a gate they cannot satisfy. That makes the drop flow load-bearing for playability — revert only alongside C01's cap, or restore the flow promptly.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the zone layout decision and the measured keystroke cost of a drop-to-take here -->
