# EPIC: Phase 1 — Vertical Slice

> [!WARNING]
> **SUPERSEDED BY PHASE 2:** This epic and its tasks were superseded and delivered in **[Phase 2 — The House](../PHASE2/EPIC_Phase2_TheHouse_PLAN.md)** (Slice A: Completing the Foundation). This file is retained as an archive of the Phase 1 planning baseline.

- **Status:** SUPERSEDED (Delivered in Phase 2 Slice A)
- **Blueprint:** `docs/SUGGEST.md` §12 "Phase 1 — Vertical Slice" (source), supported by §3.1, §3.5, §4.1, §4.2, §6, §7.1, §7.4, §11, §13
- **Size class:** M
- **Epic branch:** `feature/phase1-vertical-slice` (to be created from `develop`) — **not yet authorized**
- **Owner:** Mojtaba zamani
- **Planning date:** 2026-11-08
- **Task folder:** `docs/PHASE1/` (Superseded by `docs/PHASE2/`)

---

## Executive Summary

Phase 1 builds the smallest complete game: two rooms, one item, one real cost, one honest death, one honest ending — playable end to end. Its purpose is not content volume but **proof of the architecture**: after this phase, adding a room is writing content data, never touching the game loop (SUGGEST.md §11). Equally, it proves the design: that a costed choice with two telegraphs is more frightening than the baseline's unwarned coin flip (§4.1), demonstrated in the smallest scope that can demonstrate it.

The phase's own success test is behavioural, not technical: **a stranger plays it twice in a row without being asked** (§12).

---

## Architectural Impact

| Layer                        | Impact                                                                                                      |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Entry / shell**            | `index.py` — menu logic extracted to a screen (A01); `START GAME` launches a real run (E03)                 |
| **Screens (**`screens/`**)** | New `game.py` (B01–B04), new `death.py` and `ending.py` (E01, E02), `main_menu.py` becomes real (A01)       |
| **Game logic (**`game/`**)** | New `state.py` (A03), `content_schema.py` (A04), `effects.py` (A05), `lantern.py` (C01, C02)                |
| **Content (data)**           | New content records for THE HALL and THE OLD LIBRARY, the BOOK, the telegraphed death, the ending (Slice D) |
| **Docs**                     | `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, and `docs/SUGGEST.md` §0 re-synced to reality (A02, F01)   |
| **Persistence**              | None. Phase 1 does not save a run; `settings.json` continues untouched.                                     |

---

## Assumptions & Gaps

| ID | Assumption / gap | Confirm with |
|---|---|---|
| **ASM-1** | **"PHASE1" here means SUGGEST.md §12's Phase 1 — the vertical slice.** Note the repo's naming collision: `docs/PHASE1_SAVE_SETTINGS.md` is a *different* phase (settings persistence), which is already implemented in `config.py`. If the user meant something else, this entire plan is misdirected. | Owner |
| **ASM-2** | **No gameplay exists yet.** Verified: the only screens are `MainMenuScreen`-in-`index.py` and `SettingsScreen`; `START GAME` only updates a status label. Phase 1 is therefore greenfield gameplay. | Owner |
| **ASM-3** | **The "one honest death" lives at the HALL's left doorway**, not in a built room. §12 limits Phase 1 to the HALL and the OLD LIBRARY, so the kitchen is a *threshold* where a telegraphed death occurs, not a room. Phase 2 builds BLOOD KITCHEN as a real trade room (§6). | Owner |
| **ASM-4** | **The "one honest ending" is the HALL's front door yielding once the BOOK's knowledge is held.** This reuses both Phase 1 rooms, makes the second visit to the HALL meaningful (design pillar 3, "choices echo"), and matches §6's front-door note. | Owner |
| **ASM-5** | **The BOOK is a single high-oil-cost action that grants a knowledge flag** — *not* §6's three-consecutive-turn read. The three-turn version needs multi-turn action machinery and is listed as a Phase 2 upgrade of the LIBRARY. §12's Phase 1 wording is "the BOOK and one real cost (oil)", which this satisfies. | Owner |
| **ASM-6** | **No inventory system.** Phase 1 tracks held items as a simple set. The six-slot inventory from §3.3 belongs to Phase 2. | Owner |
| **ASM-7** | **The baseline's letter-typing is not preserved as the primary input.** §13 calls typed input "input friction" and requires selectable options; a mistyped key must never be a death. | Owner |
| **ASM-8** | **No test framework exists** (no `tests/`, `pytest.ini`, `pyproject.toml`, or `requirements.txt`). Prerequisite GP-2 chooses one; all `_TEST` tasks assume pytest. | Owner |
| **ASM-9** | Content is stored as **JSON data files**, matching the existing `settings.json` precedent. Settled in A04; if A04 decides otherwise, A05, B02, and Slice D change shape. | Owner |
| **ASM-10** | `game/settings_manager.py` is an **empty stub** while `config.py` holds the real `SettingsManager`. A02 resolves this; the plan assumes the resolution is "delete the stub" or "re-export", not a rewrite. | Owner |
| **ASM-11** | Work happens on the current branch `feature/use-settings-into-game` or a new `feature/phase1-vertical-slice`. **Git actions are not yet authorized.** | Owner |

---

## Global Prerequisites

| ID | Prerequisite | Blocks |
|---|---|---|
| **GP-1** | Confirm **ASM-1** — that this plan means SUGGEST.md's vertical slice and not the settings-persistence phase | Everything |
| **GP-2** | Choose and install a test framework (pytest recommended); add a `requirements.txt` (textual, pytest) and a `tests/` root; prove the suite runs green before any task | A06, B05, C03, D06, E04 |
| **GP-3** | Decide the **git policy**: branch name, whether per-task commits are permitted | A01 onward |
| **GP-4** | Settle the content storage format (JSON vs Python modules) — settled inside A04 | A04 onward |
| **GP-5** | Confirm the **ASM-3/ASM-4/ASM-5** scope calls (death at the threshold, ending at the front door, BOOK as a single costly read) | Slice D |
| **GP-6** | Confirm **ASM-7** — that selectable choices replace typed letters, so the baseline's exact input behavior is intentionally not preserved | B03 |

---

## Vertical Slices

| Slice | Delivers | Depends on | Ships alone? |
|---|---|---|---|
| **A — Prerequisites & Foundation** | Repo truth, run state, content-as-data format, effect resolver | GP-1..GP-6 | Yes — logic proven by tests, no UI |
| **B — The Screen** | Gameplay screen with the three zones, rendering rooms from content, selectable choices | A | Yes — a walkable placeholder room |
| **C — The Cost** | Oil drain, the lantern bar, the turn counter, the zero-oil condition | B | Yes — the run has a clock |
| **D — The Two Rooms** | HALL, OLD LIBRARY, the BOOK, one telegraphed death, one reachable ending | C | Yes — a complete playable loop |
| **E — Honest Endings on Screen** | Death screen, ending screen, run lifecycle wired to the menu | D | Yes — the game is finished for a first-time player |
| **F — Truth & Polish (optional)** | Docs re-synced; typewriter prose reveal | E | Yes — both are additive |

---

## Sub-Task Directory

### Slice A — Prerequisites & Foundation — 6 tasks, ~15h

- [ ] `TASK_A01_INFRA` — Move main menu logic into `screens/main_menu.py` (~2h) — depends GP-1..GP-6
- [ ] `TASK_A02_INFRA` — Resolve the empty `game/settings_manager.py` stub; sync structure docs (~2h) — depends A01
- [ ] `TASK_A03_SVC` — Minimal run state (~2.5h) — depends A02
- [ ] `TASK_A04_SVC` — Content record format and validator (~3h) — depends A03
- [ ] `TASK_A05_SVC` — Effect and requirement resolver (~3h) — depends A03, A04
- [ ] `TASK_A06_TEST` — Foundation unit tests (~2.5h) — depends A03, A04, A05

### Slice B — The Screen — 5 tasks, ~14h

- [ ] `TASK_B01_UI` — Gameplay screen skeleton with the three zones (~3h) — depends A05
- [ ] `TASK_B02_UI` — Render a room from content (~3h) — depends B01
- [ ] `TASK_B03_UI` — Selectable choices and room transition (~3h) — depends B02
- [ ] `TASK_B04_UI` — Status zone: lantern bar, turn counter, low-oil warning (~2.5h) — depends B01
- [ ] `TASK_B05_TEST` — Screen tests and the content-only proof (~2.5h) — depends B03, B04

### Slice C — The Cost — 3 tasks, ~8h

- [ ] `TASK_C01_SVC` — Lantern drain rules (~3h) — depends B03
- [ ] `TASK_C02_SVC` — Zero-oil condition and its honest consequence (~2.5h) — depends C01
- [ ] `TASK_C03_TEST` — Lantern rule tests (~2.5h) — depends C02

### Slice D — The Two Rooms — 6 tasks, ~17h

- [ ] `TASK_D01_SVC` — THE HALL content: hub, left doorway, front door (~3h) — depends C03, B05
- [ ] `TASK_D02_SVC` — OLD LIBRARY content: the BOOK, the shelf, the watching (~3h) — depends C03, B05
- [ ] `TASK_D03_SVC` — The BOOK: a costly read that grants knowledge (~2.5h) — depends D02
- [ ] `TASK_D04_SVC` — One honest death at the left doorway (~3h) — depends D01
- [ ] `TASK_D05_SVC` — One honest ending at the front door (~2.5h) — depends D03, D04
- [ ] `TASK_D06_TEST` — Content validation and both terminal paths reachable (~3h) — depends D05

### Slice E — Honest Endings on Screen — 4 tasks, ~8.5h

- [ ] `TASK_E01_UI` — Death screen: cause, retry, back to menu (~2.5h) — depends D04
- [ ] `TASK_E02_UI` — Ending screen (~2h) — depends D05
- [ ] `TASK_E03_UI` — Wire `START GAME` and the run lifecycle (~2h) — depends E01, E02
- [ ] `TASK_E04_TEST` — End-to-end playtest checklist, including §12's stranger test (~2h) — depends E03

### Slice F — Truth & Polish (optional) — 2 tasks, ~4h

- [ ] `TASK_F01_DOCS` — Re-sync `AGENTS.md`, `README.md`, `GENERAL_DOC.md`, and `SUGGEST.md` §0 (~1.5h) — depends E04
- [ ] `TASK_F02_UI` — Typewriter prose reveal, §7.2 (~2.5h) — depends B02

**Totals: 26 tasks, ~66.5 h**

---

## Dependency Graph

Read `X → Y` as "X must be DONE before Y starts".

```text
GP-1..GP-6 → A01 → A02 → A03 → A04 → A05 → A06
A05 → B01 → B02 → B03 → C01 → C02 → C03
B01 → B04 → B05            (B04 parallel with B02/B03)
B03 + B04 → B05
C03 + B05 → D01, D02        (D01 and D02 parallel)
D02 → D03
D01 → D04
D03 + D04 → D05 → D06
D04 → E01
D05 → E02
E01 + E02 → E03 → E04 → F01
B02 → F02
```

**Parallelization notes:** D01 (HALL) and D02 (LIBRARY) are independent once C03 and B05 land. B04 can proceed alongside B02/B03. E01 and E02 are independent of each other. Slice F may be skipped entirely without affecting anything — but F01 is recommended, because leaving the docs describing a game that doesn't exist is the exact "settings that lie" problem §13 warns about.

---

## Critical Path & MVP Cut

**Critical path (longest chain):**
`A01 → A02 → A03 → A04 → A05 → A06 → B01 → B02 → B03 → C01 → C02 → C03 → D01 → D02 → D03 → D05 → D06 → E02 → E03 → E04`
≈ 20 tasks, ≈ 51 h.

**MVP cut:** everything except Slice F. Phase 1 is not done until E04's playtest checklist passes, because §12 defines the phase by its success test — a stranger playing twice — not by the code existing.

---

## Acceptance Criteria Coverage Matrix

AC-1..AC-7 come from §12's Phase 1 bullets; AC-8..AC-12 are derived from the source rules §12 implies.

| AC | Criterion (source) | Covered by |
|---|---|---|
| **AC-1** | A gameplay screen with scene panel, status panel, and prompt line (§7.1) | B01, B02, B03, B04 |
| **AC-2** | THE HALL and THE OLD LIBRARY are playable and content-driven | D01, D02, D06 |
| **AC-3** | The BOOK exists and changes what the player can do | D03, D05 |
| **AC-4** | Oil is a real, felt cost | C01, C02, C03 |
| **AC-5** | A lantern bar and a turn counter are visible | B04, C03 |
| **AC-6** | One honest death, telegraphed at least twice, ends the run properly | D04, E01, E04 |
| **AC-7** | One honest ending the player can reach | D05, E02, E04 |
| **AC-8** | Choices are selectable; typing is never required (§13) | B03, B05 |
| **AC-9** | Adding a room is content-only, with no game-loop change (§11) | A04, A05, B02, B05 |
| **AC-10** | The repo matches its documented structure; no empty stubs remain (§11) | A01, A02 |
| **AC-11** | No text walls; a room fits one screen (§13) | D01, D02, D06 |
| **AC-12** | A stranger plays twice in a row without being asked (§12) | E04, F01 |

**Coverage check:** every AC maps to at least one task; every task cites at least one AC. ✔

---

## Risks & Spikes

| ID | Risk | Mitigation |
|---|---|---|
| **RISK-1** | **The plan targets the wrong "PHASE1"** (settings-persistence vs vertical slice) | GP-1 must be answered before A01 |
| **RISK-2** | The vertical slice quietly becomes a game-building exercise and Phase 1 never ends | The MVP cut is fixed above; content beyond two rooms is Phase 2 by definition |
| **RISK-3** | The content format (ASM-9) is chosen late and invalidates Slice D | A04 sits early on the critical path and freezes the format before any room is written |
| **RISK-4** | Prose volume outruns the estimates — Slice D is writing, not coding | Each D task names its room and its word budget; split a room's prose into its own task if it exceeds 3h |
| **RISK-5** | The "honest death" is not actually honest — the telegraphs are too subtle to notice | D04 requires two *distinct* telegraphs, and E04's checklist verifies a first-time player reports having been warned |
| **RISK-6** | Content-driven rendering is claimed but the screen ends up hardcoding a room | B05's content-only proof is a hard acceptance criterion, not a nicety |
| **RISK-7** | Working tree was reset mid-planning last session and untracked work was lost | Commit planning docs as soon as they are approved (GP-3) |

**Spikes:** none standalone. The one real unknown — content format — is a **time-boxed 30-minute decision inside A04**, since proving it costs one sample room.

---

## Definition of Done (Epic level)

- [ ] All 26 tasks DONE, or explicitly deferred with owner approval
- [ ] All ACs (AC-1..AC-12) verified by playing the game, not by inspection
- [ ] **§12's success test passes: a stranger plays twice in a row without being asked** (AC-12)
- [ ] A first-time player who dies can say *why* they died and what they'd do differently (pillar 2)
- [ ] The content-only proof holds: a new room can be added by editing content alone (AC-9)
- [ ] No hardcoded room text remains in `screens/`
- [ ] `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, and `docs/SUGGEST.md` §0 describe the real state
- [ ] No empty stubs remain anywhere in `screens/` or `game/`
- [ ] Rollback documented: reverting the epic branch returns the project to the pre-Phase-1 state; no data migration exists
- [ ] Epic branch merged per project policy **after explicit approval**

---

## Handoff to Phase 2

Phase 2 — The House (SUGGEST.md §12) assumes this foundation exists. Specifically it inherits: the run-state object (A03), the content format and validator (A04), the resolver (A05), the gameplay screen (B01–B03), and the lantern rules (C01–C02). Phase 2 then adds the six-slot inventory (§3.3), composure (§3.2), the journal (§3.4), the BLOOD KITCHEN trade room and the OLD YARD, the four-solution Hell Dog, difficulty behavior (§5.1), the death screen's "what you learned" line (§9.2), and save/load (§9.1).

**Phase 2's plan should not re-create anything in Slice A or B of this plan.** When Phase 2 is planned, it must be written against the real artifacts this phase produced.

---

## Git Policy (to be confirmed — GP-3)

| Question | Default proposed |
|---|---|
| May I create branches? | `feature/phase1-vertical-slice` from `develop` |
| May I commit per task? | Yes, one commit per task, Conventional Commits |
| May I push / open a PR / merge? | **No — separate approval every time** |
| Commit trailer | `Task: <ID>` + `Epic: Phase 1 — Vertical Slice` |

Commits are **not authorized** until the owner answers. Note RISK-7: planning docs that stay uncommitted can be lost.

---

## Change Log

| Date | Reason | Change |
|---|---|---|
| 2026-11-08 | Initial planning | Epic created; 26 tasks across 6 slices. Phase 2's earlier draft was discarded with the working tree before this plan was written, so no reconciliation with it is needed — but see "Handoff to Phase 2". |
| 2026-11-08 | A02 execution | Chose option (a): deleted the empty `game/settings_manager.py` stub; `SettingsManager` remains in `config.py`. Docs updated to match. |
| 2026-11-08 | A04 execution | Content format: JSON-compatible records in JSON files. Defined `game/content_schema.py` with room/choice/effect/requirement/tier/telegraph validator. |
