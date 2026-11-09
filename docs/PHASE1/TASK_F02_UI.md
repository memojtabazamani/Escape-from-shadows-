# Task F02: Typewriter prose reveal (§7.2)

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: F — Truth & Polish (optional)
- Layer: UI
- Status: TODO
- Estimate: ~2.5h
- Depends on: B02
- Blocks: None
- Covers: AC-1
- Suggested commit: `feat(screens): reveal room prose progressively`
- Branch: per GP-3

## Objective
Make the rooms land the way §7.2 describes: prose that arrives a little at a time rather than all at once, so the text is read instead of scanned. This is the terminal's substitute for the thing a graphical game gets from art — pacing, and the feeling that something is being told to you.

## Non-Goals
- Does not change any content. The pacing is a presentation layer over B02's renderer; if a room reads badly once paced, that is a content finding for Slice D.
- Does not implement sound or music. §5.2–5.3 and §7.2's bell note remain Phase 2; the terminal's audio channel is deliberately unused here.
- Does not implement the Shadow's appearance, a dread effect, or any animation other than the reveal.
- Does not implement §8's accessibility settings — no reduced-motion toggle, no speed preference. That is Phase 4, and this task must not invent a setting the settings screen does not have.
- Does not animate the status zone, the choice list, or the death and ending screens.
- Does not make the reveal skippable via a key binding, unless a key is added and recorded — Phase 1's bindings are settled, and a new key is a scope decision, not an implementation detail.

## Context & Constraints
- **Read first:** `docs/SUGGEST.md` §7.2 in full (including its warning about what pacing must *not* do), §7.1 (the scene zone must not scroll away), §8's note on motion and accessibility, and `screens/game.py` — B02's renderer and its line budget, and F01's documentation of the real bindings.
- **Files to modify:** `screens/game.py` and whatever pure helper module B02 placed the wrapping helper in.
- **Files to read, not modify:** the content files (the reveal must not change what is rendered, only when), `game/state.py`.
- **Conventions to respect:** PEP 8; type hints; no heavy logic in `compose()`; the reveal runs as a Textual timer or worker **outside** the synchronous render path — a blocking sleep in `compose()` or in a render method is a defect that will freeze the interface.
- **Design constraints:**
  - **The reveal is presentation only.** The text rendered in full and the text revealed progressively must be byte-identical once complete. A test can assert this; do not let the pacing change the content.
  - **It must not delay the player.** Input must remain responsive during the reveal; a player who selects a choice before the prose finishes must not be blocked, and the screen must not queue commands in a way that makes a fast player's inputs land on the wrong room.
  - **It must be interruptible.** If a player acts mid-reveal, the reveal must complete immediately rather than continuing behind the new state — otherwise a room's prose bleeds into the next room's.
  - **The room name appears first, always.** §7.1's rule is that the room name must never be what scrolls away; the reveal must not put the name last.
  - **Pacing is per room arrival and per outcome, not per character of every string.** The status zone, counters, and hints must not flicker.
  - **The reveal must not break the line budget.** A paced render still fits the scene zone; if pacing causes wrapping differences, the reveal is implemented wrong.
  - **Cost per room is a readability judgement, not a speed maximisation.** Record the chosen delay and justify it in one line; a reveal fast enough to be a formality is worse than none, because it costs frames and buys nothing.
  - **Terminals vary.** The reveal must not assume a specific terminal's refresh rate or support for cursor control beyond what Textual provides; if it degrades on a slow terminal, it must degrade to *reading normally*, never to a corrupt display.
  - No red (§7.4).

## Preconditions
- [ ] B02 DONE — a room renders from content through the renderer and the wrapping helper
- [ ] B04 DONE or in progress — the status zone exists, so it is clear what must *not* animate
- [ ] B05's screen tests pass, since this task must not break them
- [ ] F01 DONE or its controls table known, so a new key — if any — is documented rather than invented

## Actionable Steps
1. Record the current render path: where B02 assembles a room's text, and where the wrapping helper fits.
2. Decide and record the reveal mechanism (a Textual timer driving the reveal, so the interface stays responsive) and the delay per step, with a one-line justification.
3. Decide and record the interaction rule: what happens when the player acts mid-reveal — the reveal completes immediately and the action proceeds, or the action is deferred; pick one, record it, and make the other impossible.
4. Implement the reveal so the fully-revealed text is identical to B02's unpaced output.
5. Implement the interrupt behavior and verify the room name is rendered before any prose.
6. Confirm the status zone, the counters, and the footer are untouched by the reveal.
7. Verify the reveal does not break the line budget or cause different wrapping at ~80 and ~60 columns.
8. Verify responsiveness: hold a direction key during a reveal and confirm the selection moves without freeze; act mid-reveal and confirm the reveal completes rather than bleeding into the next room.
9. Confirm that if the feature were disabled, the screen would behave exactly as it does today — record how it can be turned off, so a future accessibility setting has an obvious seam.

## Test Plan
- **Tests to write:** a test asserting the fully-revealed text equals the unpaced renderer's output for the same room, and a test asserting an interrupt completes the reveal before the state changes. B05's existing screen tests must still pass unchanged — if the reveal forces them to become timing-dependent, that is a design defect, not a test problem.
- **Commands:** `python index.py`, then walk several rooms; the project's test command from GP-2.
- **Expected:** prose appears progressively; the room name is visible from the first frame; the status zone does not flicker; a mid-reveal action completes the prose and then acts; the fully-revealed text matches the unpaced renderer exactly.
- **Responsiveness check (required):** press keys rapidly during a reveal and confirm no input is lost, no input lands on the wrong room, and the app never appears frozen.
- **Equality check:** render one room with the reveal disabled and with it enabled, and confirm the final text is identical — character for character, not visually similar.
- **Budget check:** at ~80 and ~60 columns, confirm the laid-out lines still fit the scene zone with no continuation marker (AC-11).
- **Slow-terminal degradation check:** if a way to simulate a slow terminal exists, use it; if not, record that this check was not performed rather than claiming it passed.
- **Syntax check:** `python -m py_compile index.py config.py screens/*.py game/*.py`

## Definition of Done / Acceptance Criteria
- [ ] Room prose reveals progressively on arrival and on outcome
- [ ] The fully-revealed text is identical to the unpaced renderer's output, character for character
- [ ] The room name is rendered before any prose and stays visible
- [ ] Input stays responsive during a reveal; no keystrokes are lost
- [ ] An action taken mid-reveal completes the reveal before the state changes, with no bleed into the next room
- [ ] The status zone, counters, and footer do not animate or flicker
- [ ] The line budget holds at ~80 and ~60 columns
- [ ] The reveal can be disabled, and the seam for a future accessibility setting is recorded
- [ ] The delay per step and the interrupt rule are recorded with a rationale
- [ ] B05's screen tests pass unchanged and are not made timing-dependent
- [ ] No new key binding is introduced without being documented in F01's controls table
- [ ] `python -m py_compile` clean; no unrelated files changed

## Rollback / Undo
Revert this task's commit, or disable the reveal through the seam recorded in step 9. Room text renders instantly, exactly as B02 left it; no content, state, or resolver behavior is affected. Verify the screen renders and the B05 tests pass after reverting.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the chosen delay, the interrupt rule, the equality-check result, and whether the slow-terminal check was performed here -->
