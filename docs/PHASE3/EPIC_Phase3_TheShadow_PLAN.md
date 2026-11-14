# EPIC: Phase 3 — The Shadow

- **Status:** PLANNING
- **Blueprint:** `docs/SUGGEST.md` §12 "Phase 3 — The Shadow" (source), supported by §2.2, §2.3, §2.4, §3.1, §3.5, §7.3, §7.4, §7.5, §9.4
- **Size class:** L
- **Epic branch:** `feature/phase_3_the_shadow` (already created and checked out) — **git actions not yet authorized**
- **Owner:** Mojtaba zamani
- **Planning date:** 2026-11-11
- **Task folder:** `docs/PHASE3/`
- **Predecessor:** [`../PHASE2/EPIC_Phase2_TheHouse_PLAN.md`](../PHASE2/EPIC_Phase2_TheHouse_PLAN.md)

---

## Executive Summary

Phase 3 elevates *Dark Quest: Escape from Shadows* from a survival manor puzzle into a psychological horror experience centered around its titular antagonist: **The Shadow**. 

Where Phase 2 established a mechanically sound 4-room house (Hall, Blood Kitchen, Old Library, Old Yard) with inventory, composure, persistence, difficulty mercy, and a 4-solution Hell Dog puzzle (all verified across 263 passing tests), Phase 3 makes the world reactive, haunted, and persistent across runs:
1. **The Shadow as an active pursuing entity with clear rules (§2.2):** Light is both resource and barrier—the Shadow cannot enter lit rooms, tracks the player across turns (trailing behind in the room left, stalking thresholds ahead, breaching at zero oil), and manifests strictly through descriptions of absence ("a doorway with no light behind it, a chair facing the wall"), never as a sprite.
2. **History-driven second-person dialogue (§2.2):** The Shadow watches and remembers. Its dialogue is drawn directly from the player's recorded run actions ("You took the cleaver. Your hands were shaking.", "You went left in the hall. I remember.").
3. **Multiple Endings Spread & The Endings Gallery (§2.3, §9.4):** Expands the terminal narrative into 7 distinct endings ranked by comprehension and curiosity (*The Long Walk*, *Meat and Silence*, *The Quiet Exit*, *What the Book Knew*, *The New Shadow*, *Homecoming*, *Stay*), backed by an unlocked silhouette gallery screen and cross-run meta-persistence.
4. **The Three Memory Fragments (§2.4):** A photograph, a child's drawing, and a receipt dated tomorrow. Mechanically non-functional items that reward inquisitive players with the secret *Homecoming* ending, cementing the design pillar that curiosity is a valid mechanic.
5. **Dread and Terminal Grammar (§3.5, §7.4, §7.5):** A hidden turn counter that shifts presentation at Turn 20 and adds proximity narration at Turn 30; red text restricted exclusively to Shadow presence; and subtle horror techniques (delayed echo, missing line, patient prompt).

Success test: **A returning player discovers that running away only teaches the Shadow where they are going, that dying unlocks permanent lore in their Endings Gallery, and that their past decisions are quoted back to them in the dark.**

---

## Architectural Impact

| Layer | Impact |
| --- | --- |
| **Meta-Progression & Persistence** | New `game/profile.py` for cross-run unlocked endings; updates `game/save.py` to maintain backward-compatible single-slot run saves alongside meta-profile persistence. |
| **Screens (`screens/`)** | New `screens/gallery.py` (Endings Gallery modal/screen); `screens/main_menu.py` adds `GALLERY` / `ENDINGS` menu entry; `screens/ending.py` displays per-ending ASCII art vignettes and triggers profile unlocks; `screens/game.py` incorporates Shadow proximity narration, dread rhythm, and red grammar. |
| **Game Engine (`game/`)** | New `game/shadow.py` (pursuit state machine, lit-room barrier, absence generator); new `game/ending_resolver.py` (criteria evaluator for the 7 endings); new `game/endings.py` (canonical endings registry and ASCII art assets); updates to `game/state.py` (`RunState` tracks choice history, memory fragments, and Shadow state). |
| **Engine Contracts & Schema** | `game/content_schema.py` and `game/effects.py` gain new predicates (`has_memory_fragment`, `memory_fragment_count`, `shadow_state_is`, `turn_count_above`) and new effect verbs (`advance_shadow`, `set_shadow_state`, `trigger_ending`). |
| **Content (`data/content.json`)** | Authoring of the 7 endings, memory fragment items, room trade-off choices for fragments, Shadow absence descriptions, and encounter branches. |
| **Audio & Presentation** | System bell cue `CUE_SHADOW_WHISPER` triggered during Shadow manifestations; Visual rhythm updates on Turn 20+; Red terminal text strictly applied only during Shadow encounters. |
| **Docs** | Synchronization of `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, and `docs/SUGGEST.md` §0. |

---

## Assumptions & Gaps

| ID | Assumption / Gap | Resolution & Plan |
| --- | --- | --- |
| **ASM-1** | **Phase 2 foundation is complete and rock-solid.** Verified 2026-11-11: all 263 tests pass across 55 tasks. Phase 3 builds cleanly upon `RunState`, `content_schema.py`, `effects.py`, `save.py`, `journal.py`, and `screens/game.py`. | Inherited from Phase 2; no re-engineering of existing systems. |
| **ASM-2** | **Endings persistence is separate from single-run save.** When a player wins or dies, `save.json` is purged per Phase 2 design, but unlocked endings MUST persist permanently across runs in `data/profile.json`. | Addressed in Slice A (`game/profile.py`). |
| **ASM-3** | **The Shadow is never drawn as a sprite.** Per §2.2, the Shadow is rendered strictly through eerie prose descriptions of absence and subtle environmental changes, reinforced by audio cues and red text. | Addressed in Slices D and F. |
| **ASM-4** | **Lit rooms are an impenetrable barrier.** As long as lantern > 0, the Shadow cannot directly occupy the player's room; it lurks behind in previous rooms or ahead at unlit thresholds. At lantern = 0 (zero oil), the barrier breaks and the Shadow enters. | Addressed in Slice D (`game/shadow.py`). |
| **ASM-5** | **Memory fragments do not offer survival utility.** Per §2.4, the 3 fragments (Photograph, Child's Drawing, Tomorrow's Receipt) occupy inventory slots and provide lore only, acting as the key to the secret *Homecoming* ending. | Addressed in Slice C. |
| **ASM-6** | **Red text is strictly reserved for the Shadow.** Per §7.4, `#e63946` / `[red]` appears ONLY when the Shadow is actively present or speaking to maintain intense psychological punch. | Addressed in Slice F. |
| **ASM-7** | **New rooms from §6 are deferred to Phase 4.** The 4 baseline rooms are rich enough to host Phase 3's Shadow pursuit, trade-offs, and fragments. The Stairwell, Nursery, Mirror Room, etc., remain Phase 4 scope per §12. | Confirmed per roadmap in §12. |
| **ASM-8** | **Existing save file format remains backward-compatible.** Any additions to `RunState` (choice history, memory fragments, shadow state) supply sensible defaults during JSON deserialization. | Addressed in Slice G. |

---

## Global Prerequisites

| ID | Prerequisite | Blocks |
| --- | --- | --- |
| **GP-1** | Existing test suite remains 100% green (263/263 tests passing on `feature/phase_3_the_shadow`). | All tasks |
| **GP-2** | Confirm storage strategy for cross-run meta-progression (`data/profile.json`). | Slice A |
| **GP-3** | Confirm the 7 canonical ending names and criteria match `docs/SUGGEST.md` §2.3. | Slice B |
| **GP-4** | Confirm Git policy for task commits during Phase 3. | Execution phase |

---

## Vertical Slices

| Slice | Delivers | Depends on | Ships alone? |
| --- | --- | --- | --- |
| **A — Meta-Progression & The Endings Gallery** | Cross-run profile storage, Endings Gallery screen (`screens/gallery.py`), and Main Menu wiring | GP-1, GP-2 | Yes — gallery viewable immediately |
| **B — The Multiple Endings Spectrum** | 7 canonical endings authored in content, ending resolver engine, ASCII vignettes, and ending screen update | A | Yes — all 7 endings unlockable and displayed |
| **C — The Three Memory Fragments** | 3 collectible fragments, room trade-off search choices, and *Homecoming* secret ending pathway | B02, GP-1 | Yes — curiosity gameplay active |
| **D — The Shadow Pursuit Engine** | Shadow state model, lit-room barrier, zero-oil breach rule, and room transition pursuit integration | GP-1 | Yes — Shadow actively tracks player |
| **E — Player History & Shadow Voice** | Player choice tracking in `RunState`, second-person dialogue generator, audio cues, and journal whispers | D, GP-1 | Yes — Shadow speaks player's history |
| **F — Dread Counter & Quiet Horror Presentation** | Turn 20/30 thresholds, strict red color grammar, and quiet horror techniques (delayed echo, missing line, patient prompt) | D | Yes — presentation reaches horror peak |
| **G — Full Integration, Verification & Docs** | Content schema validation, full regression test suite, and complete documentation synchronization | B, C, D, E, F | Yes — complete, tested Phase 3 package |

---

## Sub-Task Directory

### Slice A — Meta-Progression & The Endings Gallery (5 tasks, ~13h)
- [x] `TASK_A01_SVC` — Profile persistence model (`game/profile.py`) for unlocked endings (~2.5h) — depends GP-1, GP-2
- [x] `TASK_A02_SVC` — Endings metadata schema and registry (`game/endings.py`, `content_schema.py`) (~2.5h) — depends A01
- [x] `TASK_A03_UI` — Endings Gallery screen (`screens/gallery.py`) with silhouettes and counts (~3.5h) — depends A02
- [x] `TASK_A04_UI` — Wire Main Menu with `ENDINGS` / `GALLERY` navigation option (~2h) — depends A03
- [x] `TASK_A05_TEST` — Profile persistence and Endings Gallery tests (~2.5h) — depends A04

### Slice B — The Multiple Endings Spectrum (6 tasks, ~17h)
- [x] `TASK_B01_SVC` — Content authoring for the 7 canonical endings in `data/content.json` (§2.3) (~3h) — depends A02
- [x] `TASK_B02_SVC` — Ending resolution engine (`game/ending_resolver.py`) (~3h) — depends B01
- [x] `TASK_B03_UI` — ASCII art vignettes for all endings (§7.3) (~3h) — depends B01
- [x] `TASK_B04_UI` — Ending screen upgrade with ASCII art, profile unlocking, and gallery link (~3h) — depends B02, B03
- [x] `TASK_B05_SVC` — "The Long Walk" and "Stay" narrative branch integration (~2.5h) — depends B02
- [x] `TASK_B06_TEST` — Ending resolution criteria and transition tests (~2.5h) — depends B04, B05

### Slice C — The Three Memory Fragments (4 tasks, ~10.5h)
- [ ] `TASK_C01_SVC` — Memory fragment item definitions and `RunState` tracking (§2.4) (~2.5h) — depends GP-1
- [ ] `TASK_C02_SVC` — House room content placement and acquisition trade-offs (§2.4, §4.3) (~3h) — depends C01
- [ ] `TASK_C03_SVC` — "Homecoming" secret ending integration and criteria validation (~2.5h) — depends C02, B02
- [ ] `TASK_C04_TEST` — Memory fragment trade-offs and Homecoming path tests (~2.5h) — depends C03

### Slice D — The Shadow Pursuit Engine (5 tasks, ~14h)
- [ ] `TASK_D01_SVC` — Shadow state model and pursuit state machine (`game/shadow.py`) (~3h) — depends GP-1
- [ ] `TASK_D02_SVC` — Lit-room barrier and zero-oil breach rules (§2.2, §3.1) (~2.5h) — depends D01
- [ ] `TASK_D03_SVC` — Shadow manifestation text generator: descriptions of absence (§2.2) (~3h) — depends D01
- [ ] `TASK_D04_SVC` — Shadow pursuit integration into gameplay room loop (~3h) — depends D02, D03
- [ ] `TASK_D05_TEST` — Shadow pursuit mechanics and movement rule tests (~2.5h) — depends D04

### Slice E — Player History & Shadow Voice (4 tasks, ~11h)
- [ ] `TASK_E01_SVC` — Player choice and action history tracking in `RunState` (~2.5h) — depends GP-1
- [ ] `TASK_E02_SVC` — History-driven second-person dialogue engine (~3h) — depends E01, D01
- [ ] `TASK_E03_SVC` — Shadow dialogue injection, audio whisper cue, and journal recording (~3h) — depends E02, D04
- [ ] `TASK_E04_TEST` — Player history recording and Shadow dialogue tests (~2.5h) — depends E03

### Slice F — Dread Counter & Quiet Horror Presentation (4 tasks, ~10.5h)
- [ ] `TASK_F01_SVC` — Dread turn thresholds (Turn 20 rhythm shift, Turn 30 proximity sentence) (~2.5h) — depends D04
- [ ] `TASK_F02_UI` — Visual grammar: strict Red color rule (`#e63946`) for Shadow presence (§7.4) (~2.5h) — depends F01, D03
- [ ] `TASK_F03_UI` — Quiet horror presentation techniques (delayed echo, missing line, patient prompt) (~3h) — depends F02
- [ ] `TASK_F04_TEST` — Dread counter thresholds and presentation rule tests (~2.5h) — depends F03

### Slice G — Full Integration, Verification & Documentation (4 tasks, ~9.5h)
- [ ] `TASK_G01_SVC` — Content schema validation and save backward compatibility audit (~2.5h) — depends B06, C04, D05, E04, F04
- [ ] `TASK_G02_TEST` — End-to-end regression and playthrough test suite (~3h) — depends G01
- [ ] `TASK_G03_DOCS` — Documentation synchronization (`AGENTS.md`, `README.md`, `GENERAL_DOC.md`, `SUGGEST.md` §0) (~2h) — depends G02
- [ ] `TASK_G04_DOCS` — Phase 3 completion report and Handoff to Phase 4 (~1.5h) — depends G03

**Totals: 32 tasks, ~85.5 h**

---

## Dependency Graph

```text
GP-1 + GP-2 ──> A01 ──> A02 ──> A03 ──> A04 ──> A05 ─┐
                         │                           │
                         └──> B01 ──> B02 ──> B04 ──> B06 ──┐
                                │      │             │      │
                                └──> B03 ──┘         │      │
                                       │             │      │
                                       └─────────────┘      │
GP-1 ──> C01 ──> C02 ──> C03 ──> C04 ───────────────────────┤
                  │       ▲                                 │
                  └───────┼─────────────────────────────────┤
                          │                                 │
GP-1 ──> D01 ──> D02 ──> D04 ──> D05 ───────────────────────┤
          │       │       │                                 │
          └───> D03 ──────┘                                 │
                  │       │                                 │
                  │       ├──> F01 ──> F02 ──> F03 ──> F04 ─┤
                  │       │                                 │
GP-1 ──> E01 ─────┼───────┼─────────────────────────────────┤
          │       │       │                                 │
          └───> E02 ──> E03 ──> E04 ────────────────────────┤
                                                            │
                                                            ▼
                                                           G01 ──> G02 ──> G03 ──> G04
```

---

## Critical Path & MVP Cut

**Critical Path:**
`GP-1 → A01 → A02 → B01 → B02 → B04 → B06 → G01 → G02 → G03 → G04`  
*(Approx. 11 core tasks / ~31 hours to the first integrated multiple-endings build).*

Adding the Shadow Pursuit engine expands the critical path:
`GP-1 → D01 → D02 → D04 → E02 → E03 → E04 → F01 → F02 → F03 → F04 → G01 → G02 → G03 → G04`  
*(Approx. 16 tasks / ~42.5 hours for the complete Phase 3 experience).*

**MVP Cut:**
- **Increment 1 (Slices A & B):** Endings Gallery + 7 Endings content & resolution engine. Immediately playable and replayable.
- **Increment 2 (Slice C):** The 3 Memory Fragments & Homecoming ending. Deepens exploration.
- **Increment 3 (Slices D, E, F):** The Shadow entity, pursuit rules, personalized second-person dialogue, dread thresholds, and red visual grammar.
- **Increment 4 (Slice G):** Complete regression verification, validation, and documentation.

---

## Acceptance Criteria Coverage Matrix

| AC | Criterion (Source) | Covered by |
| --- | --- | --- |
| **AC-1** | Endings meta-persistence records unlocked endings permanently across runs without being deleted on victory or death (§9.4) | A01, A05, G01 |
| **AC-2** | Endings Gallery screen displays unlocked endings with vignettes and locked endings as counts and silhouettes (§9.4) | A02, A03, A05 |
| **AC-3** | Main Menu includes a working `ENDINGS` / `GALLERY` option navigating to the gallery screen (§9.4) | A04, A05 |
| **AC-4** | Seven distinct canonical endings exist in content and resolve based on run conditions (§2.3) | B01, B02, B06 |
| **AC-5** | Ending 1 (*The Long Walk*): Triggers on early death in the Hall with respectful narrative tone (§2.3) | B01, B05, B06 |
| **AC-6** | Ending 2 (*Meat and Silence*): Triggers when Hell Dog is distracted with meat and player escapes (§2.3) | B01, B02, B06 |
| **AC-7** | Ending 3 (*The Quiet Exit*): Standard front door exit with key under normal conditions (§2.3) | B01, B02, B06 |
| **AC-8** | Ending 4 (*What the Book Knew*): Escaping after having fully read The Book (§2.3) | B01, B02, B06 |
| **AC-9** | Ending 5 (*The New Shadow*): Escaping when lantern oil is exactly zero (§2.3) | B01, B02, B06 |
| **AC-10** | Ending 6 (*Homecoming*): Secret ending triggered by holding all three memory fragments (§2.3, §2.4) | C01, C03, C04 |
| **AC-11** | Ending 7 (*Stay*): Refusing to leave at the final door and embracing the house (§2.3) | B01, B05, B06 |
| **AC-12** | Every ending displays a dedicated ASCII art vignette conforming to §7.3 rarity rules | B03, B04, B06 |
| **AC-13** | Three memory fragments (Photograph, Child's Drawing, Tomorrow's Receipt) exist as non-mechanical collectibles (§2.4) | C01, C04 |
| **AC-14** | Memory fragments are placed behind deliberate exploration trade-offs in the house (§2.4, §4.3) | C02, C04 |
| **AC-15** | Shadow pursuit state machine tracks pursuit stages (trailing, stalking, flanking) across turns (§2.2) | D01, D04, D05 |
| **AC-16** | Lit-room rule enforced: Shadow cannot enter lit rooms while lantern > 0 (§2.2) | D02, D05 |
| **AC-17** | At zero oil, the Shadow breaches the room and directly reaches the player (§3.1) | D02, D05 |
| **AC-18** | Shadow manifests only through absence descriptions, never as a sprite (§2.2) | D03, D05 |
| **AC-19** | Player choice history tracks key narrative decisions (cleaver taken, book read, dog action, doorway choices) | E01, E04 |
| **AC-20** | Shadow speaks in second person drawing dialogue from the player's recorded choice history (§2.2) | E02, E04 |
| **AC-21** | Shadow dialogue events trigger audio bell cues (`CUE_SHADOW_WHISPER`) and write to Journal (§3.4, §5.2) | E03, E04 |
| **AC-22** | Dread counter shifts visual rhythm at Turn 20 and injects proximity narration at Turn 30 without numerical display (§3.5) | F01, F04 |
| **AC-23** | Red text styling (`#e63946`) is strictly restricted to Shadow presence moments (§7.4) | F02, F04 |
| **AC-24** | Quiet horror techniques (delayed echo, missing line, patient prompt) are implemented with subtle restraint (§7.5) | F03, F04 |
| **AC-25** | Content schema validator passes for all Phase 3 data and save backward compatibility is preserved (§11) | G01, G02 |
| **AC-26** | Full regression passes with 0 failures across all legacy and new test suites | G02 |

---

## Risks & Spikes

| ID | Risk | Mitigation |
| --- | --- | --- |
| **RISK-1** | **Save file vs Profile data conflict:** Purging save on victory/death might accidentally delete unlocked endings. | Separate files: `data/save.json` for active single runs, `data/profile.json` for permanent meta-progression. Tested in A05. |
| **RISK-2** | **Shadow dialogue repetition:** Dynamic dialogue might feel repetitive if player makes few distinct choices. | E02 dialogue engine provides fallback eerie reflections based on turn count and general presence if history is sparse. |
| **RISK-3** | **Unbalanced memory fragment trade-offs:** Sacrificing composure/oil/items for fragments might make survival near-impossible. | C02 carefully calibrates trade-off costs to ensure all 7 endings remain realistically achievable. |
| **RISK-4** | **Red text overuse violating §7.4:** Overusing red text degrades horror impact. | F02 enforces an architectural lint/check restricting red tags strictly to Shadow encounters. |

---

## Definition of Done (Epic Level)

- [ ] All 32 tasks DONE with clean verification and test coverage
- [ ] Endings Gallery accessible from Main Menu, showing unlocked endings and locked silhouettes
- [ ] All 7 canonical endings verified achievable and properly resolved by the engine
- [ ] Each ending displays distinct narrative prose and dedicated ASCII art vignette
- [ ] Three memory fragments obtainable via deliberate room trade-offs
- [ ] Shadow pursuit engine functions according to lit-room and zero-oil rules
- [ ] Shadow generates second-person dialogue echoing player's choice history
- [ ] Audio bell cue sounds on Shadow whispers and whispers are logged in Journal
- [ ] Dread thresholds at Turn 20 and Turn 30 work smoothly without showing numbers
- [ ] Red text is strictly restricted to Shadow presence
- [ ] Quiet horror techniques (delayed echo, missing line, patient prompt) verified
- [ ] All 263 existing tests pass plus new Phase 3 test suite
- [ ] Content schema passes and save format maintains backward compatibility
- [ ] Documentation updated: `AGENTS.md`, `README.md`, `docs/GENERAL_DOC.md`, `docs/SUGGEST.md` §0

---

## Handoff to Phase 4

Phase 4 ("The Fantastic", per `docs/SUGGEST.md` §12) inherits the living, haunted manor with its persistent Shadow antagonist and multi-ending structure. Phase 4 will build on this by introducing:
- New Game Plus (§9.3): Shadow dialog referencing previous completed endings, dog recognizing player
- Selected Fantastic Ideas from §10 (e.g. Terminal column awareness, Shadow typing back, daily seed)
- Full accessibility pass (§8) beyond text speed and reduce motion

---

## Git Policy (to be confirmed)

| Question | Proposed Setting |
| --- | --- |
| Branch | `feature/phase_3_the_shadow` (already created and checked out) |
| Commits | One commit per task, Conventional Commits format |
| Push / PR / Merge | Separate user approval required before any push or merge |
| Trailer | `Task: <ID>` + `Epic: Phase 3 — The Shadow` |

---

## Change Log

| Date | Reason | Change |
| --- | --- | --- |
| 2026-11-11 | Initial planning | Created Epic plan with 32 atomic tasks across 7 vertical slices (~85.5 h total). |
