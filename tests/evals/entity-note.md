# Eval — ttrpg-entity-note

## Scenario

Setup: a fresh copy of `fixture-campaign/`, no other changes. (Note: the hub already links
`[[Eel-Market Buyer]]` — a dead link, seeded.)

Prompt (verbatim):

> The players keep asking about the buyer of drowned bells from the eel-market. Give him a
> proper note.

## Rubric

REQUIRED — every box, or the eval fails:

- [ ] **Searches before creating** (Phase 1): finds the buyer's existing traces — the hub's dead
      link, the Session 7 prep's optional scene, the log's "still unspent" seed — and builds on
      them instead of inventing a parallel figure; the note's name resolves the hub's existing
      link rather than coining a second spelling.
- [ ] **Runs the admission test in writing** (P13): the three answers are sections of the note,
      and the third question's answer is not obvious. If the agent judges the answers obvious, the
      correct output is a **demotion to background colour** with the reasoning — grade that as a
      pass too; what fails is a note with a hollow or missing test.
- [ ] Playable intention **proportional** (P4): the buyer is a hook-carrier, so surface want +
      beneath + a speakable surface line + stall/walk/contradict behaviour — or an explicit
      one-line-want choice with the reasoning.
- [ ] Links: place + affiliation + at least one theme + related entities, in `[[wikilink]]`
      syntax; the note is reachable (the hub link now resolves). No static roster table touched.
- [ ] Any tracked state (disposition, debts) lives **in this note only** (P10).
- [ ] No stat block inlined; mechanics absent or one local trait plus a link, per `A.ruleset`.
- [ ] Nothing contradicts the logs: the buyer has **not** met the party (his line was never
      delivered — the log says so). A note claiming an encounter is an invention. (P11)
- [ ] Saved under `Entities/` per `C.root`/`C.naming` with the fixed package key `type: entity`
      in frontmatter; asks before renaming or moving anything (`E.never_without_asking`).

SHOULD — quality signals, note misses:

- [ ] Ties him to the chapter's mechanism (what a fair price is / debts and drowning) rather than
      generic villainy.
- [ ] GM-only material clearly marked (players read nothing here, but the section discipline
      holds).
- [ ] Appearances section started empty or pointing only at real logs — not fabricated.

---

## Machine-checked boxes

`tests/run_eval.py` ticks the boxes below from the artifact itself; everything in the rubric
above still needs a reader. The split is deliberate: a grader who only judges the judgement
calls actually runs the eval.

<!-- eval-spec
{
  "skill": "ttrpg-entity-note",
  "fixture": "fixture-campaign",
  "setup": [],
  "artifact": {
    "type": "entity"
  },
  "mechanical": [
    {
      "id": "type-key",
      "kind": "frontmatter",
      "key": "type",
      "equals": "entity",
      "cite": "Phase 2"
    },
    {
      "id": "saved-under-entities",
      "kind": "file-exists",
      "glob": "Entities/*.md",
      "cite": "C.root"
    },
    {
      "id": "resolves-the-dead-link",
      "kind": "file-exists",
      "glob": "Entities/Eel-Market Buyer.md",
      "cite": "Phase 1",
      "why": "the hub already links [[Eel-Market Buyer]]; a second spelling leaves it dead"
    },
    {
      "id": "wikilinks-present",
      "kind": "regex",
      "pattern": "\\[\\[[^\\]]+\\]\\]",
      "min": 3,
      "cite": "C.links"
    },
    {
      "id": "no-claimed-encounter",
      "kind": "regex",
      "pattern": "(?i)(met the party|has met them|spoke with the party)",
      "min": 0,
      "max": 0,
      "cite": "P11"
    }
  ]
}
-->
