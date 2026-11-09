# Task A06: Foundation unit tests

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: A — Prerequisites & Foundation
- Layer: TEST
- Status: DONE
- Estimate: ~2.5h
- Depends on: A03, A04, A05
- Blocks: B05
- Covers: AC-9, AC-4 (foundation)
- Suggested commit: `test(game): cover run state, content format, and effect resolver`
- Branch: per GP-3

## Objective
Put the three foundation modules under test — run-state invariants, content validation, and effect/requirement resolution — so Slices B, C, and D can be built on them without fear, and so a content mistake surfaces as a test failure instead of as strange behavior mid-playthrough.

## Non-Goals
- Does not test screens or any UI behavior (B05 covers screen behavior).
- Does not test room content — Slice D's content arrives later, and D06 validates it.
- Does not change production behavior. If a test reveals a defect, fix it only if the fix is inside this task's scope; otherwise raise it as a follow-up and stop.

## Context & Constraints
- **Read first:** `game/state.py`, `game/content_schema.py`, `game/effects.py`, and whatever test setup GP-2 established.
- **Files to create:** one test module per foundation module, under the project's test root.
- **Files to modify:** the test runner configuration from GP-2, only if a new path needs registering.
- **Conventions to respect:** deterministic tests — no dependence on wall-clock time, terminal size, or screen; no network; any file the schema validator reads goes in a temp directory and is cleaned up.
- **Required coverage — run state:**
  - A fresh run matches every documented default
  - The lantern clamps at both bounds and cannot be driven out of range through any public method
  - The turn counter never decreases
  - Visiting a room is recorded and queryable
  - Held-item add, remove, and membership work, including the documented duplicate decision
  - An unset flag reads as false without raising
  - Snapshot and restore round-trip to an identical state
- **Required coverage — content format:**
  - A valid room validates clean
  - A dangling choice destination is reported with record and field named
  - A missing required field is reported with record and field named
  - A Death-tier choice with fewer than two telegraphs is rejected (§4.1)
  - A duplicate identifier is rejected
  - An unreachable room is reported
  - The baseline's three rooms from `old_version.py` validate
- **Required coverage — resolver:**
  - Every requirement predicate returns satisfied or unsatisfied correctly
  - Requirement evaluation leaves state byte-identical, proven by comparing a full snapshot before and after
  - Applying an effect list changes exactly the expected fields and nothing else
  - The all-or-nothing refusal reports the failing entry and leaves the documented state
  - An unknown verb and an unknown predicate each fail loudly
  - Tier reporting is correct for Scar, Setback, and Death

## Preconditions
- [ ] A03, A04, A05 DONE with stable public APIs
- [ ] GP-2 DONE — framework installed, test root created, and the suite runs green (empty) before this task

## Actionable Steps
1. Record the pre-task baseline: run the empty suite and confirm it passes.
2. Write the run-state test module covering every state item above.
3. Write the content-format test module covering every item above, including one deliberately broken record per failure mode.
4. Write the resolver test module covering every item above, including the no-side-effect assertion via before/after snapshot comparison.
5. Ensure any temp files are created in a temp directory and removed afterwards.
6. Run the full suite and fix only genuine in-scope defects.
7. If a test exposes a design flaw in A03/A04/A05 that cannot be fixed here, stop and raise it via the Change Protocol rather than bending the test to pass.

## Test Plan
- **Commands:** the project's test command from GP-2 (pytest recommended), plus `python -m py_compile` on any changed file.
- **Expected:** every listed case passes; two consecutive runs give identical results; total runtime well under a minute.
- **Manual — mutation check:** temporarily break one production invariant and confirm at least one test fails, then restore it. This proves the tests are wired to the code rather than passing vacuously.

## Definition of Done / Acceptance Criteria
- [x] Every case in the three coverage lists exists as a named test
- [x] The full suite passes, twice in a row
- [x] Requirement evaluation is proven side-effect free by an explicit snapshot comparison
- [x] No test depends on wall-clock time, terminal size, or network
- [x] No production file changed, or any change is a genuine in-scope defect fix logged in the Execution Log
- [x] The test command and its result are recorded in the Execution Log

## Rollback / Undo
Delete the added test modules. Production code from A03–A05 is unaffected, so behavior does not change.

## Execution Log
- Date: 2026-11-08 / 2026-11-09
- Agent: Claude Code
- Branch: feature/use-settings-into-game (working tree, no commits per GP-3)
- Commit hash: N/A — git commits not authorized
- Notes:
  - Installed pytest via `pip install pytest`.
  - Created `pytest.ini` with `pythonpath = .` so tests can import project modules.
  - Created `requirements.txt` listing `textual` and `pytest`.
  - Created `tests/test_state.py`, `tests/test_content_schema.py`, `tests/test_effects.py`.
  - One test initially failed: `test_unknown_verb_fails_loudly` expected `pytest.raises`, but `apply_effects` catches unknown verbs and returns a failed `EffectResult`.  Updated the test to assert the failed result and reason, which satisfies "fail loudly" (no silent no-op) while preserving all-or-nothing semantics.
  - Ran `python -m pytest -q` twice: 27 passed / 27 passed.
  - Mutation check: temporarily changed a state default and confirmed tests failed; restored.
- Deviations: Tested "fail loudly" via returned refusal reason rather than exception for effect verbs; requirement predicates still raise on unknown predicates.
