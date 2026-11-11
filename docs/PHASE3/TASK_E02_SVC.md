# Task E02: History-driven second-person dialogue engine

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: E — Player History & Shadow Voice
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: E01, D01
- Blocks: E03
- Covers: AC-20, §2.2
- Suggested commit: `feat(shadow): generate second-person dialogue quoting player run history`
- Branch: feature/phase_3_the_shadow

## Objective
Author the history-driven dialogue generation engine in `game/shadow_dialogue.py`, transforming past player choices recorded in `RunState.choice_history` into haunting, second-person whispers spoken by the Shadow ("You went left in the hall. I remember.", "You lifted the cleaver. Your fingers trembled on the haft.", "You read the third page. You know what is waiting.").

## Non-Goals
- Does not inject audio bells (handled in E03).
- Does not modify Textual screen widgets (handled in E03, F02).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.2 ("It speaks in the second person, and its dialogue is drawn from the player's own earlier choices. ('You went left in the hall. I remember.')").
- **Files to create:** `game/shadow_dialogue.py`.
- **Dialogue Grammar Rules:**
  - Strict second-person address ("You ...", "Your ...").
  - Never enthusiastic or theatrical; cold, intimate, and observant.
  - References specific actions: weapon taken, book read, freezing before the dog, rooms visited, items dropped.
  - Fallback reflections when history is brief: comments on breathing, pulse, or lantern flicker.

## Preconditions
- [ ] Task E01 DONE (`choice_history` populated in `RunState`).
- [ ] Working tree clean.

## Actionable Steps
1. Create `game/shadow_dialogue.py`.
2. Define a template dictionary mapping `action_tag` / `choice_id` to second-person whispered lines:
   - `took_cleaver`: "You lifted the rusted cleaver from the hook. Your knuckles were white with terror."
   - `read_book`: "You spent three wicks in the library. You turned the black pages. I was reading over your shoulder."
   - `froze_at_dog`: "You froze on the wet gravel when the hound growled. You thought if you did not move, I could not see you."
   - `took_matches`: "You took the tin box of matches. Sulfur cannot burn what has no flesh."
   - `dropped_item`: "You left your tools behind in the dark. You are stripping yourself bare for me."
3. Implement `generate_shadow_whisper(state: RunState) -> Optional[str]`:
   - Inspects `state.choice_history` for unquoted significant past choices.
   - Selects a relevant line corresponding to a choice made at least 2 turns ago.
   - Marks the action as quoted to prevent immediate repetition.
   - Returns formatted whisper string.

## Test Plan
- **Tests to write:** `tests/test_shadow_dialogue.py`:
  - `test_dialogue_quotes_specific_cleaver_choice`: Taking cleaver causes Shadow to quote cleaver action.
  - `test_dialogue_quotes_book_reading`: Reading book causes Shadow to reference reading the pages.
  - `test_dialogue_is_strictly_second_person`: Asserts all returned dialogue starts with "You" or "Your".
  - `test_fallback_when_history_empty`: Sparse history returns subtle atmospheric observation.
- **Commands:** `python -m pytest tests/test_shadow_dialogue.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/shadow_dialogue.py` generates chilling second-person dialogue drawn from player history.
- [ ] Repetition protection prevents echoing the same quote twice in a row.
- [ ] Tests pass cleanly.

## Rollback / Undo
Delete `game/shadow_dialogue.py` and `tests/test_shadow_dialogue.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
