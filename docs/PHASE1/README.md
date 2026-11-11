# Phase 1 — Vertical Slice: Task Index

> [!WARNING]
> **SUPERSEDED BY PHASE 2:** The tasks in this directory were superseded and completed within **[Phase 2 — The House](../PHASE2/README.md)** (Slice A: Completing the Foundation, tasks `A01`–`A14`). This directory is retained as a historical planning record only. Please consult [`docs/PHASE2/`](../PHASE2/README.md) for all live tasks and active execution records.

Master plan: [`EPIC_Phase1_VerticalSlice_PLAN.md`](EPIC_Phase1_VerticalSlice_PLAN.md) (Historical)
Blueprint: [`../SUGGEST.md`](../SUGGEST.md) §12

**26 tasks · ~66.5 h · critical path ≈ 20 tasks / ≈ 51 h**

> **Read the Epic's Assumptions first.** ASM-1 in particular: this plan implements SUGGEST.md's
> *vertical slice*, which is a different thing from `docs/PHASE1_SAVE_SETTINGS.md` (settings
> persistence, already implemented).

## Reading Order

1. `EPIC_Phase1_VerticalSlice_PLAN.md` — Assumptions, Global Prerequisites, MVP cut, Handoff to Phase 2
2. `TASK_A01_INFRA` … `TASK_A06_TEST` — the foundation everything else builds on
3. Whatever slice you're executing

## Status Legend

`TODO` · `IN_PROGRESS` · `BLOCKED` · `IN_REVIEW` · `DONE` · `CANCELLED`

## Slice A — Prerequisites & Foundation (6)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [A01](TASK_A01_INFRA.md) | Move main menu into `screens/main_menu.py` | 2h | GP-1..GP-6 | TODO |
| [A02](TASK_A02_INFRA.md) | Resolve the empty `settings_manager.py` stub; sync docs | 2h | A01 | TODO |
| [A03](TASK_A03_SVC.md) | Minimal run state | 2.5h | A02 | TODO |
| [A04](TASK_A04_SVC.md) | Content record format and validator | 3h | A03 | TODO |
| [A05](TASK_A05_SVC.md) | Effect and requirement resolver | 3h | A03, A04 | TODO |
| [A06](TASK_A06_TEST.md) | Foundation unit tests | 2.5h | A03, A04, A05 | TODO |

## Slice B — The Screen (5)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [B01](TASK_B01_UI.md) | Gameplay screen skeleton, three zones | 3h | A05 | TODO |
| [B02](TASK_B02_UI.md) | Render a room from content | 3h | B01 | TODO |
| [B03](TASK_B03_UI.md) | Selectable choices and room transition | 3h | B02 | TODO |
| [B04](TASK_B04_UI.md) | Status zone: lantern bar, turn counter, low-oil warning | 2.5h | B01 | TODO |
| [B05](TASK_B05_TEST.md) | Screen tests and the content-only proof | 2.5h | B03, B04 | TODO |

## Slice C — The Cost (3)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [C01](TASK_C01_SVC.md) | Lantern drain rules | 3h | B03 | TODO |
| [C02](TASK_C02_SVC.md) | Zero-oil condition and its honest consequence | 2.5h | C01 | TODO |
| [C03](TASK_C03_TEST.md) | Lantern rule tests | 2.5h | C02 | TODO |

## Slice D — The Two Rooms (6)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [D01](TASK_D01_SVC.md) | THE HALL content: hub, left doorway, front door | 3h | C03, B05 | TODO |
| [D02](TASK_D02_SVC.md) | OLD LIBRARY content: the BOOK, the shelf, the watching | 3h | C03, B05 | TODO |
| [D03](TASK_D03_SVC.md) | The BOOK: a costly read that grants knowledge | 2.5h | D02 | TODO |
| [D04](TASK_D04_SVC.md) | One honest death at the left doorway | 3h | D01 | TODO |
| [D05](TASK_D05_SVC.md) | One honest ending at the front door | 2.5h | D03, D04 | TODO |
| [D06](TASK_D06_TEST.md) | Content validation and both terminal paths reachable | 3h | D05 | TODO |

## Slice E — Honest Endings on Screen (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [E01](TASK_E01_UI.md) | Death screen: cause, retry, back to menu | 2.5h | D04 | TODO |
| [E02](TASK_E02_UI.md) | Ending screen | 2h | D05 | TODO |
| [E03](TASK_E03_UI.md) | Wire `START GAME` and the run lifecycle | 2h | E01, E02 | TODO |
| [E04](TASK_E04_TEST.md) | End-to-end playtest checklist, incl. the stranger test | 2h | E03 | TODO |

## Slice F — Truth & Polish (optional) (2)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [F01](TASK_F01_DOCS.md) | Re-sync `AGENTS.md`, `README.md`, `GENERAL_DOC.md`, `SUGGEST.md` §0 | 1.5h | E04 | TODO |
| [F02](TASK_F02_UI.md) | Typewriter prose reveal (§7.2) | 2.5h | B02 | TODO |

## Deliberately Not In This Phase

Per `../SUGGEST.md` §12, Phase 1 is two rooms only. Deferred:

- BLOOD KITCHEN and OLD YARD as real rooms (§6) — Phase 2
- Six-slot inventory (§3.3), composure (§3.2), the journal (§3.4) — Phase 2
- The Hell Dog as a four-solution puzzle (§4.3) — Phase 2
- Difficulty, Sound, and Music affecting behavior (§5.1–5.3) — Phase 2
- Save and load a run (§9.1) — Phase 2
- Multiple endings, the Shadow as a pursuing entity, memory fragments — Phase 3
- The seven new rooms in §6 — Phase 3+
- The full accessibility pass (§8) — Phase 4
