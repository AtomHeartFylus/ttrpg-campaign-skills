# The checks, in full

Read this while running Phase 2 of an audit. `SKILL.md` owns the gate, the profile slots, the
report format and the retcon protocol; this file owns what each check actually does.

Run **all** of them, minus what `E.overrides` switched off: a check that verifies a default the
table declared off does not run, and the report says which override dropped which check. A and B
are never dropped — P10 and P11 are not overridable. Each finding carries **evidence**: file, line,
and the conflicting content quoted. Nothing here is applied — every check produces a proposal.

---

### A — Single source of truth (P10)
Hunt static duplicates of tracked state. For each value declared in `C.state_locations` as living in one note
(advancement, resources, position, disposition, open threads, roster), search the repo for it appearing
**as a static copy** elsewhere: hubs, indexes, prep documents, overlays, READMEs.

```sh
rg -n "<value name>|<player or entity name>" --glob '!<the note that owns it>'
```

Report every hit as `owner note says X / copy at path:line says Y`. **Do not reconcile them
yourself**: the newer file is not necessarily the true one, and picking silently launders a guess
into the record.

Two things are not copies and are never flagged: the **exit state of a session log**, which freezes
a historical snapshot on purpose, and a **view, query or link** that renders an owner's value
elsewhere. What counts is a *typed* second copy — the hub's open-thread list is the textbook case,
since thread status belongs to `C.thread_ledger` alone.

### B — Hub versus last log
Every assertion in the state hub is checked against the last log's exit state and the logs in the
window: where the party is, what is next, what is unresolved, who is present. Divergence means the
**hub is stale** — the log is the authority (P11). Report the delta as a proposed hub update, one
line per field.

### C — Threads and unpaid seeds
Cross the arc note's thread tracker with the logs in the window. Report:

- threads marked *alive* with no appearance in the last N sessions, where **N is derived from
  `B.cadence`** — the *session* cadence — reduced to about a month of play. `B.cadence` and
  `E.audit_cadence` are different slots: how often they play, and how often you audit. Do not read
  one for the other;
- seeds visible in a log but absent from the tracker (planted and never recorded — the most common
  way a promise dies);
- threads paid at the table but still marked alive;
- content skipped from prep that carried a hook, where the prep declared no recovery (P8). **This
  bullet does not run when `E.overrides` declares `P8 — off`:** that prep keeps no content margin
  and names no first cut, so skipped content without a recovery is by design, not a finding. The
  rest of check C still runs.

A promised object, reward, favour or payment is a thread like any other and is hunted exactly as
one: an unpaid material promise absent from the tracker, or alive with no appearance in the window,
files under the same two bullets above. There is no separate ledger to cross-check it against —
this package tracks no currency, inventory or price — so the only question check C asks of it is
the one it asks of any thread: is it seeded, owned, payable and current.

Each gets a **recommendation: revive** (with the concrete scene that would pay it off) **or declare
lost** (with what the table would notice). **The decision is not made here** — it belongs to
`ttrpg-campaign-arc`; this skill hands it a decision-ready list.

### D — Prep hygiene (P1, P2)
On the prep documents in the window:

- **P2 duplication:** a trigger present in both the global reminder and a scene box; a value (a
  difficulty, a cost, a quantity) written in two places. Report both locations — a duplicated
  number is a stale number waiting to happen.
- **P1 violations:** a cross-reference standing in for descriptive content ("see the module / see
  the location note"); any link that is meant to be *opened during play* and is **not** a stat
  block. Those are the two failure shapes; quote the offending line.
- **Deviation drift (`D.deviation_policy`):** prep that contradicts the deviation ledger — running
  the source's version of something the campaign deliberately changed. High severity: it
  contradicts what the table has already been told. **A fully homebrew campaign has no ledger
  because it has no source; skip this check and do not report the absence as a finding.**

### E — Link integrity (`C.verify`)
Run the profile's verification command and report **the command, its output and the invariant**
(typically 0 broken links). A link check of this kind verifies that link targets resolve, that
heading and block anchors exist in the target, and that embeds — including media — point at files
that are actually there.

If the profile declares no command, say plainly that link integrity is **unverified**, sample by
hand, and propose adding a check. Never report an invariant you did not run.

### F — Retroactive admission test (P13)
**This whole check does not run when `E.overrides` declares `P13 — off`:** the table switched the
admission test off, so entities added in the window are not tested and no softer version is
substituted. Declare the skipped check in the report and move on.

Take the entities added in the window and re-run the admission test: why it is here, what it
represents, what question it poses. An entity written mid-prep under time
pressure often has only the first answer. For each failure, recommend one of: **give it the missing
question**, **demote it to background colour without dialogue**, or **retire it** (only if it never
reached the table). An entity the players have already met is never retired — it is demoted.

### G — Convention and leakage drift (`C.player_access`, `C.naming`, `C.root`)
Naming rules and forbidden characters; notes filed outside the folder map; frontmatter tag families
that have sprouted variants (`x/y` alongside `x-y`); orphan notes reachable from nothing; a name
that **recurs** across the session logs in the window with no entity note ever created for it —
the inverse of an orphan: a note that should exist and does not, the promotion `ttrpg-session-log`
Phase 4 asks for but nobody finished; and **secrets sitting in notes `C.player_access` says players
may read**, instead of in the `C.gm_private` location. Leakage is the highest severity in this
group: it cannot be undone after the fact. **No override drops this check:** `P12 — off` admits
mechanics and meta into player-facing text, not secrets into notes players may read, and naming and
folder rules come from `C.naming` and `C.root`, which are slots, not defaults.

### H — Retention (`B.retention`)
**Does not run when `B.retention` is empty or `deferred`** — there is no rule to check an artifact
against, and reporting an age with nothing to measure it by is inventing the rule this skill was
asked not to invent. Say plainly that retention is unverified and offer to set it, exactly as
`ttrpg-session-audio` and `ttrpg-table-dossier` do when they write such material with the slot
still empty.

When `B.retention` states a rule, walk the GM-facing material it names — dossier **Playstyle** and
**Hooks** entries (each a dated, per-session observation), the off-game note, the speaker map and
the transcript, one artifact or entry at a time — and compare its date against the rule. Report
every entry past the stated retention as a **change-list item**, never delete it yourself: deletion
is the one action in this skill nobody may take without the GM's approval, exactly like every other
proposal here. A rule stated as a season or a chapter boundary rather than a fixed day count is
read against the campaign's own record of when that season or boundary fell — do not convert it to
a day count on this skill's own authority. Anyone described may also have an entry removed on
request regardless of the stated rule (`templates/campaign-profile.md`, `B.retention`); a request
like that is applied directly, the one exception to "nothing is applied until approved," because
the request itself **is** the approval.

