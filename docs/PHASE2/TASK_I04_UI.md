# Task I04: Difficulty-gated "what you could have done" line (§9.2)

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: I — Persistence & Mercy
- Layer: UI
- Status: DONE
- Estimate: ~2h
- Depends on: I03, B03
- Blocks: I05
- Covers: AC-15, AC-16
- Suggested commit: `feat(ui): display greyed-out hint on death screen only on EASY difficulty`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Add the third informational line to the Death Screen (§9.2) — a greyed-out hint showing "What you could have done differently" — that renders exclusively when playing on EASY difficulty, providing merciful guidance for beginners while preserving mystery on MEDIUM and HARD.

## Non-Goals
- Does not change difficulty rules or numbers (handled in Slice B).
- Does not show hints on MEDIUM or HARD difficulty (preserving spoiler protection per §9.2).

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §9.2 ("3. What you could have done, greyed out, only on EASY. The greyed-out third line is a real design decision: it's mercy for some players and a spoiler for others. Bind it to difficulty"), §5.1, AC-15 and AC-16 in `EPIC_Phase2_TheHouse_PLAN.md`.
- **Files to modify:** `screens/death.py`.
- **Files to read, not modify:** `config.py` (`SettingsManager`), `game/difficulty.py`.
- **Conventions to respect:** Style the hint in subdued dim grey (`$text-muted` or Textual dim styling). Only mount or display the hint widget when `difficulty == "EASY"`.
- **Design constraints:**
  - On EASY: renders "Hint (EASY): <alternative_choice_hint>" in muted dim grey.
  - On MEDIUM and HARD: widget is completely hidden / not mounted.
  - Changes information and mercy, never the story (AC-16).

## Preconditions
- [ ] I03 DONE — Death screen displays cause and lesson.
- [ ] B03 DONE — Difficulty configuration and mercy knobs in place.
- [ ] Working tree clean and existing test suite green.

## Actionable Steps
1. In `screens/death.py`, accept an optional `hint: Optional[str]` parameter.
2. In `screens/death.py.compose()`, check the active difficulty setting from `self.app.config.get("difficulty", "MEDIUM")`.
3. If `difficulty == "EASY"` and `hint` is provided:
   - Render `#death-hint` widget styled with dim grey italics: "Could have done: <hint>".
4. If `difficulty` is MEDIUM or HARD:
   - Omit the hint widget entirely.
5. In the death invocation callers in `screens/game.py` and `game/effects.py`, pass the alternative path hint if available.

## Test Plan
- **Tests to write/update:** `tests/test_death_hint_difficulty.py`:
  - `test_hint_rendered_on_easy` — asserts `#death-hint` is visible with text when difficulty is EASY.
  - `test_hint_hidden_on_medium_and_hard` — asserts `#death-hint` is omitted when difficulty is MEDIUM or HARD.
- **Commands:** `python -m pytest tests/test_death_hint_difficulty.py -v`.

## Definition of Done / Acceptance Criteria
- [ ] Hint appears in dim grey on the death screen only when difficulty is set to EASY.
- [ ] Hint is completely omitted on MEDIUM and HARD.
- [ ] Difficulty setting contract is respected (mercy and information knob, AC-16).
- [ ] Automated tests verify both visibility states.

## Rollback / Undo
Revert hint conditional mounting in `screens/death.py`.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations -->
