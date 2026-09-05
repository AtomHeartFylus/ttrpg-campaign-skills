# Eval — ttrpg-campaign-arc

Two scenarios: planning the season (the artifact) and the one-shot gate (the refusal). The second
is the cheaper and the more important of the two — silent degradation is what the gate exists to
prevent.

---

## Scenario A — plan the rest of the season

Setup: a fresh copy of `fixture-campaign/`, no other changes. (The fixture has no arc note:
`C.arc_note` reads `none yet`. The hub is stale on purpose.)

Prompt (verbatim):

> Seven sessions in and I have no plan. Where is this campaign going? Write the arc note.

**Answer key, arithmetic:** `B.cadence` weekly × `B.horizon` ~14 sessions = **14 total, 7 played,
7 left**. `D.endgame` declares two endings — *the fen floods* or *the debt-ledgers burn* — already
seeded (Session 7's derail note put the flood in play).

### Rubric

REQUIRED:

- [ ] States the **session budget out loud** from `B.cadence` × `B.horizon`, with sessions played
      and left, and plans inside it. (Phase 3, Pacing)
- [ ] Backbone rows carry a **session range, never a single number**, a *function* ("what it must
      deliver"), and a **named first cut** per row (P8).
- [ ] Open threads: every row's **seeded-in cites a session log**; a thread with no log is not
      admitted as a thread. `the promised lantern` (quiet since Session 3) gets an explicit
      **revive or declare-lost** decision — this skill is where that decision belongs.
- [ ] **Does not duplicate thread status**: `Threads.md` (`C.thread_ledger`) stays the only home of
      a status; the arc note shapes and reads it, and the note says so (P10). Updating the ledger's
      stale rows is legitimate; keeping a second status column that disagrees with it is not.
- [ ] **Does not recompute the rotation**: who is owed a session is read from
      `ttrpg-table-dossier`'s check (Dara), and *Protagonists committed next* is a forward
      commitment with **no tally table**. (P7 + P10)
- [ ] The **endgame is `D.endgame`'s two declared endings** with the conditions that select
      between them — not an ending the agent invented — and the note says where seeding starts.
- [ ] **Deviation ledger:** the campaign is fully homebrew (`D.backbone`), so the section is
      dropped with one line of reason, not filled with invented divergences.
- [ ] Frontmatter carries `type: campaign-arc`; the note goes where the GM is asked to put it,
      since `C.arc_note` is empty — it does not invent a path silently. (Phase 0)
- [ ] Writes **no scenes, no read-aloud, no trigger boxes** — the moment it does, it has become
      `ttrpg-session-prep`. (Skill preamble)
- [ ] Nothing planned on the stale hub without flagging it: the hub says Session 6, the logs say 7,
      and the log wins (P11).

SHOULD:

- [ ] Ties a backbone row to Dara's untouched nerve (the re-ask of Brenna's question), paying the
      rotation debt in the plan rather than in prose.
- [ ] Places a low-pressure session on the horizon (P6 at arc scale).
- [ ] Maps the Wick curve across the remaining chapters (`A.resource` is declared).
- [ ] Says which of the two endings the table's choices are currently steering toward, without
      deciding it for them.

---

## Scenario B — the one-shot gate (refusal)

Setup: a fresh copy of `fixture-campaign/`, then edit its `campaign-profile.md` so `D.shape` reads
**`one-shot`** (change nothing else — the residual series material is part of the test).

Prompt (verbatim):

> Plan the arc for this campaign.

### Rubric

REQUIRED — this scenario is pass/fail on the first box:

- [ ] **Reads `D.shape`, reports that the shape excludes this skill, and stops.** No arc note is
      written. (`D.shape` gate)
- [ ] It does **not** produce a one-row or near-empty arc note, and does not rename the job into
      something it can do — silent degradation is the failure the gate exists to prevent.
- [ ] Routes the user to `ttrpg-session-prep` as the skill that owns a single evening.
- [ ] Does not invent a history to justify running anyway, and does not talk the GM out of the
      declared shape.

SHOULD:

- [ ] Notices the contradiction between `D.shape: one-shot` and the seven sessions of material in
      the repo, and asks whether the slot is wrong — **without** proceeding on its own answer.

---

## Machine-checked boxes

`tests/run_eval.py` ticks the boxes below from the artifact itself (`--scenario A` / `--scenario
B`); everything in the rubrics above still needs a reader. Scenario B is also this package's
**structural-branch fixture**: its setup rewrites `D.shape` in the profile copy, so the one-shot
branch is exercised without a second fixture campaign to keep in step.

<!-- eval-spec
{
  "skill": "ttrpg-campaign-arc",
  "fixture": "fixture-campaign",
  "scenarios": {
    "A": {
      "prompt_index": 0,
      "setup": [],
      "artifact": {
        "type": "campaign-arc"
      },
      "mechanical": [
        {
          "id": "type-key",
          "kind": "frontmatter",
          "key": "type",
          "equals": "campaign-arc",
          "cite": "Phase 0"
        },
        {
          "id": "session-budget",
          "kind": "regex",
          "pattern": "14|seven left|7 left",
          "min": 1,
          "cite": "Phase 3",
          "why": "B.cadence x B.horizon stated out loud"
        },
        {
          "id": "both-declared-endings",
          "kind": "regex",
          "pattern": "(?is)(flood.*debt-ledger|debt-ledger.*flood)",
          "min": 1,
          "cite": "D.endgame"
        },
        {
          "id": "no-scenes",
          "kind": "regex",
          "pattern": "(?i)read-aloud|trigger box",
          "min": 0,
          "max": 0,
          "cite": "skill preamble",
          "why": "an arc note that writes scenes has become the prep skill"
        }
      ]
    },
    "B": {
      "prompt_index": 1,
      "setup": [
        {
          "replace": {
            "file": "campaign-profile.md",
            "old": "- **`D.shape`** — series.",
            "new": "- **`D.shape`** — one-shot."
          }
        }
      ],
      "mechanical": [
        {
          "id": "writes-nothing",
          "kind": "untouched",
          "allow_new": [],
          "cite": "D.shape gate",
          "why": "the correct behaviour is to report the shape and stop - a near-empty arc note is the failure"
        },
        {
          "id": "no-arc-note",
          "kind": "file-exists",
          "glob": "**/*[Aa]rc*.md",
          "expect": false,
          "cite": "D.shape gate"
        }
      ]
    }
  }
}
-->
