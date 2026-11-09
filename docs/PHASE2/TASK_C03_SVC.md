# Task C03: Item definitions as content

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: C — Inventory
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: C02
- Blocks: C05
- Covers: AC-7
- Suggested commit: `content(items): define the six candidate items as content`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Turn §3.3's six candidate items from prose in the blueprint into content records with descriptions, and place each one's acquisition in the room it belongs to.

## Non-Goals
- Does not place items in rooms that do not exist yet. Slice F builds BLOOD KITCHEN and OLD YARD; **items belonging to those rooms are authored here as definitions and placed by F02 and F04.** Record which placements are deferred, so nothing is silently forgotten.
- Does not implement the drop-to-take UI — that is C04.
- Does not implement the items' *effects* beyond what the existing verbs express. The cleaver, the whistle and the book have behaviours that belong to Slices F and G; this task defines them as things you can hold.
- Does not make any item a key — §3.3's front-door key with its three routes is F06.

## Context & Constraints
- **Read first:** §3.3 in full — the six candidates, each with its weight, its cost, and its room — §6 for which room each belongs to, and GP-5, which asks the owner to confirm the item list is **exactly** these six plus the key, with no additions.
- **Files to create:** an item-definition content file following the layout A07 established (to be created), or an items section inside the existing content file if A07 chose one file.
- **Files to modify:** the content file(s) from A07 and A08 to place the items that belong to THE HALL and OLD LIBRARY.
- **Files to read, not modify:** `game/content_schema.py` — item definitions are a **new record type**; the validator must learn to check them (unique ids, every `grant_item` reference resolves to a definition, names and descriptions present). Decide whether that extension is schema work here or belongs with C02's verdict; do not silently skip validation.
- **Conventions to respect:** content-as-data (§11) — an item is a record, not a constant in a Python module. The record style must match `content_schema.py`'s existing shape: `id`, `name`, prose, and the mechanical fields.
- **Design constraints — §3.3's items are all costs, and the content must say so:**
  - **Every item description carries its cost or its risk**, because §3.3's items are not upgrades. The book is heavy and slow; the cleaver is loud. The description is where the player learns that, so it is design surface, not flavour text.
  - **Names in the game's register** — short, concrete, the register §7.4 assigns to interactables.
  - **No item may be required for a room's basic traversal.** ASM-14 and §3.3: items open *options*, not doors. The one exception is §3.3's key, which is F06's and is explicitly a three-route puzzle precisely so it cannot hard-gate.
  - **Ids are stable and referenced by content.** C03 records the id for each item; F02, F04, F05, F06, G02 and G03 all reference these ids. Choose them once, record them, and do not rename them later without following the Change Protocol.
  - **Descriptions respect the ≈ 20-line room budget** (ASM-18) — an item description is one or two lines, since it is rendered inside a room that is already near its budget.
- **Voice:** §7.4 — dim grey for narration, white for interactables. Item names are interactables; their descriptions are narration. Keep both registers distinct in the writing.

## Preconditions
- [ ] C02 DONE — the new verbs and predicates exist and the validator accepts them
- [ ] GP-5 answered — the item list is confirmed as exactly §3.3's six plus the key
- [ ] A07 and A08 DONE — the hall, the library, and the content layout exist
- [ ] The content schema's route for a new record type is decided (here, or C02's verdict)
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `game/content_schema.py` to see how a record type is declared and validated, and follow that shape.
2. Author all six item definitions: `id`, `name`, a one-or-two-line description that names the cost or the risk, and any mechanical field the design needs.
3. Record every item id in the Execution Log — six ids that five later tasks depend on.
4. Place the items belonging to THE HALL and OLD LIBRARY using `grant_item` in the appropriate choices.
5. Record the deferred placements explicitly: which items belong to BLOOD KITCHEN, OLD YARD, and the front door, and which task places each.
6. Extend the validator to check that every `grant_item` reference resolves to a definition, and that item ids are unique — or record the handoff if the schema extension belongs elsewhere.
7. Confirm no content makes an item a traversal requirement.
8. Walk the two existing rooms and confirm every obtainable item is described and its cost is legible.

## Test Plan
- **Tests to write/update:** extend `tests/test_content_house.py` and add `tests/test_item_definitions.py` (to be created):
  - `test_all_six_items_have_definitions` — the completeness check.
  - `test_every_grant_item_reference_resolves` — the referential-integrity check, which is also the validator's new rule.
  - `test_item_ids_are_unique_and_stable` — asserts the ids recorded in the log are the ids in the content.
  - `test_every_item_description_states_a_cost_or_risk` — the §3.3 design rule, made mechanical.
  - `test_no_item_is_required_for_basic_traversal` — the ASM-14 guard at the content level.
- **Commands:** `python -m pytest tests/test_item_definitions.py -v`; then `python -m pytest -v`.
- **Manual verification:** in each existing room, take an item and read its description; confirm you would know it is a cost, not a gift.
- **Ledger check:** confirm the deferred-placement list names a task for every unplaced item. An item with no owning task is how §3.3 quietly becomes four items.

## Definition of Done / Acceptance Criteria
- [ ] All six §3.3 items exist as content records with ids, names, and descriptions
- [ ] Every definition states the item's cost or risk in its description
- [ ] Item ids are unique, recorded in the Execution Log, and referenced consistently
- [ ] Every `grant_item` reference resolves to a definition, validated mechanically
- [ ] Items belonging to THE HALL and OLD LIBRARY are placed; all others are recorded with their owning task
- [ ] No item is required for basic traversal
- [ ] Item descriptions fit within the room prose budget
- [ ] Item records live in content, not in a Python module
- [ ] `python -m pytest -v` passes, including A13's suite, C01's and C02's tests

## Rollback / Undo
Revert this task's commit; items vanish from content and any `grant_item` reference made in this task becomes invalid, so `validate_content()` fails. C05 and Slice F's item placement depend on these ids — revert as a group, and if F02/F04 have landed, their references must be reverted with it.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record ALL SIX ITEM IDS and the deferred-placement ledger here — five later tasks read this -->
