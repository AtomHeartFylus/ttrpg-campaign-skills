---
name: ttrpg-session-log
description: "Write the session log: the authoritative record of what actually happened at the table, as opposed to what was prepped. Use when the user reports how the session went, or asks to write, update or complete the log (diary, after-action note, session record) for a session already played. Does not write the prep (see ttrpg-session-prep), the in-fiction opening recap (see ttrpg-table-recap), or process the recording and its transcript (see ttrpg-session-audio)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.5"
---

# Session log

Produces the note that records **what really happened**, distinct from the prep that was written
before. It is read by the recap writer, by the next prep, and by anyone reconstructing the
campaign a year later.

> **P11 — the log is the authority.** The cycle is `prep → play → log → recap → next prep`.
> What does not reach the log is lost within a month. Recordings and transcripts are memory aids,
> not minutes: on divergence, the log wins.

> **Deliberate exception to P10.** Every tracked value lives in exactly one place — the entity note.
> The **Exit state** section below is the single admitted exception: it freezes a historical snapshot
> of that night on purpose, and is never read as current state.

---

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled in this folder.
> A complete worked log for an **invented** campaign, annotated, is in
> [references/example-log.md](references/example-log.md) — a shape to calibrate on, never content
> to reuse; it logs the session `ttrpg-session-prep`'s example prepared.

## Phase 0 — Read the campaign profile

**Find it before declaring it missing.** Search the repo/vault root for a file named
`campaign-profile.md` (`rg --files -g campaign-profile.md`, or the equivalent), and **if that comes
back empty, search by frontmatter** (`rg -l "type: campaign-profile"`, or `grep -rl "type: campaign-profile" .` where ripgrep is absent): the schema declares that
type, `ttrpg-campaign-setup` explicitly tolerates a renamed profile, and no other skill may call a
renamed profile an absent one. A profile that exists but was not found re-interviews a GM who
already answered.

| Slot | Used for | If empty |
|---|---|---|
| `A.ruleset` | what "advancement" means here, in the measure that system uses (a step of progression, a milestone, or none at all) | record no advancement, only fiction |
| `A.resource` | whether Exit state carries a resource value at all | drop those rows — do not invent a resource |
| `A.resource_shape` | **the shape of the Exit-state rows** — see the branch below | `A.resource` set but shape empty → ask once, record the answer in the profile; **never default to per-character** |
| `A.resource_scale`, `A.resource_zero` | the units the Exit-state value is recorded in, and whether anyone crossed the threshold that ends a character — a zero-crossing is never a footnote, it is the headline of the session | record the bare number the GM reports, and ask what it means before writing any consequence |
| `B.language` | **the language the log is written in**, headings included | write in the language of the surrounding notes, say which you chose, and offer to record it |
| `B.absence` | who advances when absent | ask once: *do absent characters advance?*, then write it back |
| `B.distance`, `B.retention`, `C.gm_private` | **the gate on Phase 4's write-back to a player's dossier**: a new hook or a playstyle line is a note about a real person. Under `close` / `self-insert` record only what the player said on the record, keep it where `C.gm_private` says, and honour the retention rule | `B.distance` empty or `deferred` → ask before writing anything about the player; `C.gm_private` empty while players can read the repo → stop and ask; `B.retention` empty → say plainly the note is kept indefinitely |
| `B.size` | how many per-player moments to expect | ask table size |
| `D.guide` | the "was the prepared beat played, and how did it land?" question | drop that question |
| `D.shape` | one-shot / series / open sandbox — see the branch below | ask once; do not assume `series` |
| `D.backbone`, `D.official_material` | which official chapter/module the session covered | record the fiction only |
| `D.recap` | whether a recap follows, so the log's link/property points at it | leave the recap link empty |
| `C.root`, `C.naming`, `C.frontmatter`, `C.state_locations`, `C.hub`, `C.links`, `C.verify` | log path and name, frontmatter, dossier property names, state hub, verification command | write where told; skip link verification |
| `C.blocks` | how this vault writes the callouts and checkboxes the skeleton shows | keep the roles, render them as plain headings and blockquotes |
| `C.thread_ledger` | where a thread's status is updated when this session opens or pays one — the only place it lives (P10) | list the threads in *Pending for next session* and say once there is no ledger; do not start a rival list |
| `E.deliverable`, `E.retroactivity` | saved note vs. draft; whether past logs may be corrected | save the note, correct nothing retroactively |
| `E.overrides` | which strong defaults this table switched off — see the branch below | all defaults in force |

If the search finds no profile, run `ttrpg-campaign-setup` first — do not guess conventions.

**`E.overrides` branch — mandatory.** Read it before Phase 3 and drop what the table switched off,
saying once which override you honoured. Four overridable defaults reach this skill:

| Override | What stops being required here |
|---|---|
| `P7 — off` | the per-player accounting of who carried the evening and who was chorus, and the Diary entry that feeds the rotation check |
| `P8 — off` | *Missed opportunities* as a mandatory section: unplayed prep needs no recoverable/lost verdict |
| `P9 — off` | the derailment material the next red team would read — record what happened and stop |
| `P12 — off` | the wall between this internal record and player-facing text; naming players and mechanics is no longer a boundary the recap has to undo |

P1, P2, P3, P10 and P11 hold regardless: this note stays the authority for what happened, and no
tracked value is duplicated out of it — those are not preferences.

**`A.resource_shape` branch — mandatory.** The Exit state does **not** always have one row per
character. `per-character` → one row per character. `shared party clock` → **exactly one row for
the whole party**; per-character rows here invent state the game does not track. `per-faction` or
another per-entity shape → one row per entity, named as the profile names them. Empty with
`A.resource` set → ask once and record it; `A.resource` empty → no resource rows at all.

**`D.shape` branch — mandatory.** `series` → as written. `one-shot` → no previous log and no next
session: drop Phase 1 input 2, drop *Pending for next session*, and let *Narrative seeds* become a
short note of what the ending deliberately left open. `open sandbox` → *Pending* is written against
the **active fronts** (which moved, which advanced while the party was elsewhere), not a chapter.
**Empty → ask once**; do not assume `series`.

## Phase 1 — Read before asking

1. **The prep of the session just played** (locate it by its `type: session-prep` frontmatter
   when names vary). Its top global-threads callout (P2) is your checklist:
   each thread either happened or became a **missed opportunity**; its per-scene trigger boxes are
   the second pass. Note which scenes were optional (P8).
2. **The previous session log.** Its *Pending for next session* checklist — resolved, still open,
   or overtaken.
3. **The dossiers of the players present.** Current tracked properties, open hooks/bonds,
   playstyle notes you may have to update.
4. **The transcript, if one exists** (see `ttrpg-session-audio`). Memory aid only: names and
   campaign terms come out mangled and speaker turns are unreliable (P11). Never paste it in.
   Its **speaker-map note** sits beside it and is owned by that skill: read it to attribute a
   moment, never copy the table into this log.

If the prep note cannot be found, say so and proceed from testimony alone — the missed-opportunity
section is then guesswork and must be marked as such.

## Phase 2 — Collect the facts

The GM supplies scattered bullets. Fill the gaps with **targeted questions, maximum 2 at a time**,
only about what is actually missing. Skip any question whose profile slot is empty.

1. **Present / absent** — who was at the table? (drives advancement, per `B.absence`)
2. **Deviations from prep** — what went differently? Walk the global-threads callout: which
   triggers were played? **Triggers never played become *missed opportunities*.**
3. **Memorable moments, per player** — who carried a scene, notable portrayal, unexpected choices;
   one line per player present, not one for the evening.
4. **The recurring guide's beat** (`D.guide`) — played? how did it land?
5. **Hooks and bonds that emerged** — new names invoked, relationships exposed, backstory that
   surfaced in play.
6. **Exit state** — advancement, dramatic-resource values at the granularity `A.resource_shape`
   declares, rewards handed out, deaths and what followed, where each character ended the night.
7. **Narrative seeds** — lines or choices by the players that are reusable as future hooks.

**Invent nothing.** An unconfirmed fact is asked about or omitted; a plausible reconstruction
written as fact poisons every downstream document (P11).

## Phase 3 — Write the log

Path, file name and frontmatter per `C.root` / `C.naming` / `C.frontmatter`. Callout syntax below
is illustrative — render them as `C.blocks` declares.

> **The skeleton is structural; its labels are not English.** The headings below name *sections*,
> not wording. **Write every heading, table column and parenthetical label in `B.language`**, so the
> note reads as one document instead of English scaffolding over prose in another language. Keep the
> section *order* and *meaning*; translate the words. If `B.language` is empty, match the notes
> already in the repo and **state which language you chose** — `ttrpg-table-recap`, whose fallback is
> "the language of the log", must inherit a decision rather than an accident.

```markdown
---
type: session-log   <!-- fixed package key: how recap, next prep and audit FIND this artifact -->
<frontmatter per C.frontmatter: session tag, chapter/front tag, log tag;
 properties linking prep and recap so the hub's query self-populates>
---

# Session N — Log (<place, chapter or front>)   <!-- blocks per C.blocks, headings in B.language -->

> [!info] What this note is
> The record of what actually happened, not the prep (<link to the prep note>).

## At a glance
(table: Covered / Present / Absent / Outcome)

## What actually happened
(bullets in play order; deviations from prep marked; players named where they carried a moment)

## Missed opportunities (to recover)
(prep triggers never played + how each seed can come back, or a declaration that it is lost)

## Hooks and bonds that emerged
(only if there is something new)

## Exit state
(advancement — present characters only; resource rows at the granularity A.resource_shape
 declares — per character, ONE for the party, or one per entity; rewards; anomalies explained)

## Narrative seeds

## Pending for next session          <!-- drop entirely when D.shape is one-shot -->
(checklist: to do, to collect, to decide)
```

Rules for the body:

- **The full roster goes only in the first log, or when it changes.** Afterwards present/absent is
  enough — the roster is not state you duplicate (P10).
- **Missed opportunities are written as recoverable or lost, never as a silent gap.** A prep
  trigger that vanished without a line is the exact thing that disappears within a month. Mirrors
  the prep's content-margin rule (P8).
- **Name the player behind a moment** in the log — it is the internal document. What crosses into
  player-facing text is `ttrpg-table-recap`'s problem, not yours (P12).
- Keep *What actually happened* in play order and factual; mark interpretation as interpretation.

## Phase 4 — Update the state (P10)

The log is a record; the **current** values live in the entity notes. `ttrpg-table-dossier` owns
the shape of a player dossier and runs downstream of this skill — write the values, do not
redesign the note.

- **Player dossiers** (paths and property names per `C.state_locations`):
  - advancement — **only for the players present**, per the `B.absence` rule; absent characters
    stay behind and catch up when they play. If `B.absence` is silent, ask once and then record
    the answer in the profile rather than deciding session by session.
  - dramatic-resource value (`A.resource`), rewards held, and any other tracked property —
    end-of-session values, overwritten not appended. Where `A.resource_shape` is a shared party
    clock, the value belongs to the party's note, **not** copied into each dossier (P10).
  - **one Diary entry per session the player attended**, linking this note and marked *carried* or
    *chorus*: that mark is the rotation check's only input, so a chorus evening with no entry reads
    as an absence. The individual moment is the entry's content when there was one.
  - new hooks/bonds; and update the playstyle notes if the evening revealed something new about
    the player — that section is what feeds the next red team (P9).
- **The thread ledger** (`C.thread_ledger`): threads this session **opened, advanced or paid** get
  their row updated there — the only place a thread's *status* lives (P10), shaped by
  `ttrpg-campaign-arc` — citing this log as the seeding or paying session. This note keeps the
  *history*, never the status. Slot empty → list them in *Pending for next session*, say once that
  there is no ledger yet, and do not open a rival list.
- **The campaign state hub** (`C.hub`): if `C.frontmatter` declares queries/views driven by properties, correct
  frontmatter is the whole update — **do not hand-edit generated tables**. Update by hand only
  what lives in no property and in no ledger: last session played, where the characters are, what
  comes next. **Not the open threads**: the hub views the ledger, it does not retype it.
- **Never copy a tracked value into an index, a prep note or a summary table** (P10). The only
  frozen copy is this log's *Exit state*.

## Phase 5 — Verify and hand off

- The global-threads callout of the prep has been walked item by item; nothing silently dropped.
- Every player present has either a named moment or an explicit note that they were chorus (P7)
  — **while `E.overrides` leaves P7 in force**; with `P7 — off` the evening is recorded without
  per-player accounting, and the header says so.
  **State no threshold here:** how long is too long is one number, defined once in
  `ttrpg-table-dossier` from `B.size / B.protagonists`. This log records the fact; that skill's
  rotation check reads the diaries and decides whether it is a finding.
- Advancement applied to present characters only; no tracked value duplicated outside *Exit state*.
- No invented fact: everything in the note was reported, or read from prep/transcript with the
  divergence resolved in favour of testimony (P11).
- Headings and labels are in `B.language`; the note is not English scaffolding over other prose.
- Exit-state rows match `A.resource_shape` — no per-character rows for a shared clock.
- Links follow `C.links` syntax; run the `C.verify` command — invariant as declared
  (typically **0 broken links**).
- Commit as a single change with a descriptive message (e.g. *add Session N log + update present
  dossiers*), if `E.deliverable` asks for commits at all. Do not commit if it does not.

Then say what is now unblocked: the recap (`ttrpg-table-recap`) reads *What actually happened*, if
`D.recap` declares one; the next prep (`ttrpg-session-prep`) reads *Exit state*, *Missed
opportunities* and *Pending* — for a one-shot, only *Exit state* exists and nothing is unblocked.

## What NOT to do

- Do not invent, smooth over or reconstruct a fact you were not told.
- Do not ask more than 2 questions at a time, and do not ask about slots the profile leaves empty.
- Do not advance or reward absent characters against the `B.absence` convention.
- Do not hardcode one Exit-state row per character; read `A.resource_shape` and follow it.
- Do not write English headings over a log in another language; translate the skeleton.
- Do not state your own chorus threshold — cite `ttrpg-table-dossier`'s.
- Do not paste transcript text into the log, and do not treat the transcript as authoritative.
- Do not write the evening as one undifferentiated summary — per-player moments are the point
  (P7; moot when the profile switches it off).
- Do not let a prep trigger disappear without becoming a missed opportunity or an explicit loss
  (P8; moot when the profile switches it off).
- Do not copy advancement, resources or thread status into the hub, an index or the next prep.
- Do not put mechanics, meta or player names into anything meant to be read to the table (P12).
- Do not write the in-fiction recap here — the log is internal, unpoetic and complete.
