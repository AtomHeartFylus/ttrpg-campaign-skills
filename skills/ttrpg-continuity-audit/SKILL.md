---
name: ttrpg-continuity-audit
description: "Produce a health-check report on a campaign repo plus a proposed change list, applying nothing until approved. Use when asked to check the campaign for drift, inconsistencies, stale state, duplicated values, dangling threads or broken links, or as a recurring check every few sessions. Covers the single-source-of-truth hunt, state hub versus last session log, unpaid seeds with a revive-or-declare-lost recommendation, prep hygiene, the link-integrity command, retroactive admission-test failures, and the retcon protocol for correcting past notes. Does not decide the fate of a thread (see ttrpg-campaign-arc), rewrite prep (see ttrpg-session-prep), or fix notes silently."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Continuity audit

Produces a **report plus a proposed change list**. It is the recurring check that a campaign repo
still tells one story: state written once, the hub matching the last night played, threads either
alive or buried, links resolving.

> **Output discipline.** This skill **reports**; it does not silently fix. Findings are evidence
> (path, line, the two conflicting values), changes are proposals, and nothing is applied until the
> user approves a subset. A silent mass edit destroys the only record of which value was true.

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

| Slot | Used for | If empty |
|---|---|---|
| §2 Dramatic resource | which values are tracked and therefore duplicable | skip the resource checks |
| §6 Structure | the deviation ledger prep must stay consistent with | skip the deviation-drift check |
| §7 Table conventions | absent-player rule → expected state divergence, not a bug | flag attendance divergences as questions, not findings |
| §8 Player-facing outputs | what players may read, and where GM-only material must live | assume no note is player-readable |
| §9 Repo conventions | state single-source-of-truth locations, folder map, naming, link syntax, verification command | audit only what the user names; report the rest as unverifiable |
| §10 Working agreements | retroactivity, review bluntness, what may not be touched without asking | assume retroactivity is **not** granted; propose only |

If the profile is missing, run `ttrpg-campaign-setup` first — an audit without declared invariants
is an opinion.

## Phase 1 — Read before auditing

1. **The campaign state hub** (§9) — every value it asserts.
2. **The last session log** — especially its frozen exit state.
3. **The arc note** (`ttrpg-campaign-arc`) — the thread tracker and the deviation ledger.
4. **The last two or three prep documents** — for P1/P2 hygiene.
5. **The indexes and hubs** — where static tables breed.
6. **The entity notes created since the last audit** — the retroactive admission test.

Record the audit window: *from session N to session M*. Everything below is scoped to it, except
the invariant checks, which are repo-wide.

## Phase 2 — The checks

Run all of them. Each finding carries **evidence**: file, line, and the conflicting content quoted.

### A — Single source of truth (P10)
Hunt static duplicates of tracked state. For each value declared in §9 as living in one note
(levels, resources, position, disposition, open threads, roster), search the repo for it appearing
**as a static copy** elsewhere: hubs, indexes, prep documents, overlays, READMEs.

```sh
rg -n "<value name>|<player or entity name>" --glob '!<the note that owns it>'
```

Report every hit as `owner note says X / copy at path:line says Y`. **Do not reconcile them
yourself**: the newer file is not necessarily the true one, and picking silently launders a guess
into the record. The one legitimate exception is the **exit state of a session log**, which freezes
a historical snapshot on purpose — never flag it, and never "update" it.

### B — Hub versus last log
Every assertion in the state hub is checked against the last log's exit state and the logs in the
window: where the party is, what is next, what is unresolved, who is present. Divergence means the
**hub is stale** — the log is the authority (P11). Report the delta as a proposed hub update, one
line per field.

### C — Threads and unpaid seeds
Cross the arc note's thread tracker with the logs in the window. Report:

- threads marked *alive* with no appearance in the last N sessions (N = the profile's cadence
  reduced to about a month of play);
- seeds visible in a log but absent from the tracker (planted and never recorded — the most common
  way a promise dies);
- threads paid at the table but still marked alive;
- content skipped from prep that carried a hook, where the prep declared no recovery (P8).

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
- **Deviation drift (§6):** prep that contradicts the deviation ledger — running the source's
  version of something the campaign deliberately changed. High severity: it contradicts what the
  table has already been told.

### E — Link integrity (§9)
Run the profile's verification command and report **the command, its output and the invariant**
(typically 0 broken links). A link check of this kind verifies that link targets resolve, that
heading and block anchors exist in the target, and that embeds — including media — point at files
that are actually there.

If the profile declares no command, say plainly that link integrity is **unverified**, sample by
hand, and propose adding a check. Never report an invariant you did not run.

### F — Retroactive admission test
Take the entities added in the window and re-run the admission test from `ttrpg-entity-note`: why
it is here, what it represents, what question it poses. An entity written mid-prep under time
pressure often has only the first answer. For each failure, recommend one of: **give it the missing
question**, **demote it to background colour without dialogue**, or **retire it** (only if it never
reached the table). An entity the players have already met is never retired — it is demoted.

### G — Convention and leakage drift (§8, §9)
Naming rules and forbidden characters; notes filed outside the folder map; frontmatter tag families
that have sprouted variants (`x/y` alongside `x-y`); orphan notes reachable from nothing; and
**secrets sitting in notes the profile says players may read**, instead of in the GM-only location
§8 declares. Leakage is the highest severity in
this group: it cannot be undone after the fact.

## Phase 3 — The retcon protocol

When profile §10 grants retroactivity — the consistency of the work outranks fidelity to what was
already played — past notes **may** be corrected. The protocol is what keeps that from becoming
memory laundering:

1. **The correction is recorded.** Every retcon states what it replaced, why, and the date/session.
   Keep it where the campaign's divergences already live (the arc note's deviation ledger) so
   future prep inherits it. A correction nobody can find is a new inconsistency.
2. **Anything already read aloud to the table is flagged as such before changing it.** The players'
   memory is a copy of the old version that you cannot edit. Mark such a change explicitly in the
   proposal (`read aloud: yes — session N`) and offer the choice: reconcile it *in fiction*
   (someone lied, the record was wrong, the memory was distorted) or leave the discrepancy standing.
   Silently editing text the table has heard makes their memory wrong, and they will notice.
3. **Session logs record what happened; they are not rewritten** (P11). Correct a misspelled name
   or a mis-attributed line — never the events. Frozen exit-state snapshots are untouchable (P10).
4. **If §10 does not grant retroactivity**, propose nothing beyond the typo class and say why.

## Phase 4 — The report

```markdown
# Continuity audit — <date>, sessions <N>–<M>

## Invariants
| Check | Result | Evidence |
|---|---|---|
| Link integrity | <pass/fail: 0 broken> | `<command>` → <output> |
| Single source of truth | <n duplicates> | see F1… |
| Hub vs last log | <in sync / n divergences> | |

## Findings
<ordered by blast radius, each: severity · where (path:line) · evidence quoted · recommendation>
- **F1 — blocking** · <path:line> · <the two conflicting values> · <recommendation>

## Threads to decide  → ttrpg-campaign-arc
| Thread | Last seen | Recommendation | Why |
|---|---|---|---|

## Proposed changes — NOTHING APPLIED
| # | File | Change | Reason | Read aloud? | Risk |
|---|---|---|---|---|---|
```

**Severity:** *blocking* (contradicts what the table was told, or leaks a secret) ·
*drift* (will contradict something soon) · *cosmetic* (convention only).
Order findings by blast radius, not by the order you found them.

Then: ask for approval, apply **only** the approved rows, and **re-run the verification command
afterwards**, reporting its output. An audit that ends without re-verification proved nothing.

## Phase 5 — Verify the audit itself

- Every finding cites a path, a line and the actual conflicting text — no finding rests on memory.
- No duplicate was reconciled, no note renamed or moved, no file edited before approval.
- Session-log exit states were left untouched and were not flagged as duplicates.
- Every unpaid thread carries a revive-or-declare-lost recommendation, and none was decided here.
- The link-integrity result quotes the command actually run, or is reported as unverified.
- Every proposed retcon says what it replaces, why, and whether it was read aloud.
- The change list is a proposal; the applied subset, if any, is exactly what was approved, and the
  verification command was re-run after applying.

## When to run

Every 3–5 sessions, at every chapter boundary, before any arc pass, and after any bulk import or
reorganisation of the repo.

## What NOT to do

- Do not fix silently, and do not batch "obvious" fixes into an unrelated task.
- Do not resolve a duplicate by keeping the value you happened to read last — report both.
- Do not touch the frozen exit state of a session log, or rewrite the events in one.
- Do not decide the fate of a thread; hand the decision to the arc pass.
- Do not rename, move or reorganise notes without asking (§10).
- Do not claim the link invariant without running the command.
- Do not retcon material already read aloud without flagging it — and never without a record.
- Do not report cosmetic convention drift above a leaked secret or a contradicted deviation.
