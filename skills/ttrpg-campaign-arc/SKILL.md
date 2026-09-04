---
name: ttrpg-campaign-arc
description: "Produce and maintain the arc note that plans the campaign above the single session: backbone table, canon-vs-homebrew deviation ledger, open-thread tracker, spotlight budget across sessions, pacing over the campaign horizon and a seeded endgame. Use when asked to plan an arc, season or chapter, to review where the campaign is going, to check which threads are still open, or to decide what the next few sessions must deliver. Covers what each chapter must deliver, why each divergence from the source was made, who owns each unpaid seed, and who is owed the spotlight. Does not write a playable session (see ttrpg-session-prep), record a played one (see ttrpg-session-log), or audit the repo for drift (see ttrpg-continuity-audit)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Campaign arc

Produces **one living arc note** — the layer between the campaign profile (facts that do not
change) and session prep (one evening). It is read when deciding what the *next few* sessions must
do, and rewritten in place after every chapter boundary.

**This skill plans; it does not write a session.** The moment you are writing read-aloud text,
scenes or trigger boxes, you are in `ttrpg-session-prep` and should stop here.

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

| Slot | Used for | If empty |
|---|---|---|
| §1 System | level/progression checkpoints the backbone must respect | plan in fiction only, no progression row |
| §2 Dramatic resource | the arc-level curve: where it must be lowest, where it can be regained | drop the curve row entirely |
| §3 Tone | where the register must shift, and which breaks are admitted | ask once; do not invent tone shifts |
| §4 Canon source | which part of the corpus each chapter leans on | drop the canon column and the deviation ledger |
| §5 Recurring guide | the guide's arc across the campaign and where it resolves | drop that row |
| §6 Structure | the backbone itself: modules/chapters vs homebrew vs sandbox; how deviations are recorded | ask once — without it there is no backbone to map |
| §7 Table conventions | cadence × horizon = session budget; table size and protagonists per session → rotation period | ask cadence and table size; both are load-bearing here |
| §9 Repo conventions | where the arc note lives, link syntax, verification command | ask where the note goes |
| §10 Working agreements | how blunt the review is; what may not be changed without asking | propose, do not restructure |

If the profile is missing, run `ttrpg-campaign-setup` first — do not guess a backbone.

## Phase 1 — Read before planning, in this order

1. **The campaign state hub** (§9): where the party is, what is next, what is unresolved.
   *If it contradicts the last session log, stop and say so* — the log wins (P11) and everything
   planned on a stale hub is wrong.
2. **Every session log since the last arc pass.** Extract, per session: seeds planted, hooks left
   unpaid, promises made at the table, who was actually protagonist, where the register drifted,
   and which planned content was skipped.
3. **The backbone source** (§6): the module/chapter list, or the list of fronts if homebrew.
   What each unit *contains* versus what it must *deliver here*.
4. **The player dossiers**: hooks and exposed nerves that have never been touched; who is owed a
   session; who is leaving or joining.
5. **The previous arc note.** What was predicted and did not happen is the most useful input you
   will get: it is where the plan was too tight.

## Phase 2 — The arc note

```markdown
---
<frontmatter per profile §9>
---

# <Campaign> — Arc

> Planning layer. Current state lives in <state hub>; what happened lives in the session logs.
> Nothing here is a source of truth for state (P10).

## Session budget
<cadence × horizon (§7) = N sessions; sessions played; sessions left; what that buys>

## Backbone
| Chapter / region | Sessions (range) | What it must deliver | Tone shift | Resource curve | Status |
|---|---|---|---|---|---|

## Deviation ledger
| # | What the source says | What we do instead | Why | What it binds downstream | Since |
|---|---|---|---|---|---|

## Open threads
| Thread | Seeded in | Owner | What would pay it off | Status |
|---|---|---|---|---|

## Spotlight budget
| Session | Protagonists | Owed next |
|---|---|---|

## Pacing
<where the register shifts; where the quiet session goes; where the endgame seeding starts>

## Endgame
<the final beats, the conditions that select between endings, what is deliberately left open>
```

## Phase 3 — Required elements

### The backbone table (§6)
One row per chapter, region or front. Columns carry weight:

- **Sessions (range)**, never an exact number. A chapter that "takes 3 sessions" takes 2 or 5. The
  range is the contract; the row also names **what falls first** if it runs long (P8 at arc scale).
- **What it must deliver** — the *function* of the chapter, not its content: the reveal that must
  land, the relationship that must change, the capability the party must gain, the question that
  must be forced. Content is prep's problem; if a chapter has no function, it is filler and either
  gets one or gets cut.
- **Tone shift** — where the register changes and what it changes *to* (§3). A campaign that stays
  at one intensity for twenty sessions has no climax, only a plateau.
- **Resource curve** (§2) — where the dramatic resource must be at its lowest and where it can be
  regained. Pressure that never eases stops being felt. Drop this column if §2 is empty.

**Sandbox degradation:** if §6 declares no backbone, the rows are **fronts** — a pressure, who
drives it, what happens if the party never intervenes, and the visible sign it has advanced. Same
columns otherwise. Never invent a linear plot for a table that chose a sandbox.

### The deviation ledger (§4, §6)
**Every deliberate divergence from the source is recorded with its reason.** Not for bookkeeping:
the divergence is what future prep must stay consistent with, and a divergence remembered only in
the GM's head becomes a contradiction three months later, at the table, in front of everyone.

Each entry states what the source says, what this campaign does instead, **why**, and **what it
binds downstream** — the consequences now locked in (an NPC who cannot appear, a secret that no
longer exists, a rule inverted for the whole campaign). Entries are append-only and dated by
session; reversing a deviation is a new entry, not an edit. Drop this section only if §4 and §6
both declare no source material.

### The open-thread tracker (P11)
Fed by the session logs, not by memory. One row per live promise, with four fields that are all
mandatory:

- **Seeded in** — link to the log where it entered the fiction. If you cannot cite it, the table
  never actually saw it: it is an idea, not a thread.
- **Owner** — which PC or NPC carries it. A thread nobody owns is not going to come back.
- **What would pay it off** — the concrete scene or revelation that closes it. Without this the
  thread cannot be scheduled, only worried about.
- **Status** — *alive* / *paid (link the log)* / *lost*. **"Lost" is a legitimate, deliberate
  status**: declaring a seed dead is planning; letting it rot unlisted is drift.

At every arc pass, decide each *alive* thread: schedule it into a backbone row, or declare it lost.
`ttrpg-continuity-audit` finds and reports dangling threads; **the decision is made here.**

### Spotlight budget across sessions (P7)
P7 forbids a spotlight table *inside prep*, because nobody scrolls to it mid-session. The arc note
is the **one admitted exception**: it is read while planning, never during play. Keep a running
tally of who was protagonist in each session (from the logs, not from intent) and who is owed one.

Fairness is measured over the horizon, not over the evening. Table size ÷ protagonists per session
(§7) gives the **rotation period** — the number of sessions after which everyone has carried one;
nobody may stay chorus longer than that. Read the tally against the
backbone: assign the chapter whose *function* matches a player's untouched nerve to that player.
A player who has been chorus for six sessions is the next protagonist — that is a scheduling fact,
not a preference.

### Pacing over the horizon (§7)
Cadence × horizon gives the real session budget. Say it out loud in the note, then check the
backbone against it: a backbone that needs 40 sessions on a 20-session horizon is a plan to end the
campaign in the middle, and the cut is decided **now**, not by exhaustion later.

Plan explicitly: where the register shifts (§3), where the **quiet session** goes (P6 at arc scale
— a whole low-pressure session is legitimate and must be scheduled or it will never happen), where
the resource curve bottoms out (§2), and which chapters are compressible if attendance collapses
or the horizon shortens.

### The endgame, seeded early
Decide the endgame while there is still time to seed it. Record:

- **The final beats** — the two or three images the campaign is built to arrive at.
- **What must already exist** for them to land: which entity, promise or object must be planted,
  and **in which session** it is planted. Write those seeds into the backbone rows as delivery
  requirements, not as hopes.
- **The conditions that select between endings** — the states of the world the players' choices
  actually control, so the ending is earned rather than chosen by the GM at the last minute.
- **The recurring guide's resolution** (§5), if the profile declares one.
- **What is deliberately left open** — mark it as a choice, so a later pass does not "fix" it.

A finale improvised in the last session is a finale nobody was allowed to affect.

## Phase 4 — When to run a pass

At every chapter boundary, and whenever three sessions have gone by without one. A pass is not a
rewrite: update the tables in place, append to the ledger, and produce a short delta —
*what changed, what is now scheduled, what was declared lost.*

## Phase 5 — Verify

- Every backbone row has a function ("what it must deliver"), a session **range**, and a named
  first cut. No row exists that is only content.
- The backbone total fits the session budget, or the overflow is explicitly cut here.
- Every deviation entry has a reason and a downstream binding; none was edited away.
- Every open thread has all four fields, and each *alive* thread was either scheduled or declared
  lost in this pass.
- The spotlight tally is built from the logs, and the next 2–3 protagonists are named.
- Tone shift, quiet session and resource low point are each scheduled to a specific chapter.
- The endgame's required seeds appear as delivery requirements in specific backbone rows.
- No tracked state (levels, resources, position, roster) is copied into this note (P10) — it links
  to the state hub instead.
- Run the profile's verification command (§9) — invariant as declared (typically 0 broken links).

## What NOT to do

- Do not write scenes, read-aloud text or trigger boxes here — that is `ttrpg-session-prep`.
- Do not assign exact session numbers to chapters; ranges, or the plan breaks on session two.
- Do not plan a chapter whose only description is its content.
- Do not record a deviation without its reason, and do not silently reverse one.
- Do not list a thread you cannot trace to a session log; do not leave a dead thread "alive".
- Do not copy levels, resources or a roster into this note.
- Do not distribute the spotlight equally per session; budget it across the arc.
- Do not leave the ending for the ending.
- Do not invent a backbone, a tone shift or a resource curve the profile does not support.
