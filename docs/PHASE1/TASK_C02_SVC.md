# Task C02: Zero-oil condition and its honest consequence

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: C — The Cost
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: C01
- Blocks: C03, D05
- Covers: AC-4, AC-6
- Suggested commit: `feat(game): handle the zero-oil condition honestly`
- Branch: per GP-3

## Objective
Decide and implement what happens when the oil runs out — and make it honest rather than surprising. The run must end in a way the player saw coming, consistent with SUGGEST.md's rule that an unwarned ending is a bug (§4.1, §13).

## Non-Goals
- Does not implement the Shadow reaching you at zero oil (§3.1, §2.2) — the Shadow is Phase 3.
- Does not implement a refill item or an oil can; the BLOOD KITCHEN's oil is Phase 2 content (§6).
- Does not implement the death screen itself (E01) — it routes to the existing Death-tier placeholder from B03.
- Does not implement difficulty scaling of the mercy shown here (Phase 2, §5.1).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.1 (zero oil is a real state, and the design intent that light is both resource and leash), §4.1 (death must be earned, with warnings), §13 ("unwarned death" is the single biggest fairness flaw in the baseline), and `game/lantern.py` (C01's rates and any zero predicate).
- **Files to modify:** `game/lantern.py` (a zero-state predicate if C01 did not expose one) and `screens/game.py` (the behavior).
- **Files to create:** none expected.
- **Files to read, not modify:** `game/state.py`, `game/effects.py`.
- **Conventions to respect:** PEP 8; type hints; the outcome must be expressed through the same tier and result vocabulary the rest of the game uses, so E01 can route it without a special case bolted on.
- **Design decision to make and record — choose one, in the Execution Log, with a reason:**
  - **(a) Zero oil is a Scar that closes the winning path.** With no light the BOOK cannot be read, so the only remaining exit is the telegraphed death. The run does not end abruptly; it becomes unwinnable, and the player can see that. *Recommended — it keeps the cost a cost rather than a cutscene.*
  - **(b) Zero oil is its own telegraphed ending.** The dark takes you, but only after at least two warnings (the amber meter dropping, a prose warning, then a second prose warning). This satisfies §4.1 but ends the run more bluntly.
- **Warning requirement (mandatory under either option):** the player must receive **at least two distinct warnings** before the outcome lands — a persistent visual warning (the amber meter from B04 already provides one) plus at least one prose telegraph from content. A silent zero is prohibited by §13.
- **Rationale for either option must cite §4.1's requirement that death be earned, not incidental.**

## Preconditions
- [ ] C01 DONE — the lantern can actually reach zero
- [ ] B04 DONE — the amber low-oil warning exists, so warning one is in place
- [ ] The decision above is made and recorded

## Actionable Steps
1. Record the decision and the reasoning in the Execution Log.
2. Ensure a zero-oil predicate exists in `game/lantern.py` and is the single source of truth for "the light is gone".
3. Implement the outcome per the chosen option, expressed through the existing result and tier vocabulary rather than a new bespoke path.
4. Implement the prose warning hook: the second warning must come from content, so add the requirement that the relevant room records carry a low-oil telegraph variant — and record that as a constraint Slice D must satisfy.
5. Verify the player always receives the meter warning plus at least one prose warning before the outcome takes effect.
6. Verify the outcome cannot occur without the warnings, even if content is authored carelessly: assert the warning count in the code path rather than trusting the content.
7. Play a run to zero oil and confirm the experience matches the recorded decision.

## Test Plan
- **Tests to write:** C03 owns them. C03 must cover: the zero predicate flips exactly at zero; the outcome cannot fire before the required warnings are delivered; under option (a) the winning path becomes unreachable at zero oil; under option (b) the outcome routes to the death path with its telegraphs attached.
- **Commands:** `python index.py`
- **Expected:** the lantern reaching zero produces the recorded outcome, preceded by the amber warning and at least one prose warning, with no abrupt or unannounced end.
- **Manual:** a first-time-observer check — play to zero and confirm you could have predicted what was coming.
- **Syntax check:** `python -m py_compile index.py screens/*.py game/*.py`

## Definition of Done / Acceptance Criteria
- [ ] The zero-oil behavior matches the recorded decision, and the reason is logged
- [ ] At least two distinct warnings precede the outcome, and the code path asserts this
- [ ] The outcome uses the existing result and tier vocabulary, not a parallel mechanism
- [ ] The outcome cannot fire silently, even with careless content
- [ ] The constraint this places on Slice D's content is recorded for D01 and D02
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. Zero oil becomes inert — the lantern reaches zero and nothing further happens — which is unsatisfying but harmless. C01's drain rules remain intact.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the chosen option and its reasoning here -->
