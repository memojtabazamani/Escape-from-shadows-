# Task A04: Content record format and validator

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: A — Prerequisites & Foundation
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: A03
- Blocks: A05, B02
- Covers: AC-9
- Suggested commit: `feat(game): define content record format and validator`
- Branch: per GP-3

## Objective
Define the record format describing a room, its choices, their conditions, and their effects — and a validator that catches malformed or unreachable content before a player ever sees it. This is the engine/content split from SUGGEST.md §11: after this task, adding a room is writing content, not touching the game loop.

## Non-Goals
- Does not write any actual room content (Slice D).
- Does not execute or apply effects (A05).
- Does not render anything (Slice B).
- Does not define Phase 2 concepts: composure costs, the six-slot inventory, or the journal.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §11 (engine vs content; effects as small declarative entries; requirements as conditions) and §4.1 (the three-tier consequence model the format must express: Scar / Setback / Death).
- **Files to create:** `game/content_schema.py`.
- **Files to read, not modify:** `old_version.py` (the baseline's HALL, LIBRARY, YARD and their two-way choices — the format must be able to express these), `config.py` (style precedent).
- **Decision required (GP-4 / ASM-9):** content storage format. Default proposal is **JSON data files**, matching the existing `settings.json` precedent. Spend **at most 30 minutes** proving it — write one sample room in each candidate format and judge readability — then record the decision and reason in the Epic Change Log. If the answer is Python modules, A05, B02, and Slice D change shape: stop and re-plan.
- **Format must express, at minimum:**
  - **Room:** identifier, display name, arrival prose, and its interactables or exits
  - **Choice:** identifier, label, destination room, effect list, and requirement list
  - **Effect:** a named operation with parameters — "lose oil by N", "grant item X", "set flag Y"
  - **Requirement:** a condition over run state — "has item X", "flag Y is set", "lantern above N"
  - **Tier:** Scar / Setback / Death, per §4.1
  - **Telegraph:** prose shown *before* a costly or lethal choice, so §4.1's "every death needs two telegraphs" is expressible as data
- **Conventions to respect:** PEP 8; type hints; standard library only (no new dependencies); **validation errors must name the record and the field**, never just "invalid content".

## Preconditions
- [ ] A03 DONE
- [ ] GP-4 answered, or the 30-minute spike completed and recorded
- [ ] `docs/SUGGEST.md` §3.1, §4.1, and §11 read in full

## Actionable Steps
1. Write the field vocabulary as a table in the module docstring: room fields, choice fields, effect verbs, requirement predicates, tiers, telegraph fields — each with type and required/optional.
2. Prove the format choice with one sample room in each candidate format; pick one; record the decision and reason in the Epic Change Log.
3. Create `game/content_schema.py` with the record definitions and the vocabulary constants.
4. Implement single-record validation returning a list of problems, each naming the record identifier and the field.
5. Implement whole-set validation adding cross-record integrity checks: every choice destination exists, no duplicate identifiers, every referenced item and flag is defined, and no room is unreachable from the start room.
6. Implement the §4.1 rule: any choice with tier Death must carry **at least two** telegraphs, or validation fails.
7. Express `old_version.py`'s three rooms and their choices as sample records in the chosen format and confirm they validate — this proves the format is sufficient.
8. Confirm the failure cases produce useful messages: a dangling destination, a missing required field, a Death choice with one telegraph, and a duplicate identifier.
9. Run py_compile and validate the samples.

## Test Plan
- **Tests to write:** deferred to A06 by design. A06 must cover: a valid room passes; each broken case above yields exactly one problem naming the right record and field; and the baseline's three rooms validate.
- **Commands:** `python -m py_compile game/content_schema.py`, then validate the sample set.
- **Expected:** samples validate clean; each deliberately broken sample is caught with a specific message.
- **Manual:** read the messages as a content author would — if a message does not tell you how to fix the record, rewrite it.

## Definition of Done / Acceptance Criteria
- [x] The format expresses every room and choice in `old_version.py`, plus tiers, requirements, and telegraphs
- [x] Errors name the record identifier and the field
- [x] Whole-set validation catches dangling destinations, duplicates, undefined references, and unreachable rooms
- [x] A Death-tier choice with fewer than two telegraphs is rejected
- [x] The format decision is recorded in the Epic Change Log with its reason
- [x] Standard library only; no new dependencies
- [x] `python -m py_compile game/content_schema.py` clean

## Rollback / Undo
Delete `game/content_schema.py` and the sample content. Only A05 and B02 depend on it, and neither exists yet at this point.

## Execution Log
- Date: 2026-11-08
- Agent: Claude Code
- Branch: feature/use-settings-into-game (working tree, no commits per GP-3)
- Commit hash: N/A — git commits not authorized
- Notes:
  - Format decision: **JSON-compatible records stored in JSON files**.  Records are plain dicts/lists and can be authored in `content/rooms.json`; the validator loads them with `json.load`.  Chosen because it matches the existing `settings.json` precedent, lets non-programmers author content, and keeps the engine/content split clean.
  - Created `game/content_schema.py` with dataclasses and validator.
  - Validation covers: required fields, unique room/choice ids, dangling destinations, known effect verbs and requirement predicates, key checking, death-tier telegraph count ≥2, and reachability from `start_room`.
  - Added `SAMPLE_CONTENT` with hall, a death-threshold room, and old_library; it validates with 0 problems.
  - Verified `python -m py_compile game/content_schema.py` and the validator run clean.
- Deviations: None
