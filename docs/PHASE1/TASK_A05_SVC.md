# Task A05: Effect and requirement resolver

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: A — Prerequisites & Foundation
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: A03, A04
- Blocks: A06, B01, C01
- Covers: AC-9
- Suggested commit: `feat(game): add declarative effect and requirement resolver`
- Branch: per GP-3

## Objective
Implement the single place that answers two questions about a choice: *may the player take it?* and *what happens when they do?* — by evaluating A04's requirement conditions and applying A04's effect list against A03's run state.

## Non-Goals
- Does not render choices or prose (Slice B).
- Does not define the *values* of any cost or gate — that is content (Slice D).
- Does not implement the lantern drain *rates* (C01); it only applies the costs content declares.
- Does not write to disk; Phase 1 has no save file.
- Does not know anything about specific rooms or the ending.

## Context & Constraints
- **Read first:** `game/state.py` (A03's mutation API), `game/content_schema.py` (A04's vocabulary), `docs/SUGGEST.md` §11 bullet 3 ("effects as small declarative entries, not branches ... conditionals become requirements").
- **Files to create:** `game/effects.py`.
- **Files to read, not modify:** `docs/SUGGEST.md` §4.1 — the resolver must return a tier (Scar / Setback / Death) so callers can route to the right outcome.
- **Conventions to respect:** PEP 8; type hints; standard library only. **No branching on room or choice identifiers anywhere in this module** — that is the entire point of the abstraction (AC-9). If the resolver needs a specific room's name to work, the format in A04 is wrong; fix that instead of special-casing here.
- **Design constraints:**
  - Requirement evaluation is **side-effect free** — asking "can I take this?" must never change state.
  - Effect application is **all-or-nothing**; if any entry cannot apply, apply nothing and report which entry failed. Decide, document, keep it consistent.
  - Every refusal carries a **machine-readable reason**, so the death screen and any future hint line can use it without re-deriving anything.
  - Unknown effect verbs and unknown requirement predicates **fail loudly** — a content bug, never a silent no-op.

## Preconditions
- [ ] A03 DONE and its mutation API stable
- [ ] A04 DONE and the vocabulary frozen for this task
- [ ] The test framework (GP-2) is available so the resolver can be exercised directly

## Actionable Steps
1. Read A03's and A04's public APIs and write down exactly which calls the resolver will make — make this interface contract explicit before coding.
2. Create `game/effects.py`.
3. Implement requirement evaluation: given a requirement list and run state, return satisfied/unsatisfied plus the reasons for any failure. Cover every predicate A04 defines (item held, flag set, lantern above or below a threshold, turn count past a value).
4. Implement effect application: given an effect list and run state, apply every entry through A03's mutation API and return a structured result describing what changed.
5. Implement refusal propagation: when an entry cannot apply, report which entry failed and leave state in the documented all-or-nothing condition.
6. Implement tier reporting: expose the resolved choice's tier without applying or interpreting it.
7. Re-read the module and remove any reference to a specific room or choice by name.
8. Exercise the resolver against A04's sample content.

## Test Plan
- **Tests to write:** deferred to A06 by design. A06 must cover: each predicate satisfied and unsatisfied; effect application changing exactly the expected state fields and nothing else; the all-or-nothing refusal path reporting the failing entry; unknown verb and unknown predicate each raising; and a before/after snapshot proving requirement evaluation mutates nothing.
- **Commands:** `python -m py_compile game/effects.py`, then resolve every choice in A04's sample set.
- **Expected:** each sample choice resolves to a tier and an applicable effect list; no unknown verbs or predicates encountered; requirement evaluation provably changes nothing.
- **Manual:** inspect one choice's structured result and confirm it is readable enough for E01's death screen to consume directly.

## Definition of Done / Acceptance Criteria
- [x] Requirements evaluate with no side effects
- [x] Effect application is all-or-nothing and names the failing entry on refusal
- [x] Refusals carry a machine-readable reason
- [x] Unknown verbs and predicates fail loudly
- [x] Tier reporting works for Scar, Setback, and Death
- [x] The module references no room or choice by name (AC-9)
- [x] `python -m py_compile game/effects.py` clean; no other files changed

## Rollback / Undo
Delete `game/effects.py`. Consumers B01/C01 do not exist yet at this point.

## Execution Log
- Date: 2026-11-08
- Agent: Claude Code
- Branch: feature/use-settings-into-game (working tree, no commits per GP-3)
- Commit hash: N/A — git commits not authorized
- Notes:
  - Created `game/effects.py` with `check_requirements`, `apply_effects`, and `resolve_choice`.
  - Requirement evaluation is side-effect-free; effect application snapshots the state before touching it and restores on any failure.
  - Unknown effect verbs and requirement predicates raise `ValueError`.
  - Resolved every choice in the A04 sample content successfully; observed the expected lantern spend and flag set.
  - Verified no room or choice name appears in the module.
- Deviations: None
