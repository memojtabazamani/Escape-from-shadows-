# Task F07: Lantern refills and the trade structure (§3.1)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: F — The House
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: F02
- Blocks: F08
- Covers: AC-7
- Suggested commit: `feat(content): add lantern refill mechanics and risk-trade decisions`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the lantern oil refill locations and trade mechanics into the house, ensuring oil refills are scarce and always require a deliberate trade (such as reaching behind the hanging carcass in the kitchen or expending composure).

## Non-Goals
- Does not modify basic lantern drain logic — Slice C and A05 established the drain engine.
- Does not create infinite or free oil fountains (refills are finite and costly).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.1 ("Refills are scarce and always a trade: the oil can in the kitchen is behind the thing in the kitchen. At zero oil, the Shadow can reach you"), AC-7 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `data/rooms/blood_kitchen.json`, item definitions, `game/effects.py` (ensure `refill_lantern` effect is supported).
- **Files to read, not modify:** `game/lantern.py`, `game/content_schema.py`.
- **Conventions to respect:** Conforms to `content_schema.py` and `effects.py`.
- **Design constraints:**
  - Finding the oil canister in the kitchen requires reaching behind the looming silhouette or butchered meat (costs composure and turn).
  - Using the oil canister restores lantern oil up to the maximum capacity.
  - The canister has limited uses (1 single refill).
  - The Matchbox from The Hall provides an emergency single relight if lantern oil runs dry.

## Preconditions
- [ ] F02 (Blood Kitchen) content is authored.
- [ ] Lantern engine supports refilling.
- [ ] Content schema validator passing.

## Actionable Steps
1. Ensure `game/effects.py` has a declarative `refill_oil` or `add_oil` verb that clamps oil to max.
2. In `blood_kitchen.json`, author the trade interaction to extract the Oil Canister:
   - Descriptive warning: grease-streaked metal can resting on an iron hook behind cold hanging carcass.
   - Cost: -3 Composure, consumes 1 turn.
   - Grants item: `oil_canister` (or immediately refills lantern, according to player choice).
3. If held as an item, allow consuming `oil_canister` to replenish oil.
4. Ensure the oil trade can only be taken once per run (sets flag `kitchen_oil_claimed`).
5. Author Matchbox interaction: allows striking a match when oil reaches 0 to buy 1 extra turn of faint illumination.

## Test Plan
- **Tests to write/update:** `tests/test_lantern_refills.py`:
  - `test_oil_canister_refills_lantern` — using the oil canister increases lantern oil and clamps at max.
  - `test_kitchen_oil_trade_is_finite` — canister can only be taken once per run.
  - `test_matchbox_relight_at_zero_oil` — matchbox provides a single grace turn in darkness.
- **Commands:** `python -m pytest tests/test_lantern_refills.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Lantern refill trade is integrated into the Blood Kitchen.
- [ ] Acquiring oil carries an authentic composure/risk trade.
- [ ] Refill verb clamps cleanly to max capacity.
- [ ] Oil refill is strictly finite per run.
- [ ] All tests pass cleanly.

## Rollback / Undo
Revert refill choices from `blood_kitchen.json` and effects.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
