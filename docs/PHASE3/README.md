# Phase 3 — The Shadow: Task Index

Master plan: [`EPIC_Phase3_TheShadow_PLAN.md`](EPIC_Phase3_TheShadow_PLAN.md)  
Blueprint: [`../SUGGEST.md`](../SUGGEST.md) §12 ("Phase 3 — The Shadow"), supported by §2.2, §2.3, §2.4, §3.1, §3.5, §7.3, §7.4, §7.5, §9.4  
Predecessor: [`../PHASE2/`](../PHASE2/README.md)

**32 tasks · ~85.5 h · critical path ≈ 16 tasks / ≈ 42.5 h**

> **Read the Epic's Assumptions first.** Phase 3 inherits a fully functional, verified 4-room manor with 263 passing tests from Phase 2. Phase 3 breathes life into the title antagonist: the Shadow becomes a stateful pursuing entity governed by light rules, its voice echoes the player's recorded run history, the 7-ending narrative spectrum unfolds alongside a permanent Endings Gallery, and the three memory fragments reward deep curiosity.

## Reading Order

1. `EPIC_Phase3_TheShadow_PLAN.md` — Executive Summary, Assumptions, Global Prerequisites, Architecture Impact, Critical Path, and Acceptance Criteria
2. `TASK_A01_SVC` … `TASK_A05_TEST` — Slice A: Meta-progression and Endings Gallery foundation
3. Whatever slice you're executing in dependency order

## Status Legend

`TODO` · `IN_PROGRESS` · `BLOCKED` · `IN_REVIEW` · `DONE` · `CANCELLED`

---

## Slice A — Meta-Progression & The Endings Gallery (5)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [A01](TASK_A01_SVC.md) | Profile persistence model (`game/profile.py`) for unlocked endings | 2.5h | GP-1, GP-2 | DONE |
| [A02](TASK_A02_SVC.md) | Endings metadata schema and registry (`game/endings.py`, `content_schema.py`) | 2.5h | A01 | DONE |
| [A03](TASK_A03_UI.md) | Endings Gallery screen (`screens/gallery.py`) with silhouettes and counts | 3.5h | A02 | DONE |
| [A04](TASK_A04_UI.md) | Wire Main Menu with `ENDINGS` / `GALLERY` navigation option | 2h | A03 | DONE |
| [A05](TASK_A05_TEST.md) | Profile persistence and Endings Gallery tests | 2.5h | A04 | DONE |

## Slice B — The Multiple Endings Spectrum (6)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [B01](TASK_B01_SVC.md) | Content authoring for the 7 canonical endings in `data/content.json` (§2.3) | 3h | A02 | DONE |
| [B02](TASK_B02_SVC.md) | Ending resolution engine (`game/ending_resolver.py`) | 3h | B01 | DONE |
| [B03](TASK_B03_UI.md) | ASCII art vignettes for all endings (§7.3) | 3h | B01 | DONE |
| [B04](TASK_B04_UI.md) | Ending screen upgrade with ASCII art, profile unlocking, and gallery link | 3h | B02, B03 | DONE |
| [B05](TASK_B05_SVC.md) | "The Long Walk" and "Stay" narrative branch integration | 2.5h | B02 | DONE |
| [B06](TASK_B06_TEST.md) | Ending resolution criteria and transition tests | 2.5h | B04, B05 | DONE |

## Slice C — The Three Memory Fragments (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [C01](TASK_C01_SVC.md) | Memory fragment item definitions and `RunState` tracking (§2.4) | 2.5h | GP-1 | TODO |
| [C02](TASK_C02_SVC.md) | House room content placement and acquisition trade-offs (§2.4, §4.3) | 3h | C01 | TODO |
| [C03](TASK_C03_SVC.md) | "Homecoming" secret ending integration and criteria validation | 2.5h | C02, B02 | TODO |
| [C04](TASK_C04_TEST.md) | Memory fragment trade-offs and Homecoming path tests | 2.5h | C03 | TODO |

## Slice D — The Shadow Pursuit Engine (5)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [D01](TASK_D01_SVC.md) | Shadow state model and pursuit state machine (`game/shadow.py`) | 3h | GP-1 | TODO |
| [D02](TASK_D02_SVC.md) | Lit-room barrier and zero-oil breach rules (§2.2, §3.1) | 2.5h | D01 | TODO |
| [D03](TASK_D03_SVC.md) | Shadow manifestation text generator: descriptions of absence (§2.2) | 3h | D01 | TODO |
| [D04](TASK_D04_SVC.md) | Shadow pursuit integration into gameplay room loop | 3h | D02, D03 | TODO |
| [D05](TASK_D05_TEST.md) | Shadow pursuit mechanics and movement rule tests | 2.5h | D04 | TODO |

## Slice E — Player History & Shadow Voice (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [E01](TASK_E01_SVC.md) | Player choice and action history tracking in `RunState` | 2.5h | GP-1 | TODO |
| [E02](TASK_E02_SVC.md) | History-driven second-person dialogue engine | 3h | E01, D01 | TODO |
| [E03](TASK_E03_SVC.md) | Shadow dialogue injection, audio whisper cue, and journal recording | 3h | E02, D04 | TODO |
| [E04](TASK_E04_TEST.md) | Player history recording and Shadow dialogue tests | 2.5h | E03 | TODO |

## Slice F — Dread Counter & Quiet Horror Presentation (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [F01](TASK_F01_SVC.md) | Dread turn thresholds (Turn 20 rhythm shift, Turn 30 proximity sentence) | 2.5h | D04 | TODO |
| [F02](TASK_F02_UI.md) | Visual grammar: strict Red color rule (`#e63946`) for Shadow presence (§7.4) | 2.5h | F01, D03 | TODO |
| [F03](TASK_F03_UI.md) | Quiet horror presentation techniques (delayed echo, missing line, patient prompt) | 3h | F02 | TODO |
| [F04](TASK_F04_TEST.md) | Dread counter thresholds and presentation rule tests | 2.5h | F03 | TODO |

## Slice G — Full Integration, Verification & Documentation (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [G01](TASK_G01_SVC.md) | Content schema validation and save backward compatibility audit | 2.5h | B06, C04, D05, E04, F04 | TODO |
| [G02](TASK_G02_TEST.md) | End-to-end regression and playthrough test suite | 3h | G01 | TODO |
| [G03](TASK_G03_DOCS.md) | Documentation synchronization (`AGENTS.md`, `README.md`, `GENERAL_DOC.md`, `SUGGEST.md` §0) | 2h | G02 | TODO |
| [G04](TASK_G04_DOCS.md) | Phase 3 completion report and Handoff to Phase 4 | 1.5h | G03 | TODO |

---

## Recommended Sequencing If Time Is Short

`A → B → C → D → E → F → G`

1. **Slice A & B (Endings & Gallery):** Delivers immediate visible replayability and meta-progression across runs.
2. **Slice C (Memory Fragments):** Adds mystery and non-mechanical curiosity exploration.
3. **Slice D & E (The Shadow & Voice):** Introduces the core antagonist, its rules, and dynamic personalized dialogue.
4. **Slice F (Dread & Atmosphere):** Polishes tension and psychological presentation.
5. **Slice G (Verification & Docs):** Guarantees zero regression and seamless handoff.

---

## Deliberately Not In This Phase

Per [`../SUGGEST.md`](../SUGGEST.md) §12, deferred to Phase 4:
- New Game Plus (§9.3)
- The seven new rooms in §6 (The Stairwell, The Nursery, The Mirror Room, The Long Corridor, The Cellar, The Chapel)
- The fantastic ideas in §10 (e.g. terminal column awareness, Shadow typing back, co-op terminal sharing, daily seeds)
- The full accessibility pass (§8) beyond text speed and reduce motion
