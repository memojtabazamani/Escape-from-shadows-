# Task H01: The system bell as a horror channel (§5.2)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: H — Sound & Music Made Real
- Layer: SVC
- Status: TODO
- Estimate: ~3h
- Depends on: A13
- Blocks: H04
- Covers: AC-18, AC-24
- Suggested commit: `feat(audio): implement terminal bell cues for key horror moments respecting sound setting`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Implement terminal audio cues using the standard terminal system bell (`\a` / `sys.stdout.write('\a')` or Textual `app.bell()`) tied strictly to the persisted `Sound` setting, ringing only at three specific horror moments: a heavy door swinging open, the Hell Dog's chain rattles, and the Shadow's whisper.

## Non-Goals
- Does not introduce external audio libraries (pygame, playsound, etc.) — terminal bell only.
- Does not make audio essential to game completion (the game must be fully playable and informative even if the bell is muted or unsupported in the terminal, per ASM-7 and RISK-8).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §5.2 ("Sound: A terminal has exactly one reliable audio channel: the system bell. Use it as a horror tool... Bell on: a door opening, the dog's collar, the Shadow's first word. Bell off: the same moments, but silent"), AC-18 and AC-24 in `EPIC_Phase2_TheHouse_PLAN.md`, ASM-7, RISK-8.
- **Files to create:** `game/sound.py`.
- **Files to modify:** `screens/game.py` (call sound dispatcher during designated narrative triggers).
- **Files to read, not modify:** `config.py` (`SettingsManager`), `screens/game.py`.
- **Conventions to respect:** Wrap system bell calls in a clean service helper that checks `self.app.config.get("sound", True)`. Gracefully catch `IOError` or environment limitations without crashing.
- **Design constraints:**
  - When `sound == True`: triggers terminal bell (`\a`) on designated moments.
  - When `sound == False`: completely silent; narrative text and visual pacing remain 100% complete.
  - The three designated bell moments:
    1. The study door in the Old Library quietly creaking open on the 3rd read turn.
    2. The Hell Dog's iron chain rattling in the Old Yard.
    3. The Shadow's first direct whisper.

## Preconditions
- [ ] A13 DONE — baseline screen and game loop functional.
- [ ] `SettingsManager` in `config.py` supplies the `sound` boolean setting.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. Create `game/sound.py` with `play_cue(app, cue_name: str) -> bool`.
2. Implement sound dispatch checking `app.config.get("sound", True)` before emitting `app.bell()` or writing `\a` to terminal output stream.
3. Define the three allowed cue identifiers: `CUE_DOOR_OPEN`, `CUE_DOG_CHAIN`, `CUE_SHADOW_WHISPER`.
4. Ensure unhandled terminal bell exceptions (e.g. headless environment or redirected stdout) are silently handled without impacting game flow.
5. In `screens/game.py`, invoke `play_cue` when encountering the designated scene events.
6. Verify that setting `sound` to False in Settings screen disables all bell emissions.

## Test Plan
- **Tests to write/update:** `tests/test_sound_service.py`:
  - `test_bell_emitted_when_sound_enabled` — verifies `app.bell()` called when sound setting is True.
  - `test_bell_suppressed_when_sound_disabled` — verifies no bell emitted when sound setting is False.
  - `test_sound_fails_gracefully_in_headless_env` — verifies zero crashes if stdout bell fails.
- **Commands:** `python -m pytest tests/test_sound_service.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] `game/sound.py` encapsulates system bell logic.
- [ ] Sound setting toggle in `config.py` directly controls whether bell sounds.
- [ ] Three designated moments trigger the cue.
- [ ] Headless/muted terminals run cleanly without exceptions (RISK-8).
- [ ] Automated tests pass cleanly.

## Rollback / Undo
Delete `game/sound.py` and remove sound triggers from `screens/game.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
