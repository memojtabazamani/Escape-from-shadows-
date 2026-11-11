# Task E03: Shadow dialogue injection, audio whisper cue, and journal recording

## Metadata
- Epic: [EPIC_Phase3_TheShadow_PLAN.md](EPIC_Phase3_TheShadow_PLAN.md)
- Slice: E — Player History & Shadow Voice
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: E02, D04
- Blocks: E04
- Covers: AC-20, AC-21, §2.2, §3.4, §5.2
- Suggested commit: `feat(shadow): inject Shadow whispers into gameplay with audio cues and journal logging`
- Branch: feature/phase_3_the_shadow

## Objective
Wire generated Shadow dialogue into the live gameplay flow in `screens/game.py`: triggering the system bell audio cue (`play_cue(CUE_SHADOW_WHISPER)`), appending the whisper into the player's in-game Journal under the "Shadow Whispers" category, and displaying the whispered prose in the scene zone.

## Non-Goals
- Does not change visual rhythm timers (governed by Music setting in Slice F).
- Does not break the game if audio bell is muted or disabled (per §5.2).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §2.2, §3.4 ("The Journal: An in-game notebook that auto-records... lines the Shadow has said"), §5.2 ("Sound: the terminal system bell... a door opening, the dog's collar, the Shadow's first word"), `game/sound.py`, `game/journal.py`.
- **Files to modify:** `screens/game.py`, `game/journal.py`.
- **Precedent:** `CUE_SHADOW_WHISPER` is already defined in `game/sound.py`.

## Preconditions
- [ ] Task E02 DONE (`generate_shadow_whisper()` available).
- [ ] Journal model and sound service operational.

## Actionable Steps
1. In `screens/game.py`, inside room render / transition logic:
   - When Shadow proximity or turn threshold triggers a whisper beat:
     - Generate whisper line: `whisper = generate_shadow_whisper(self.state)`.
     - Trigger audio bell: `play_cue(CUE_SHADOW_WHISPER, config=getattr(self.app, "config", None))`.
     - Record into Journal: `self.state.journal.record_shadow_line(whisper)`.
     - Append formatted whisper to the scene text area.
2. In `game/journal.py`, ensure `record_shadow_line(line: str)` stores entries under category `"whispers"`.
3. Ensure on EASY difficulty, Shadow taunts double as helpful navigational hints per §5.1 / Phase 2 Task B04 integration.

## Test Plan
- **Tests to write/update:** `tests/test_shadow_whisper_injection.py`:
  - `test_whisper_triggers_sound_cue`: Asserts `play_cue` is called with `CUE_SHADOW_WHISPER`.
  - `test_whisper_logged_in_journal`: Asserts whispered line is appended to journal under whispers.
  - `test_whisper_rendered_in_scene`: Asserts whisper appears in `GameScreen` text widget.
- **Commands:** `python -m pytest tests/test_shadow_whisper_injection.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Shadow whispers are delivered into the scene zone.
- [ ] System bell sounds appropriately on whispers when sound is enabled.
- [ ] Whispers are reliably preserved in the player's Journal.
- [ ] Tests pass cleanly.

## Rollback / Undo
Revert edits to `screens/game.py` and `game/journal.py`.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations -->
