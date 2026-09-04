---
name: ttrpg-session-prep
description: "Write the session prep document a GM actually holds during play: global-threads callout, at-a-glance table, scenes in play order with per-scene trigger boxes, inlined read-aloud, dramatic compass and non-combat exits. Use when asked to prepare, write or update a session (prep note, session script, running sheet) for a tabletop campaign. Does not record what happened (see ttrpg-session-log), write the opening recap (see ttrpg-table-recap), create standalone entity notes (see ttrpg-entity-note), or plan the arc above the session (see ttrpg-campaign-arc)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.1"
---

# Session prep

Produces the document the GM relies on **while playing**, with a full table talking. Every
structural choice below exists to make information findable under pressure.

> **P1 — self-sufficiency.** This is the *only* sheet open during the evening. Everything needed
> to run — environment descriptions, read-aloud text, quotes, the tables and rules used that night
> — is inlined. The **only** exception is enemy stat blocks, which stay linked. This is a
> deliberate exception to the repository's "link, don't copy" rule and applies to prep only.

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

**Supporting references** — read the one you need, not both by default:
- [references/scene-anatomy.md](references/scene-anatomy.md) — how a single scene is built: the
  block vocabulary, the two levels of reminders, staging defects, NPC intention, dramatic compass,
  white space, combat with an objective. Read it while writing or fixing scenes.
- [references/red-team.md](references/red-team.md) — the derailment prediction pass and the content
  margin. Read it before finishing, or hand it to a sub-agent as a standalone pass.

---

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
| §7 Table conventions | table size and protagonists-per-session → spotlight rotation; session length → content margin; absent-player rule | ask table size; it drives P7 |
| §9 Repo conventions | where the note goes, link syntax, frontmatter, verification command | write the file where told, skip link verification |

If the profile is missing, run `ttrpg-campaign-setup` first — do not guess conventions.

## Phase 1 — Read before writing, in this order

1. **The campaign state note** (the hub that holds current state). Extract: where the characters
   are, who has unresolved hooks, current levels/resources, what comes next.
   *If the state is stale, say so before proceeding* — everything downstream inherits the error.
2. **The official module/chapter** for this session, if any (§6). It is the canvas **and the source
   to inline from**: its descriptions, read-aloud text, encounter tables and mechanics are *carried
   into* the prep, rewritten and fused with your own location notes, not cited by reference. Keep
   an attribution link. Never copy stat blocks.
3. **The previous session log.** Exit state, loose ends, seeded hooks, missed opportunities.
4. **The dossiers of the expected players.** Playstyle notes (who charges in, who must be handed a
   scene, who is chorus), their hooks (the exposed nerves), tracked properties.
   *Missing-hook check:* if a session protagonist has no recorded hooks, make collecting them the
   first scene. Do not wait for it to happen naturally — plan it.
5. **The location notes** the characters will cross: environment and local rules.
6. **The recurring guide note** (§5), to write this session's beat.

## Phase 2 — Mandatory structure

```markdown
---
<frontmatter per §9: session tag, module tag>
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
<!-- each scene: [!todo] trigger box → read-aloud → mechanics/GM notes → dramatic compass
     → "If they derail:" — see references/scene-anatomy.md -->
```

The whole document is written to be **scanned**, not read: scene text lives in labelled blocks,
and the connective tissue between them stays clipped.

## Phase 3 — Required elements (each scene, unless noted)

| Element | Rule | Detail |
|---|---|---|
| Trigger box | opens every scene, before the read-aloud; single source of truth against the global box | scene-anatomy |
| Inlined read-aloud | only what the senses perceive; reveals go to GM notes | scene-anatomy |
| NPC playable intention | for interactive NPCs whose will is not obvious, scaled to role | scene-anatomy |
| Dramatic compass | question / what earns a reward here / non-combat exit | scene-anatomy |
| White space | 1–2 conversation scenes per session, written or they get skipped | scene-anatomy |
| Combat with an objective | never depletion; explicit exit condition | scene-anatomy |
| `If they derail:` | the pressure that persists when they do the unplanned | red-team |
| Content margin | 1–2 optional scenes; main path alone must satisfy | red-team |

Plus, once per session:

- **Recurring guide's beat** (§5) — one prepared, written beat that advances their arc or reveals
  character. The rest of the session they may be purely functional. No guide declared → skip.
- **Distributed spotlight** (P7) — protagonists per §7, the rest chorus, rotating. **No spotlight
  section or table**: the cross-scene arc goes in the top `[!warning]` box, the per-scene focus is
  a `Spotlight → <PC>:` checkbox in that scene's trigger box.
- **Dramatic-resource triggers** (§2) — state *where* it is spent (explicit costs, visible at the
  table) and *where* it can be regained. A session that never touches it leaves the emotional core
  switched off. Keep no transaction log: the end-of-session value in the player notes is the source
  of truth (P10).
- **Canon quotes** (§4) — placed where the table can actually listen, since they stop the game,
  each with its declared delivery mode. If a recording exists inside the repo, embed it in the
  quote block rather than linking to a network source.
- **Red team pass** (P9) — before verification, run or delegate it; fold the results into the
  `If they derail:` lines.

## Phase 4 — Verify

- Links follow §9 syntax; run the profile's verification command and report its actual result —
  never claim an invariant you did not run.
- The top `[!warning]` box contains only global threads; every scene opens with a trigger box.
- **Single source of truth:** no trigger duplicated between the global box and a scene box; every
  value (DC, cost) lives in exactly one place.
- **Self-sufficiency:** no cross-reference for descriptive content; every scene has its inlined
  read-aloud; the only link meant to be opened during play is a stat block.
- **Distributed spotlight:** no summary spotlight table; cross-scene arc in the global box,
  per-scene focus marked `Spotlight → <PC>:`.
- Every scene has a dramatic compass and a non-combat exit; at least one white-space scene exists;
  every scene has an `If they derail:` line.
- Any figure appearing with dialogue passed the admission test (P13) when its note was written.

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
