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
>
> **The four states of a slot**, and what each means to every skill that reads it:
> a **leftover placeholder** = never asked, so stop and ask before producing anything that needs it;
> **`deferred: <when>`** = the answer belongs to a conversation that has not happened yet (session
> zero decides `B.distance`, `B.safety`, `D.tone`, `C.player_access`, `B.absence`) and reads exactly
> like empty — ask or drop, never guess, and never write `none` in its place; **`none`** = asked and
> answered empty, so the corresponding section is off, deliberately and durably; **a value** = use
> it, in the GM's own wording.
>
> **Declared defaults.** Four slots carry an explicit **`default:`** below (`B.hooks_count`,
> `C.inline_exception`, `D.recap`'s ceiling, `E.audit_cadence`). That declared value is
> the *only* thing a skill may put in place of an empty slot, and only while saying out loud that it
> did. Everywhere else the skill asks once or drops the section: a number that lives in a skill
> instead of here is a hardcoded constant with a friendlier name.
>
> **Two tiers, one schema.** Slots marked **`(core)`** are the minimum the cycle cannot start
> without. The setup interview offers a **quick start** that walks only those — plus the
> dependents a core answer implies (`A.resource` with a value drags its whole resource family —
> shape, scale, loss/gain, asymmetry, zero; `D.recap` with a form drags its ceiling) — writes `deferred: session zero` on the five that
> table owns, and leaves every other slot as an untouched placeholder: by the four-state rule
> that reads as *never asked*, so the first skill that needs one stops, asks once, and writes the
> answer back here. Core marks pace the interview; they change nothing about how a slot is read.
> Keep this note short. It is a data sheet, not a setting bible: link out to the long notes.

---

## §A — Game

- **`A.ruleset`** *(core)* — <the system and edition you play, in the terms you use for it, plus any
  supplement that changes preparation; `diceless` is an answer too>
- **`A.adjudicated`** — what the rules decide: <combat, resource attrition, social conflict…>
- **`A.fiction`** — what is deliberately never rolled for
- **`A.houserules`** — only the ones that change how a session is *prepared*
- **`A.resource`** *(core)* — the mechanic carrying the emotional weight: <name, or `none`>
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

- **`B.size`** *(core)* — how many players
- **`B.protagonists`** *(core)* — how many players carry a single session. With `B.size` this fixes the
  rotation period (P7); no skill may hardcode a constant instead, and this note offers none:
  a number here that nobody chose would be the constant, one indirection later.
- **`B.cadence`** — weekly / monthly / irregular
- **`B.horizon`** — expected total length of the campaign
- **`B.length`** — session length and hard stop; drives content margin (P8)
- **`B.absence`** — the fixed in-fiction convention for absent players, and whether they advance
- **`B.distance`** *(core)* — **`self-insert` | `close` | `fictional`**: how far the characters sit from the
  players themselves. `self-insert` (players portray themselves, under their own names) and `close`
  make the safety conversation, the hook harvest and the playstyle notes **load-bearing rather than
  optional**: material aimed at a character is aimed at a person. Any skill that harvests hooks,
  writes GM-facing notes about a player, or plans a scene aimed at one **must branch on this slot**.
- **`B.safety`** *(core)* — which tools, who may invoke them, what happens when invoked, refresh cadence.
  **Consent slots are the exception to `none`:** here and in `B.consent_recording` /
  `B.consent_offgame`, a `none` that nobody at the table pronounced reads as *unanswered*, not as a
  decision. Silence never switches a safety tool off
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
- **`B.hooks_count`** — how many exposed nerves to harvest per player. **`default:` 2–3**
- **`B.hooks_staging`** — <parallels the player connects on their own | literal appearances | both>
- **`B.language`** — language of play, and language of the repo if different. **Empty is one rule
  for every skill:** write in the language of the notes around you, say in the output which language
  you chose, and offer to record it here. Only a repo with nothing to infer from earns a question

## §C — Repository and artifacts

- **`C.root`** *(core)* — repo/vault root and folder map
- **`C.granularity`** — note granularity (e.g. one note per entity, small and linked)
- **`C.links`** *(core)* — link syntax and its escaping rules
- **`C.frontmatter`** — tag families; which values are properties. One key is **not** yours to
  declare: `type:` on package artifacts (`campaign-profile`, `session-prep`, `session-log`,
  `session-recap`, `entity`, `dossier`, `campaign-arc`) is the package's own cross-skill
  contract — fixed by the skills, identical in every campaign, and how one skill finds another's
  artifact whatever the file is named
- **`C.blocks`** — how your note system writes a **callout/admonition, a checkbox and a quote**.
  The skeletons in these skills show one dialect; a skill keeps the *roles* and renders them in
  yours. `plain headings and blockquotes` is a complete answer
- **`C.state_locations`** — which note holds which tracked value (the single sources of truth, P10)
- **`C.hub`** — the campaign state note every prep starts from
- **`C.arc_note`** / **`C.thread_ledger`** — where the arc plan, the deviation ledger and the open
  threads live. The ledger is the **only** home of a thread's status (P10): the hub views it
- **`C.verify`** — the verification command and its invariant (e.g. `0 broken links`)
- **`C.naming`** — file naming rules and forbidden characters
- **`C.portability`** *(setup-only)* — how this repo reaches your other machines, and where the
  canonical copies of skills and overlays live inside it. All persistent campaign memory lives in
  files here.
- **`C.inline_exception`** — which documents may inline source material and which must stay linked.
  **`default:` prep documents inline everything except stat blocks (P1)**
- **`C.gm_private`** — where GM-only material lives. **Required whenever `C.player_access` lets
  players read the repo.** A skill must never improvise this location.
- **`C.player_access`** — what players may read: player-facing reference, recaps, logs, nothing
- **`C.capture_paths`** — only if `B.consent_recording` is `yes`: raw audio folder (ignored by
  version control), transcript folder (versioned, and home of the per-session **speaker-map note**
  beside its transcript pair), naming rule. The **off-game note path** belongs here only when
  `B.consent_offgame` is also `yes` — otherwise the slot would promise a file that is never written.
  **Precedence:** for the off-game note, `C.player_access` / `C.gm_private` decide *whether and
  where* it may live and this slot only supplies a path that obeys them; if the two disagree, the
  access rule wins and the skill stops and asks. Reach is a consent question, not a layout one.

## §D — Campaign shape and content

- **`D.shape`** *(core)* — **`one-shot` | `series` | `open sandbox`**. The single most branch-heavy slot:
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
- **`D.tone`** *(core)* — dominant register, admitted breaks, and the recurring thematic pressure
- **`D.recap`** *(core)* — form of the opening recap (in-fiction prose / a verse form / none), who reads it,
  and the **reading-time ceiling** (minutes, or a form-native unit). **`default:` three to five
  minutes**, for the ceiling only — the form itself is never defaulted
- **`D.identity`** — the rule for what the recap calls each protagonist (real name, role, epithet).
  The per-character value lives in that player's dossier.

## §E — Declared overrides and working agreements

- **`E.overrides`** *(core)* — the principles this campaign deliberately **switches off or replaces**, each
  with one line of reason. P4, P5, P6, P7, P8, P9, P12 and P13 are strong defaults, not laws: a table
  that wants pure tactical play, or has no interest in a moral question per scene, declares it
  **here** and every skill obeys. P1, P2, P3, P10, P11, P14 and P15 are not overridable — violating
  them produces documents that fail at the table, state that silently desynchronises, or an
  assistant whose claims about its own run cannot be checked.
  Format: `P7 — off: all six players are protagonists every session by design.`
- **`E.deliverable`** — default output: a saved note in the repo, or a draft in chat
- **`E.review`** — how blunt the assistant should be; whether unsolicited improvement is wanted
- **`E.never_without_asking`** — e.g. renaming or reorganising existing notes
- **`E.retroactivity`** — may past material be corrected for consistency, and **where** corrections
  are recorded, so a retcon leaves a trace
- **`E.audit_cadence`** — how often the **continuity audit** runs. **`default:` every 3–5
  sessions**. Not the rotation check (that follows `B.protagonists`), and not `B.cadence`, which is
  how often you play

---

## Filled example (excerpt)

> The campaign below is **invented**, and deliberately not the one you are running: a worked
> example that named a real system or a real table would get copied instead of read. Notice the
> shape, not the content — every value is stated in that campaign's own terms.

> **`A.resource` — Salt.** `A.resource_shape`: shared party clock. `A.resource_scale`: a
> seven-notch dial on the crew's map, full when a voyage begins. Lost when an oath sworn on the
> water is broken, and one notch on any landfall made out of season; regained by giving back
> something the sea returned, and by a night at anchor spent telling the truth. **Asymmetry:** the
> crew holds it, the drowned can spend it against them and may never be given it. At zero: the next
> storm names one of them, and being named is permanent. At the table it lives as a dial everyone
> can reach and turn.

> **`B.distance` — self-insert.** The players portray themselves under their own names, in their own
> professions and cities. Hooks are real people they named; scenes aim at real nerves. Safety
> conversation refreshed before any heavy arc, not once at session zero.

> **`E.overrides` — none.** All defaults in force.
