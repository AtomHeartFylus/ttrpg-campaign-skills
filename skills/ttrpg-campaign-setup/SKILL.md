---
name: ttrpg-campaign-setup
description: "Bootstrap a campaign repository and produce its filled campaign-profile.md — the contract every other ttrpg-* skill reads — or adopt and audit a repo that already has material. Use when starting a campaign vault, filling or revising the campaign profile, or establishing the conventions of a repo that grew without them. Does not run session zero or write player dossiers (see ttrpg-table-dossier), write session prep (see ttrpg-session-prep), or chase drift and dangling threads (see ttrpg-continuity-audit)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.18"
---

# Campaign setup

Produces the **filled campaign profile** — the contract every other skill in this package reads
first — plus the folder skeleton, the state hub and the conventions the profile declares.
Read by an agent that starts cold on a machine it has never seen before.

> **The deliverable is the profile.** Folders, hubs and scripts are what its answers imply. If you
> finish with a beautiful skeleton and an unfilled profile, you produced nothing.

> **This skill does not contain the slot list, and never will.** The schema lives in one file —
> [references/campaign-profile.md](references/campaign-profile.md), bundled into this folder — and
> the interview is a *walk over that file*. A hand-copied list here is how five slots — endgame,
> protagonists-per-session, frame of reference, recording consent, audit cadence — reached the
> schema and were silently never asked. P10 applied to this package: one source of truth.
> Principles are cited by tag (`P1`…`P15`), full text in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled in this folder.

---

## Phase 0 — Find out whether a profile already exists, then pick the mode
<!-- phase0: search-protocol -->

**Search before you conclude.** From the vault root, look for `campaign-profile.md` at any depth
(`rg --files -g campaign-profile.md`, `find . -name campaign-profile.md`, or the tooling's search)
and grep for `type: campaign-profile` in case it was renamed. Only if both come back empty is there
no profile: one a folder deeper than expected is not an absent profile, and re-interviewing a GM
who already answered forty questions is the fastest way to be fired.

| Situation | Mode | What you do |
|---|---|---|
| Empty or near-empty repo, no profile found | **Bootstrap** | Phases 1 → 5 in order |
| Repo already holds real material, no profile found | **Adoption** | Phase 4 first, then interview only the slots material cannot answer |
| A profile was found | **Audit** | Phase 5 only: declared conventions vs. actual state; report drift, change nothing without asking |

Never mix modes silently. Say which one you are in, and where you searched, before the first
question or the first write.

### Bootstrap without a full profile — draft in chat (W21b)

Bootstrap mode sometimes begins with *no profile at all* — the GM wants to explore before
committing to a file. When `E.deliverable` is `draft in chat` (or no repo path exists yet to write
to), run the Bootstrap interview conversationally and produce the **filled-profile draft as a reply
artifact**, not as a file write. Two additional rules apply to this sub-mode:

1. **Open the reply** with a one-line declaration: `Running without a full profile — Bootstrap draft
   mode.` Name every slot you intend to ask on the fly (those you cannot read from existing
   material), so the GM sees the scope before answering the first question.
2. **Close the reply** with the standard P14 run report, extended to list: which slots you asked on
   the fly and what the GM said, which you left `deferred: <when>` because they belong to a
   conversation still to come, and which remain empty because the GM answered `none`. This extended
   report is mandatory even if the rest of the report would otherwise be brief.
3. **After presenting the draft**, offer explicitly to record the confirmed answers into the profile
   file. Do not write to the profile — or create any file — without the GM's explicit consent in
   that same session. Do not fill any slot the GM did not answer; invent nothing.

## Phase 1 — Read before writing

1. **The bundled schema** — `references/campaign-profile.md`. This *is* the interview script; open
   it now. If it is missing, stop and report a broken install: do not reconstruct it from memory.
2. **Whatever exists already** — file tree, `README`, any conventions note. Two minutes of `ls`
   and `rg` prevents an interview that asks what the repo already answers.
3. **The GM's own words** — a pitch, a chat log, a hand-written page. Mine answers from it *and
   then confirm them*: an inferred slot value is a guess until the GM says yes.

If the repo is not under version control, or has no sync path to the GM's other machines, flag
it now and recommend addressing it: version control is the only reliable recovery path from a bad
write and the only basis for enforcing the portability rule (Phase 3.5), but it is a strong
recommendation, not a hard requirement.

## Phase 2 — The interview: walk the bundled schema

**Open by offering both walks, explicitly — before asking a single question.** Read the bundled
schema now and count its **slot bullets** (lines starting `- **\`X.y\`**`) and how many of those
carry `*(core)*` — not raw text occurrences of the string "(core)", which also appears once in the
preamble and would overcount by one — so what you say is the real count from the file, never a
number written into this skill (which goes stale the day a slot is added).
Tell the GM there are two paces — a **full walk** (every slot, in schema order) and a **quick
start** (only the `(core)` slots plus their dependents) — with those two counts, and let the GM
choose. Do not infer the choice from how busy or rushed the GM sounds: ask.

**The procedure, literally:**

1. Read `references/campaign-profile.md` top to bottom, then walk its sections in the order it
   declares them (§A first, §E last) and, inside each, its slots in written order. Do not reorder,
   do not skip, do not batch a section away because it "looks optional".
2. For every slot: ask using the slot's own explanatory line, record the answer in the GM's
   vocabulary, move on. Group 3–5 adjacent slots per message so the GM is not interrogated one line
   at a time — but no slot may be dropped from the walk.
3. At the end, **diff your filled profile against the schema**: a slot in the schema and absent
   from your output was skipped. Go back and ask it.

**Two walks — full or quick start.** The full walk above is the default. When the GM chooses the
quick start (offered up front, see above): walk only the slots the schema marks **`(core)`**
— plus the dependents a core answer implies (`A.resource` with a value drags its whole resource
family; `D.recap` with a form drags its ceiling) — write `deferred: session zero` on the five that
table owns exactly as below, and **leave every other slot as its untouched placeholder**; never
write `none` into a slot you did not ask. Close by naming, in the report, the slot ids never asked:
the first skill needing one stops, asks once, writes back. A quick start is pacing, not a smaller
schema — the diff test above still runs, accepting only *named* placeholders outside the core set.

**Empty is an answer.** Write `none` into the slot — or `deferred: <when>` when the answer belongs
to a conversation that has not happened yet.
The distinction is load-bearing downstream:

| Slot content | Meaning downstream |
|---|---|
| leftover placeholder | never asked → **stop and ask** before producing anything that needs it |
| `deferred: <when>` | the answer belongs to a conversation still to come → reads as empty: ask or drop, never guess |
| `none` | asked, answered empty → **drop that section**, silently and permanently |
| a value | use it, in the GM's wording |

**Write `deferred: session zero`, never `none`, for what session zero owns** — `B.distance`,
`B.safety`, `D.tone`, `C.player_access`, `B.absence`. The interview runs before that table happens,
and a `B.safety: none` recorded today switches off the safety tools *permanently* on the strength of
a conversation nobody has had yet. `ttrpg-table-dossier` fills them in from the session-zero table
and writes the answers back.

Depth per slot, the asymmetry questions GMs forget to state, wording for the gating slots below,
and how to walk a GM who answers in paragraphs: [references/interview.md](references/interview.md).

### The slots that gate other skills' behaviour

Ask each explicitly, out loud, and never infer it.

**`B.distance` — `self-insert` | `close` | `fictional`.** At `self-insert` or `close`, hooks
harvested about a character are aimed at a real person; every skill that harvests hooks, writes
playstyle notes or aims a scene at a player branches here. Say that out loud when you ask. Record
the closer value when there is hesitation; write `deferred: session zero` if the table has not
met. Guessing is the one thing this slot never tolerates. Exact wording:
[references/interview.md](references/interview.md).

**`B.consent_recording` — an explicit `yes`, or no capture pipeline exists.** Ask who agreed, in
words, and whether that covers everyone including guests. Never infer consent from a file, a folder
or "I always record". Write the gate as the schema asks — the token `yes`/`no` first, then their
sentence in their own language — so the answer is legible to a reader *and* to the tooling.
Anything short of explicit yes → write `no`, leave `C.capture_paths` empty,
audio skill stays off. An assumption here is a harm, not a bug. Exact wording:
[references/interview.md](references/interview.md).

**`D.shape` — `one-shot` | `series` | `open sandbox`.** The most branch-heavy slot in the schema;
state plainly which package skills the answer switches off:

| `D.shape` | Consequence to state at interview time |
|---|---|
| `one-shot` | No previous log, no arc note, no cross-session rotation, no opening recap. The cross-session skills (arc, recap, continuity audit) **have nothing to operate on: they say so and stop, unless the GM explicitly asks for a closing chronicle — which is written as an ending, not as an opening**. Never an invented history. Prep and entity notes still apply; the hub collapses into the prep note. |
| `series` | What the package is shaped for: chapters, rotation across sessions, arc note, recap. |
| `open sandbox` | Fronts and pressures instead of chapters. The arc note holds fronts; `D.backbone` must say so, or the arc skill hunts a chapter list that does not exist. |

Record the answer verbatim; if the GM keeps a switched-off section anyway, that goes in
`E.overrides`.

**`E.overrides` branch — mandatory.** Every other skill *obeys* this slot; this one **fills** it, so
collect instead of obeying: one override per line, each with one line of reason, in the form the
schema declares — `P7 — off: <reason>`. A bare `P7 — off` is an argument nobody recorded.

| Principle | At interview | If the GM asks to switch it off |
|---|---|---|
| P1, P2, P3, P10, P11, P14, P15 | not overridable | **contradict once, with the reason**: switched off they produce documents that fail at the table, or state that desynchronises. Then record the wish as a working agreement, not as an override, and say which skills keep enforcing it |
| P4, P5, P6, P7, P8, P9, P12, P13 | strong defaults, legitimately switchable | record verbatim with its reason and move on — no second question, no talking the GM out of it |

Repeat every recorded override in the setup's **closing report**, by tag and reason: that is how the
GM learns which sections of the other skills just went quiet.

## Phase 3 — What the answers imply

### 3.1 Folder skeleton
**Create only what the answers justify** — small, linked, per-entity notes, never monoliths, in
`B.language`. Annotated skeleton and its per-folder conditions (items, official/reworked,
gm-private): [references/repo-conventions.md](references/repo-conventions.md). Write the resulting
map into `C.root` as a folder → content table: an agent that cannot answer "where does this note
belong?" from the profile invents a folder, and the second folder for the same thing is how a
vault dies.

### 3.2 The state hub, and the party note if the resource needs one (P10)

**`A.resource_shape` decides whether one more note exists.** A `shared party clock` has exactly one
home and it is not a dossier: create the party note here and record it in `C.state_locations`, or
every later skill will look for a note nobody made. `per-faction` → the value lives on each faction
note. `per-character` → no extra note; it is a dossier property.

Exactly one note is the campaign's current state (`C.hub`): what does **not** live as a property of
an entity note and is not owned by a ledger — where the party is, last session played, what comes
next. Per-entity values live only in that entity's note, and **open threads live only in
`C.thread_ledger`**; both are *read* here through a view, a query or a link, with the mapping
recorded in `C.state_locations`. **Static roster tables are forbidden** in hub, indexes and
prep: they desynchronise on the first update and then lie confidently. No query mechanism → link to
the entity notes and say the values are *there*. `D.shape` = `one-shot` → the hub collapses into
the prep note; say so in `C.hub` rather than creating an empty hub.

### 3.3 Frontmatter, tags, links, names
Decide once — `C.frontmatter` / `C.links` / `C.naming` — apply everywhere; the one exception,
the prep document inlining rather than linking (P1), is recorded in `C.inline_exception` so nobody
"fixes" it later. Full worked detail, needed once at setup, not every run:
[references/repo-conventions.md](references/repo-conventions.md).

### 3.4 Verification command and invariant
This skill bundles a link/reference checker —
[references/check_links.py](references/check_links.py), stdlib Python 3.9+ — so `C.verify` is no
longer a project the GM has to build first. **Propose it, do not install it as a side effect**:
offer to copy the bundled script to `<repo>/scripts/check_links.py` and to record
`python scripts/check_links.py <repo root>` as the exact `C.verify` command, invariant **0 broken
wikilinks, embeds and relative markdown links** (case-only mismatches are reported separately, not
counted against the invariant; it does not resolve ambiguous wikilink targets — two files sharing a
name — say so). Only once the GM agrees, copy the file, run it once, and report
the actual number: a baseline already red is not an invariant, it is decoration. If the GM
declines, or the vault is not a place scripts can live, write `none — invariant unverifiable` — the
honest fallback, and no longer the first thing tried. Every skill here ends its Verify phase with
whatever `C.verify` now names.

### 3.5 Portability — all memory lives in files in the repo
**Every persistent fact about this campaign must exist as a file inside the repo** (`C.portability`).
Checklist and the fresh-agent test: [references/repo-conventions.md](references/repo-conventions.md).

### 3.6 Overlay skills, when the profile cannot hold something
Something irreducibly specific to this campaign and not a profile slot — house aesthetics, this
table's recurring patterns, a casting rule for figures in this setting — belongs in a **campaign
overlay skill**, never in a base skill here. This folder bundles the template:
[references/overlay-SKILL.md](references/overlay-SKILL.md); point the GM at it when the need comes
up. Writing the overlay is the GM's job (or a later session's), not this skill's. When a clone is
reachable, `python scripts/validate_overlay.py <overlay path>` checks delegation, restatement and
length once the overlay exists; without one, the template's own size check is the only guard.

## Phase 4 — Adoption mode (the repo already has material)

The existing repo is **the authority on its own conventions**. Describe it; do not improve it.
Full procedure, needed only in this mode: [references/adoption.md](references/adoption.md).

## Phase 5 — Verify

- **Slot coverage, mechanically:** when a clone of `ttrpg-campaign-skills` is reachable, run
  `python scripts/validate_profile.py <profile path>` and report its findings — it reads the
  schema itself, so an invariant this skill does not know about is still enforced. Otherwise, diff
  the slot ids in `references/campaign-profile.md` against the profile you wrote by hand. Either
  way, every schema slot holds a value, an explicit `none`, or a `deferred: <when>` — or, after a
  declared quick start only, an untouched placeholder outside the core set, named in the closing
  report; a slot missing from your output is a slot you never asked. **A slot session zero owns is
  `deferred: session zero`, never `none`** — see the four states above.
- Each `none` was *asked*, not assumed. `B.consent_recording` is `yes` only if someone said yes,
  and `C.capture_paths` is filled only then. `E.overrides` is explicit — `none` is a valid and
  common answer, blank is not. `C.gm_private` is filled whenever `C.player_access` lets players
  read anything.
- The §C slots answer without further conversation: where a new note of each kind goes, the link
  syntax, which values are properties, which note is `C.hub`, what `C.verify` is and its invariant.
- The hub contains no static roster table; no tracked value appears in two places (P10).
- `C.verify` runs and meets its declared invariant; report the actual number. Nothing needed for
  the next session lives outside the repo.
- Adoption mode only: the profile describes the repo **as it is**; the gap list was reported and
  nothing renamed, moved or reorganised.

## Close with the run report (P14)

End the **reply** with it — skeleton in [references/PRINCIPLES.md](references/PRINCIPLES.md). Not inside the profile, which is a data sheet. List the slots you wrote a value into, the ones you wrote `deferred: <when>` on,
the ones left untouched on purpose (quick start), and every command you ran with its real output —
shown before running. **For every slot written `deferred: session zero`, say what stalls if session
zero (`ttrpg-table-dossier`) is skipped:** read the Phase 0 tables of `ttrpg-session-prep`,
`ttrpg-table-dossier` and `ttrpg-table-recap` for each slot's "if empty" consequence — do not
invent the wording. If those files are not reachable, list the deferred slots and say the stall
consequence could not be read this run.

## What NOT to do

- Do not restate the slot list in your plan, your notes or a fork of the schema. Walk the file.
- Do not invent a slot value, and do not "reasonably assume" one. Ask, or write `none`.
- Do not infer `B.consent_recording` from anything. It is a sentence someone said, or it is `no`.
- Do not leave a template placeholder in a delivered profile outside a declared quick start —
  downstream skills read it as "never asked" and stall; after a quick start that stall is the
  designed behaviour, but only for slots named as unasked in the report. Do not conclude "no profile exists" without searching the whole vault.
- Do not build folders for material the profile does not declare, and do not create a static roster
  or state table anywhere, however convenient.
- Do not name a verification command you have not run.
- Do not store any campaign fact outside the repo, this conversation included.
- Do not restructure an existing vault to match this skeleton. Adopt it, report the gaps, ask.
- Do not turn the profile into a setting bible: it is a data sheet that links out.
