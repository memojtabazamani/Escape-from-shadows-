# Task F01: Re-sync `AGENTS.md`, `README.md`, `GENERAL_DOC.md`, and `SUGGEST.md` §0

## Metadata
- Epic: [EPIC_Phase1_VerticalSlice_PLAN.md](EPIC_Phase1_VerticalSlice_PLAN.md)
- Slice: F — Truth & Polish (optional)
- Layer: DOCS
- Status: TODO
- Estimate: ~1.5h
- Depends on: E04
- Blocks: None
- Covers: AC-10, AC-12
- Suggested commit: `docs: describe the game that now exists`
- Branch: per GP-3

## Objective
Make the documentation describe the game that actually exists. Today `AGENTS.md` promises a `game/` directory that hosts shared state while the directory is mostly empty, and `SUGGEST.md` §0 was written when the game had no gameplay at all. §13's sharpest warning is that a project which documents a game it does not have is lying to its own next contributor — this task removes that lie.

## Non-Goals
- Does not document Phase 2+ material as if it exists. SUGGEST.md's later sections are *proposals* and must stay clearly framed as such.
- Does not restructure the documentation scheme or introduce new doc files beyond what the sync needs.
- Does not rewrite `SUGGEST.md`'s design content (§1–§14) — only §0, which is the section that claims a current state.
- Does not add a changelog, contributing guide, or code-of-conduct.
- Does not touch `docs/PHASE1/`'s task files; their statuses are updated by their own execution logs.
- Does not document features from Slice F's F02 or any deferred item as delivered.

## Context & Constraints
- **Read first:** all four documents in full — `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, `docs/SUGGEST.md` §0 — then the actual state of the repo: `index.py`, `screens/`, `game/`, the content files, and whatever `requirements.txt` and `tests/` now contain.
- **Files to modify:** `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, `docs/SUGGEST.md` (§0 only).
- **Files to read, not modify:** everything else.
- **Conventions to respect:** match each document's existing voice and heading structure; keep edits surgical where the document is otherwise correct; do not reformat unrelated content (a diff full of whitespace makes a doc-sync unreviewable).
- **Required corrections — verify each against the code before writing, and do not assume:**
  - **The structure diagram.** Every document that shows a directory tree must show the tree that exists — the new modules, screens, content files, tests, and dependency file. Remove `settings_manager.py` from any diagram if A02 deleted the stub.
  - **The controls table.** The documented keys must match the real bindings — including the gameplay screen's keys and the death and ending screens' actions, not only the menu's.
  - **The run instructions.** Whatever is needed to install and start the game must be stated, including the test framework if GP-2 added one.
  - **The dependency section.** If a `requirements.txt` now exists, the install instructions must use it rather than describing a manual `pip install`.
  - **`AGENTS.md`'s "Common Tasks".** It currently tells contributors to edit `self.options` in `index.py` to add a menu option, and to add screens by pushing them from `index.py`. Both are now wrong — the menu lives in `screens/main_menu.py`, and adding a room is a content task. This section must describe the real workflow, and it should state the AC-9 claim explicitly: adding a room does not touch the game loop.
  - **`AGENTS.md`'s "Things to Avoid".** Add whatever Phase 1 established as a rule — at minimum: do not hardcode room text in `screens/`, and do not edit the resolver to accommodate a specific room.
  - **`SUGGEST.md` §0.** Rewrite it to describe the state as it is now: what exists, what the slice covers, and what is genuinely deferred. §0 must not claim the later sections are implemented.
  - **The phase naming collision.** `docs/PHASE1_SAVE_SETTINGS.md`, `docs/PHASE2/`, and `docs/PHASE1/` now use "phase" for two different things. Every document that refers to a phase must make clear which sense it means, or the next plan will be built on the wrong one.
  - **The test command.** If a test suite exists, the documents must say how to run it. If one does not, do not claim one.
- **Verification discipline:** every factual claim added must be checked against a file. A doc-sync that introduces a new false claim is worse than the stale docs it replaced.

## Preconditions
- [ ] E04 DONE — the checklist has been run, so the documented behavior is the verified behavior
- [ ] The full test suite passes, or its failures are recorded and are *not* documented as passing
- [ ] A02 DONE — the `settings_manager.py` question is settled one way or the other
- [ ] GP-2 resolved — the documents can state the real test command, or explicitly state there is none

## Actionable Steps
1. Record a baseline: list every factual claim in the four documents that the repo currently contradicts. Do this as a written list before editing, so the sync has a definition of done of its own.
2. Read the repo's real state — tree, bindings, content files, dependency file, tests — and let the documents follow it.
3. Update the structure diagrams in `AGENTS.md`, `README.md`, and `docs/GENERAL_DOC.md`.
4. Update the controls tables to include the gameplay, death, and ending screens' keys.
5. Update the run and install instructions, including the test command.
6. Rewrite `AGENTS.md`'s "Common Tasks" and "Things to Avoid" for the real workflow, including the content-only claim from AC-9.
7. Rewrite `SUGGEST.md` §0 to describe the current state, leaving §1–§14 untouched and clearly framed as proposals.
8. Disambiguate the phase naming everywhere it appears in the four documents.
9. Re-read the documents against the checklist's findings and confirm no line describes behavior that failed the playtest — if a checklist line failed, the docs must not claim it works.
10. Verify by a fresh reader's test: hand the four documents to someone who has not seen the repo and ask them to name the files in `screens/` and the keys used in game — if they cannot, the sync is incomplete.

## Test Plan
- **Commands:** none required for the docs themselves, but the documented commands must be *executed* to prove they work: the install steps, the run command, and the test command, each run as written from a clean checkout.
- **Expected:** every command in the documents runs as written and produces the documented result; no diagram shows a file that does not exist and no file that exists is missing from the diagram.
- **Contradiction sweep:** for each of the four documents, confirm that no remaining sentence describes the pre-Phase-1 state — no empty stubs, no "currently stubbed" remarks, no menu-options-in-`index.py` guidance.
- **Fresh-reader check:** the reader test in step 10, with the result recorded.
- **Reviewability check:** confirm the diff contains no unrelated reformatting or whitespace churn.

## Definition of Done / Acceptance Criteria
- [ ] Every structure diagram matches the real tree, with no missing or invented files
- [ ] Every controls table matches the real bindings, including the gameplay, death, and ending screens
- [ ] The install, run, and test commands run as written from a clean checkout
- [ ] `AGENTS.md`'s "Common Tasks" and "Things to Avoid" describe the real workflow and state the content-only rule
- [ ] `SUGGEST.md` §0 describes the current state; §1–§14 remain proposals and are not claimed as delivered
- [ ] The two senses of "phase" are disambiguated wherever the four documents use the word
- [ ] No document claims behavior that failed the E04 playtest
- [ ] No pre-Phase-1 staleness remains (empty stubs, "currently stubbed", menu-options guidance)
- [ ] The fresh-reader check has been performed and its result recorded
- [ ] The diff contains no unrelated reformatting
- [ ] No source file changed by this task

## Rollback / Undo
Revert this task's commit. All four documents return to their pre-sync text; the repo is unaffected. Note that reverting reinstates the stale claims, so revert only if the sync itself introduced an inaccuracy.

## Execution Log
<!-- Filled during execution: date, who/what agent, branch, commit hash, notes, deviations; record the baseline contradiction list and the fresh-reader check result here -->
