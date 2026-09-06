# Eval — ttrpg-session-log

## Scenario

Setup: a fresh copy of `fixture-campaign/`, then **delete `Sessions/Session 7 — Log.md`** and, in
each of the three present dossiers (`Ada — Maren`, `Bruno — Tobit`, `Cleo — Iole`), remove the
Session 7 diary line and set `marks: 5` (Maren `wick: 3`, Tobit `wick: 4`) — the copy now
represents the morning after Session 7, before any bookkeeping.

Prompt (verbatim):

> We played Session 7 last night. Dara couldn't come. Quick notes: Tobit paid Ulde's toll with a
> true regret — Bruno gave him a guild expulsion as new backstory. On the ferry Brenna turned
> Sorrel's old question on Iole and Cleo answered with a drowned sister. Maren kept the
> eel-catcher promise out loud. At the bell-house Iole dove without the rope plan, took a wound
> from the cold, and they cut the bell loose before finding the body — Tobit found the guild-mark
> after and they worked out it was Ulde's brother on their own. Write the log.

## Rubric

REQUIRED — every box, or the eval fails:

- [ ] Walks the prep's global-threads callout and turns unplayed triggers into **missed
      opportunities** (the upstream-rise seed; the cut eel-market scene with its recovery plan).
      Nothing prepped vanishes silently. (P8, Phase 2.2)
- [ ] Asks **at most 2 targeted questions at a time**, only about genuinely missing facts (e.g.
      end-of-night Wick values, whether marks were earned) — and asks nothing whose slot or answer
      is already on the record. (Phase 2) This scenario's testimony resolves within the two-round
      cap, so the cap itself is not exercised here — if it ever is hit on a messier session, the
      correct behaviour is to stop, mark the remaining gaps inline with a same-language
      unresolved-fact marker (never the literal English word in a non-English log), add a matching
      *Pending for next session* line for each (or name it in the run report on a one-shot, which
      has no such section), and name them all in the run report — never keep asking or invent a
      value.
- [ ] **Invents no fact.** Anything not in the testimony and not answered is omitted or asked, not
      reconstructed. (P11)
- [ ] Exit state: **one row per character** (`A.resource_shape`: per-character), Sorrel not
      advanced (`B.absence`), the wound recorded. (Phase 3)
- [ ] Every present player gets a named moment or an explicit chorus note; carried/chorus marks
      feed the diaries. (P7)
- [ ] Phase 4 runs: the three present dossiers get updated values and one diary entry each;
      thread updates (`the false bell` → paid, `the fen's debt-ledgers` → opened) go to
      `Threads.md`, **not** into a rival list in the log. (P10)
- [ ] The hub's "last session played" is updated by hand; **no tracked values are copied into the
      hub** (the fixture's roster table is pre-existing drift — updating it would be a P10
      failure; flagging it is a bonus).
- [ ] Headings in English per `B.language`; the note saved under `Sessions/` per `C.naming`;
      frontmatter carries the fixed package key `type: session-log`. (Phase 3)
- [ ] **Closes with the run report** (P14): declared defaults used and where declared, overrides
      honoured, inputs unavailable, language chosen, commands run with their real output — in the
      reply, never inside the artifact.

SHOULD — quality signals, note misses:

- [ ] Deviations from prep are marked as deviations (the skipped ledger-read, the bell cut before
      the body).
- [ ] Says what is now unblocked (recap; next prep) per Phase 5.
- [ ] New hooks (the guild expulsion) written back to Bruno's dossier as on-the-record material
      (`B.distance` is `fictional`, so no extra gate applies — but the phrasing stays the
      player's own).
- [ ] Hands `ttrpg-entity-note` the eel-catcher (`Eel-Market Buyer`, already a known dead link in
      this fixture) as a name recurring in this session's testimony with no entity note — without
      creating that note itself. (Phase 4)

---

## Machine-checked boxes

`tests/run_eval.py` ticks the boxes below from the artifact itself; everything in the rubric
above still needs a reader. The split is deliberate: a grader who only judges the judgement
calls actually runs the eval.

<!-- eval-spec
{
  "skill": "ttrpg-session-log",
  "fixture": "fixture-campaign",
  "setup": [
    {
      "delete": "Sessions/Session 7 — Log.md"
    },
    {
      "replace": {
        "file": "Dossiers/Ada — Maren.md",
        "old": "marks: 6\nwick: 4",
        "new": "marks: 5\nwick: 3"
      }
    },
    {
      "replace": {
        "file": "Dossiers/Ada — Maren.md",
        "old": "- [[Session 7 — Log]] — *chorus*; kept the eel-catcher's promise on the water.\n",
        "new": ""
      }
    },
    {
      "replace": {
        "file": "Dossiers/Bruno — Tobit.md",
        "old": "marks: 6\nwick: 3",
        "new": "marks: 5\nwick: 4"
      }
    },
    {
      "replace": {
        "file": "Dossiers/Bruno — Tobit.md",
        "old": "- [[Session 7 — Log]] — *carried* (paid the toll in a true regret; called Ulde's tell).\n",
        "new": ""
      }
    },
    {
      "replace": {
        "file": "Dossiers/Cleo — Iole.md",
        "old": "marks: 6\nwick: 3",
        "new": "marks: 5\nwick: 3"
      }
    },
    {
      "replace": {
        "file": "Dossiers/Cleo — Iole.md",
        "old": "- [[Session 7 — Log]] — *carried* (the dive; the drowned-sister answer).\n",
        "new": ""
      }
    }
  ],
  "artifact": {
    "type": "session-log"
  },
  "mechanical": [
    {
      "id": "type-key",
      "kind": "frontmatter",
      "key": "type",
      "equals": "session-log",
      "cite": "Phase 3"
    },
    {
      "id": "saved-under-sessions",
      "kind": "file-exists",
      "glob": "Sessions/*7*.md",
      "cite": "C.root"
    },
    {
      "id": "dossiers-updated",
      "kind": "regex-changed",
      "pattern": "(?m)^marks:\\s*6",
      "min": 1,
      "cite": "Phase 4",
      "why": "the three present dossiers carry the new values - checked across every changed file, since a dossier is `type: dossier`, not the log's own `type: session-log`"
    },
    {
      "id": "sorrel-not-advanced",
      "kind": "regex",
      "pattern": "(?i)sorrel",
      "min": 1,
      "cite": "B.absence",
      "why": "the absent player is accounted for, not silently dropped"
    }
  ]
}
-->
