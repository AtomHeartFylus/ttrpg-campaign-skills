---
name: ttrpg-campaign-arc
description: "Produce and maintain the arc note that plans the campaign above the single session: backbone table, canon-vs-homebrew deviation ledger, open-thread tracker, pacing over the campaign horizon and a seeded endgame. Use when asked to plan an arc, season or chapter, to review where the campaign is going, to check which threads are still open, or to decide what the next few sessions must deliver. Covers what each chapter must deliver, why each divergence from the source was made, who owns each unpaid seed, and the forward commitment of who is protagonist in the next few sessions. Requires an ongoing campaign: it does not serve a one-shot. Does not measure spotlight fairness or decide whether anyone has been chorus too long (see ttrpg-table-dossier, which owns the rotation formula and the ledger), does not write a playable session (see ttrpg-session-prep), record a played one (see ttrpg-session-log), or audit the repo for drift (see ttrpg-continuity-audit)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.1"
---

# Campaign arc

Produces **one living arc note** — the layer between the campaign profile (facts that do not
change) and session prep (one evening). It is read when deciding what the *next few* sessions must
do, and rewritten in place after every chapter boundary.

**This skill plans; it does not write a session.** The moment you are writing read-aloud text,
scenes or trigger boxes, you are in `ttrpg-session-prep` and should stop here.

> **`D.shape` gate — read it before anything else, and be willing to stop.**
> This skill plans **across** sessions. That layer does not exist for every campaign.
>
> - **`series`** → the skill as written.
> - **`one-shot`** → **this skill does not serve a one-shot. Say so and stop.** There is no session
>   budget, no chapter boundary, no rotation across sessions, no deviation accumulating over months
>   and no endgame to seed early — the endgame is tonight. Do not produce a one-row arc note: an
>   arc note for a single evening is `ttrpg-session-prep`'s job wearing the wrong name. Report that
>   the shape excludes this skill and route the user to prep. **Degrading silently into a
>   near-empty arc note is the failure this gate exists to prevent.**
> - **`open sandbox`** → the skill runs, with one substitution applied throughout: **every backbone
>   row is a front**, not a chapter, and "what it must deliver" becomes "what it presses on if the
>   party never intervenes". Pacing and the endgame remain; the linear ordering does not.
> - **empty** → **ask once** which of the three this campaign is, write the answer into the profile,
>   and do not assume `series`.

---

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

**Supporting reference:** [references/arc-elements.md](references/arc-elements.md) — how each
section of the arc note is built (backbone rows, deviation ledger, thread tracker, pacing,
endgame). Read it while writing the note; Phase 3 below carries only the summary.

## Phase 0 — Read the campaign profile

**Find it before declaring it missing.** Search the repo/vault root for a file named
`campaign-profile.md` (`rg --files -g campaign-profile.md`, or the equivalent) before concluding
there is none. A profile that exists but was not found re-interviews a GM who already answered.

| Slot | Used for | If empty |
|---|---|---|
| `D.shape` | **the gate above** — whether this skill runs at all | **ask once**; never assume `series` |
| `A.ruleset` | level/progression checkpoints the backbone must respect | plan in fiction only, no progression row |
| `A.resource` | the arc-level curve: where it must be lowest, where it can be regained | drop the curve column entirely |
| `D.tone` | where the register must shift, and which breaks are admitted | ask once; do not invent tone shifts |
| `D.canon_source` | which part of the corpus each chapter leans on | drop the canon column and the deviation ledger |
| `D.guide` | the guide's arc across the campaign and where it resolves | drop that row |
| `D.backbone`, `D.unit`, `D.deviation_policy` | the backbone itself: modules/chapters vs homebrew vs fronts; how deviations are recorded | ask once — without it there is no backbone to map |
| `D.endgame` | the declared endings and the conditions selecting between them | ask once; seeds cannot wait for the last chapter |
| `B.cadence`, `B.horizon` | cadence × horizon = the session budget | ask cadence; it is load-bearing here |
| `B.size`, `B.protagonists` | passed through to `ttrpg-table-dossier`'s rotation check — **not recomputed here** | that skill asks; do not substitute a number |
| `C.arc_note`, `C.thread_ledger`, `C.hub`, `C.links`, `C.verify` | where the arc note and ledger live, link syntax, verification command | ask where the note goes |
| `E.review`, `E.never_without_asking`, `E.overrides` | how blunt the review is; what may not be changed without asking; which defaults are off | propose, do not restructure |

If the search finds no profile, run `ttrpg-campaign-setup` first — do not guess a backbone.

## Phase 1 — Read before planning, in this order

1. **The campaign state hub** (`C.hub`): where the party is, what is next, what is unresolved.
   *If it contradicts the last session log, stop and say so* — the log wins (P11) and everything
   planned on a stale hub is wrong.
2. **Every session log since the last arc pass.** Extract, per session: seeds planted, hooks left
   unpaid, promises made at the table, who was actually protagonist, where the register drifted,
   and which planned content was skipped.
3. **The backbone source** (`D.backbone`): the module/chapter list, or the list of fronts.
   What each unit *contains* versus what it must *deliver here*.
4. **The player dossiers**: hooks and exposed nerves that have never been touched; **who is owed a
   session, read from `ttrpg-table-dossier`'s rotation check rather than recounted here**; who is
   leaving or joining.
5. **The previous arc note.** What was predicted and did not happen is the most useful input you
   will get: it is where the plan was too tight.

## Phase 2 — The arc note

```markdown
---
<frontmatter per C.frontmatter>
---

# <Campaign> — Arc

> Planning layer. Current state lives in <state hub>; what happened lives in the session logs.
> Nothing here is a source of truth for state (P10).

## Session budget
<B.cadence × B.horizon = N sessions; sessions played; sessions left; what that buys>

## Backbone            <!-- rows are FRONTS when D.shape is open sandbox -->
| Chapter / region / front | Sessions (range) | What it must deliver | Tone shift | Resource curve | Status |
|---|---|---|---|---|---|

## Deviation ledger
| # | What the source says | What we do instead | Why | What it binds downstream | Since |
|---|---|---|---|---|---|

## Open threads
| Thread | Seeded in | Owner | What would pay it off | Status |
|---|---|---|---|---|

## Protagonists committed next
<a forward commitment only — who carries the next 2–3 sessions and on which of their hooks.
 NO tally table: the ledger and the threshold live in ttrpg-table-dossier>

## Pacing
<where the register shifts; where the quiet session goes; where the endgame seeding starts>

## Endgame
<the final beats, the conditions that select between endings, what is deliberately left open>
```

## Phase 3 — Required elements

Each section of the skeleton is built as [references/arc-elements.md](references/arc-elements.md)
specifies — read it while writing. The summary:

| Section | The non-negotiable |
|---|---|
| Backbone | one row per chapter **or front**; a session **range**, never a number; a *function*, not content; a named first cut (P8) |
| Deviation ledger | every divergence carries its **reason** and what it **binds downstream**; append-only; drop the section only when there is no source material at all |
| Open threads | four mandatory fields; **seeded-in must cite a log** or it is an idea, not a thread; *lost* is a legitimate status |
| Pacing | cadence × horizon is stated out loud, and the overflow is cut **here**, not by exhaustion later |
| Endgame | the final beats, what must already exist for them to land, and **in which session it is planted** |

### Protagonists committed next (P7) — this skill does **not** own the ledger
**`ttrpg-table-dossier` owns the rotation formula, the tolerance and the ledger**, derived per
player from the dossier diaries. It answers *has anyone been chorus too long?* **Do not restate the
arithmetic, do not state a threshold, and do not build a tally table here** — two tallies from two
sources drift, and the one you keep in the arc note is the one nobody updates.

What this skill owns is the **forward commitment**: read that skill's rotation check, then decide
*which* of the coming backbone rows each owed player gets. Assign the chapter or front whose
*function* matches that player's untouched nerve. Name the next 2–3 protagonists and the hook each
is built on, and write it where prep will read it. That is scheduling, not measurement.

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
- The next 2–3 protagonists are **named as a commitment**, each tied to a backbone row and a hook.
  No tally table, no threshold and no rotation arithmetic appears in this note — that check was
  read from `ttrpg-table-dossier`, not recomputed.
- `D.shape` was read before Phase 1: a one-shot was refused outright, a sandbox has fronts.
- Tone shift, quiet session and resource low point are each scheduled to a specific chapter.
- The endgame's required seeds appear as delivery requirements in specific backbone rows.
- No tracked state (levels, resources, position, roster) is copied into this note (P10) — it links
  to the state hub instead.
- Run the `C.verify` command — invariant as declared (typically 0 broken links).

## What NOT to do

- Do not write scenes, read-aloud text or trigger boxes here — that is `ttrpg-session-prep`.
- Do not assign exact session numbers to chapters; ranges, or the plan breaks on session two.
- Do not plan a chapter whose only description is its content.
- Do not record a deviation without its reason, and do not silently reverse one.
- Do not list a thread you cannot trace to a session log; do not leave a dead thread "alive".
- Do not copy levels, resources or a roster into this note.
- Do not distribute the spotlight equally per session; commit named protagonists forward.
- Do not build a spotlight tally table, restate the rotation formula, or name a threshold for how
  long is too long as chorus — `ttrpg-table-dossier` owns all three and this note reads its answer.
- Do not run this skill for a one-shot, and do not soften the refusal into a one-row arc note.
- Do not leave the ending for the ending.
- Do not invent a backbone, a tone shift or a resource curve the profile does not support.
