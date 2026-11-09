# Task A03: Minimal run state

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: A — Prerequisites & Foundation
- Layer: SVC
- Status: DONE
- Estimate: ~2.5h
- Depends on: A02
- Blocks: A04, A06
- Covers: AC-4 (foundation)
- Suggested commit: `feat(game): add minimal run state for lantern, turns, and flags`
- Branch: per GP-3

## Objective
Create the single object that holds everything about one attempt at the game — lantern oil, turn count, visited rooms, held items, and flags — with documented defaults and invariants, so every screen reads and mutates one shared thing instead of scattered variables.

**Deliberately minimal.** Phase 1 needs only what its two rooms and one cost require. Phase 2 grows this object; this task must not pre-build Phase 2's fields.

## Non-Goals
- Does not include composure, the journal, or a six-slot inventory — all Phase 2 (§3.2–3.4).
- Does not render anything (Slice B).
- Does not implement the lantern *rules* (C01) — this task defines the field and its bounds only.
- Does not write to disk; Phase 1 has no save file.
- Does not build the content graph (A04).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.1 (lantern), §3.5 (turn counter), §11 bullet 2 (one state object owned by the app, like `self.app.config` already is), `config.py` (style precedent: small, documented, dependency-free).
- **Files to create:** `game/state.py`.
- **Files to read, not modify:** `config.py`.
- **Conventions to respect:** PEP 8; type hints; module docstring; standard library only; comment density similar to `config.py`.
- **Fields to define — nothing more:**
  - **lantern** — a bounded scale (define the range once and clamp on write, so no caller can exceed full or drop below zero)
  - **turn count** — monotonic; never decrements
  - **visited rooms** — a set of room identifiers, so C01 can tell a first entry from a re-entry
  - **held items** — a simple set of item identifiers (ASM-6: no slot cap in Phase 1)
  - **flags** — named booleans; reading an unset flag is safe and returns false
- **Do not** put Textual widgets, screen references, or anything UI-related here — it must be plain data.

## Preconditions
- [ ] A02 DONE
- [ ] GP-2 DONE (the test framework exists, since A06 will test this directly)
- [ ] The field list above is agreed before coding

## Actionable Steps
1. Write a short field table in the module docstring: field, type, default, and range or invariant for each.
2. Create `game/state.py` with the run-state class.
3. Implement fresh-run construction with documented defaults.
4. Implement clamping for the lantern scale on write, and document whether an out-of-range write raises or clamps.
5. Implement turn advancement as a single monotonic operation — no direct field assignment from callers.
6. Implement room-visit recording plus a "have I been here" query.
7. Implement held-item add, remove, and membership — with a decision, documented, about adding an item already held.
8. Implement flag set, clear, and a safe read defaulting to false.
9. Implement snapshot-to-dictionary and restore-from-dictionary, with missing keys falling back to defaults (Phase 2's save file will depend on this contract, so define it now).
10. Add a docstring to each public method stating the invariant it protects.
11. Confirm importing the module performs no I/O and prints nothing.

## Test Plan
- **Tests to write:** deferred to A06 by design. A06 must cover: fresh defaults, lantern clamping at both bounds, the monotonic turn counter, visit recording and query, held-item add/remove/membership including the duplicate decision, flag read-before-set, and snapshot/restore round-trip identity.
- **Commands:** `python -m py_compile game/state.py` and a scratch import check.
- **Expected:** py_compile clean; import is side-effect free; a fresh snapshot contains no non-serializable values.

## Definition of Done / Acceptance Criteria
- [ ] `game/state.py` exists with a documented field table
- [ ] Lantern cannot leave its range through any public method
- [ ] The turn counter cannot decrease
- [ ] Unset flags read as false without raising
- [ ] Visited-room and held-item queries work
- [ ] A snapshot/restore pair exists and is documented
- [ ] No composure, journal, or slot-capped inventory is present (those are Phase 2)
- [ ] No UI imports, no I/O, no side effects on import
- [ ] `python -m py_compile game/state.py` clean; no other files changed

## Rollback / Undo
Delete `game/state.py`. Nothing imports it yet at this point in the plan.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
