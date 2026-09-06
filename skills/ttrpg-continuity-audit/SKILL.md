---
name: ttrpg-continuity-audit
description: "Produce a health-check report on a campaign repo plus a proposed change list, applying nothing until approved. Use when asked to check the campaign for drift, inconsistencies, stale state, duplicated values, threads that have gone quiet or broken links, or as the recurring check at the cadence the profile declares. Requires a campaign with accumulated history: it does not serve a one-shot. Does not decide the fate of a thread (see ttrpg-campaign-arc), rewrite prep (see ttrpg-session-prep), or fix notes silently."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.12"
---

# Continuity audit

Produces a **report plus a proposed change list**. It is the recurring check that a campaign repo
still tells one story: state written once, the hub matching the last night played, threads either
alive or buried, links resolving.

> **Output discipline.** This skill **reports**; it does not silently fix. Findings are evidence
> (path, line, the two conflicting values), changes are proposals, and nothing is applied until the
> user approves a subset. A silent mass edit destroys the only record of which value was true.

> **`D.shape` gate — read it first, and be willing to stop.**
> An audit compares a repo against **its own accumulated history**. That history is what a one-shot
> does not have.
>
> - **`series`** → the skill as written.
> - **`one-shot`** → **this skill does not serve a one-shot. Say so and stop.** There is no hub to
>   go stale, no previous log to contradict, no thread carried across sessions, no convention drift
>   accumulated over months and no arc note to cross-check. What remains is a link check — run
>   `C.verify` and report its output, then end. **Do not produce an audit report whose every
>   section reads "nothing to check": that is a false pass, and it is exactly the silent
>   degradation this gate exists to prevent.**
> - **`open sandbox`** → the skill runs in full, with one substitution: check C against the
>   **fronts** rather than a chapter backbone, and treat a front that advanced off screen as
>   expected state, not drift.
> - **empty** → **ask once**, write the answer into the profile, and do not assume `series`.

---

> Principles are cited below by tag (`P1`…`P15`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled in this folder.

**Supporting reference:** [references/checks.md](references/checks.md) — the seven checks of Phase 2
in full. Read it while auditing; Phase 2 below carries only the summary table.

## Phase 0 — Read the campaign profile
<!-- phase0: find-profile, d-shape, overrides -->

**Find it before declaring it missing.** Search the repo/vault root for a file named
`campaign-profile.md` (`rg --files -g campaign-profile.md`, or the equivalent), and **if that comes
back empty, search by frontmatter** (`rg -l "type: campaign-profile"`, or `grep -rl "type: campaign-profile" .` where ripgrep is absent): the schema declares that
type, `ttrpg-campaign-setup` explicitly tolerates a renamed profile, and no other skill may call a
renamed profile an absent one. A profile that exists but was not found re-interviews a GM who
already answered.

| Slot | Used for | If empty |
|---|---|---|
| `D.shape` | **the gate above** — whether this skill runs at all | **ask once**; never assume `series` |
| `E.audit_cadence` | **how often this audit runs** — the only slot that answers it. Not the spotlight rotation check, which follows `B.protagonists` | use the **`default:` the slot itself declares**, **say in the report you used it**, and offer to record the table's real cadence |
| `B.cadence` | **session** cadence — used only to convert "about a month of play" into a number of sessions in check C. **Not the audit cadence** | ask how often they play; do not substitute `E.audit_cadence` |
| `A.resource` | which values are tracked and therefore duplicable | skip the resource checks |
| `D.backbone`, `D.deviation_policy` | the deviation ledger prep must stay consistent with | skip the deviation-drift check — a fully homebrew campaign has no ledger and its absence is not a finding |
| `B.absence` | absent-player rule → expected state divergence, not a bug | flag attendance divergences as questions, not findings |
| `C.player_access`, `C.gm_private` | what players may read, and where GM-only material must live | assume no note is player-readable |
| `C.state_locations`, `C.hub`, `C.root`, `C.naming`, `C.links`, `C.arc_note`, `C.thread_ledger` | single-source-of-truth locations, folder map, naming, link syntax, where the ledgers live | audit only what the user names; report the rest as unverifiable |
| `C.verify` | the link-integrity command and its invariant | report link integrity as **unverified**; never claim an invariant you did not run |
| `B.retention` | **check H** — how long GM-facing material about real people (dossier **Playstyle** entries, off-game notes, speaker maps, transcripts — all dated by their owning skill; dossier **Hooks** entries carry no date and are always reported not-measurable) is kept | check H does not run; report retention as **unverified** and offer to set the rule |
| `E.retroactivity` | **whether past material may be corrected, and where corrections are recorded** | assume retroactivity is **not** granted; propose only the typo class |
| `E.review`, `E.never_without_asking` | review bluntness, and what may not be touched without asking | be plain; propose, never apply |
| `E.overrides` | which strong defaults this table switched off — see the branch below | all defaults in force |

If the search finds no profile, run `ttrpg-campaign-setup` first — an audit without declared
invariants is an opinion.

**`E.overrides` branch — mandatory.** Read the slot **before running the checks**, not while writing
the report. A check that verifies a default the table switched off **does not run**, and its absence
is declared in one line: which override, therefore which check. Reporting the violation of a default
the profile declares off is noise, and noise teaches the table to ignore the report.

| Override | What stops being reported |
|---|---|
| `P8 — off` | the skipped-hook half of check C: that prep keeps no content margin and names no first cut, so skipped content with no declared recovery is not a finding. Threads and unrecorded seeds are still checked |
| `P13 — off` | check F entirely — no retroactive admission test on the entities added in the window, and no softer substitute for it |
| `P12 — off` | nothing here. The leakage half of check G is `C.player_access`, not P12: mechanics or meta in player-facing text stop being drift, a secret in a note players may read does not |
| `P4`, `P5`, `P6`, `P7`, `P9` — off | nothing: this skill grades no prep against them. Do not invent a check in order to skip it |

P1, P2, P3, P10, P11, P14 and P15 hold whatever the slot says: checks A, B and D rest on them, and a value
written twice is a defect, not a preference. Checks E and G read slots, not defaults.

## Phase 1 — Read before auditing

Package artifacts are located by their fixed `type:` frontmatter keys (`session-prep`,
`session-log`, `session-recap`, `entity`, `dossier`, `campaign-arc`), never by filename — the
same rule that finds a renamed profile.

1. **The campaign state hub** (`C.hub`) — every value it asserts.
2. **The last session log** — especially its frozen exit state.
3. **The arc note** (`ttrpg-campaign-arc`) — the thread tracker and the deviation ledger.
4. **The last two or three prep documents** — for P1/P2 hygiene.
5. **The indexes and hubs** — where static tables breed.
6. **The entity notes created since the last audit** — the retroactive admission test.
7. **The dated Playstyle entries in the player dossiers (never the Hooks section, which carries no
   date), and any off-game notes, speaker maps or transcripts in the window** — for check H, and
   only when `B.retention` states a rule.

Record the audit window: *from session N to session M*. Everything below is scoped to it, except
the invariant checks, which are repo-wide.

## Phase 2 — The checks

Run all of them **minus what `E.overrides` switched off** (see the branch in Phase 0), as
[references/checks.md](references/checks.md) specifies — read it while
auditing. Each finding carries **evidence**: file, line, and the conflicting content quoted.

| Check | Hunts | Never |
|---|---|---|
| **A** — single source of truth (P10) | static copies of a value `C.state_locations` says lives in one note | reconcile them yourself; and never flag a session log's frozen *exit state* |
| **B** — hub vs last log | every assertion in `C.hub` against the last log's exit state | treat the hub as authority — the log wins (P11) |
| **C** — threads and unpaid seeds | alive-but-absent threads, seeds in logs but not in the tracker, threads paid but still open, skipped hooks with no recovery (P8) | decide a thread's fate — hand `ttrpg-campaign-arc` a revive-or-declare-lost list |
| **D** — prep hygiene (P1, P2) | a trigger in both reminder levels, a value written twice, cross-references standing in for description, deviation drift | report deviation drift when the campaign is fully homebrew and has no ledger |
| **E** — link integrity (`C.verify`) | the command's real output and its invariant | claim an invariant you did not run |
| **F** — retroactive admission test (P13) | entities added in the window with no third answer | retire an entity the players have already met — demote it |
| **G** — convention and leakage drift | naming, folder map, tag variants, orphans, a recurring name never promoted to an entity note, and **secrets in notes `C.player_access` says players may read** | rank cosmetic drift above a leak; leakage cannot be undone |
| **H** — retention (`B.retention`) | dossier Playstyle entries, off-game notes, speaker maps and transcripts past the stated retention; dossier Hooks entries reported not-measurable, always | delete or remove anything yourself — list it and cite the owning skill; run when `B.retention` is empty or `deferred` |

**Reopening a switched-on default.** `E.overrides` is filled once, at setup, by a GM who had never
seen the package applied (`ttrpg-campaign-setup` reads the eight strong defaults out loud, but a
first answer is still a guess). Restricted to the three principles this skill's own checks actually
measure — **P8** (the skipped-hook half of check C), **P13** (check F), **P12**/`C.player_access`
(the leakage half of check G); never P4–P7 or P9, which this skill grades no prep against by
design (the table above), and P7 belongs to `ttrpg-table-dossier`. If **this run's** check finds a
violation of one of those three, add one line to the change list **proposing** it as a single
observation: "this run found X; if the table recognises it as a deliberate choice rather than
drift, here is how it is registered in `E.overrides`." Never count prior runs and never depend on
archived reports to justify the proposal — this package creates no artifact for a past audit
report (no `type:`, no `C.` slot names where one would live), so a claim resting on "the last two
reports also showed this" is exactly as unfalsifiable to a reader as an invented number: propose
from what is in front of you, once, per run. If the GM independently recalls this recurring across
sessions, that is their observation to offer, not a count this skill performs.

## Phase 3 — The retcon protocol

When `E.retroactivity` grants retroactivity — the consistency of the work outranks fidelity to what
was already played — past notes **may** be corrected. The protocol is what keeps that from becoming
memory laundering:

1. **The correction is recorded — where `E.retroactivity` says corrections are recorded.** That
   slot owns the location; this skill does not pick one. Every retcon states what it replaced, why,
   and the date/session, so a retcon leaves a trace and future prep inherits it. A correction
   nobody can find is a new inconsistency.
   - **If `E.retroactivity` names no location:** the usual home is the arc note's deviation ledger,
     where the campaign's divergences already live. **That ledger does not exist for a fully
     homebrew campaign** — `ttrpg-campaign-arc` drops it when there is no source material — so
     there is no target to fall back on. **Ask** where retcons should be recorded, propose a
     dedicated corrections section in the arc note or the state hub, and **write the answer into
     `E.retroactivity`.** Do not record a retcon into a ledger you have not confirmed exists, and
     do not create one silently.
2. **Anything already read aloud to the table is flagged as such before changing it.** The players'
   memory is a copy of the old version that you cannot edit. Mark such a change explicitly in the
   proposal (`read aloud: yes — session N`) and offer the choice: reconcile it *in fiction*
   (someone lied, the record was wrong, the memory was distorted) or leave the discrepancy standing.
   Silently editing text the table has heard makes their memory wrong, and they will notice.
3. **Session logs record what happened; they are not rewritten** (P11). Correct a misspelled name
   or a mis-attributed line — never the events. Frozen exit-state snapshots are untouchable (P10).
4. **If `E.retroactivity` does not grant retroactivity**, propose nothing beyond the typo class and
   say why.

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

## Checks not run
- `<override, as the profile states it>` → check `<letter>` not run

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
- Every proposed retcon says what it replaces, why, whether it was read aloud, and **is recorded
  where `E.retroactivity` declares** — or the location was asked for, not invented.
- The report names the cadence slot it ran on, and says when it used the slot's declared `default:`.
- Every check dropped for an override says which override dropped it; checks A and B ran regardless.
- Check H proposed no deletion or removal of its own: every past-due entry is a change-list row
  citing the skill that owns the artifact, including a removal requested by the person described.
- Check H reports undated material (always dossier Hooks entries) as **not measurable**, never as
  "nothing overdue" — the two are different claims and the report never collapses them.
- Check H is reported as **unverified**, not skipped in silence, when `B.retention` is empty or
  `deferred`.
- The change list is a proposal; the applied subset, if any, is exactly what was approved, and the
  verification command was re-run after applying.

## When to run

**`E.audit_cadence` declares it. Read the slot; it is the only thing that answers this question.**
Run at that cadence, and additionally at every chapter boundary, before any arc pass, and after any
bulk import or reorganisation of the repo — those three are event triggers, not a cadence, and hold
whatever the slot says.

**If `E.audit_cadence` is empty**, use the **`default:` the slot itself declares** (every 3-5
sessions) — the number belongs to the profile, not this skill — **state in the report that you used
it**, and offer to record the table's real cadence. A weekly table and one that plays twice a year
do not want the same number, which is why it is a slot. It is neither `B.cadence`, how often they
*play*, nor the spotlight rotation cadence, which follows `B.protagonists` — the slot says so.

## Close with the run report (P14)

End the **reply** with it — skeleton in [references/PRINCIPLES.md](references/PRINCIPLES.md). The report's own "Checks not run" section is not a substitute: one is about the campaign, the other
about this run. `E.audit_cadence` is a declared default — if you used it, say so. Every check you
could not run is named with the reason, and every command is shown before it runs and reported
with its real output. **Never write an invariant you did not measure.** Close with **next
suggested step**, one line: if the "Threads to decide" table has any rows, name `ttrpg-campaign-arc`
as the next step for them; otherwise say there is none this run — no new phase, just the line.

## What NOT to do

- Do not fix silently, and do not batch "obvious" fixes into an unrelated task.
- Do not resolve a duplicate by keeping the value you happened to read last — report both.
- Do not touch the frozen exit state of a session log, or rewrite the events in one.
- Do not decide the fate of a thread; hand the decision to the arc pass.
- Do not rename, move or reorganise notes without asking (`E.never_without_asking`).
- Do not claim the link invariant without running the command.
- Do not run this skill for a one-shot, and do not emit a report whose sections all say "nothing
  to check" — refuse and run the link check alone.
- Do not record a retcon into a deviation ledger you have not confirmed exists; `E.retroactivity`
  owns the location, and a homebrew campaign may have no ledger at all.
- Do not read `B.cadence` for `E.audit_cadence`, or the reverse, and do not invent a cadence number.
- Do not report the violation of a default `E.overrides` declares off, or drop a check silently.
- Do not retcon material already read aloud without flagging it — and never without a record.
- Do not report cosmetic convention drift above a leaked secret or a contradicted deviation.
- Do not delete or remove anything past its stated retention yourself — list it and cite the
  skill that owns the artifact; do not run check H, or invent an age limit, when `B.retention` is
  empty or `deferred` — report it unverified instead.
- Do not report a dossier's Hooks entries as "nothing overdue" — they carry no date, so they are
  always **not measurable**, never compliant.
