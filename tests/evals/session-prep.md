# Eval — ttrpg-session-prep

Two scenarios: the full prep (the artifact) and a reduced prep explicitly requested (P05).

## Scenario A — the full prep

Setup: a fresh copy of `fixture-campaign/`, no other changes. (The fixture's hub is stale on
purpose — noticing is part of the eval.)

Prompt (verbatim):

> Prepare Session 8. The party wakes on the far bank; I want Ulde's gratitude and the rising
> water to matter tonight.

## Rubric

REQUIRED — every box, or the eval fails:

- [ ] Reads the profile first and asks about **no slot the profile already answers** (system,
      Wick, tone, guide, safety are all filled — a question about any of them is a Phase 0
      failure).
- [ ] **Flags the stale hub** before or while prepping ("Hub says Session 6 but a Session 7 log
      exists") instead of silently trusting either. (Phase 1.1)
- [ ] Builds on the Session 7 log's exit state and pending list: far bank, Iole's wound,
      Brenna's unpaid toll, the upstream rise, Ulde's gratitude. (Phase 1.3)
- [ ] **Spotlight per rotation:** Session 8 protagonists are **Maren and Sorrel** (Tobit and Iole
      carried S7; diaries prove it). Cross-scene arc in the top callout, per-scene
      `Spotlight → <PC>:` marks, **no spotlight table**. (P7)
- [ ] Top callout holds only session-spanning threads; every scene opens with a trigger box; **no
      value appears in both levels**. (P2)
- [ ] Every scene has a dramatic compass with a non-combat exit (P5); at least one written
      white-space scene exists (P6); every scene ends with an `If they derail:` pressure line (P9).
- [ ] Wick triggers appear where spent/regained, with values only at scene level; nothing about a
      resource the profile doesn't declare. (`A.resource`)
- [ ] Read-aloud blocks contain senses only; the reveals live in GM notes with seeding. (P3)
- [ ] Content margin: at least one scene tagged optional, named as first cut, hook recovery
      declared. (P8)
- [ ] Invents no state: every fact in the prep traces to the profile, the logs, the dossiers or
      the entity notes.
- [ ] The prep's frontmatter carries the fixed package key `type: session-prep`. (Phase 2)
- [ ] **Closes with the run report** (P14): declared defaults used and where declared, overrides
      honoured, inputs unavailable, language chosen, commands run with their real output — in the
      reply, never inside the artifact.

SHOULD — quality signals, note misses:

- [ ] Sorrel's return (absent in S7) is staged through her own hooks (the re-ask of Brenna's
      question is sitting in her dossier).
- [ ] The eel-market buyer's line moves into Ulde's mouth, as Session 7's recovery plan declared.
- [ ] Reports that `C.verify` is `none declared yet` instead of claiming a link check.

---

## Scenario B — reduced prep, explicitly requested

Setup: a fresh copy of `fixture-campaign/`, no other changes — same starting state as Scenario A.

Prompt (verbatim):

> Prepare Session 8, but keep it short tonight — I have to cut prep time in half before the table
> sits down. The party wakes on the far bank; I want Ulde's gratitude and the rising water to
> matter tonight.

### Rubric

REQUIRED — every box, or the eval fails:

- [ ] Treats the request as a **per-run accommodation**, not a default: nothing is written to
      `E.overrides`, and no slot is treated as if it licensed a shorter prep on its own.
      (`references/reduced-prep.md`)
- [ ] **Irreducible core kept, for every scene that made the cut:** trigger box, inlined
      read-aloud, dramatic compass with a non-combat exit, an `If they derail:` line, and
      per-scene `Spotlight → <PC>:` marks for Maren and Sorrel (same rotation answer as Scenario A
      — the ledger did not change).
- [ ] **Declares the deferrals by name, in the run report** — content margin, a written
      white-space scene, the recurring guide's beat, and the full red-team prediction pass — not a
      vague "shortened this week". A report that omits an element without naming it fails this box
      even if the prep itself is otherwise fine.
- [ ] No optional/content-margin scene, no separately written white-space scene, and no prepared
      beat for the recurring guide appear in the document — consistent with what was declared
      deferred.
- [ ] Frontmatter still carries `type: session-prep`. (Phase 2)
- [ ] **Closes with the run report** (P14), same as Scenario A.

SHOULD:

- [ ] The reduced prep is still scannable in the same format as a full one — no continuous
      narrative creeping back in under time pressure.

---

## Machine-checked boxes

`tests/run_eval.py` ticks the boxes below from the artifact itself; everything in the rubric
above still needs a reader. The split is deliberate: a grader who only judges the judgement
calls actually runs the eval.

<!-- eval-spec
{
  "skill": "ttrpg-session-prep",
  "fixture": "fixture-campaign",
  "scenarios": {
    "A": {
      "prompt_index": 0,
      "setup": [],
      "artifact": {
        "type": "session-prep"
      },
      "mechanical": [
        {
          "id": "type-key",
          "kind": "frontmatter",
          "key": "type",
          "equals": "session-prep",
          "cite": "Phase 2",
          "why": "how the log and the audit find this artifact later"
        },
        {
          "id": "spotlight-marks",
          "kind": "regex",
          "pattern": "Spotlight\\s*(?:→|->)\\s*\\S",
          "min": 2,
          "cite": "P7",
          "why": "per-scene focus is marked in the scene's trigger box"
        },
        {
          "id": "no-spotlight-table",
          "kind": "regex",
          "pattern": "(?m)^#{2,4}.*spotlight",
          "min": 0,
          "max": 0,
          "i": true,
          "cite": "P7",
          "why": "a summary spotlight section is forbidden"
        },
        {
          "id": "derail-lines",
          "kind": "regex",
          "pattern": "If they derail:",
          "min": 3,
          "cite": "P9",
          "why": "every scene carries the pressure that persists off-script"
        },
        {
          "id": "content-margin",
          "kind": "regex",
          "pattern": "(?i)optional|content margin",
          "min": 1,
          "cite": "P8"
        },
        {
          "id": "protagonists-are-maren-and-sorrel",
          "kind": "regex",
          "pattern": "(?s)Maren.*Sorrel|Sorrel.*Maren",
          "min": 1,
          "cite": "P7",
          "why": "Tobit and Iole carried S7; the diaries are the only input to the rotation"
        }
      ]
    },
    "B": {
      "prompt_index": 1,
      "setup": [],
      "artifact": {
        "type": "session-prep"
      },
      "mechanical": [
        {
          "id": "type-key",
          "kind": "frontmatter",
          "key": "type",
          "equals": "session-prep",
          "cite": "Phase 2"
        },
        {
          "id": "spotlight-marks",
          "kind": "regex",
          "pattern": "Spotlight\\s*(?:→|->)\\s*\\S",
          "min": 2,
          "cite": "P7",
          "why": "the irreducible core keeps per-scene spotlight marks"
        },
        {
          "id": "derail-lines-kept",
          "kind": "regex",
          "pattern": "If they derail:",
          "min": 1,
          "cite": "references/reduced-prep.md",
          "why": "the irreducible core keeps this line even when the fuller red-team pass is deferred"
        },
        {
          "id": "no-content-margin",
          "kind": "regex",
          "pattern": "(?i)\\(optional\\)",
          "min": 0,
          "max": 0,
          "cite": "references/reduced-prep.md",
          "why": "content margin is one of the four deferred elements"
        }
      ]
    }
  }
}
-->
