# Eval — ttrpg-table-recap

## Scenario

Setup: a fresh copy of `fixture-campaign/`, no other changes.

Prompt (verbatim):

> Write the recap to open Session 8.

## Rubric

REQUIRED — every box, or the eval fails:

- [ ] Reads `D.recap` and produces **in-fiction prose** within the three-minute ceiling — it
      neither picks another form nor asks for one. (Phase 0)
- [ ] **P12 sweep passes:** no player names, no marks, no Wick, no thresholds, no session number in
      the body, no address to the table, no "next time". The cut eel-market scene **does not
      appear anywhere** — a skipped scene did not happen.
- [ ] Every beat traces to `Sessions/Session 7 — Log.md`; nothing is invented or promoted. (P11)
- [ ] Protagonists named by **role-epithet from the dossiers** (`D.identity`): the warden, the
      debt-scribe, the bell-diver — stable identities, not fresh inventions.
- [ ] Sorrel's absence handled by the `B.absence` convention **in fiction** (she remained at the
      camp), never as "Dara was away".
- [ ] The closing image **seals** the chapter (no bridge to Session 8, no question to the
      players). The upstream rise is admissible — the log says it was staged once.
- [ ] Register holds fen-gothic per `D.tone` throughout, wry breaks inside the register.
- [ ] If saved as a note: frontmatter carries the fixed package key `type: session-recap`. (Phase 2)
- [ ] **Closes with the run report** (P14): declared defaults used and where declared, overrides
      honoured, inputs unavailable, language chosen, commands run with their real output — in the
      reply, never inside the artifact.

SHOULD — quality signals, note misses:

- [ ] A Weir Ballads line woven into the fabric, not dropped as a block (`D.canon_source`).
- [ ] Individual moments commemorated at the scale they had (the drowned-sister answer: quiet,
      not epic).
- [ ] Shows rather than explains (the regret rendered as gesture, not psychology).
- [ ] Declares it timed the reading against the ceiling. (Phase 4)

---

## Machine-checked boxes

`tests/run_eval.py` ticks the boxes below from the artifact itself; everything in the rubric
above still needs a reader. The split is deliberate: a grader who only judges the judgement
calls actually runs the eval.

<!-- eval-spec
{
  "skill": "ttrpg-table-recap",
  "fixture": "fixture-campaign",
  "setup": [],
  "artifact": {
    "type": "session-recap"
  },
  "mechanical": [
    {
      "id": "type-key",
      "kind": "frontmatter",
      "key": "type",
      "equals": "session-recap",
      "cite": "Phase 2"
    },
    {
      "id": "no-player-names",
      "kind": "regex",
      "pattern": "(?<![A-Za-z])(Ada|Bruno|Cleo|Dara)(?![A-Za-z])",
      "min": 0,
      "max": 0,
      "cite": "P12",
      "why": "a recap is in-fiction: player names are table talk"
    },
    {
      "id": "no-mechanics",
      "kind": "regex",
      "pattern": "(?i)\\b(wick|marks?|threshold)\\b",
      "min": 0,
      "max": 0,
      "cite": "P12"
    },
    {
      "id": "no-eel-market",
      "kind": "regex",
      "pattern": "(?i)eel-market",
      "min": 0,
      "max": 0,
      "cite": "P11",
      "why": "the cut scene did not happen; it may not be recapped"
    },
    {
      "id": "role-epithets",
      "kind": "regex",
      "pattern": "(?i)warden|debt-scribe|bell-diver",
      "min": 2,
      "cite": "D.identity"
    }
  ]
}
-->
