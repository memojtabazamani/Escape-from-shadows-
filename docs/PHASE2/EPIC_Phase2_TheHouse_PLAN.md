# EPIC: Phase 2 — The House

- **Status:** PLANNING
- **Blueprint:** `docs/SUGGEST.md` §12 "Phase 2 — The House" (source), supported by §2.1, §3.1–3.5, §4.1–4.3, §5.1–5.3, §6, §7.1–7.2, §9.1–9.2, §11, §13
- **Size class:** L
- **Epic branch:** `feature/phase_2_the_house` (already exists, currently checked out) — **git actions not yet authorized**
- **Owner:** Mojtaba zamani
- **Planning date:** 2026-11-09
- **Task folder:** `docs/PHASE2/`
- **Predecessor:** [`../PHASE1/EPIC_Phase1_VerticalSlice_PLAN.md`](../PHASE1/EPIC_Phase1_VerticalSlice_PLAN.md)

---

## Executive Summary

Phase 2 turns the vertical slice into **the house**. All four baseline rooms become real rooms with real costs (§6); the three settings that currently change nothing become the game's mercy system (§5); and the baseline's coin-flip Hell Dog becomes a four-solution puzzle the player can reason about (§4.3). The phase adds the three state systems the design leans on — six-slot inventory (§3.3), composure (§3.2), and the journal (§3.4) — plus save/load (§9.1) and a death screen that teaches instead of just stopping (§9.2).

**Critical structural finding (verified 2026-11-09):** Phase 1 was executed only through **Slice A**. `game/state.py`, `game/effects.py`, `game/content_schema.py`, and `tests/` exist; the gameplay screen, lantern rules, room content, and the death/ending screens **do not**. `START GAME` still only prints a status line. Phase 2 sits entirely on top of that unbuilt loop, so **Slice A of this plan completes Phase 1's loop** before any Phase 2 feature begins. The owner confirmed this approach on 2026-11-09.

The phase's own success test is behavioural: **a player who dies can say why they died, and reaches for the cleaver, the whistle, or the book on purpose next run** — not by luck.

---

## Architectural Impact

| Layer | Impact |
| --- | --- |
| **Entry / shell** | `index.py` — `START GAME` launches a real run and the menu gains a working "CONTINUE" (A12, I02) |
| **Screens (`screens/`)** | New `game.py` (A01–A04), `death.py`, `ending.py` (A11), `journal.py` (E03); `game.py` gains composure/inventory zones (D04, C04) and a journal overlay (E03) |
| **Game logic (`game/`)** | New `lantern.py` (A05, A06), `difficulty.py` (B01–B04), `inventory.py` (C01–C03), `composure.py` (D01–D03), `journal.py` (E01, E02), `multiturn.py` (F01), `save.py` (I01, I02) |
| **Engine contracts** | `game/effects.py` and `game/content_schema.py` gain new verbs/predicates (C02, D01, F01); the validator gains rules for the six-slot cap, the four dog solutions, and per-room prose length (F08) |
| **Content (data)** | New content set for THE HALL, BLOOD KITCHEN, OLD LIBRARY, OLD YARD, the items of §3.3, the four dog solutions, three key routes, and five terminal states (Slices A, F, G) |
| **Settings** | `config.py` values finally have consumers: `difficulty` (Slice B), `sound` → system bell (H01), `music` → visual rhythm (H02, H03) |
| **Persistence** | New single-slot save file, built on the `RunState.snapshot()`/`restore()` contract `game/state.py` already exposes (I01, I02) |
| **Docs** | `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, `docs/SUGGEST.md` §0 re-synced (A14); `docs/PHASE1/` marked superseded where Slice A replaces it (A14) |

---

## Assumptions & Gaps

| ID | Assumption / gap | Confirm with |
| --- | --- | --- |
| **ASM-1** | **Phase 1's Slices B–F are unbuilt.** Verified 2026-11-09: no `screens/game.py`, no `game/lantern.py`, no content files, no `death.py`/`ending.py`. **Confirmed by owner:** Slice A of this plan absorbs that work rather than blocking Phase 2 on it. | Owner — **confirmed** |
| **ASM-2** | Slice A re-plans Phase 1's Slice B–F work **inside `docs/PHASE2/`**; `docs/PHASE1/` is left untouched and remains the detailed precedent. Double bookkeeping is a real risk — see RISK-1. | Owner |
| **ASM-3** | **Content stays JSON-compatible records**, the format Phase 1's A04 settled in `game/content_schema.py`. Phase 2 extends the format; it does not replace it. | Owner |
| **ASM-4** | The engine's verbs today are only `spend_oil`, `grant_item`, `set_flag`, and predicates only `has_flag`, `has_item`, `lantern_above`. Phase 2 **must extend both** (composure, inventory slots, turn counters, item cap). This is planned extension, not a redesign. | Owner |
| **ASM-5** | **Six slots is a hard cap** (§3.3). A seventh item requires dropping one; the drop is a real choice, not a silent swap. | Owner |
| **ASM-6** | **Composure distortion is capped at the last 20% of the bar and always carries a tic** (italic, stutter, repeated word), per §3.2's explicit caveat. Distortion never affects the *existence* of an exit, only its description. | Owner |
| **ASM-7** | **"Sound" means the terminal system bell only** (§5.2). There is no audio pipeline; the game must be fully playable and complete with the bell off or unavailable in the host terminal. | Owner |
| **ASM-8** | **"Music" means visual rhythm**, not audio (§5.3): typewriter reveal, pulsing borders, background deepening. Music OFF produces instant text and a flat, static layout. | Owner |
| **ASM-9** | **One save slot** (§9.1). `RunState.snapshot()`/`restore()` already provide the contract; the save file wraps it with room, journal, and endings-seen. | Owner |
| **ASM-10** | **Endings in this phase are the Phase 1 set plus the terminal states the four rooms imply.** The full 5–7 ending spread and the endings gallery (§2.3, §9.4) are Phase 3. | Owner |
| **ASM-11** | **The Shadow is not a pursuing entity in Phase 2.** It may speak, taunt, and hint (§5.1 EASY hints are its taunts, §3.4 records its lines), but pursuit rules and history-drawn dialogue are Phase 3 (§2.2). | Owner |
| **ASM-12** | **Memory fragments (§2.4) are Phase 3.** The kitchen's meat does not yet hide a fragment (§4.3 option 3's parenthetical is a Phase 3 entanglement). | Owner |
| **ASM-13** | **The seven new rooms in §6** (Stairwell, Nursery, Mirror Room, Long Corridor, Cellar, Chapel, plus the Front Door as a room) are **Phase 3+**. Phase 2 reworks the four baseline rooms only; the staircase in the HALL is *described*, not walkable. | Owner |
| **ASM-14** | **Difficulty changes information and mercy, never story** (§5.1). No difficulty gates a room, an item, or a solution. HARD removes safety nets, never fairness (§5.1 caveat). | Owner |
| **ASM-15** | **Git actions are not authorized.** The branch `feature/phase_2_the_house` already exists and is checked out; see "Git Policy". | Owner |
| **ASM-16** | Accessibility beyond **text speed and reduce motion** is Phase 4 (§8), except where §5.3 delivers it for free (Music OFF *is* instant text). High contrast, colorblind glyphs, plain mode, pause-anywhere are Phase 4. | Owner |
| **ASM-17** | Only **the front door** produces an *escape* ending in Phase 2; the other terminal states are the death screen and the zero-composure walk. §2.3's ending spread is Phase 3. | Owner |
| **ASM-18** | **A room fits one screen** (§13): prose budget ≈ 20 usable lines per room, enforced by the validator (F08) rather than by hope. | Owner |

---

## Global Prerequisites

| ID | Prerequisite | Blocks |
| --- | --- | --- |
| **GP-1** | Confirm **ASM-1** — Slice A absorbs Phase 1's unbuilt Slice B–F. | Everything — **confirmed 2026-11-09** |
| **GP-2** | Prove the existing baseline is green before touching anything: `python -m pytest` in the repo root must pass the three Phase 1 test modules, and `python index.py` must start. | A01 onward |
| **GP-3** | Decide the **git policy**: whether per-task commits are permitted on `feature/phase_2_the_house`. | A01 onward |
| **GP-4** | Decide whether `docs/PHASE1/` tasks are marked **superseded** once Slice A lands, or left as historical record (RISK-1). | A14 |
| **GP-5** | Confirm the **item list is exactly** §3.3's six candidates plus the front-door key, with no additions. | Slice C, Slice F |
| **GP-6** | Confirm the **difficulty parameter table** values (the actual numbers) — the *shape* is planned in B01, the numbers need an owner decision. | B02, B03, B05 |
| **GP-7** | Confirm **ASM-11/ASM-13** — no Shadow pursuit, no new rooms in this phase. | Slices F, G |

---

## Vertical Slices

| Slice | Delivers | Depends on | Ships alone? |
| --- | --- | --- | --- |
| **A — Completing the Foundation** | The missing Phase 1 loop: gameplay screen, lantern, HALL + LIBRARY content, one death, one ending, run lifecycle, honest docs | GP-1..GP-3 | Yes — Phase 1's vertical slice finally exists |
| **B — Difficulty as a Real System** | `DifficultyConfig` seam; lantern/composure generosity, mercy knobs, hints, HARD countdowns | A | Yes — EASY and HARD measurably differ |
| **C — Inventory** | Six slots, item definitions as content, drop-to-take, inventory display | A | Yes — items are held and shown |
| **D — Composure** | The second bar: drains, capped unreliability, the zero-composure walk | A, B02 | Yes — nerve is a resource |
| **E — The Journal** | Rooms seen, deaths, the Shadow's lines; a keybound journal screen | A | Yes — death converts into retained knowledge |
| **F — The House** | The four rooms reworked per §6, multi-turn actions, refills, the three key routes | C, D, E | Yes — the house is playable and costly |
| **G — The Hell Dog** | The dog's one discoverable rule and its four solutions | F | Yes — the encounter stops being a coin flip |
| **H — Sound & Music Made Real** | The system bell as a horror channel; visual rhythm; instant-text path | A | Yes — the presentation toggles stop lying |
| **I — Persistence & Mercy** | Single-slot save/load, "CONTINUE", the death screen's teaching lines | A, B, E | Yes — a run survives a restart |

---

## Sub-Task Directory

### Slice A — Completing the Foundation — 14 tasks, ~38h

Finishes the Phase 1 loop (Phase 1's Slices B–F). Mirrors `docs/PHASE1/TASK_B01`–`F01`; this folder is the live record.

- [x] `TASK_A01_UI` — Gameplay screen skeleton with the three zones (~3h) — depends GP-2, GP-3
- [ ] `TASK_A02_UI` — Render a room from content records (~3h) — depends A01
- [ ] `TASK_A03_UI` — Selectable choices, requirement gating, room transition (~3h) — depends A02
- [ ] `TASK_A04_UI` — Status zone: lantern bar, turn counter, low-oil warning (~2.5h) — depends A01
- [ ] `TASK_A05_SVC` — Lantern drain rules (~3h) — depends A03
- [ ] `TASK_A06_SVC` — Zero-oil condition and its honest consequence (~2.5h) — depends A05
- [ ] `TASK_A07_SVC` — THE HALL content: hub, two doorways, the stuck front door (~3h) — depends A06, A04
- [ ] `TASK_A08_SVC` — OLD LIBRARY content and the BOOK's costly read (~3h) — depends A03
- [ ] `TASK_A09_SVC` — One honest death at the left doorway (~2.5h) — depends A07
- [ ] `TASK_A10_SVC` — One honest ending at the front door (~2.5h) — depends A08, A09
- [ ] `TASK_A11_UI` — Death screen and ending screen (~3.5h) — depends A09, A10
- [ ] `TASK_A12_UI` — Wire `START GAME` and the run lifecycle (~2h) — depends A11
- [ ] `TASK_A13_TEST` — Vertical-slice regression suite and the first-stranger playtest (~3h) — depends A12
- [ ] `TASK_A14_DOCS` — Re-sync `AGENTS.md`, `README.md`, `GENERAL_DOC.md`, `SUGGEST.md` §0 (~1.5h) — depends A13

### Slice B — Difficulty as a Real System — 6 tasks, ~16h

- [ ] `TASK_B01_SVC` — `DifficultyConfig`: the parameters seam (§11) (~2.5h) — depends A13
- [ ] `TASK_B02_SVC` — Lantern and composure generosity by difficulty (~2.5h) — depends B01
- [ ] `TASK_B03_SVC` — Mercy knobs: restart point and journal auto-fill (~3h) — depends B02
- [ ] `TASK_B04_SVC` — Hints: the Shadow's taunts double as hints on EASY (~2.5h) — depends B02
- [ ] `TASK_B05_UI` — HARD: choices that expire on hesitation (~3h) — depends B01
- [ ] `TASK_B06_TEST` — Difficulty behavior tests (~2.5h) — depends B03, B04, B05

### Slice C — Inventory — 5 tasks, ~14h

- [ ] `TASK_C01_SVC` — Six-slot inventory in `RunState` (~3h) — depends A13
- [ ] `TASK_C02_SVC` — Inventory requirements and effect verbs (~2.5h) — depends C01
- [ ] `TASK_C03_SVC` — Item definitions as content (§3.3) (~3h) — depends C02
- [ ] `TASK_C04_UI` — Inventory display and the drop-to-take flow (~3h) — depends C02
- [ ] `TASK_C05_TEST` — Inventory tests (~2.5h) — depends C03, C04

### Slice D — Composure — 5 tasks, ~14h

- [ ] `TASK_D01_SVC` — Composure stat, drains, and recovery (~3h) — depends A13, B02
- [ ] `TASK_D02_SVC` — Unreliable narration, capped at 20% and always signalled (~3h) — depends D01
- [ ] `TASK_D03_SVC` — Zero composure: the voluntary walk into the Shadow (~2.5h) — depends D01
- [ ] `TASK_D04_UI` — Composure bar and the distortion tic (~3h) — depends D02
- [ ] `TASK_D05_TEST` — Composure tests (~2.5h) — depends D03, D04

### Slice E — The Journal — 4 tasks, ~11h

- [ ] `TASK_E01_SVC` — Journal model: rooms, deaths, Shadow lines (~2.5h) — depends A13
- [ ] `TASK_E02_SVC` — Journal writes on room entry and on death (~3h) — depends E01, A11
- [ ] `TASK_E03_UI` — Journal screen, keybound overlay (~3h) — depends E01
- [ ] `TASK_E04_TEST` — Journal tests (~2.5h) — depends E02, E03

### Slice F — The House — 8 tasks, ~24.5h

- [ ] `TASK_F01_SVC` — Multi-turn action support in the engine (~3.5h) — depends A13
- [ ] `TASK_F02_SVC` — BLOOD KITCHEN as the trade room (§6) (~3h) — depends D05, E04
- [ ] `TASK_F03_SVC` — OLD LIBRARY rework: the three-turn read (~3h) — depends F01, C05
- [ ] `TASK_F04_SVC` — OLD YARD: rain, mud, the wall, the doghouse (§6) (~3h) — depends D05, E04
- [ ] `TASK_F05_SVC` — THE HALL rework: hub, staircase, the yielding front door (~3h) — depends F02, F03, F04
- [ ] `TASK_F06_SVC` — The front door key: three routes, two of them traps (~3h) — depends F05
- [ ] `TASK_F07_SVC` — Lantern refills and the trade structure (§3.1) (~3h) — depends F02
- [ ] `TASK_F08_TEST` — Full-house validation: prices, reachability, prose budget (~3h) — depends F06, F07

### Slice G — The Hell Dog — 4 tasks, ~11.5h

- [ ] `TASK_G01_SVC` — The dog's rule: it only moves when you do (§6) (~3h) — depends F08
- [ ] `TASK_G02_SVC` — The four solutions: slow, quick, meat, whistle (§4.3) (~3h) — depends G01
- [ ] `TASK_G03_SVC` — The whistle needs the book, and the dog comes back later (~3h) — depends G02
- [ ] `TASK_G04_TEST` — Hell Dog tests: four solutions, distinct outcomes (~2.5h) — depends G03

### Slice H — Sound & Music Made Real — 4 tasks, ~11h

- [ ] `TASK_H01_SVC` — The system bell as a horror channel (§5.2) (~3h) — depends A13
- [ ] `TASK_H02_UI` — Visual rhythm: typewriter and pulsing tied to Music (§5.3, §7.2) (~3h) — depends A02
- [ ] `TASK_H03_UI` — Instant text and reduce-motion path (§5.3, §8) (~2.5h) — depends H02
- [ ] `TASK_H04_TEST` — Presentation toggle tests (~2.5h) — depends H01, H03

### Slice I — Persistence & Mercy — 5 tasks, ~13.5h

- [ ] `TASK_I01_SVC` — Save file: serialize the run (~3h) — depends C05, D05, E04
- [ ] `TASK_I02_SVC` — Load, `CONTINUE`, and save-slot lifecycle (~3h) — depends I01
- [ ] `TASK_I03_UI` — Death screen with the "what you learned" line (§9.2) (~3h) — depends A11, E02
- [ ] `TASK_I04_UI` — Difficulty-gated "what you could have done" line (§9.2) (~2h) — depends I03, B03
- [ ] `TASK_I05_TEST` — Save/load round-trip and death-screen tests (~2.5h) — depends I02, I04

**Totals: 55 tasks, ~153.5 h**

---

## Dependency Graph

Read `X → Y` as "X must be DONE before Y starts".

```text
GP-2 + GP-3 → A01 → A02 → A03 → A05 → A06 → A07 → A09 ─┐
              A01 → A04 ─────────────────┘               │
              A03 → A08 ─────────────────────────────────┤
              A08 + A09 → A10 ───────────────────────────┤
              A09 + A10 → A11 → A12 → A13 ───────────────┴─→ (all slices below)

A13 → B01 → B02 → B03 ─┐
           B02 → B04 ───┤
           B01 → B05 ───┤
      B03 + B04 + B05 → B06

A13 → C01 → C02 → C03 ─┐
                  C04 ──┤
            C03 + C04 → C05

A13 + B02 → D01 → D02 → D04 ─┐
                 D01 → D03 ───┤
           D03 + D04 → D05

A13 → E01 → E02 ─┐
      E01 → E03 ─┤
      E02 + E03 → E04

A13 → F01 ─┐
D05 + E04 → F02, F04        (F02 and F04 parallel)
F01 + C05 → F03
F02 + F03 + F04 → F05 → F06
F02 → F07
F06 + F07 → F08

F08 → G01 → G02 → G03 → G04

A13 → H01 ─┐
A02 → H02 → H03 ─┤
      H01 + H03 → H04

C05 + D05 + E04 → I01 → I02 ─┐
A11 + E02 → I03 → I04 ───────┤
      I02 + I04 → I05
```

**Parallelization notes.** After A13 the six independent tracks (B, C, E, F01, H, and the I01 chain) can run in parallel. Within Slice F, F02 (kitchen) and F04 (yard) are independent; F03 needs F01's multi-turn machinery and C05's inventory. Slice H is fully independent of Slices C–G — it may be done first if a quick morale win is wanted, since it makes an existing menu toggle stop lying. Slice I's save task must land after the state systems it serializes (C, D, E), or the save file will need a second migration later.

---

## Critical Path & MVP Cut

**Critical path (longest chain of tasks):**

`A01 → A02 → A03 → A05 → A06 → A07 → A08 → A10 → A11 → A12 → A13 → B01 → B02 → D01 → D02 → D04 → D05 → F02 → F05 → F06 → F07 → F08 → G01 → G02 → G03 → G04`

≈ 26 tasks, ≈ 74.5 h. Slice I adds an independent ≈ 8.5 h chain (`I01 → I02 → I05`) that can run in parallel from A11 onward.

**MVP cut.** The **first releasable increment is Slice A alone**: it completes Phase 1 and produces a finished, honest two-room game. Everything after A13 is Phase 2 proper and can be sequenced by appetite. If schedule pressure appears, the recommended order is **A → F → G → B → I → C → D → E → H**: the four rooms and the dog are what §12 is *about*; inventory, composure, and the journal are the systems that make them cost something, and they land best once there is a house to spend them in.

Phase 2 is **not** done until §12's six bullets are all satisfied and AC-1..AC-24 are verified by playing, not by inspection.

---

## Acceptance Criteria Coverage Matrix

AC-1..AC-6 come from §12's Phase 2 bullets; AC-7..AC-24 are derived from the source rules §12 implies.

| AC | Criterion (source) | Covered by |
| --- | --- | --- |
| **AC-1** | All four baseline rooms exist as content, are reachable, and are playable (§6, §12) | A07, A08, F02, F03, F04, F05, F08 |
| **AC-2** | THE HALL is a hub, not a corridor; the front door is visibly stuck and yields on the third attempt (§6) | A07, F05 |
| **AC-3** | BLOOD KITCHEN is a trade room — entering costs composure, not the run (§6, §4.1) | F02 |
| **AC-4** | Reading the BOOK takes three consecutive turns with the door unwatched, and the candle burns down (§6) | A08, F01, F03 |
| **AC-5** | OLD YARD is the closest thing to outside; escape and survival read as different goals (§6) | F04 |
| **AC-6** | Six-slot inventory cap, and the cap forces a real choice (§3.3) | C01, C04, C05 |
| **AC-7** | Every §3.3 candidate item exists, is obtainable, and is tied to its room (§3.3) | C03, F02, F04, F05 |
| **AC-8** | The front door key has three routes and exactly two are traps (§3.3) | F06 |
| **AC-9** | Composure is a second bar with real drains, visible to the player (§3.2) | D01, D04, D05 |
| **AC-10** | Unreliable narration is confined to the last 20% and always carries a tic (§3.2 caveat) | D02, D04, D05 |
| **AC-11** | Zero composure does not kill — the player walks into the Shadow (§3.2) | D03, D05 |
| **AC-12** | The journal auto-records rooms seen, deaths, and lines the Shadow has said (§3.4) | E01, E02, E04 |
| **AC-13** | The Hell Dog is a four-solution puzzle, not a coin flip (§4.3, §6) | G02, G03, G04 |
| **AC-14** | The dog only moves when the player moves; standing still is safe and costs oil (§6) | G01, G04 |
| **AC-15** | The death screen states how you died and what you learned (§9.2) | A11, I03, I05 |
| **AC-16** | Difficulty changes information and mercy, never the story (§5.1) | B01, B02, B03, B04, B06 |
| **AC-17** | HARD is leaner, not cheaper: no unfairness, no unreachable content (§5.1 caveat) | B03, B06 |
| **AC-18** | Sound drives the system bell at named moments; the game is complete without it (§5.2) | H01, H04 |
| **AC-19** | Music controls text speed and visual rhythm; OFF means instant and flat (§5.3) | H02, H03, H04 |
| **AC-20** | A run can be saved and resumed; the menu's "CONTINUE" is real (§9.1) | I01, I02, I05 |
| **AC-21** | Every death in this phase carries at least two distinct telegraphs (§4.1, §13) | A09, F02, F03, F04, F08 |
| **AC-22** | Adding a room is still content-only, with no game-loop change (§11) | A02, F08 |
| **AC-23** | No text walls: every room fits one screen (§13) | A07, A08, F02, F03, F04, F08 |
| **AC-24** | No setting lies: every menu toggle changes observable behaviour (§13) | A14, B06, H04 |

**Coverage check:** every AC maps to at least one task, and every task cites at least one AC. ✔

---

## Risks & Spikes

| ID | Risk | Mitigation |
| --- | --- | --- |
| **RISK-1** | **Double bookkeeping.** Slice A duplicates Phase 1's Slice B–F on paper. Two folders describing the same work drift, and nobody knows which is live. | A14 marks `docs/PHASE1/` tasks superseded with a pointer here (GP-4). This folder is the live record from the moment it lands. |
| **RISK-2** | Slice A is 14 tasks of *unbuilt* work disguised as Phase 2 work, and the phase quietly becomes "Phase 1, again". | Slice A is a hard boundary: Slice B does not start until A13's playtest passes. The first increment is Slice A alone, and it is releasable. |
| **RISK-3** | The engine contracts (`effects.py`, `content_schema.py`) were written for two rooms and one item. Six slots, composure, multi-turn actions, and four dog solutions may not fit without a redesign. | ASM-4 flags the extension as expected. C02 and F01 are the two tasks where the fit is decided; if the format must change, trigger the Change Protocol rather than bending the design. |
| **RISK-4** | **Unreliable narration (§3.2) is the highest-variance feature in the phase** — wonderful once, infuriating when overdone. | ASM-6 caps it at 20% and mandates a tic. D02's DoD requires a signal on *every* distorted line, and D05 tests the cap. |
| **RISK-5** | Difficulty becomes a difficulty-flavoured story branch (violating §5.1) because it is easier to gate content than to tune mercy. | ASM-14 plus B06: a test asserts that the set of reachable rooms and the set of solutions are identical on EASY, MEDIUM, and HARD. |
| **RISK-6** | Prose volume outruns the estimates — Slice F is writing, not coding, and each room now has more states (distorted, low-oil, first visit, revisit). | Each F task names its room and its prose budget. Split a room's prose into its own task if it exceeds its estimate. |
| **RISK-7** | The save file is designed before the state systems exist and needs a second migration. | I01 depends on C05, D05, and E04 — the state is frozen before it is serialized. |
| **RISK-8** | The system bell (§5.2) is disabled or silent in many terminals, so the horror cue carries no information. | ASM-7 and H04: every bell moment must have a non-audio counterpart, and H04 tests the game with the bell forced off. |
| **RISK-9** | The dog's four solutions (§4.3) collapse into two because two of them lead to the same place. | G04 asserts four distinct outcomes, and §13's "choices that don't matter" pitfall is cited in G02's DoD. |
| **RISK-10** | The 20-line prose budget (ASM-18) is broken by the kitchen and the nursery-adjacent scenes. | F08's validator enforces the budget mechanically, so it fails at validation time, not in front of a player. |

**Spikes:** one, time-boxed. **The engine-contract fit (RISK-3)** deserves a 60-minute bounded investigation at the head of `TASK_C02_SVC` — extend the existing verb/predicate tables, or introduce a small condition/effect expression layer. The decision is recorded in C02 and applies to D01, F01, F06, and G02.

---

## Definition of Done (Epic level)

- [ ] All 55 tasks DONE, or explicitly deferred with owner approval
- [ ] Slice A complete: the Phase 1 vertical slice exists and its playtest passes
- [ ] All ACs (AC-1..AC-24) verified **by playing the game**, not by inspection
- [ ] All four rooms playable, each fitting one screen, each with a real cost
- [ ] The Hell Dog has four distinct, discoverable solutions, and the whistle route requires the book
- [ ] A player who dies can say *why* they died and what they'd do differently (pillar 2)
- [ ] Difficulty changes outcomes observably on all three settings, without gating any content
- [ ] Sound and Music each produce an observable difference with the toggle on and off
- [ ] The game is fully playable and complete with **both** toggles off
- [ ] A run survives quitting and relaunching
- [ ] The content-only proof still holds: a new room is added by editing content alone (AC-22)
- [ ] No hardcoded room prose remains in `screens/`
- [ ] `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, and `docs/SUGGEST.md` §0 describe the real state
- [ ] `docs/PHASE1/` no longer contradicts this plan (GP-4)
- [ ] Rollback documented: reverting the epic branch returns the project to the post-Slice-A state
- [ ] Epic branch merged per project policy **after explicit approval**

---

## Handoff to Phase 3

Phase 3 — The Shadow (§12) assumes this phase's systems exist. It inherits: the four-room house (Slice F), the six-slot inventory (C), composure and its distortion (D), the journal (E), the difficulty seam (B), and the save format (I). Phase 3 then adds the Shadow as a **pursuing entity with rules** (§2.2) — the lit-room rule, the learning pattern, second-person dialogue drawn from the player's own history — plus the 5–7 ending spread and the endings gallery (§2.3, §9.4), and the three memory fragments (§2.4).

**Phase 3's plan must not re-create anything here.** When Phase 3 is planned, it must be written against the real artifacts this phase produced — in particular the save format (which gains "endings seen") and the journal (which becomes the Shadow's memory source).

---

## Git Policy (to be confirmed — GP-3)

| Question | Default proposed |
| --- | --- |
| May I create branches? | Branch `feature/phase_2_the_house` **already exists and is checked out** — no new branch needed |
| May I commit per task? | Proposed: yes, one commit per task, Conventional Commits |
| May I push / open a PR / merge? | **No — separate approval every time** |
| Commit trailer | `Task: <ID>` + `Epic: Phase 2 — The House` |

**Commits are not authorized until the owner answers.** The working tree currently holds one unrelated pending deletion (`docs/PHASE2/PHASE2_USE_SETTINGS_INTO_GAME.md`, removed before this plan was written); it is not part of this epic and should be resolved deliberately, not swept into a task commit.

---

## Change Log

| Date | Reason | Change |
| --- | --- | --- |
| 2026-11-09 | Initial planning | Epic created: 55 tasks across 9 slices (~153.5 h). Slice A added, by owner decision, to complete the unbuilt Phase 1 loop (verified: Phase 1 executed only through Slice A). |
