# Task E04: End-to-end playtest checklist, including §12's stranger test

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: E — Honest Endings on Screen
- Layer: TEST
- Status: TODO
- Estimate: ~2h
- Depends on: E03
- Blocks: F01
- Covers: AC-6, AC-7, AC-12
- Suggested commit: `test(app): add the end-to-end playtest checklist`
- Branch: per GP-3

## Objective
Verify the phase the way §12 defines it — by playing, and by watching someone else play. This task produces the human checklist that decides whether Phase 1 is done, and records its results. It is the only task in the plan whose verification cannot be automated.

## Non-Goals
- Does not automate the playtest. A script cannot tell you whether a stranger wanted a second run; §12's success test is behavioural by definition.
- Does not replace D06's automated reachability tests or B05's screen tests — this sits on top of them, and assumes they pass.
- Does not fix defects it finds. Every finding becomes a report against the task that owns it (D01–D05, B01–B04, E01–E03); this task records, it does not repair.
- Does not perform the documentation re-sync (F01).
- Does not evaluate Phase 2+ material: difficulty behaviour, composure, the journal, save/load, the Shadow, or the seven rooms in §6 are out of scope and their absence is not a finding.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §12 in full (the phase's bullets and its stated success test), §4.1 (death must be earned — this is what the death checklist line is checking), §4.2 (telegraph quality), §7.1 (the three zones), and §13's pitfall list (each pitfall is effectively a checklist line).
- **Files to create:** the playtest checklist document (a Markdown file in the docs tree, not a test module), plus a small test module for the one automatable item below.
- **Files to modify:** none in the application.
- **Conventions to respect:** the checklist is written to be re-run — every line must be a concrete observation with a pass/fail, not an opinion. Where a line needs a person, say so; where it can be scripted, script it.
- **The checklist must cover, at minimum:**
  - **Cold start:** `python index.py` from a clean checkout; the menu appears; nothing errors on startup with an empty, corrupt, or missing `settings.json`.
  - **The run lifecycle:** launch → play → die → retry → menu → launch again, with no state leak (E03's cycle check, repeated by hand).
  - **The three zones:** scene, status, and footer are all present and legible at ~80 and ~60 columns; the room name stays visible under long prose.
  - **Choices:** selectable, wrapping, Enter selects, a refused choice changes nothing observable, no typing is required at any point (AC-8).
  - **The cost:** the lantern visibly drains as rooms are entered; the turn counter advances; a low-oil warning appears before the lantern is empty; the drain is *felt* — a player can describe the lantern as a limit by the end of the first run.
  - **The death (AC-6):** the telegraphs are noticed *before* the choice is made — ask the player after they die whether they were warned, and record their exact words; the death states its cause; the player can say why they died and what they would do differently.
  - **The ending (AC-7):** reachable by a player who is not following instructions; the reason the door opened is understandable in retrospect.
  - **The loop:** the second visit to the HALL reads differently because of what happened in the library (design pillar 3).
  - **Content-only (AC-9):** add a room by editing content only, confirm it renders, then revert. This is the architectural claim of the whole phase, and it must be re-verified by hand at least once.
  - **§12's stranger test (AC-12):** a person who has not seen the game plays it *without being asked to continue*, and starts a second run unprompted. Record what they said and did. This single line is the phase's definition of success.
- **The one automatable item:** the E03 independence test — two consecutive fresh runs share no mutable state. Write it as a test, since a shared-defaults bug is invisible in a single playthrough and deterministic to check.

## Preconditions
- [ ] E03 DONE — the run is launchable and its lifecycle is wired
- [ ] D06, B05, C03, and A06 all pass — this task assumes the automated suites are green, so any failure here is a new finding
- [ ] `python index.py` launches from a clean checkout
- [ ] A person who has not seen the game is available for the stranger test, or its absence is recorded as a gap

## Actionable Steps
1. Record the pre-task baseline: run the full automated suite and record the result, so findings can be attributed correctly.
2. Write the checklist document with every line as a concrete observation and a pass/fail box, grouped by the areas listed above.
3. Write the run-independence test (two consecutive fresh runs are deeply equal and mutually unaffected).
4. Run the three cold-start variants by hand: missing `settings.json`, empty file, and corrupt file; record the behavior for each.
5. Play a full run as the developer, filling in the checklist honestly — including any line that fails.
6. Run the content-only check: add a room by editing content alone, confirm it renders with no change to `screens/`, then revert and confirm the revert is clean.
7. Conduct the stranger test: hand over the game, say nothing beyond how to run it, and observe. Record whether they played a second run unprompted; if they did not, record what they said and treat it as a finding.
8. For the death, ask the player afterwards whether they felt warned, and record their exact words rather than a summary.
9. Record every finding against the owning task; do not fix anything in this task.
10. Fill the checklist and the Execution Log, including the stranger test's outcome.

## Test Plan
- **Commands:** the project's test command from GP-2 (the full suite, not a subset), then `python index.py` for each manual line, plus `python -m py_compile index.py config.py screens/*.py game/*.py`.
- **Expected:** the automated suite passes; every checklist line is filled with a pass/fail and an observation; the stranger test either passes or produces a recorded finding.
- **Honesty requirement:** a checklist line that was not actually run must be marked "not run", never ticked. A playtest checklist with unearned ticks is worse than no checklist, because the phase's definition of done rests on it.
- **Repeat run:** re-run the entire checklist a second time on a fresh checkout — the second run is what catches state-dependent defects, and §12's success test itself is about the *second* run.
- **Stranger test protocol (record verbatim):** do not prompt, do not hint, do not explain the lantern, do not say "try the other door." Note the time to first death or first ending, whether they read the room text, and whether they start a second run without being asked.

## Definition of Done / Acceptance Criteria
- [ ] The checklist document exists with every line stated as a concrete pass/fail observation
- [ ] Every line has been run and marked, with "not run" used honestly where applicable
- [ ] The full automated suite passes on a clean checkout
- [ ] All three cold-start `settings.json` variants behave correctly
- [ ] The run-independence test exists and passes
- [ ] The content-only check has been performed and reverted cleanly
- [ ] The death checklist confirms the player felt warned, with their words recorded
- [ ] §12's stranger test has been conducted, with its outcome recorded — a second unprompted run, or a specific finding explaining why not
- [ ] Every finding is recorded against an owning task and none were fixed here
- [ ] The checklist has been re-run a second time on a fresh checkout
- [ ] No application file changed by this task

## Rollback / Undo
Delete the checklist document and the run-independence test. No application behavior changes, so no user-facing rollback exists. Note that findings recorded here are *not* reverted by this rollback; they remain valid against the tasks that own them.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the stranger test's outcome and the list of findings here -->
