# Task B01: `DifficultyConfig`, the parameters seam

## Metadata
- Epic: [EPIC_Phase2_TheHouse_PLAN.md](EPIC_Phase2_TheHouse_PLAN.md)
- Slice: B — Difficulty as a Real System
- Layer: SVC
- Status: DONE
- Estimate: ~2.5h
- Depends on: A13
- Blocks: B02, B05
- Covers: AC-16
- Suggested commit: `feat(difficulty): add the difficulty parameter seam`
- Branch: feature/phase_2_the_house (per GP-3; Git Policy not yet confirmed)

## Objective
Create the one place where difficulty is read: a `DifficultyConfig` that turns the `difficulty` setting into named parameters, so Slices B, D and I consume numbers instead of branching on a string.

## Non-Goals
- Does not change any observable behaviour. After this task the game plays **identically on all three settings** — this task builds the seam, B02–B05 pull its levers. That separation is deliberate: it is what §11 warns must not be retrofitted later.
- Does not author the parameter values — GP-6 owns those. This task defines the **shape** and fills it with explicit placeholders clearly marked as unconfirmed.
- Does not implement hints, mercy, or expiry — those are B03, B04, B05.
- Does not add a setting or a menu option. The three difficulties already exist in `config.py`.

## Context & Constraints
- **Read first:** §5.1 in full — "**Difficulty changes information and mercy, never story.** No difficulty locks a room, an item, or a solution. HARD removes safety nets, not fairness. HARD removes safety nets, never fairness." — plus §11's seam advice ("put the hook in now... retrofitting it is where bugs live"), §3.1 and §3.2 for the two bars the parameters govern, and `docs/PHASE1/README.md`'s "Deliberately Not In This Phase" entry that defers §5.1–5.3 to Phase 2 (this task is that deferral being paid).
- **Files to create:** `game/difficulty.py` (to be created).
- **Files to modify:** none, if the seam is consumed lazily. If a call site is needed, `game/lantern.py` and `game/composure.py` may read it later — **but not in this task**; wiring is B02's job.
- **Files to read, not modify:** `config.py` — `SettingsManager.get("difficulty")` returns `"EASY" | "MEDIUM" | "HARD"`, and `DEFAULT_SETTINGS["difficulty"] == "MEDIUM"`; `game/state.py` — `RunState` is where a config would be attached; `screens/settings.py` — the existing toggle pattern and its `EASY/MEDIUM/HARD` order (B05 and D-readers must agree with it).
- **Conventions to respect:** PEP 8, type hints, and the dataclass style `game/state.py` already uses. Module docstrings in the Phase 1 style — `game/state.py`'s docstring explains its contract and who depends on it; match that.
- **Design constraints — the seam's whole value is in its shape:**
  - **One lookup, one object.** Every difficulty-dependent number comes from `DifficultyConfig`; no module reads the raw `"EASY"`/`"MEDIUM"`/`"HARD"` string directly. This is the property B06 tests mechanically.
  - **Parameters are named for what they do, not for the setting.** `lantern_generosity`, not `easy_lantern`. A parameter named after a difficulty invites a second branch.
  - **Unknown or missing difficulty falls back to MEDIUM**, matching `SettingsManager`'s self-repairing `load()`. A corrupted settings file must not crash a run.
  - **No parameter may gate content.** The config carries numbers and booleans about *generosity, information, and mercy* — never a room id, an item id, or a solution's availability. This is ASM-14 made structural, and it is what keeps RISK-5 closed.
  - **Placeholders must be visibly unconfirmed** until GP-6 answers — a comment naming GP-6 beside each value.
- **Voice:** the module docstring should state the §5.1 rule in one sentence, because it is the rule a future contributor is most likely to break.

## Preconditions
- [ ] A13 DONE — the loop is green and the playtest passed
- [ ] `config.py` provides `difficulty` with the three values and a MEDIUM default
- [ ] `game/state.py` and `game/lantern.py` exist and are the consumers to come
- [ ] `python -m pytest` green (baseline recorded)

## Actionable Steps
1. Read `config.py`'s `DEFAULT_SETTINGS` and `screens/settings.py`'s difficulty cycling to confirm the three values and their order.
2. Create `game/difficulty.py` with a frozen dataclass and a factory that maps a difficulty string to it.
3. Name the parameter groups by concern: **generosity** (the two bars), **information** (hints), **mercy** (restart and journal), **pressure** (expiry, countdowns) — so B02–B05 each have an obvious home and none of them needs to add a field to a neighbour's group.
4. Give every field a value, with a `# GP-6: unconfirmed` comment on each, and choose the values so that MEDIUM reproduces **today's** behaviour exactly — the baseline must not move.
5. Implement the unknown-value fallback to MEDIUM and make it total: no code path raises on a bad difficulty string.
6. Write the module docstring with the §5.1 rule and a note that all consumers must read parameters, never the string.
7. Prove the seam is inert: run the game on EASY, MEDIUM and HARD and confirm nothing differs yet.

## Test Plan
- **Tests to write/update:** new `tests/test_difficulty_config.py` (to be created):
  - `test_each_difficulty_produces_a_distinct_config` — asserts the three configs are not all equal (the seam is wired to something).
  - `test_unknown_difficulty_falls_back_to_medium` — asserts `None`, `""`, and a nonsense string all yield the MEDIUM config rather than raising.
  - `test_medium_reproduces_the_pre_slice_defaults` — the baseline-stability check; asserts MEDIUM's values equal the numbers A05 and D01 shipped with.
  - `test_config_carries_no_content_identifiers` — a guard for ASM-14: asserts no field value matches a room, item, or solution id.
- **Commands:** `python -m pytest tests/test_difficulty_config.py -v`; then `python -m pytest`.
- **Manual verification:** play a full run on each of the three settings and confirm the experience is unchanged; the only observable difference should be the number in the settings screen.
- **Inertness check:** this is the task's sharpest test — if behaviour *did* change on EASY, the seam has leaked a decision that belongs to B02–B05.

## Definition of Done / Acceptance Criteria
- [x] `game/difficulty.py` exists with a frozen dataclass and a total factory
- [x] Every field is named for its effect and commented with GP-6 until confirmed
- [x] MEDIUM reproduces pre-slice behaviour exactly
- [x] Unknown or missing difficulty falls back to MEDIUM without raising
- [x] No field carries a room, item, or solution identifier
- [x] No behaviour is observable different on any setting yet — verified by playing all three
- [x] The module docstring states the §5.1 rule
- [x] No file outside `game/difficulty.py` and its test was modified
- [x] `python -m pytest` passes, including the three pre-existing modules

## Rollback / Undo
Revert this task's commit; the module vanishes and nothing else changes, since nothing consumes it. B02, B05, and D01 depend on it, so revert as a group if any of them have landed.

## Execution Log
<!-- Filled during execution: date, agent, branch, commit hash, notes, deviations; record the parameter list and which values await GP-6 here -->
