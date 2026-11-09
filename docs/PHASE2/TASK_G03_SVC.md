# Task G03: The whistle needs the book, and the dog comes back later

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: G — The Hell Dog
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: G02
- Blocks: G04
- Covers: AC-13
- Suggested commit: `feat(content): gate whistle on Book knowledge and implement dog's delayed return`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Author the interlocking narrative logic connecting the Silver Whistle with the Old Library's Book (§3.3, §4.3): blowing the whistle without knowing the beast's true name fails (or enrages it), whereas blowing it with the name causes the beast to slink away — only for it to return later near the front door to challenge the final escape.

## Non-Goals
- Does not author the Library three-turn read (completed in F03).
- Does not author the final front door unlock sequence (completed in F05/F06).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §3.3 ("Silver Whistle — the Hell Dog's actual weakness. Only works if you know its name"), §4.3 ("Whistle (only if you read the book) — the dog leaves. It comes back. Later. Somewhere worse"), AC-13 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `data/rooms/old_yard_dog.json`, `data/rooms/the_hall.json` (front door escape encounter).
- **Files to read, not modify:** `game/content_schema.py`.
- **Conventions to respect:** Conforms strictly to schema in `game/content_schema.py`.
- **Design constraints:**
  - Whistle attempt WITHOUT `knows_dog_name`: a shrill, piercing blast pierces the rain. The dog raises its head, unaffected, its eyes blazing with heightened fury (composure loss, dog advances).
  - Whistle attempt WITH `knows_dog_name`: player sounds the exact melodic frequency learned from the tome and utters the name. The dog whimpers, retreats into the mud, and disappears into the perimeter fog.
  - Sets flag: `dog_whistled_away`.
  - Later in The Hall during the final Front Door attempt (F05), if `dog_whistled_away` is true, the dog reappears outside the threshold window / portico, snarling in wait, requiring a final decisive action (e.g. using the Rusty Cleaver, throwing final scrap, or slamming the iron door shut in time).

## Preconditions
- [ ] G02 DONE — Four solutions authored.
- [ ] F03 DONE — `knows_dog_name` flag set up in the Book reading.
- [ ] Content schema validator passing.

## Actionable Steps
1. In `old_yard_dog.json`, branch the "Blow Silver Whistle" choice based on predicate `has_flag: "knows_dog_name"`.
2. Author failed whistle branch: shrill sound without name, beast attacks/advances, player barely retreats.
3. Author successful whistle branch: beast cowers and slinks away into darkness; award flag `dog_whistled_away`.
4. In `the_hall.json` (front door resolution), add conditional encounter state when `dog_whistled_away` is set:
   - As player works the front door latch, heavy breathing and red eyes appear in the entryway fog.
   - Player must make a final split-second reaction: slam the heavy oak door shut, or brandish the cleaver to seal the exit.
5. Record appropriate Journal revelations for both branches.
6. Verify line budgets (≤ 20 lines).

## Test Plan
- **Tests to write/update:** `tests/test_hell_dog_whistle.py`:
  - `test_whistle_without_book_fails` — whistle with missing name flag fails with consequence.
  - `test_whistle_with_book_banishes_dog` — whistle with name flag banishes dog and sets `dog_whistled_away`.
  - `test_dog_reappears_at_front_door_if_whistled` — front door encounter checks `dog_whistled_away` and triggers tense climax.
- **Commands:** `python -m pytest tests/test_hell_dog_whistle.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Whistle without the Book's name fails with telegraphed consequence.
- [ ] Whistle with the Book's name pacifies and banishes the dog.
- [ ] Banished dog reappears at the front door to fulfill §4.3 ("It comes back. Later. Somewhere worse").
- [ ] All tests pass cleanly.

## Rollback / Undo
Revert whistle conditional branches in yard and hall content.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
