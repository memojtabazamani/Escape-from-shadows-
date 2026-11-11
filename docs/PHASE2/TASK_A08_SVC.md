# Task A08: OLD LIBRARY content and the BOOK's costly read

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: A — Completing the Foundation
- Layer: SVC
- Status: DONE
- Estimate: ~3h
- Depends on: A03
- Blocks: A10
- Covers: AC-1, AC-4, AC-23
- Suggested commit: `content(library): add the old library and the book's costly read`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author OLD LIBRARY as the information room, where the BOOK is the single best source of knowledge in the game and reading it costs oil — a single costly read, not the three-turn scene.

## Non-Goals
- Does not implement the three-consecutive-turn read. §6 wants it; Phase 1's ASM-5 deferred it because multi-turn machinery did not exist. **That machinery is F01, and the three-turn version is F03** — this task authors the single costly read F03 later upgrades.
- Does not author the book as a carried item with a composure cost — the item record is C03, and its carrying drain is D01.
- Does not author the HALL — that is A07; this task only supplies the library room the hall's right-hand passage leads to.
- Does not define what the knowledge unlocks beyond setting the flag — A10 consumes that flag for the ending.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §6's OLD LIBRARY entry — "The information room. The BOOK is the best item in the game and reading it takes **three consecutive turns** during which you cannot see the door. The candle burns down while you read." — plus §3.3's Book entry ("the single best source of information in the game, and it's heavy, slow to read, and *watched*"), §7.4, and §13.
- **Files to modify:** the content file(s) from A07, following the layout decision recorded there.
- **Files to read, not modify:** `game/content_schema.py` for the record shape and the validator; `game/effects.py` for `spend_oil` and `set_flag`; `game/lantern.py` (from A05) — the careful-action drain cost should come from `drain_for_action`, not from a bespoke number in the content.
- **Conventions to respect:** content as data (§11); the read is expressed as effects on a choice, not as a branch in the loop; the knowledge is a **flag**, matching A10's expectation and the existing `knows_exit` precedent in `SAMPLE_CONTENT`.
- **Design constraints:**
  - **≈ 20 usable lines** (§13, ASM-18).
  - **The cost must be felt.** The read should consume enough oil that a player notices the bar move and has to weigh a second read.
  - **The room must carry the "watched" quality** (§3.3) without implementing pursuit — ASM-11 keeps the Shadow out of this phase. It is a feeling in the prose, not a mechanic.
  - The read is repeatable at a cost, but must not be farmable: decide the behaviour on a second read and record it.
  - Titles and prose in the calm, dim register §7.4 assigns to narration.
- **Voice:** restraint. "Shelves lean like tired sentinels" is the register — the library is quiet, and the quiet is the threat.

## Preconditions
- [x] A03 DONE — choices render, resolve, and respect requirements
- [x] A05 DONE — careful-action drain is defined in `game/lantern.py`
- [x] A07 DONE — the content file layout is decided and the hall's passage exists
- [x] The flag name for the gained knowledge is chosen and recorded (A10 depends on it)
- [x] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Author the library room: `id`, `name`, and `prose` within the ≈ 20-line budget — the shelves, the lectern, and the sense of being watched.
2. Author the read choice: label it as the player's own action, apply `spend_oil` using `game/lantern.py`'s careful-action cost, and apply `set_flag` for the knowledge.
3. Choose and record the knowledge flag's name. A10, C03 and G03 all consume it — pick one name now rather than three later.
4. Decide the second-read behaviour (repeat at full cost, reduced cost, or refuse with a reason) and implement it consistently; record the decision.
5. Author the return path to the hall, so the loop `hall → library → hall` is complete and A05's revisit discount can be felt.
6. Author the "watched" quality as prose only. Do not add a pursuit mechanic, a timer, or a Shadow entity.
7. Confirm the validator is clean and that no library prose appears under `screens/`.

## Test Plan
- **Tests to write/update:** extend `tests/test_content_house.py`:
  - `test_library_is_reachable_from_the_hall` — asserts the destination resolves and the room is reachable from `start_room`.
  - `test_book_read_spends_oil_and_sets_the_knowledge_flag` — asserts both effects via `resolve_choice`.
  - `test_library_prose_fits_the_line_budget` — asserts the ≈ 20-line limit.
  - `test_second_read_follows_the_recorded_decision` — asserts whichever behaviour was chosen, so it cannot drift silently.
- **Commands:** `python -m pytest tests/test_content_house.py -v`; then `python -m pytest`.
- **Manual verification:** enter the library, read, and confirm the bar visibly drops and the run's flags change. Confirm the return to the hall is cheaper than the first entry (A05).

## Definition of Done / Acceptance Criteria
- [x] The library is reachable from the hall and the content set validates clean
- [x] The read spends oil, drawn from `game/lantern.py`'s careful-action cost rather than a hardcoded number
- [x] The read grants knowledge as a named flag, recorded so A10, C03 and G03 can consume it
- [x] The knowledge flag's name is recorded in the Execution Log
- [x] The second-read behaviour is decided, implemented, and tested
- [x] The room reads as watched without implementing any pursuit
- [x] Prose is within the ≈ 20-line budget and no prose appears under `screens/`
- [x] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; the hall's right-hand passage has no destination and `validate_content()` fails with an unresolved destination — the correct, loud failure. A10 depends on the knowledge flag this task sets, so revert them together.

## Execution Log
- **Date:** 2026-11-09
- **Agent:** Antigravity
- **Branch:** feature/phase_2_the_house (No git commit per user instruction)
- **Knowledge Flag Name:** `knows_exit` (standardized across A08, A10, C03, G03)
- **Second-Read Decision:** Repeat at full cost (`spend_oil: 25`, matching `CAREFUL_ACTION_DRAIN`). Re-affirms `knows_exit`. Since lantern oil is a depleting resource and flags are idempotent, repeating the read costs valuable light without granting duplicative or farmable advantages.
- **Notes:**
  - Added atmospheric description for `old_library` in `data/content.json` embodying quiet sentinel shelves, heavy lectern/tome, and cold watched tension without mechanical pursuit.
  - Configured `library_read` choice with `spend_oil: 25` and `set_flag: "knows_exit"`.
  - Added return path `library_return` to `hall`.
  - Guarded room transition oil drain in `screens/game.py` so action choices within the same room do not incur spurious room re-entry drain.
  - Extended `tests/test_content_house.py` with 5 new tests asserting reachability, oil spend, flag grant, line budget, sentinel/tome/watched atmospheric keywords, second-read repetition, and lack of hardcoded screen prose.
  - Verified with 59 passing tests and clean compilation.
