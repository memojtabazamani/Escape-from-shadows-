# Task C01: Memory fragment item definitions and `RunState` tracking (§2.4)

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: C — The Three Memory Fragments
- Layer: SVC
- Status: TODO
- Estimate: ~2.5h
- Depends on: GP-1
- Blocks: C02
- Covers: AC-13, §2.4
- Suggested commit: `feat(items): add memory fragment items and RunState fragment tracking`
- Branch: feature/phase_3_the_shadow

## Objective
Define the three memory fragment items in content and schema (`old_photograph`, `child_drawing`, `dated_receipt`) and update `RunState` with explicit tracking (`memory_fragments: set[str]`), helper methods, and serialization snapshot/restore support.

## Non-Goals
- Does not place the acquisition choices in rooms yet (handled in C02).
- Does not trigger the Homecoming ending yet (handled in C03).
- Does not grant mechanical survival buffs (fragments deliberately do not help survive, per §2.4).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.4 ("Memory Fragments: Scatter three items that don't help you survive at all — a photograph, a child's drawing, a receipt dated tomorrow. Collecting them changes nothing mechanically. They only change the ending. This teaches players that curiosity is a mechanic, not a waste of turns."), `game/state.py`.
- **Files to modify:** `game/state.py`, `game/content_schema.py`.
- **Item IDs:**
  - `old_photograph`: "A cracked sepia photograph showing three smiling figures standing on the front porch of this manor. None of them have faces."
  - `child_drawing`: "Crayon on yellowed butcher paper. A large dark shape looms over a small bed, but the child drew a heart around its chest."
  - `dated_receipt`: "A crumpled carbon slip from a local apothecary. The ink is fresh, stamped with tomorrow's date."
- **Constraints:** Must preserve 6-slot inventory cap (`INVENTORY_CAP = 6`). Snapshot/restore must remain backward-compatible.

## Preconditions
- [ ] Baseline test suite is green.
- [ ] `RunState` model in `game/state.py` verified.

## Actionable Steps
1. In `game/state.py`:
   - Add field `memory_fragments: set[str] = field(default_factory=set)` to `RunState`.
   - In `__post_init__()`, ensure `self.memory_fragments = set(self.memory_fragments)`.
   - Add helper method `add_memory_fragment(self, fragment_id: str) -> None`.
   - Add helper property `has_all_memory_fragments(self) -> bool` (returns `len(self.memory_fragments) >= 3`).
   - In `snapshot()`, include `"memory_fragments": sorted(self.memory_fragments)`.
   - In `restore(data)`, load `"memory_fragments"` defaulting to empty set.
2. In `game/content_schema.py`:
   - Add predicate `has_memory_fragment` and `memory_fragment_count`.
   - Add verb `record_memory_fragment`.

## Test Plan
- **Tests to write:** `tests/test_memory_fragments_model.py`:
  - `test_runstate_tracks_memory_fragments`: Adding fragments updates the set.
  - `test_has_all_memory_fragments`: Returns True when all 3 canonical IDs are held, False otherwise.
  - `test_snapshot_restore_roundtrip`: Snapshot serializes and restores memory fragments perfectly.
  - `test_backward_compatible_restore`: Deserializing older save without memory_fragments defaults safely.
- **Commands:** `python -m pytest tests/test_memory_fragments_model.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `RunState` tracks memory fragments and serializes without errors.
- [ ] Schema supports memory fragment predicates and verbs.
- [ ] Backward compatibility with existing save states is guaranteed.
- [ ] Tests pass cleanly.

## Rollback / Undo
Revert edits to `game/state.py` and `game/content_schema.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
