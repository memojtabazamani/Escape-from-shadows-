# Phase 2 — The House: Task Index

Master plan: [`EPIC_Phase2_TheHouse_PLAN.md`](EPIC_Phase2_TheHouse_PLAN.md)
Blueprint: [`../SUGGEST.md`](../SUGGEST.md) §12
Predecessor: [`../PHASE1/`](../PHASE1/)

**55 tasks · ~153.5 h · critical path ≈ 26 tasks / ≈ 74.5 h**

> **Read the Epic's Assumptions first.** ASM-1 in particular: **Phase 1 was executed only through
> Slice A** (`game/state.py`, `game/effects.py`, `game/content_schema.py`, `tests/` exist; the
> gameplay screen, lantern rules, room content, and death/ending screens do not). **Slice A of this
> plan completes that missing loop**, by owner decision, before any Phase 2 feature begins.

## Reading Order

1. `EPIC_Phase2_TheHouse_PLAN.md` — Executive Summary, Assumptions, Global Prerequisites, MVP cut, Handoff to Phase 3
2. `TASK_A01_UI` … `TASK_A14_DOCS` — Slice A: the foundation everything else builds on
3. Whatever slice you're executing

## Status Legend

`TODO` · `IN_PROGRESS` · `BLOCKED` · `IN_REVIEW` · `DONE` · `CANCELLED`

## Slice A — Completing the Foundation (14)

Completes Phase 1's unbuilt loop. Mirrors `../PHASE1/TASK_B01`–`F01`; **this folder is the live record.**

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [A01](TASK_A01_UI.md) | Gameplay screen skeleton with the three zones | 3h | GP-2, GP-3 | DONE |
| [A02](TASK_A02_UI.md) | Render a room from content records | 3h | A01 | TODO |
| [A03](TASK_A03_UI.md) | Selectable choices, requirement gating, room transition | 3h | A02 | TODO |
| [A04](TASK_A04_UI.md) | Status zone: lantern bar, turn counter, low-oil warning | 2.5h | A01 | TODO |
| [A05](TASK_A05_SVC.md) | Lantern drain rules | 3h | A03 | TODO |
| [A06](TASK_A06_SVC.md) | Zero-oil condition and its honest consequence | 2.5h | A05 | TODO |
| [A07](TASK_A07_SVC.md) | THE HALL content: hub, two doorways, the stuck front door | 3h | A06, A04 | TODO |
| [A08](TASK_A08_SVC.md) | OLD LIBRARY content and the BOOK's costly read | 3h | A03 | TODO |
| [A09](TASK_A09_SVC.md) | One honest death at the left doorway | 2.5h | A07 | TODO |
| [A10](TASK_A10_SVC.md) | One honest ending at the front door | 2.5h | A08, A09 | TODO |
| [A11](TASK_A11_UI.md) | Death screen and ending screen | 3.5h | A09, A10 | TODO |
| [A12](TASK_A12_UI.md) | Wire `START GAME` and the run lifecycle | 2h | A11 | TODO |
| [A13](TASK_A13_TEST.md) | Vertical-slice regression suite and the first-stranger playtest | 3h | A12 | TODO |
| [A14](TASK_A14_DOCS.md) | Re-sync `AGENTS.md`, `README.md`, `GENERAL_DOC.md`, `SUGGEST.md` §0 | 1.5h | A13 | TODO |

## Slice B — Difficulty as a Real System (6)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [B01](TASK_B01_SVC.md) | `DifficultyConfig`: the parameters seam (§11) | 2.5h | A13 | TODO |
| [B02](TASK_B02_SVC.md) | Lantern and composure generosity by difficulty | 2.5h | B01 | TODO |
| [B03](TASK_B03_SVC.md) | Mercy knobs: restart point and journal auto-fill | 3h | B02 | TODO |
| [B04](TASK_B04_SVC.md) | Hints: the Shadow's taunts double as hints on EASY | 2.5h | B02 | TODO |
| [B05](TASK_B05_UI.md) | HARD: choices that expire on hesitation | 3h | B01 | TODO |
| [B06](TASK_B06_TEST.md) | Difficulty behavior tests | 2.5h | B03, B04, B05 | TODO |

## Slice C — Inventory (5)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [C01](TASK_C01_SVC.md) | Six-slot inventory in `RunState` | 3h | A13 | TODO |
| [C02](TASK_C02_SVC.md) | Inventory requirements and effect verbs | 2.5h | C01 | TODO |
| [C03](TASK_C03_SVC.md) | Item definitions as content (§3.3) | 3h | C02 | TODO |
| [C04](TASK_C04_UI.md) | Inventory display and the drop-to-take flow | 3h | C02 | TODO |
| [C05](TASK_C05_TEST.md) | Inventory tests | 2.5h | C03, C04 | TODO |

## Slice D — Composure (5)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [D01](TASK_D01_SVC.md) | Composure stat, drains, and recovery | 3h | A13, B02 | TODO |
| [D02](TASK_D02_SVC.md) | Unreliable narration, capped at 20% and always signalled | 3h | D01 | TODO |
| [D03](TASK_D03_SVC.md) | Zero composure: the voluntary walk into the Shadow | 2.5h | D01 | TODO |
| [D04](TASK_D04_UI.md) | Composure bar and the distortion tic | 3h | D02 | TODO |
| [D05](TASK_D05_TEST.md) | Composure tests | 2.5h | D03, D04 | TODO |

## Slice E — The Journal (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [E01](TASK_E01_SVC.md) | Journal model: rooms, deaths, Shadow lines | 2.5h | A13 | TODO |
| [E02](TASK_E02_SVC.md) | Journal writes on room entry and on death | 3h | E01, A11 | TODO |
| [E03](TASK_E03_UI.md) | Journal screen, keybound overlay | 3h | E01 | TODO |
| [E04](TASK_E04_TEST.md) | Journal tests | 2.5h | E02, E03 | TODO |

## Slice F — The House (8)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [F01](TASK_F01_SVC.md) | Multi-turn action support in the engine | 3.5h | A13 | TODO |
| [F02](TASK_F02_SVC.md) | BLOOD KITCHEN as the trade room (§6) | 3h | D05, E04 | TODO |
| [F03](TASK_F03_SVC.md) | OLD LIBRARY rework: the three-turn read | 3h | F01, C05 | TODO |
| [F04](TASK_F04_SVC.md) | OLD YARD: rain, mud, the wall, the doghouse (§6) | 3h | D05, E04 | TODO |
| [F05](TASK_F05_SVC.md) | THE HALL rework: hub, staircase, the yielding front door | 3h | F02, F03, F04 | TODO |
| [F06](TASK_F06_SVC.md) | The front door key: three routes, two of them traps | 3h | F05 | TODO |
| [F07](TASK_F07_SVC.md) | Lantern refills and the trade structure (§3.1) | 3h | F02 | TODO |
| [F08](TASK_F08_TEST.md) | Full-house validation: prices, reachability, prose budget | 3h | F06, F07 | TODO |

## Slice G — The Hell Dog (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [G01](TASK_G01_SVC.md) | The dog's rule: it only moves when you do (§6) | 3h | F08 | TODO |
| [G02](TASK_G02_SVC.md) | The four solutions: slow, quick, meat, whistle (§4.3) | 3h | G01 | TODO |
| [G03](TASK_G03_SVC.md) | The whistle needs the book, and the dog comes back later | 3h | G02 | TODO |
| [G04](TASK_G04_TEST.md) | Hell Dog tests: four solutions, distinct outcomes | 2.5h | G03 | TODO |

## Slice H — Sound & Music Made Real (4)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [H01](TASK_H01_SVC.md) | The system bell as a horror channel (§5.2) | 3h | A13 | TODO |
| [H02](TASK_H02_UI.md) | Visual rhythm: typewriter and pulsing tied to Music | 3h | A02 | TODO |
| [H03](TASK_H03_UI.md) | Instant text and reduce-motion path (§5.3, §8) | 2.5h | H02 | TODO |
| [H04](TASK_H04_TEST.md) | Presentation toggle tests | 2.5h | H01, H03 | TODO |

## Slice I — Persistence & Mercy (5)

| Task | Title | Est. | Depends on | Status |
|---|---|---|---|---|
| [I01](TASK_I01_SVC.md) | Save file: serialize the run | 3h | C05, D05, E04 | TODO |
| [I02](TASK_I02_SVC.md) | Load, `CONTINUE`, and save-slot lifecycle | 3h | I01 | TODO |
| [I03](TASK_I03_UI.md) | Death screen with the "what you learned" line (§9.2) | 3h | A11, E02 | TODO |
| [I04](TASK_I04_UI.md) | Difficulty-gated "what you could have done" line (§9.2) | 2h | I03, B03 | TODO |
| [I05](TASK_I05_TEST.md) | Save/load round-trip and death-screen tests | 2.5h | I02, I04 | TODO |

## Recommended Sequencing If Time Is Short

`A → F → G → B → I → C → D → E → H`

The four rooms and the dog are what §12 is about. Inventory, composure, and the journal make them
cost something — and land better once there is a house to spend them in.

## Deliberately Not In This Phase

Per `../SUGGEST.md` §12, deferred to Phase 3+:

- Shadow as a pursuing entity with rules (§2.2) — Phase 3
- Shadow dialogue drawn from the player's own history (§2.2) — Phase 3
- The 5–7 ending spread and the endings gallery (§2.3, §9.4) — Phase 3
- The three memory fragments (§2.4) — Phase 3
- New Game Plus (§9.3) — Phase 4
- The seven new rooms in §6 (Stairwell, Nursery, Mirror Room, Long Corridor, Cellar, Chapel) — Phase 3+
- The fantastic ideas in §10 — Phase 4, pick 2–3
- The full accessibility pass (§8) beyond text speed and reduce motion — Phase 4

## Supersedes

Slice A of this plan supersedes Phase 1's unbuilt Slices B–F on paper. `../PHASE1/` remains the
detailed precedent; where the two disagree, **this folder wins** once `TASK_A14_DOCS` marks the
Phase 1 tasks superseded (GP-4).
