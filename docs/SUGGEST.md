# Escape from Shadows — Ideas & Suggestions

> A design notebook for **Dark Quest / Escape from Shadows**.
> Pure ideas — no code, no implementation. Pick what excites you and turn it into a plan.

## How to Read This

Every idea is tagged so you can skim:

| Tag | Meaning |
|-----|---------|
| 🟢 **Quick win** | Small, self-contained, high payoff. Do these first. |
| 🔵 **Core system** | Bigger, but it's what turns a script into a game. |
| 🟣 **Fantastic** | Ambitious, weird, memorable. The stuff people tell friends about. |
| ⚠️ **Careful** | Powerful but easy to get wrong — read the caveat. |

---

## 0. Where the Game Stands Today

Honest snapshot, because good ideas start from an accurate map:

- The **shell is real**: a working Textual app with a main menu, a settings screen, and JSON-persisted settings.
- The **game is not wired in yet**: `START GAME` only prints a status line. There is no gameplay screen.
- The **baseline story** is a linear chain of three `input()` prompts — HALL → (BLOOD KITCHEN *or* OLD LIBRARY) → OLD YARD → a HELL DOG → win or lose.
- **`main_menu.py` and `game/settings_manager.py` are empty stubs** — the menu logic currently lives in `index.py`, and settings logic lives in `config.py`.
- **Difficulty, Sound, and Music settings are stored but have zero effect** on anything.

That last point is the biggest opportunity in the whole repo: *three settings already exist, and the game doesn't use any of them.*

---

## 1. Design Pillars

Before features, decide what the game *is*. Suggested pillars — argue with them:

1. **Dread over gore.** The scariest thing in a terminal is what the player imagines between the lines. Restraint beats red text.
2. **Every death is a lesson.** A player should be able to say *why* they died, and what they'd do differently.
3. **Choices echo.** A decision in the HALL should still be costing you in the OLD YARD.
4. **The terminal is a character.** This isn't a game that happens to run in a terminal; the terminal's narrowness, monospace grid, and limitations are the aesthetic.
5. **Short, replayable, complete.** A 15–20 minute run that ends properly beats an unfinished epic.

---

## 2. Narrative Architecture

### 2.1 The Premise You Already Have

The baseline implies a house with a **HALL**, a **BLOOD KITCHEN**, an **OLD LIBRARY**, an **OLD YARD**, and a **HELL DOG**. That's a manor. Lean into it: you woke up in a house that is not yours, it is not night, and *it is not outside*.

### 2.2 The Shadow as a Named Antagonist 🔵

Right now "shadows" is only the title. Give it rules:

- It **cannot enter lit rooms** — so light is both your resource and your leash.
- It **learns**: it appears in the room you just left, then the room you're about to enter, then the room you *considered* entering.
- It **speaks in the second person**, and its dialogue is drawn from the player's own earlier choices. ("You went left in the hall. I remember.")
- It is never drawn as a sprite — only as a **description of what's missing**: a doorway with no light behind it, a chair that is now facing the wall.

### 2.3 Multiple Endings 🔵

The baseline has exactly two outcomes. Aim for a spread of 5–7, sorted by *how much you understood* rather than by *how well you did*:

| Ending | Requirement | Tone |
|--------|-------------|------|
| **The Long Walk** | Die in the first room | Failure, but the shadow respects you |
| **Meat and Silence** | Feed the Hell Dog | Ugly survival |
| **The Quiet Exit** | Leave through the front door | Standard win |
| **What the Book Knew** | Read the book *and* escape | Best "true" ending |
| **The New Shadow** | Escape with the lantern empty | You got out. Something came with you. |
| **Homecoming** 🟣 | Find all three memory fragments | Secret ending, recontextualizes the house |
| **Stay** 🟣 | Refuse to leave at the final door | The player chooses the house |

### 2.4 Memory Fragments 🟣

Scatter three items that don't help you survive at all — a photograph, a child's drawing, a receipt dated tomorrow. Collecting them changes nothing mechanically. They only change the ending. This teaches players that *curiosity is a mechanic*, not a waste of turns.

---

## 3. The Core Loop

Right now the loop is: read text → pick a letter → read text. That's a **quiz**, not a game, because nothing accumulates. Add state that the player can feel.

### 3.1 The Lantern 🔵

Your central resource. Every room you enter costs oil.

- Oil drains **faster** when you take a slow, careful action (searching, reading).
- Oil drains **slower** in rooms you've already lit.
- **At zero oil, the Shadow can reach you.** This creates the game's core tension: *understanding the world costs you the safety to explore it.*
- Refills are scarce and always a trade: the oil can in the kitchen is behind the thing in the kitchen.

### 3.2 Composure (a second bar) 🔵

Lantern is time. **Composure** is nerve.

- Drops when you witness something awful, when the Shadow speaks to you, or when you run.
- Low composure **lies to you**: room descriptions become unreliable, items get renamed, a safe exit might be described as locked.
- At zero composure you don't die — you **walk into the Shadow voluntarily**. Different, scarier, recoverable with a story consequence.

⚠️ *Careful:* unreliable narration is wonderful once and infuriating if overdone. Cap it: only the last 20% of the bar distorts text, and always signal it with a tic (italic text, a stutter, a repeated word).

### 3.3 Inventory 🔵

Keep it small — **six slots maximum**. Constraints create choices.

Candidate items, all tied to the baseline rooms:

- **Matchbox** (HALL) — relight the lantern, once.
- **Rusty Cleaver** (BLOOD KITCHEN) — solves the Hell Dog, costs you composure every turn you carry it.
- **The Book** (OLD LIBRARY) — the single best source of information in the game, and it's heavy, slow to read, and *watched*.
- **Silver Whistle** (OLD YARD) — the Hell Dog's actual weakness. Only works if you know its name.
- **Dog's Tooth** — taken from the Hell Dog. Useless. Proof.
- **Front Door Key** — obtainable three different ways. Two of them are traps.

### 3.4 The Journal 🔵

An in-game notebook that auto-records: rooms seen, things that killed you, lines the Shadow has said. This is your **anti-frustration system** — it converts a death into retained knowledge, so a second run feels smart instead of random.

### 3.5 Dread Counter 🔵

A simple turn counter that the player can *see*, but with no stated limit. Around turn 20, the music (if on) gains a second layer. Around turn 30, room descriptions get one extra sentence describing the Shadow's position. **Never tell the player the number means anything.** They'll figure it out and start optimizing — which is the fun.

---

## 4. Choice Design

### 4.1 The Instant-Death Problem ⚠️

In the baseline, choosing `l` in the HALL is an immediate loss with no warning and no information. That's not tension — that's a coin flip, and coin flips feel unfair on run one and meaningless on run two.

**Fix: the three-tier consequence model.**

| Tier | Cost | When to use |
|------|------|-------------|
| **Scar** | Permanent small penalty | Most choices. Accumulating scars *is* the difficulty curve. |
| **Setback** | Lost item, lost time, lost composure | Bad-but-informed choices |
| **Death** | Run over | Only when the player had at least two clear warnings |

Death should be *earned by the player*: they saw the blood on the kitchen threshold, they heard the thing breathing, and they walked in anyway. That death is a story. An unwarned death is a bug.

### 4.2 Telegraph, Don't Announce 🔵

Instead of `"The BLOOD KITCHEN — you lose"`, write:

> The door to the left is warm. There is a smell, and it is recent.
> Something on the other side is breathing in time with you.

Now the choice is *informed*. The player who goes left anyway has made a decision, and decisions create memory.

### 4.3 Choices With No Safe Answer 🟣

The best horror choices are not right/wrong, they're **which cost**. Example for the OLD YARD Hell Dog:

1. **Move slowly** — costs oil and composure, but you keep the cleaver clean.
2. **Move quickly** — costs nothing if you're lucky, wakes the dog if you're not.
3. **Throw the meat** (only with the kitchen item) — the dog lives, you lose the meat *and* a memory fragment you didn't notice was in it.
4. **Whistle** (only if you read the book) — the dog leaves. It comes back. Later. Somewhere worse.

---

## 5. Making the Existing Settings Real

You already ship Difficulty / Sound / Music. Here's what they could actually do.

### 5.1 Difficulty 🔵

Difficulty should change **information and mercy**, never the story:

| | EASY | MEDIUM | HARD |
|---|---|---|---|
| **Lantern oil** | Generous | Standard | Tight |
| **Hints** | Shadow's taunts double as hints | Occasional | None |
| **Deaths** | Checkpoint at last room | Restart room chain | Restart from HALL |
| **Journal** | Auto-fills on death | Fills on death | Only what you noted yourself |
| **Choice countdowns** | None | None | Some choices expire if you hesitate |

⚠️ *Careful:* HARD should be *leaner*, not *cheaper*. Take away safety nets, not fairness.

### 5.2 Sound 🟢

A terminal has exactly one reliable audio channel: **the system bell**. Use it as a horror tool and it becomes the most memorable thing in the game.

- Bell on: a door opening, the dog's collar, the Shadow's first word.
- Bell off: the same moments, but silent — which is *worse* once the player has learned to fear the bell.
- Because it's a terminal, the bell may also be disabled by the user's environment. Design so the game is complete without it.

### 5.3 Music 🟢

There's no audio pipeline in a plain terminal — so define "music" as **visual rhythm**:

- Music ON: text types out character by character, panel borders pulse on a slow beat, the background color deepens by one shade every 10 turns.
- Music OFF: text appears instantly, layout is static and flat.

That makes the toggle a genuine *presentation* choice, and it doubles as an accessibility option for players who need instant text.

---

## 6. Rooms & Set-Pieces

Existing rooms, reworked, plus new ones. Each entry: **the hook**, and **what it costs**.

### The Existing Four

- **THE HALL** — Keep it as the "safe" tutorial room, but make it a *hub*, not a corridor. Two doors, a staircase up, and a front door that is visibly, insultingly, unlocked-but-stuck. The player will try it three times across two runs. Let the third attempt work.
- **BLOOD KITCHEN** 🩸 — The instant-loss room becomes the **trade room**. Everything you need is here (oil, matches, meat, cleaver) and everything here wants something from you. Entering costs composure, not the run.
- **OLD LIBRARY** 📚🕯️ — The information room. The BOOK is the best item in the game and reading it takes **three consecutive turns** during which you cannot see the door. The candle burns down while you read. The most classic horror scene available to you: *you know someone came in, because the door is open now.*
- **OLD YARD** 🛖 — Make it the closest thing to *outside* — rain, mud, a wall too high to climb, a doghouse. This is where the game teaches you that escape and survival are different goals.

### New Rooms

| Room | Hook | Cost |
|------|------|------|
| **The Stairwell** 🟣 | The staircase has more steps going up than coming down. | Compose yourself or lose a piece of your map |
| **The Nursery** ⚠️ | Everything is child-height. Something is still playing. | Highest composure loss in the game |
| **The Mirror Room** 🟣 | It reflects the room you were in *two rooms ago*. | Reveals a room you skipped — and what's in it now |
| **The Long Corridor** 🟣 | The same corridor three times, subtly different. | On the third pass, one door is gone |
| **The Cellar** | Absolute dark. Requires the lantern to be above half. | You cannot bring the book down here |
| **The Chapel** | A single lit candle that has been burning a very long time. Someone is maintaining it. | Leaving the candle lit costs you the lantern fill |
| **The Front Door** 🟣 | The exit. It is always visible from the HALL and never reachable until the end. | Every time you pass it, composure drops |

### The Hell Dog, Reworked 🔵

The baseline treats it as a coin flip with two outcomes. Make it a **puzzle with four solutions**, as laid out in §4.3, and give it one rule the player can discover: *it only moves when you do.* Standing still is safe and costs oil. This turns the encounter into a resource-management scene instead of a dice roll — and it's genuinely tense in a turn-based terminal.

---

## 7. Presentation in the Terminal

### 7.1 Screen Layout 🟢

The terminal's narrow width is a constraint you can design *with*. Suggested game screen:

```text
┌─ OLD LIBRARY ────────────────────── turn 14 ─┐
│                                              │
│   The candle has burned to a stub.           │
│   The book is open at a page that was        │
│   blank when you opened it.                  │
│                                              │
│   [ door ]   [ book ]   [ shelf ]            │
│                                              │
├──────────────────────────────────────────────┤
│ LANTERN ██████░░░░  COMPOSURE ████████░░     │
│ > read the book                              │
└──────────────────────────────────────────────┘
```

Three fixed zones: **scene** (never scrolls within a room), **status** (bars + prompt), **footer** (key hints). Stable layout means the player's eye never hunts.

### 7.2 Typewriter Text 🟢

Reveal prose a few characters at a time. It's a five-line change with an enormous atmosphere payoff — and it gives you a free "any key to skip" that doubles as a tension release. Tie the speed to the Music setting (§5.3).

### 7.3 ASCII Art 🟢

Reserve ASCII art for **three moments only**: the title screen, the Hell Dog, and each ending. Rarity is what makes it land. A dog rendered in forty characters is scarier than a paragraph describing one.

### 7.4 Color as Grammar 🔵

Don't color for decoration — color for *meaning*, and keep it consistent for the whole game:

| Color | Always means |
|-------|--------------|
| Dim grey | Description / narration |
| White | Things you can interact with |
| Cyan | Your own actions and options |
| Amber | Time, light, and resource warnings |
| Red | **Only** when the Shadow is present |

If red appears exactly four times in a whole playthrough, it will terrify people.

### 7.5 Quiet Horror Techniques 🟣

Small tricks that cost little and stick for years:

- **Delayed echo.** A room description includes one sentence you saw in a different room twenty turns ago.
- **The missing line.** Occasionally render a room with the last line simply absent — no error, no explanation.
- **The patient prompt.** Once per run, the input prompt waits an unusually long time before accepting input. Nothing happens. It's just... late.
- **Your own words.** Feed the player's earliest chosen action back as Shadow dialogue at the climax.
- **One-frame change.** For a single refresh, a word in the status bar is different. Turn counters are a great victim.

⚠️ *Careful:* never break the frame in a way the player can't tell is intentional. Ambiguity between "haunting" and "buggy" destroys trust fast.

### 7.6 The Map 🟣

An optional overlay (bound to a key) showing rooms as a hand-drawn-feeling grid. Rooms you've entered are drawn; rooms you've *heard* are drawn as a dashed outline; rooms where you died are drawn with an X that stays across runs.

That last detail is free replayability: **your map accumulates your history.**

---

## 8. Accessibility & Comfort

The excellent thing about a terminal game is that accessibility is cheap to add here. Make these first-class settings:

- **Text speed** (instant / fast / slow) — also covers screen-reader users.
- **Reduce motion** — no pulsing borders, no typewriter, no color shifts.
- **High contrast** — swap the gothic palette for a pure two-tone theme.
- **Colorblind-safe mode** — the meaning table in §7.4 should have glyph equivalents (a marker character per category), so color is never the only signal.
- **Plain mode** — no ASCII art, no effects; pure prose.
- **Content warnings on the title screen** — this is a horror game in a nursery and a kitchen full of blood. Say so before the player starts. It costs nothing and it's the right thing to do.
- **Pause at any time.** Let people step away from a tense scene.

---

## 9. Persistence, Runs & Meta

### 9.1 Save & Resume 🟢

You already have `SettingsManager`, a proven JSON persistence pattern in this repo. A save file is the same idea with different contents: current room, inventory, lantern, composure, turn count, journal entries, endings seen. One slot is fine; the "continue" option on the main menu becomes real.

### 9.2 Death Screen That Respects the Player 🔵

Never show just "YOU LOSE." Show:

1. **How you died**, in one sentence.
2. **What you learned** (auto-journal entry).
3. **What you could have done**, *greyed out*, only on EASY.
4. **"Again"** and **"Back to menu"**.

The greyed-out third line is a real design decision: it's mercy for some players and a spoiler for others. Bind it to difficulty.

### 9.3 New Game Plus 🟣

After any ending, unlock a second pass where:

- The Shadow's dialogue now references the ending you got.
- The Hell Dog recognizes you.
- One room has changed in a way only a returning player would notice.

This costs very little content and converts a 20-minute game into a game people replay.

### 9.4 The Endings Gallery 🟣

A screen listing all endings as silhouettes: the ones you got are named, the ones you missed are just *counts* ("3 of 7"). Achievements without the pop-up gamification — just a quiet record of what you've seen.

---

## 10. Fantastic Ideas (the fun ones)

Borrow freely. Steal the cheap ones, dream about the expensive ones.

1. **The game remembers your terminal.** 🟣 Use the actual terminal column count in the prose: "the corridor is exactly as wide as this window." On a narrow terminal, the room feels narrower. Free, and nobody expects it.
2. **The Shadow types back.** 🟣 For exactly one prompt in the endgame, the player's typed input is *answered* before they press Enter.
3. **A room you can only reach by being wrong.** 🟣 Die in the BLOOD KITCHEN twice. The third time, it's a different room. No explanation, ever.
4. **A companion who lies.** 🟣 A second voice in the journal that gives advice. It's right for the first half. It is the Shadow for the second half.
5. **Real-time dread.** 🟣 After 25 minutes of wall-clock play, regardless of turns, something changes permanently for that session. Makes a long game feel haunted rather than long.
6. **The book reads you.** 🟣 The LIBRARY's book describes the player's own run so far — the rooms in order, the choices made. Mechanically it's just a log. Dramatically it's the best scene you could write.
7. **A door that opens only if you close the game.** 🟣 One ending requires quitting and relaunching, where the main menu has quietly changed. Enormous payoff, moderate cost, extremely memorable.
8. **Difficulty as narrative.** 🟣 EASY/MEDIUM/HARD isn't a menu — the Shadow *comments* on your choice. "Easy. Of course."
9. **Co-op by terminal share.** 🟣 Two people, one keyboard, no screen sharing: player A reads only descriptions, player B reads only the options, and they cannot see each other's text. Communication is the puzzle.
10. **A seed of the day.** 🟣 One procedural room layout shared by everyone that day, with a community-wide "who escaped" tally in the journal.

---

## 11. Architecture Suggestions (Conceptual, No Code)

The repo already separates `screens/` from `game/` — the base version's story logic just doesn't live in either yet. Suggested split, in words:

- **Engine vs. content.** The engine knows how to *walk a story graph*: show a scene, present options, apply effects, move to the next scene. The content is *data* — rooms, choices, costs, requirements. With that split, adding a room is writing content, not touching the game loop. This is the single highest-leverage structural change available.
- **A game state object** owned by the app (like `self.app.config` already is), holding lantern, composure, inventory, flags, turn count, and journal. Every screen reads and mutates this one object. It's also exactly what gets serialized to a save file.
- **Effects as small declarative entries**, not branches: "costs 1 oil, costs 2 composure, grants the cleaver, sets flag `saw_the_kitchen`." Conditionals become requirements: "requires flag `read_the_book`."
- **Two remaining stubs.** `main_menu.py` and `game/settings_manager.py` are empty. Decide deliberately: either move the existing menu into `screens/main_menu.py` for consistency with `settings.py`, and either make `game/settings_manager.py` the real implementation with `config.py` as a thin re-export, or delete the stubs so there's one obvious place for each thing. Right now `index.py` holds menu logic, which contradicts the layout documented in `AGENTS.md` and `GENERAL_DOC.md`.
- **Wire difficulty in from the start** rather than retrofitting it — see §5, where the difficulty table is the natural home of every "mercy" knob in §3 and §9.

---

## 12. Roadmap

Four phases, each ending in something playable. Don't start phase 2 until phase 1 is fun.

### Phase 1 — Vertical Slice 🟢
- A gameplay screen (scene panel + status panel + prompt line).
- The HALL and the OLD LIBRARY only, with the BOOK and one real cost (oil).
- Lantern bar and turn counter.
- One honest death, one honest ending.
- **Success test:** a stranger plays it twice in a row without being asked.

### Phase 2 — The House 🔵
- All four baseline rooms, reworked per §6.
- Inventory, composure, the journal.
- The Hell Dog as a four-solution puzzle.
- Death screen with the "what you learned" line.
- Difficulty actually doing something.
- Save/load.

### Phase 3 — The Shadow 🟣
- Shadow as a pursuing entity with rules.
- Shadow dialogue drawing on the player's own history.
- Multiple endings + endings gallery.
- The three memory fragments.

### Phase 4 — The Fantastic 🟣
- Pick 2–3 items from §10. Not all of them.
- New Game Plus.
- Accessibility pass (§8) if not already done — ideally do it here *and* earlier.

---

## 13. Pitfalls to Avoid

- ⚠️ **Unwarned death.** The single biggest fairness flaw in the baseline. Every death needs two telegraphs.
- ⚠️ **Choices that don't matter.** If `b` and `d` always lead to the same place, players learn to stop reading. Even cosmetic differences must *show*.
- ⚠️ **Input friction.** Requiring players to type letters is a fine retro flourish, but pair it with selectable options — a mistyped key should never be a death.
- ⚠️ **Text walls.** A terminal screen holds about 20 useful lines. If a room needs 40, it's two rooms.
- ⚠️ **Effects for their own sake.** One haunting moment per run beats six. Repetition converts eerie into annoying.
- ⚠️ **Settings that lie.** Difficulty, Sound, and Music currently change nothing. Shipping invisible toggles trains players to distrust the menu.
- ⚠️ **Scope creep into phase 3 before phase 1 is fun.** The vertical slice is the whole project's risk; everything else is amplification.

---

## 14. The One-Sentence Version

**You already have the house, the dog, the book, and three settings that do nothing — turn the settings into mercy, the rooms into costs, and the Shadow into something that remembers, and this stops being a script and becomes a game.**
