---
name: ttrpg-session-prep
description: "Write the session prep document a GM actually holds during play. Use when asked to prepare, write or update a session (prep note, session script, running sheet) for a tabletop campaign. Covers the required pre-reading, the mandatory structure (global-threads callout, at-a-glance table, scenes in play order with per-scene trigger boxes and read-aloud), the required elements (dramatic question per scene, non-combat exit, spotlight distribution, dramatic-resource triggers, white space, recurring-guide beat, content margin) and a derailment red team. Does not record what happened (see ttrpg-session-log), write the opening recap (see ttrpg-table-recap), or create standalone entity notes (see ttrpg-entity-note)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Session prep

Produces the document the GM relies on **while playing**, with a full table talking. Every
structural choice below exists to make information findable under pressure.

> **P1 — self-sufficiency.** This is the *only* sheet open during the evening. Everything needed
> to run — environment descriptions, read-aloud text, quotes, the tables and rules used that night
> — is inlined. The **only** exception is enemy stat blocks, which stay linked. This is a
> deliberate exception to the repository's "link, don't copy" rule and applies to prep only.

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

Read `campaign-profile.md` (path per the campaign repo). Slots used here:

| Slot | Used for | If empty |
|---|---|---|
| §1 System | which mechanics to inline in a scene | inline nothing mechanical; keep scenes fiction-first |
| §2 Dramatic resource | the spend/regain triggers section | drop that section entirely — do not invent a resource |
| §3 Tone | register of read-aloud text; the recurring thematic pressure | ask once, then proceed |
| §4 Canon source | quote blocks and their delivery mode | no quote blocks |
| §5 Recurring guide | the one prepared beat per session | no beat section |
| §6 Structure | which official module/chapter this session leans on | treat as fully homebrew |
| §7 Table conventions | table size → spotlight rotation; session length → content margin; absent-player rule | ask table size; it drives P7 |
| §9 Repo conventions | where the note goes, link syntax, frontmatter, verification command | write the file where told, skip link verification |

If the profile is missing, run `ttrpg-campaign-setup` first — do not guess conventions.

## Phase 1 — Read before writing, in this order

1. **The campaign state note** (the hub/index that holds current state). Extract: where the party
   is, who has unresolved hooks, current levels/resources, what comes next.
   *If the state is stale, say so before proceeding* — everything downstream inherits the error.
2. **The official module/chapter** for this session, if any (profile §6). It is the canvas **and
   the source to inline from**: its descriptions, read-aloud text, encounter tables and mechanics
   are *carried into* the prep (rewritten and fused with your own location notes, not cited by
   reference). Keep only an attribution link. Never copy stat blocks.
3. **The previous session log.** Exit state, loose ends, seeded hooks, missed opportunities to
   recover.
4. **The dossiers of the expected players.** Playstyle notes (who charges in, who must be handed a
   scene, who is chorus), their hooks/bonds (the exposed nerves), tracked properties.
   *Missing-hook check:* if a session protagonist has no recorded hooks, make collecting them the
   first scene of the session. Do not wait for it to happen naturally — plan it.
5. **The location notes** the party will cross: environment and local rules.
6. **The recurring guide note** (profile §5), to write this session's beat.

## Phase 2 — Mandatory structure

```markdown
---
<frontmatter per profile §9: session tag, module tag>
---

# Session N — Title

> [!warning] Don't forget at the table — global threads of the evening
> (ONLY threads that span the WHOLE session; per-scene triggers live in the scene boxes — P2)

> [!info] How to use this note
> (state that it is the complete, self-sufficient reference: everything descriptive, all
> read-aloud text and mechanics are here; the only things to open elsewhere are stat blocks,
> plus the attribution link to the official module and the list of homebrew deviations)

## At a glance
(table: Where / Antagonists / Key NPCs / Level / Expected outcome)

### Session objectives
### Arc of the evening
### Content margin        <!-- P8: which scenes are optional, what falls first -->

## Scenes (in play order)
...
```

**Every scene opens with a `> [!todo] Don't miss in this scene` box** of tickable checkboxes,
*before* the read-aloud. Then **inline** (never defer to another file):

| Block | Contains |
|---|---|
| `> [!quote] Read aloud` | the opening text — P3: only what the senses perceive |
| `> [!quote]` | canon quotes (profile §4) with the delivery mode noted |
| `> [!example]` | the mechanics used here: DCs, costs, local rules, typed-enemy traits |
| `> [!info]` | GM-only notes: hidden truths, NPC playable intention (P4), how to seed clues |
| `> [!abstract] Dramatic compass` | the three answers required by P5 |
| `If they derail:` | closing line of the scene — the pressure that persists (P9) |

Between blocks, the connective prep text stays clipped and scannable. **Never write the prep as
continuous narrative prose**: prose belongs inside the read-aloud blocks; between them the GM must
*find* things under pressure.

### The two levels of reminders (P2)

**Level 1 — top `[!warning]` box: global threads only.** 4–6 lines, one each, exclusively what
spans the whole session and belongs to no single scene:
- the dominant register of the recurring guide for the evening;
- a hidden urgency seeded across the session (something that sets up the *next* one);
- the cross-scene spotlight arc (which protagonist carries several scenes);
- the *principle* of the dramatic resource that night (where it burns, where it can be regained —
  no per-scene numbers);
- the *principle* of what earns a reward (choices and portrayal, never tactics).

**Level 2 — `[!todo]` box opening each scene: that scene's triggers.** Tickable checkboxes: an
NPC's focus on a specific PC, the key mechanic with its DC, the prepared beat if it falls here,
where the resource is spent or regained *here*, what earns a reward *here*, and the scene's
spotlight line marked `Spotlight → <PC>:`.

Allocation test: with a scene open, its `[!todo]` box alone answers *"what do I risk forgetting
right here?"*; the top box alone answers *"what must I not lose sight of all evening?"*.
A trigger answering both is in the wrong level or duplicated — **single source of truth**.

## Phase 3 — Required elements

### Self-sufficiency and staging — no bare schematics
Three recurring defects:

1. **Cross-references.** Every "read the description from the module / see the location note" is
   replaced by the actual text, inlined in a read-aloud block, fusing the sources into one clean
   passage. Only stat blocks stay linked.
2. **Schematics you cannot stage.** Bare tables and DC bullets are not enough: for every obstacle
   write *what triggers it, what leads to what, and how you put it on stage*. Entry routes,
   negotiations and reveals are described in words with the mechanics box beside them.
   **Key NPC lines are written speakable**, not summarised ("the guide explains the geography"
   → give him the sentences).
3. **Reveals inside read-aloud** (P3). Hidden truths move to a GM `[!info]` note marked
   *not to be read*, with how to seed the clues instead.

Test: a GM who never read the module can run the scene from this text alone — and the players
still discover what they are meant to discover.

### NPCs as subjects (P4)
Every interactive NPC whose will is not obvious declares, in a GM `[!info]` note: **what it wants**
(surface want, and beneath it the hidden truth when they differ — an NPC used as bait may sincerely
believe its own request) and **how to make it respond** (what each line and gesture pushes toward;
what it does if the players stand still, walk away, or contradict it).
Make the surface want **surface to the players too** — a speakable line, a described gesture —
or the NPC has no direction at the table and the scene does not start.
Scale it: full box only where a misread will breaks a scene or kills a hook; type-level behaviour
for crowds; one framing note for a large cast; nothing for obvious motives, hazards and atmosphere;
mark a deliberately will-less NPC as a choice.

### Dramatic compass per scene (P5)
`> [!abstract] Dramatic compass` states:
1. **The question** this scene poses that the players cannot answer immediately. If the answer is
   obvious, the scene is decorative.
2. **What deserves a reward here** — a concrete example of the moment that earns the campaign's
   reward currency *in this scene*. Reward moral choices and portrayal; **never** tactical play or
   a cool action.
3. **The non-combat exit condition** — cross, convince, endure, protect, renounce.

Without this block, the table's natural gravity rewards action, and rewards get handed out for the
wrong reasons.

### White space (P6)
At least **1–2 explicit conversation scenes**: no checks, no combat, no mechanical pressure. The
prep contains only the context and two or three trigger questions. Candidates: the march between
two locations, a rest at a safe point, a dialogue with the recurring guide or between PCs.
If it is not written, it gets skipped.

### The recurring guide's beat (profile §5)
One prepared, written beat per session — not improvisable. It advances the guide's arc or reveals
character. The rest of the session the guide may be purely functional. Skip this section entirely
if the profile declares no recurring guide.

### Distributed spotlight (P7)
2–3 protagonists per session, the rest chorus, rotating. **No spotlight section or table**: the
cross-scene arc goes in the top `[!warning]` box, the per-scene focus is a `Spotlight → <PC>:`
checkbox in that scene's `[!todo]` box.

### Dramatic-resource triggers (profile §2)
The mechanic must bite: state **where it is spent** (explicit costs, visible at the table) and
**where it can be regained**. A session that never touches it leaves the emotional core switched
off. Do not keep a transaction log in prep — the source of truth is the end-of-session value in
the player notes (P10); prep only says *where*.

### Quotes from the canon source (profile §4)
Place quotes where the table can actually listen — they stop the game. For each, note the delivery
mode declared in the profile (recorded actor reading / GM reading aloud). If the recording exists
locally in the repo, **embed it in the quote block** rather than linking out to a network source.

### Typed enemies and local rules
When an encounter spawns creatures characterised by a local trait, **inline the trait's mechanical
effect** in the `[!example]` box and link the full table. The stat block stays a link; the trait is
short and needed at the table.

### Combat only when it earns its place (P5)
No filler combat. Every fight has an **objective that is not depletion** — cross, extinguish, free,
hold N rounds, protect someone — and an explicit exit condition written in the scene. Boss
set-pieces deserve the evening; everything else is an obstacle.

## Phase 3bis — Derailment red team (P9)

Before verification, run (or delegate) a prediction pass:

1. **Input:** the scene plan just written + the playstyle sections of every expected player's
   dossier + past session logs (real derailments already observed are the best predictor).
2. **Output:** the **3–5 most likely derailing choices** of this table for this session, each with
   its **response pressure** — never a wall, always a consequence.
3. Fold each response into the `If they derail:` line of the affected scene.

Ask explicitly: *"what if they solve this from an angle I did not plan — using an NPC, a rule or an
agreement as leverage?"* A group that habitually plays laterally is not derailing; that is its
style, and it deserves coherent consequences rather than walls. Record this table's recurring
patterns in the campaign overlay so the question sharpens every session.

## Phase 3ter — Content margin (P8)

Prepare more than one session can cover:
- **1–2 optional scenes** beyond the main path, tagged `(optional)` in the title. They fall first
  when time runs short and cover the gap if the group burns through the core.
- The main path alone must already make a satisfying session. Optional scenes are margin, not a
  crutch.
- If an optional scene carries a hook and gets skipped, write in `If they derail:` how the seed can
  be recovered later — or declare it lost.

## Phase 4 — Verify

- Links follow the profile's syntax (§9); run the profile's verification command — invariant as
  declared (typically **0 broken links**).
- The top `[!warning]` box answers *"what must I not lose sight of all evening?"* and contains only
  global threads; every scene opens with a `[!todo]` box answering *"what do I risk forgetting
  right here?"*.
- **Single source of truth:** no trigger duplicated between the global box and a scene box; every
  value (DC, cost) lives in exactly one place.
- **Self-sufficiency:** no cross-reference for descriptive content; every scene has its inlined
  read-aloud; the only link meant to be opened during play is a stat block.
- **Distributed spotlight:** no summary spotlight table; cross-scene arc in the global box,
  per-scene focus marked `Spotlight → <PC>:`.
- **NPCs as subjects:** every interactive NPC with a non-obvious will declares its playable
  intention, its surface want reaches the players, and no box was written for obvious motives.
- Every scene has a dramatic compass and a non-combat exit; at least one white-space scene exists.

## What NOT to do

- Do not copy stat blocks; do inline everything else needed that night.
- Do not leave "see the module / see the location note" for descriptive content.
- Do not write the prep as continuous narrative.
- Do not plan equal spotlight for every player, and do not create a spotlight table.
- Do not duplicate a trigger between the global box and a scene box.
- Do not write NPCs as passive objects — and do not inflate: obvious motives, hazards and
  atmosphere need no intention box.
- Do not insert filler combat, or a fight without an objective and an exit condition.
- Do not announce in read-aloud what the players are supposed to discover.
- Do not invent a dramatic resource, guide beat or canon quote that the profile does not declare.
