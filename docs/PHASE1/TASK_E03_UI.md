# Task E03: Wire `START GAME` and the run lifecycle

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: E — Honest Endings on Screen
- Layer: UI
- Status: TODO
- Estimate: ~2h
- Depends on: E01, E02
- Blocks: E04
- Covers: AC-1, AC-10
- Suggested commit: `feat(app): launch a real run from the main menu`
- Branch: per GP-3

## Objective
Replace the placeholder that has been pretending to start a game since the project began — `START GAME` only updating a status label — with a real run: the menu builds a fresh run state and pushes the gameplay screen, and every exit from a run (death, ending, or quitting mid-run) returns the app to a clean, consistent place.

## Non-Goals
- Does not change the menu's items, order, or appearance beyond what the launch needs (A01 settled the menu's structure).
- Does not implement the gameplay screen, the death screen, or the ending screen — all three exist by now; this task connects them.
- Does not implement save or resume (§9.1 is Phase 2), so there is no "continue" path and no run survives app exit.
- Does not make difficulty, sound, or music affect the run (§5.1–5.3 are Phase 2). The run is constructed identically regardless of the settings file; this task must not quietly begin honoring them.
- Does not remove B01's temporary entry point without confirming nothing else references it.
- Does not add a pause menu, an in-run settings screen, or a quit confirmation — quitting mid-run is Escape, and Phase 1 does not ask twice.

## Context & Constraints
- **Read first:** `index.py` (the current `action_select` that only updates a status label, and the `options` list), `screens/main_menu.py` (A01's extracted menu), `screens/game.py` (B01's temporary entry point, which this task removes), `game/state.py` (A03's run state and its construction), and `docs/SUGGEST.md` §5.1, so it is explicit which settings must *not* affect the run yet.
- **Files to modify:** `index.py` — `START GAME` launches a run; the status-label pretend-path is deleted. `screens/main_menu.py` — the launch action. `screens/game.py` — remove B01's temporary entry point.
- **Files to read, not modify:** `config.py` (`SettingsManager`), `screens/death.py` and `screens/ending.py` — the two exits this task must route consistently.
- **Conventions to respect:** PEP 8; type hints; `self.app` for shared state; screens pushed and popped as the existing code already does; no heavy logic in `compose()`.
- **Design constraints:**
  - **One construction path for a fresh run.** The menu's launch and the death screen's retry (E01) and the ending screen's optional fresh run (E02) must all produce a run the same way. If this task finds three copies of run construction, that is a defect to fix here, not to add a fourth of.
  - **Where does the run state live?** Decide and record: on the app (accessible as `self.app.run` or equivalent) or passed to the screen. The app-owned choice is the one that survives screen pops and matches how `config` is already shared — but the decision must be recorded, not assumed.
  - **The app must be returnable to a clean state.** After a death, an ending, or Escape mid-run, the menu must be exactly as it was, with no run state leaking into the next launch. Confirm by launching, dying, and launching again.
  - **Delete the pretend-path.** The status-label update must be gone, not left as a fallback, or the next contributor will find two ways to start a game and pick the wrong one (AC-10's spirit).
  - **Settings are read but ignored.** The run may be constructed with the settings available, but nothing may branch on difficulty, sound, or music. Record this explicitly so Phase 2 knows where the seam is.
  - **Quit still works.** EXIT must still exit, and Escape mid-run must not exit the app — only leave the run.
  - No red (§7.4), no new keys beyond those already bound.

## Preconditions
- [ ] E01 and E02 DONE — both terminal screens exist and replace their placeholders
- [ ] A01 DONE — the menu lives in `screens/main_menu.py`
- [ ] A03 DONE — run state has a construction path
- [ ] B01's temporary entry point is locatable and its comment says it is temporary
- [ ] The app launches and the settings screen still works

## Actionable Steps
1. Record the current `START GAME` behavior and locate every place a run is currently constructed, so the count is known before changing anything.
2. Decide and record where the run state lives (app-owned, recommended) and the single construction path a fresh run takes.
3. Enforce that single path: refactor E01's retry and E02's fresh run to call it if they do not already, so all three entry points agree.
4. Implement `START GAME` to construct a fresh run and push the gameplay screen.
5. Delete the status-label pretend-path from `index.py`.
6. Remove B01's temporary entry point from `screens/game.py` after confirming nothing else references it.
7. Route the run's exits consistently: Escape mid-run returns to the menu and discards the run; death goes to E01; the ending goes to E02; EXIT still exits.
8. Verify no settings value influences the run by inspecting the construction path against §5.1 and confirming nothing branches on difficulty, sound, or music.
9. Play the cycle twice: launch → play → die → retry → quit to menu → launch again. Confirm each launch is clean.

## Test Plan
- **Tests to write:** E04's end-to-end checklist covers this wiring and is the primary verification. A unit test asserting two consecutive fresh runs are deeply equal and independent (no shared mutable state) is worth adding to E04 — a shared-defaults bug is exactly the kind of defect that survives a single playthrough.
- **Commands:** `python index.py`
- **Expected:** `START GAME` opens the gameplay screen on a fresh run; Escape mid-run returns to the menu; dying reaches E01; winning reaches E02; retry from E01 and a fresh run from E02 both start clean; EXIT exits.
- **Cycle check (required):** launch, play, die, retry, return to menu, launch again, and confirm the second launch behaves identically to the first — same starting lantern, same turn counter, no held items, no flags. This is the state-leak check and it is the reason this task exists.
- **Independence check:** confirm two runs constructed in sequence do not share mutable state — mutating one must not affect the other.
- **Pretend-path check:** confirm no status-label "starting game with difficulty X" path remains anywhere.
- **Settings check:** change `settings.json`'s difficulty to each of the three values, launch a run each time, and confirm the run is identical. Then restore the original file.
- **Odd-width and narrow-width check:** the menu and the gameplay screen still render at ~60 columns.
- **Syntax check:** `python -m py_compile index.py config.py screens/*.py game/*.py`

## Definition of Done / Acceptance Criteria
- [ ] `START GAME` launches a real run on a fresh run state
- [ ] The status-label pretend-path is deleted, not retained as a fallback
- [ ] Exactly one fresh-run construction path exists, used by the menu, E01's retry, and E02's fresh run
- [ ] Where the run state lives is decided and recorded
- [ ] Escape mid-run returns to the menu and discards the run; EXIT still exits
- [ ] Two consecutive runs are independent — no shared mutable state, no leaked lantern, turns, items, or flags
- [ ] No settings value affects the run; the seam for Phase 2 is recorded
- [ ] B01's temporary entry point is removed, with no dangling references
- [ ] The menu and gameplay screens still render at ~60 columns
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. `START GAME` returns to its non-functional state and the run is unreachable from the menu; the gameplay screen keeps B01's temporary entry point, so the slice remains manually playable. Verify the app launches and the menu and settings screens still work.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record where run state lives, the construction-path refactor, and the settings-independence result here -->
