---
type: campaign-profile
schema: 2
---

# Campaign Profile — <Campaign name>

> This note is the **contract between your campaign and the base skills**. Every skill in
> `ttrpg-campaign-skills` reads it before doing anything, and speaks in the slot names below
> instead of the vocabulary of one game.
>
> **Sections are named, not numbered** (`§A`…`§E`). Slots are cited as `§B.consent`, `§D.shape`.
> Adding a slot never renumbers another one — the previous numbered scheme drifted the moment
> three authors added slots in parallel.
>
> Slots marked **`(setup-only)`** are recorded for the humans and for the setup interview; no skill
> branches on them. Every other slot must be read by at least one skill — an unread slot is either
> dead weight or a missing Phase 0 row, and `scripts/check_contract.py` fails on it.
>
> **Empty slots are legitimate**: they switch the corresponding sections of a skill *off*.
> A skill may never invent a slot value it cannot find here — it asks, or drops the section.
> Keep this note short. It is a data sheet, not a setting bible: link out to the long notes.

---

## §A — Game

- **`A.ruleset`** — <e.g. D&D 5e + a supplement / Call of Cthulhu 7e / a PbtA hack / diceless>
- **`A.adjudicated`** — what the rules decide: <combat, resource attrition, social conflict…>
- **`A.fiction`** — what is deliberately never rolled for
- **`A.houserules`** — only the ones that change how a session is *prepared*
- **`A.resource`** — the mechanic carrying the emotional weight: <name, or `none`>
- **`A.resource_shape`** — <per-character | shared party clock | per-faction | other: describe>
  Decides whether a log's exit state has one row per character, one row, or one per entity.
- **`A.resource_scale`** — starting value and units, in the game's own terms
- **`A.resource_loss` / `A.resource_gain`** — the named triggers, each side
- **`A.resource_asymmetry`** — who may hold, give or receive it, and who may not
- **`A.resource_zero`** — what happens at zero
- **`A.resource_handling`** *(setup-only)* — how it lives at the table (tokens, tracker, sheet);
  the gesture is part of the mechanic

> `A.resource` = `none` switches off every resource section in prep, log and arc. Do not invent one.

## §B — Table

- **`B.size`** — how many players
- **`B.protagonists`** — how many players carry a single session (default 2–3). With `B.size` this
  fixes the rotation period (P7); no skill may hardcode a constant instead.
- **`B.cadence`** — weekly / monthly / irregular
- **`B.horizon`** — expected total length of the campaign
- **`B.length`** — session length and hard stop; drives content margin (P8)
- **`B.absence`** — the fixed in-fiction convention for absent players, and whether they advance
- **`B.distance`** — **`self-insert` | `close` | `fictional`**: how far the characters sit from the
  players themselves. `self-insert` (players portray themselves, under their own names) and `close`
  make the safety conversation, the hook harvest and the playstyle notes **load-bearing rather than
  optional**: material aimed at a character is aimed at a person. Any skill that harvests hooks,
  writes GM-facing notes about a player, or plans a scene aimed at one **must branch on this slot**.
- **`B.safety`** — which tools, who may invoke them, what happens when invoked, refresh cadence
- **`B.consent_recording`** — **is the table recorded, and who has explicitly agreed?** A skill may
  not start or continue a capture pipeline without an explicit `yes` here. Empty or `no` → stop and
  ask; never infer consent from the existence of an audio file.
- **`B.consent_offgame`** — separate and narrower: **may the out-of-character talk of the evening be
  curated into a durable, themed, timecoded note?** Agreeing to be recorded is not agreeing to be
  indexed. Explicit `yes`, per person. Empty or `no` → transcripts and session-log material are
  produced as normal and the off-game note simply is not written. Never inferred from
  `B.consent_recording`. Whoever is indexed may have any entry removed without discussion, which is
  why entries are short pointers with timecodes and never reproductions.
- **`B.frame`** — the cultural, historical or genre register a figure must belong to in order to
  land with *this* table; which real or public figures are admissible and how they are handled.
  When someone names a subject outside the frame, cast the nearest parallel inside it.
- **`B.retention`** — how long GM-facing material *about the real people at the table* is kept:
  playstyle notes, harvested hooks, off-game entries, transcripts. State the rule and who can
  trigger a deletion. Anyone described may have an entry removed on request, without discussion;
  this slot says what happens by default to everything nobody asks about. Empty → a skill writing
  such material says it is keeping it indefinitely, and offers to set the rule.
- **`B.hooks_count`** — how many exposed nerves to harvest per player (default 2–3)
- **`B.hooks_staging`** — <parallels the player connects on their own | literal appearances | both>
- **`B.language`** — language of play, and language of the repo if different

## §C — Repository and artifacts

- **`C.root`** — repo/vault root and folder map
- **`C.granularity`** — note granularity (e.g. one note per entity, small and linked)
- **`C.links`** — link syntax and its escaping rules
- **`C.frontmatter`** — tag families; which values are properties
- **`C.state_locations`** — which note holds which tracked value (the single sources of truth, P10)
- **`C.hub`** — the campaign state note every prep starts from
- **`C.arc_note`** / **`C.thread_ledger`** — where the arc plan, deviation ledger and open threads live
- **`C.verify`** — the verification command and its invariant (e.g. `0 broken links`)
- **`C.naming`** — file naming rules and forbidden characters
- **`C.portability`** *(setup-only)* — how this repo reaches your other machines, and where the
  canonical copies of skills and overlays live inside it. All persistent campaign memory lives in
  files here.
- **`C.inline_exception`** — which documents may inline source material (default: prep documents,
  everything except stat blocks — P1) and which must stay linked
- **`C.gm_private`** — where GM-only material lives. **Required whenever `C.player_access` lets
  players read the repo.** A skill must never improvise this location.
- **`C.player_access`** — what players may read: player-facing reference, recaps, logs, nothing
- **`C.capture_paths`** — only if `B.consent_recording` is `yes`: raw audio folder (ignored by
  version control), transcript folder (versioned), naming rule. The **off-game note path** belongs
  here only when `B.consent_offgame` is also `yes` — otherwise the slot would promise a file that is
  never written.

## §D — Campaign shape and content

- **`D.shape`** — **`one-shot` | `series` | `open sandbox`**. The single most branch-heavy slot:
  a one-shot has no previous log, no arc note, no rotation across sessions and no recap; a sandbox
  has fronts instead of chapters. Every skill declares what it does for each value; a skill that
  cannot serve a value must say so and stop, not degrade silently.
- **`D.backbone`** — published modules / chapters / fully homebrew / fronts
- **`D.unit`** — what one session covers
- **`D.official_material`** / **`D.own_material`** *(setup-only)* — where each lives; placement of
  new notes is governed by `C.root`
- **`D.deviation_policy`** — how much you diverge from the source, and where divergences are recorded
- **`D.endgame`** — the declared possible endings and the conditions that select between them.
  Seeds are planted early, so this cannot wait for the last chapter.
- **`D.canon_source`** — a text or corpus the campaign quotes: which, its status in-world
  (verbatim canon / rewritten / does not exist in-world), how it is delivered at the table, where
  recordings live
- **`D.guide`** — a recurring anchor NPC: who, their arc, their voice in one line, and whether they
  owe a prepared beat every session
- **`D.tone`** — dominant register, admitted breaks, and the recurring thematic pressure
- **`D.recap`** — form of the opening recap (in-fiction prose / a verse form / none), who reads it,
  and the **reading-time ceiling** (minutes, or a form-native unit)
- **`D.identity`** — the rule for what the recap calls each protagonist (real name, role, epithet).
  The per-character value lives in that player's dossier.

## §E — Declared overrides and working agreements

- **`E.overrides`** — the principles this campaign deliberately **switches off or replaces**, each
  with one line of reason. P5, P6, P7, P8, P9, P12 and P13 are strong defaults, not laws: a table
  that wants pure tactical play, or has no interest in a moral question per scene, declares it
  **here** and every skill obeys. P1, P2, P3, P10 and P11 are not overridable — violating them
  produces documents that fail at the table or state that silently desynchronises.
  Format: `P7 — off: all six players are protagonists every session by design.`
- **`E.deliverable`** — default output: a saved note in the repo, or a draft in chat
- **`E.review`** — how blunt the assistant should be; whether unsolicited improvement is wanted
- **`E.never_without_asking`** — e.g. renaming or reorganising existing notes
- **`E.retroactivity`** — may past material be corrected for consistency, and **where** corrections
  are recorded, so a retcon leaves a trace
- **`E.audit_cadence`** — how often the continuity audit runs

---

## Filled example (excerpt)

> **`A.resource` — Hope.** `A.resource_shape`: per-character. 33 points each. Lost by accepting a
> sin (cost 2), by dying, by circle-specific hazards; regained through acts of mercy, familiar
> spirits, inspiration, surviving your own circle. **Asymmetry:** the damned cannot receive it.
> At zero: a despair roll, three per campaign, failure is permanent loss. At the table it lives in
> physical tokens handed across the table.

> **`B.distance` — self-insert.** The players portray themselves under their own names, in their own
> professions and cities. Hooks are real people they named; scenes aim at real nerves. Safety
> conversation refreshed before any heavy arc, not once at session zero.

> **`E.overrides` — none.** All defaults in force.
