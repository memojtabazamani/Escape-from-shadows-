# Task E01: Death screen — cause, retry, back to menu

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: E — Honest Endings on Screen
- Layer: UI
- Status: TODO
- Estimate: ~2.5h
- Depends on: D04
- Blocks: E03
- Covers: AC-6
- Suggested commit: `feat(screens): add the death screen with cause and retry`
- Branch: per GP-3

## Objective
Give the slice's death a screen that tells the truth: what killed you, and what you may do next. This replaces B03's commented Death-tier placeholder and is where pillar 2 ("the player always understands why they died") becomes visible rather than merely true in the data.

## Non-Goals
- Does not implement the death *condition* or its telegraphs (D04) — this task renders a result D04 already produces.
- Does not implement §9.2's "what you learned" line or the "you could have done X" hint — Phase 2.
- Does not implement difficulty-gated mercy, extra retries, or a life system — Phase 2 (§5.1).
- Does not implement the Shadow, the dread counter, or a death animation (§7.2's typewriter is F02's, and Phase 1 does not animate the death).
- Does not add a second death screen or a variant ending screen.
- Does not persist anything: Phase 1 has no save (§9.1 is Phase 2), so a retry starts a fresh run, not a restored one.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §4.1 (the three-tier model; death must be earned), §9.2 (what the death screen should eventually say — read it to know what to *defer*, not to build), §7.4 (color as grammar: red is reserved for the Shadow, which does not appear in Phase 1), and `screens/game.py` (B03's Death-tier placeholder, which this task replaces).
- **Files to create:** `screens/death.py`.
- **Files to modify:** `screens/game.py` — replace the commented Death placeholder with a push of the real screen; remove the placeholder comment.
- **Files to read, not modify:** `game/effects.py` (the death result D04 produces), `game/state.py` (what a retry must discard), `screens/settings.py` and `screens/main_menu.py` for structure precedent.
- **Conventions to respect:** PEP 8; type hints; `Screen` subclass; CSS in the class attribute; `BINDINGS` rendered into the footer, not hand-listed; `self.app` for shared state; reuse the existing selection/menu interaction shape rather than inventing a new one.
- **Design constraints — the screen's job is honesty and speed:**
  - **The cause is the headline.** The text D04 supplied must be shown prominently and verbatim. Do not paraphrase it, soften it, or bury it below flavour prose.
  - **No new information may be withheld.** A player who dies must be able to say why. If the cause string is empty, that is a D04 defect — report it, do not substitute a generic message.
  - **The screen must not gloat and must not lecture.** §4.1 wants death to be the player's own doing; a taunting screen undermines that, and an explanatory screen removes the lesson. Say what happened and stop.
  - **Red is forbidden** (§7.4) — the Shadow does not appear in Phase 1, so its colour does not either. Use dim, or the neutral palette already in use.
  - **Two actions only:** retry (a fresh run) and back to the main menu. Both must be reachable without typing (AC-8).
  - **Retry must discard the dead run completely.** No state may leak from the dead run into the new one — the retry path must go through the same fresh-run construction E03 defines, not re-enter the old state object.
  - The screen must be dismissible with Escape as well, matching every other screen.

## Preconditions
- [ ] D04 DONE — a death result carrying a one-sentence cause is produced
- [ ] B03's Death placeholder exists and is commented for replacement
- [ ] A fresh-run construction path is defined or is being defined by E03; coordinate, since retry depends on it
- [ ] The app launches and the menu and settings screens still work

## Actionable Steps
1. Record the shape of D04's death result (at minimum: a cause string) and confirm the placeholder receives it.
2. Decide and record the screen's layout: what is shown, and in which order (recorded as: cause first, then the two actions).
3. Create `screens/death.py` with the screen class, its `CSS`, and its `BINDINGS`.
4. Render the cause prominently and verbatim from the result; do not restate or paraphrase it.
5. Implement the two actions — retry and back to the menu — and render them in the footer from the bindings.
6. Replace B03's commented Death placeholder in `screens/game.py` with the push of this screen, and delete the placeholder comment.
7. Implement retry as a *fresh* run via E03's construction path, verifying no dead-run state survives; if E03 has not landed, implement the call site against the agreed path and leave a clearly marked note rather than duplicating construction logic.
8. Verify with a real death: walk the left doorway, confirm the screen shows the exact cause, confirm retry starts a clean run, and confirm back-to-menu returns cleanly.
9. Verify at ~60 columns that the cause and both actions remain visible and unambiguous.

## Test Plan
- **Tests to write:** E04's end-to-end checklist covers this screen. A screen test asserting the rendered cause matches the result verbatim belongs in E04 or a follow-up; do not duplicate B05's screen-test harness here.
- **Commands:** `python index.py`, then walk the death path.
- **Expected:** the death screen shows the cause exactly as D04 produced it; retry starts a fresh run with a full lantern and no held items; back to menu returns cleanly; Escape dismisses.
- **State-leak check (required):** die, retry, and confirm the new run starts with a full lantern, no held items, no flags set, and the turn counter at its initial value — then die again by the same route and confirm the second death shows the same cause.
- **Placeholder check:** confirm no commented Death-tier placeholder remains in `screens/game.py`.
- **Readability check:** at ~60 columns, confirm the cause is not truncated and both actions are visible.
- **Syntax check:** `python -m py_compile index.py screens/*.py`

## Definition of Done / Acceptance Criteria
- [ ] `screens/death.py` exists and renders D04's cause verbatim as the headline
- [ ] The cause is never paraphrased and never replaced by a generic message
- [ ] Two actions exist: retry (fresh run) and back to the main menu
- [ ] Neither action requires typing (AC-8)
- [ ] Retry starts a provably clean run; no state leaks from the dead run
- [ ] Neither retry nor back-to-menu errors on repeat use
- [ ] No red anywhere on the screen (§7.4)
- [ ] The screen is dismissible with Escape
- [ ] The Death-tier placeholder in `screens/game.py` is replaced, with its comment removed
- [ ] Layout holds at ~60 columns
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit. `screens/death.py` is removed and a Death-tier choice again routes to the placeholder in `screens/game.py`; the death result from D04 remains produced but unrendered. Verify the game still launches and the doorway choice does not crash.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the layout decision and the state-leak check result here -->
