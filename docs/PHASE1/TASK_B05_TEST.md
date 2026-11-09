# Task B05: Screen tests and the content-only proof

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: B — The Screen
- Layer: TEST
- Status: TODO
- Estimate: ~2.5h
- Depends on: B03, B04, A06
- Blocks: C03, D01, D02
- Covers: AC-1, AC-8, AC-9
- Suggested commit: `test(screens): cover room rendering, choice sequencing, and meters`
- Branch: per GP-3

## Objective
Test the screen's logic without a real terminal, and prove the architectural claim the whole slice rests on: that a room can be added by editing content alone (AC-9). This is the gate that lets Slice C and Slice D proceed on a trustworthy base.

## Non-Goals
- Does not implement new screen behavior — it tests what B01–B04 built.
- Does not test the lantern *rules* (C03 owns those) or the run state and resolver in isolation (A06 owns those).
- Does not perform the human playtest — that is E04.
- Does not test visual styling by pixel comparison; it tests logic and observable behavior.

## Context & Constraints
- **Read first:** `screens/game.py`, the pure helpers introduced by B02 and B04, `game/effects.py`, `game/state.py`, and A06's test setup.
- **Files to create:** a screen-level test module under the project's test root.
- **Files to modify:** the test runner configuration only if a new path needs registering.
- **Conventions to respect:** follow A06's established structure; deterministic tests; no terminal-size dependence (pass an explicit width where the code accepts one); no network; temp files cleaned up.
- **Required coverage — pure helpers:**
  - Prose wrapping: at the boundary width, with an empty string, with text longer than the line budget, and with a zero width
  - The scene line budget truncation path produces the marked continuation rather than overflowing
  - The meter helper: zero, full, mid-range, a width of one, and an out-of-range value
  - The low-oil threshold flips exactly at its named boundary
- **Required coverage — choice sequencing (the correctness core of this slice):**
  - A permitted choice applies exactly its declared effects and nothing else
  - A permitted choice transitions to its declared destination room
  - **A refused choice applies nothing** — assert by comparing a full run-state snapshot before and after
  - A refused choice performs no transition
  - A Death-tier choice routes to the death placeholder rather than continuing
  - Selection movement wraps at both ends
- **Required coverage — the content-only proof (AC-9):**
  - Rendering a room that exists only in the test's content fixture works with no change to any file under `screens/`
  - A room added to the fixture is reachable by identifier and renders its own prose

## Preconditions
- [ ] B01–B04 DONE and the screen is playable by hand
- [ ] A06 DONE — the test framework and its structure exist
- [ ] The content fixture approach is decided (a small in-test content set is recommended, so tests do not depend on Slice D)

## Actionable Steps
1. Decide and record how tests supply content: a small fixture content set is preferred over reading Slice D's real content, so these tests stay stable as content is authored.
2. Write the pure-helper tests, including the boundary and degenerate cases listed above.
3. Write the choice-sequencing tests, using an explicit snapshot comparison for the refused-choice case — do not infer it from a screen message.
4. Write the content-only proof: build a fixture room that exists nowhere in the repo, render it, and assert its prose appears.
5. Confirm no test reads from or writes to the real content directory.
6. Run the full suite together with A06's and confirm everything passes.
7. If a test exposes a defect in B01–B04, fix it only if it is in scope; otherwise raise it as a follow-up and stop.

## Test Plan
- **Commands:** the project's test command from GP-2, plus `python -m py_compile` on changed files.
- **Expected:** all listed cases pass; the full suite (A06 + B05) passes twice consecutively; runtime stays well under a minute.
- **Manual — mutation check:** temporarily reverse the check/apply order in the selection action and confirm the refused-choice test fails, then restore. This proves the sequencing test is real.
- **Independence check:** confirm the suite passes with the content directory absent, since tests must not depend on authored content.

## Definition of Done / Acceptance Criteria
- [ ] Every case in the three coverage lists exists as a named test
- [ ] The refused-choice case is asserted by snapshot comparison, not by reading screen text
- [ ] The content-only proof passes: a fixture-only room renders with no `screens/` change
- [ ] No test depends on the real content directory, wall-clock time, terminal size, or network
- [ ] The full suite passes twice in a row
- [ ] No production file changed, or any change is a genuine in-scope fix logged in the Execution Log

## Rollback / Undo
Delete the added screen test module. Production code is unaffected.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
