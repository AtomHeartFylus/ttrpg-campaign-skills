# Eval — ttrpg-continuity-audit

**This file is also the fixture's answer key.** Any new defect seeded into `fixture-campaign/`
must be added to the table below in the same commit.

## Scenario

Setup: a fresh copy of `fixture-campaign/`, no other changes.

Prompt (verbatim):

> Run a continuity check on this campaign.

## Seeded defects (answer key)

| # | Defect | Where | What a correct finding says |
|---|---|---|---|
| 1 | Stale hub | `Hub.md` "Last session played: Session 6" | Session 7 log exists; hub was never updated |
| 2 | Desynced duplicate values | `Hub.md` roster vs `Dossiers/*` | hub says 5 marks each / Tobit Wick 4; dossiers say 6 marks (present three) / Tobit Wick 3 — dossiers are the source of truth (P10) |
| 3 | Static roster table exists at all | `Hub.md` | forbidden by P10 regardless of values; propose removal or a generated view |
| 4 | Broken links (3) | `Hub.md` → `[[Eel-Market Buyer]]`; `Session 6 — Log.md`'s `prep:` → `[[Session 6 — The Long Reach]]`; `Session 7 — The Drowned Toll.md` → `[[Bell-Wight — stats]]` (twice) | none of the three target notes exist — `scripts/check_links.py .` finds exactly these |
| 5 | Thread ledger not updated after S7 | `Threads.md` | "the false bell" still *open* though log 7 pays it; "the fen's debt-ledgers" never opened despite log 7's pending item |
| 6 | Hub retypes thread statuses | `Hub.md` "Open threads" vs `Threads.md` | duplicates the ledger (P10) and already disagrees with it ("eel-catcher's promise — paid (Session 6)" vs ledger's Session 7) |
| 7 | Duplicated trigger in prep (P2) | `Sessions/Session 7 — The Drowned Toll.md` | "lying to Ulde costs 1 Wick" sits in BOTH the global callout and Scene 1's box |
| 8 | Dangling seeds | `Threads.md` "the promised lantern" (quiet since S3); S6's heron-omen | each needs a revive-or-declare-lost recommendation |

## Rubric

REQUIRED — every box, or the eval fails:

- [ ] Finds at least **6 of the 8** seeded defects. (Phase 2, the checks)
- [ ] Finds **1, 2 and 5**, specifically — hub staleness and ledger drift are the checks the skill
      exists for.
- [ ] **Applies nothing**: the output is a report plus a proposed change list, and the fixture copy
      is byte-identical afterwards except for the report note itself, if it saved one. (Phase 4)
- [ ] Where two copies of a value disagree, it names the **source of truth** and proposes the fix
      in that direction (dossiers/ledger win; hub is a view). (P10)
- [ ] Every dangling seed gets a **revive-or-declare-lost** recommendation, not a bare listing.
- [ ] Reports **which checks it could not run** (e.g. `C.verify` is `none declared yet` → says
      links were checked by hand or not at all — it never claims a command it didn't run).
- [ ] Invents no defect: every finding traces to a real line in the fixture.
- [ ] **Closes with the run report** (P14): declared defaults used and where declared, overrides
      honoured, inputs unavailable, language chosen, commands run with their real output — in the
      reply, never inside the artifact.
- [ ] Run report ends with a **next suggested step** line naming `ttrpg-campaign-arc` — this
      fixture's dangling threads (defect 8) give it a non-empty "Threads to decide" table, so the
      line is exercised, not just declared possible.
- [ ] **Check H (retention)** is attempted, since the fixture's `B.retention` states a rule ("GM
      notes about players kept for the season, then deleted") — and reports honestly that the
      dossiers' Playstyle/Hooks entries here carry no per-entry date to test, rather than inventing
      an age or a past-due finding that is not in the fixture. Not a seeded defect: the correct
      output is "nothing overdue found" or "undated, cannot verify," never a fabricated one.
- [ ] If it proposes registering an override in `E.overrides`, it is restricted to **P8, P12 or
      P13 only** (the three principles checks C/G/F actually measure — never P4–P7 or P9, which
      this skill grades no prep against, and never P7, which `ttrpg-table-dossier` owns), phrased
      as a single-run observation ("this run found X") — never citing a repeated pattern across
      runs or an archived prior report, which this package has no artifact or slot for.

SHOULD — quality signals, note misses:

- [ ] Findings cite file + line/section, not just prose.
- [ ] Thread decisions (lantern) are routed to `ttrpg-campaign-arc`, not decided in the audit.
- [ ] The report distinguishes ERROR-grade drift (P10 violations) from hygiene notes.

---

## Machine-checked boxes

`tests/run_eval.py` ticks the boxes below from the artifact itself; everything in the rubric
above still needs a reader. The split is deliberate: a grader who only judges the judgement
calls actually runs the eval.

<!-- eval-spec
{
  "skill": "ttrpg-continuity-audit",
  "fixture": "fixture-campaign",
  "setup": [],
  "mechanical": [
    {
      "id": "applies-nothing",
      "kind": "untouched",
      "allow_new": [
        ".*[Aa]udit.*",
        ".*[Rr]eport.*"
      ],
      "cite": "Phase 4",
      "why": "an audit proposes; it does not edit the campaign"
    },
    {
      "id": "names-the-stale-hub",
      "kind": "regex",
      "pattern": "(?i)hub",
      "min": 1,
      "cite": "defect 1"
    },
    {
      "id": "names-the-ledger-drift",
      "kind": "regex",
      "pattern": "(?i)(false bell|thread ledger|Threads\\.md)",
      "min": 1,
      "cite": "defect 5"
    }
  ]
}
-->
