---
name: ttrpg-session-log
description: "Write the session log: the authoritative record of what actually happened at the table, as opposed to what was prepped. Use when the user reports how the session went, or asks to write, update or complete the log (diary, after-action note, session record) for a session already played. Covers fact collection by targeted questions without inventing, deviations from prep checked against the prep's global-threads callout, per-player memorable moments, the frozen exit state, narrative seeds, the pending checklist for the next session, and the state updates in player dossiers and the campaign hub. Does not write the prep (see ttrpg-session-prep), the in-fiction opening recap (see ttrpg-table-recap), or process the recording and its transcript (see ttrpg-session-audio)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Session log

Produces the note that records **what really happened**, distinct from the prep that was written
before. It is read by the recap writer, by the next prep, and by anyone reconstructing the
campaign a year later.

> **P11 — the log is the authority.** The cycle is `prep → play → log → recap → next prep`.
> What does not reach the log is lost within a month. Recordings and transcripts are memory aids,
> not minutes: on divergence, the log wins.

> **Deliberate exception to P10.** Every tracked value lives in exactly one place — the entity
> note. The **Exit state** section below is the single admitted exception: it freezes a historical
> snapshot of that night on purpose, and is never read as current state.

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

| Slot | Used for | If empty |
|---|---|---|
| §1 System | what "advancement" means here (level / XP / milestone / none) | record no advancement, only fiction |
| §2 Dramatic resource | the end-of-session value per character in Exit state | drop those columns — do not invent a resource |
| §5 Recurring guide | the "was the prepared beat played, and how did it land?" question | drop that question |
| §6 Structure | which official chapter/module the session covered | record the fiction only |
| §7 Table conventions | who levels when absent; table size drives how many per-player moments | ask once: *do absent characters advance?* |
| §8 Player-facing outputs | whether a recap follows, so the log's link/property points at it | leave the recap link empty |
| §9 Repo conventions | log path and name, frontmatter, dossier property names, state hub, verification command | write where told; skip link verification |
| §10 Working agreements | saved note vs. draft; whether past logs may be corrected | save the note, correct nothing retroactively |

If the profile is missing, run `ttrpg-campaign-setup` first — do not guess conventions.

## Phase 1 — Read before asking

1. **The prep of the session just played.** Its top global-threads callout (P2) is your checklist:
   each thread either happened or became a **missed opportunity**. Its per-scene trigger boxes are
   the second pass. Also note which scenes were optional (P8).
2. **The previous session log.** Its *Pending for next session* checklist — resolved, still open,
   or overtaken.
3. **The dossiers of the players present.** Current tracked properties, open hooks/bonds,
   playstyle notes you may have to update.
4. **The transcript, if one exists** (see `ttrpg-session-audio`). Memory aid only: names and
   campaign terms come out mangled and speaker turns are unreliable (P11). Never paste it in.

If the prep note cannot be found, say so and proceed from testimony alone — but then the
missed-opportunity section is guesswork and must be marked as such.

## Phase 2 — Collect the facts

The GM supplies scattered bullets. Fill the gaps with **targeted questions, maximum 2 at a time**,
and only about what is actually missing. Skip any question whose profile slot is empty.

1. **Present / absent** — who was at the table? (drives advancement, per §7)
2. **Deviations from prep** — what went differently? Walk the global-threads callout: which
   triggers were played? **Triggers never played become *missed opportunities*.**
3. **Memorable moments, per player** — who carried a scene, notable portrayal, unexpected choices.
   One line per player present is the target, not one line for the evening.
4. **The recurring guide's beat** (§5) — played? how did it land?
5. **Hooks and bonds that emerged** — new names invoked, relationships exposed, backstory that
   surfaced in play.
6. **Exit state** — advancement, dramatic-resource values (§2), rewards handed out, deaths and
   what followed, where each character physically ended the night.
7. **Narrative seeds** — lines or choices by the players that are reusable as future hooks.

**Invent nothing.** An unconfirmed fact is either asked about or omitted. A plausible
reconstruction written as fact poisons every downstream document (P11).

## Phase 3 — Write the log

Path, file name and frontmatter per profile §9. Callout syntax below is illustrative — use plain
headings if the vault does not support callouts.

```markdown
---
<frontmatter per §9: session tag, chapter tag, log tag;
 properties linking prep and recap so the hub's query self-populates>
---

# Session N — Log (<place or chapter>)

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
(advancement — present characters only; dramatic-resource values; rewards; anomalies explained)

## Narrative seeds

## Pending for next session
(checklist: to do, to collect, to decide)
```

Rules for the body:

- **The full roster goes only in the first log, or when it changes.** Afterwards
  present/absent is enough — the roster is not state you duplicate (P10).
- **Missed opportunities are written as recoverable or lost, never as a silent gap.** A prep
  trigger that vanished without a line is the exact thing that disappears within a month. Mirrors
  the prep's content-margin rule (P8).
- **Name the player behind a moment** in the log — it is the internal document. Player names never
  cross into player-facing text (P12); that is `ttrpg-table-recap`'s problem, not yours.
- Keep *What actually happened* in play order and factual. Interpretation, if any, is marked as
  interpretation.

## Phase 4 — Update the state (P10)

The log is a record; the **current** values live in the entity notes. `ttrpg-table-dossier` owns
the shape of a player dossier and runs downstream of this skill — write the values, do not
redesign the note.

- **Player dossiers** (paths and property names per §9):
  - advancement — **only for the players present**, per the §7 absent-player rule; absent
    characters stay behind and catch up when they play. If §7 is silent, ask once and then record
    the answer in the profile rather than deciding session by session.
  - dramatic-resource value (§2), rewards held, and any other tracked property — end-of-session
    values, overwritten not appended.
  - a one-line entry in the dossier's own log section for an individual moment, linking this note.
  - new hooks/bonds; and update the playstyle notes if the evening revealed something new about
    the player — that section is what feeds the next red team (P9).
- **The campaign state hub:** if §9 declares queries/views driven by frontmatter, correct
  frontmatter is the whole update — **do not hand-edit generated tables**. Update by hand only
  what lives in no property: last session played, where the characters are, what comes next,
  threads still open.
- **Never copy a tracked value into an index, a prep note or a summary table** (P10). The only
  frozen copy is this log's *Exit state*.

## Phase 5 — Verify and hand off

- The global-threads callout of the prep has been walked item by item; nothing silently dropped.
- Every player present has either a named moment or an explicit note that they were chorus (P7) —
  a player who is chorus three sessions running is a finding worth reporting to the GM.
- Advancement applied to present characters only; no tracked value duplicated outside *Exit state*.
- No invented fact: everything in the note was reported, or read from prep/transcript with the
  divergence resolved in favour of testimony (P11).
- Links follow §9 syntax; run the profile's verification command — invariant as declared
  (typically **0 broken links**).
- Commit as a single change with a descriptive message (e.g. *add Session N log + update present
  dossiers*), if §10 asks for commits at all. Do not commit if it does not.

Then say what is now unblocked: the recap (`ttrpg-table-recap`) reads *What actually happened*, if
§8 declares one; the next prep (`ttrpg-session-prep`) reads *Exit state*, *Missed opportunities* and *Pending*.

## What NOT to do

- Do not invent, smooth over or reconstruct a fact you were not told.
- Do not ask more than 2 questions at a time, and do not ask about slots the profile leaves empty.
- Do not level, reward or advance absent characters against the §7 convention.
- Do not paste transcript text into the log, and do not treat the transcript as authoritative.
- Do not write the evening as one undifferentiated summary — per-player moments are the point.
- Do not let a prep trigger disappear without becoming a missed opportunity or an explicit loss.
- Do not copy levels, resources or open threads into the hub, an index or the next prep.
- Do not put mechanics, meta or player names into anything meant to be read to the table (P12).
- Do not write the in-fiction recap here — the log is internal, unpoetic and complete.
