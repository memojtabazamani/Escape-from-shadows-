# Task B05: HARD — choices that expire on hesitation

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: B — Difficulty as a Real System
- Layer: UI
- Status: TODO
- Estimate: ~3h
- Depends on: B01
- Blocks: B06
- Covers: AC-16, AC-17
- Suggested commit: `feat(difficulty): expire choices on hesitation on hard`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
On HARD, make hesitation cost you: a choice held too long expires per its own content rule, and its loss is visible — while EASY and MEDIUM wait indefinitely.

## Non-Goals
- Does not expire choices on any other difficulty — the parameter is off, not merely generous.
- Does not implement the timer's display as a general UI feature; the *expiry* is what this task builds, and §5.3's visual rhythm (H02) is where the terminal's sense of time gets its polish.
- Does not gate any room, item, or solution behind an expiry. ASM-14: HARD removes safety nets, not content. An expired choice must always have a remaining alternative.
- Does not implement multi-turn actions — that is F01. This is about wall-clock or turn-based hesitation on a *single* decision, not about actions that occupy several turns.
- Does not add a settings toggle for expiry. It is a consequence of HARD, per §5.1.

## Context & Constraints
- **Read first:** §5.1's HARD bullet and its caveat, §4.3's "choices with no safe answer" (the design reason hesitation is a legitimate pressure), §7.1's footer-prompt zone — where a "time is passing" signal belongs if you add one — and §13's input-friction pitfall, which is the failure mode this task is most likely to cause by accident.
- **Files to modify:** `screens/game.py` (A03's choice-selection path); `game/difficulty.py`'s pressure parameters.
- **Files to read, not modify:** `game/effects.py` — an expired choice is *not* a requirement failure and must not be routed through `check_requirements()`, which would report it as a gate and mislabel it in the reason text; `game/content_schema.py` — expiring is a **new per-choice content field**, so the validator must learn to accept it (record whether you extend the schema here or hand that to C02, which owns engine-contract extension).
- **Conventions to respect:** content-as-data — which choices expire, and after how long, is content, not code; the screen reads it.
- **Design constraints — this is the highest-risk task in Slice B, because it can make the game feel broken:**
  - **Turn-based, not wall-clock.** Textual's event loop and a terminal's latency make real timers unreliable and unfair — a player reading slowly is not hesitating. Count *turns* or *refusals* in the room, and record the decision and its justification.
  - **Every expiry must be telegraphed and recoverable.** §4.1's rule generalises: an unannounced expiry is as unfair as an unwarned death. The player must see it coming, and losing a choice must leave the room playable.
  - **No expiry may strand the run.** B06 asserts the reachable-content sets are identical across difficulties; that assertion is what keeps this task honest.
  - **The footer prompt must reflect the state** (§7.1) — if time is passing, the prompt says so; silence while a choice decays is the input-friction pitfall.
  - **Accessibility-sensitive:** §8's Phase 4 list includes pause-anywhere, and a HARD that punishes slow reading is exactly what §8 anticipates. Record the tension and keep the mechanism turn-based so a future pause feature can honour it.
  - **The timer must be visible to a *player*, not just to a test.** Decide and record the cue, and confirm it in the manual verification.
- **Voice:** the cue that time is passing should be the house's, not a progress bar's — but it must be unambiguous. Decide the register and record it.

## Preconditions
- [ ] B01 DONE — the pressure parameters exist and MEDIUM is inert
- [ ] A03 DONE — choice selection is implemented and is the path being extended
- [ ] A04 DONE — the status and footer zones render, since the cue lives there
- [ ] The content schema's extension route is decided — this task, or C02 (sponsor to RISK-3's spike)
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Decide the hesitation measure — turns in the room, refusals, or revisits — and record why the wall clock was rejected.
2. Decide the content field that carries a choice's expiry, and extend `game/content_schema.py` (or record the handoff to C02 if the spike's route is to be decided there).
3. Author at least one expiring choice in existing content, with its duration and its expiry text.
4. Implement the countdown in the gameplay screen's selection path, gated on the pressure parameter.
5. On expiry, express the loss through the screen's own channel — **not** through `check_requirements()`, so it is not mislabelled as a gate.
6. Add the footer-prompt cue so the player sees the state (§7.1).
7. Ensure the room remains playable after an expiry, and that every lost choice leaves an alternative.
8. Walk HARD: hesitate deliberately, watch a choice expire, recover, finish the run.
9. Walk EASY and MEDIUM: confirm the cue never appears and no choice ever expires.

## Test Plan
- **Tests to write/update:** new `tests/test_difficulty_pressure.py` (to be created):
  - `test_choice_expires_on_hard_only` — asserts the parameter across all three difficulties.
  - `test_expiry_is_preceded_by_a_visible_cue` — asserts the cue renders before the loss, guarding §4.1's generalisation.
  - `test_room_remains_playable_after_an_expiry` — asserts a viable choice still exists.
  - `test_reachable_content_is_identical_on_every_difficulty` — the ASM-14 guard, shared with B06 and asserted here at the point of risk.
  - `test_expiry_is_not_reported_as_a_requirement_failure` — asserts the reason text and routing are correct.
- **Commands:** `python -m pytest tests/test_difficulty_pressure.py -v`; then `python -m pytest -v`.
- **Manual verification:** on HARD, hold a choice and confirm you *saw* it coming and could still finish. On MEDIUM, confirm nothing ever expires.
- **Fairness walk:** on HARD, note every expiry you trigger and confirm the run remained completable after each.

## Definition of Done / Acceptance Criteria
- [ ] Expiry is turn-based, and the choice of measure is recorded with its justification
- [ ] Expiring is a content field, validated by `content_schema.py`
- [ ] Expiry occurs on HARD only
- [ ] A visible cue precedes every expiry, in the footer-prompt zone per §7.1
- [ ] The room is playable after any expiry and no expiry strands the run
- [ ] Reachable rooms, items and solutions are identical on all three difficulties — asserted by test
- [ ] Expiry is not routed through or labelled as a requirement failure
- [ ] The tension with §8's pause-anywhere is recorded as a Phase 4 note
- [ ] `python -m pytest -v` passes, including the three pre-existing modules and A13's suite

## Rollback / Undo
Revert this task's commit; HARD loses its time pressure and choices wait indefinitely, which is safe but leaves §5.1's HARD bullet only half-delivered. If the market schema extension was authored here and C02 has since landed, keep the schema change and revert only the screen logic.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the hesitation measure, the cue's register, the schema-extension route, and the fairness walk here -->
