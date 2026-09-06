# Eval — ttrpg-table-dossier

Two scenarios: the rotation check (the question only this skill answers) and onboarding a player
(the harvest gated on `B.distance`). Run them in separate sessions, each on its own fixture copy.

---

## Scenario A — the rotation check

Setup: a fresh copy of `fixture-campaign/`, then **extend the diaries** so the rotation has enough
history to say something. Append to each dossier's `## Diary`, exactly as written (no links —
these sessions have no logs in the fixture, and the rotation check derives from diaries alone):

- `Ada — Maren`: `- Session 8 — carried.` `- Session 9 — chorus.` `- Session 10 — carried.` `- Session 11 — chorus.`
- `Bruno — Tobit`: `- Session 8 — chorus.` `- Session 9 — carried.` `- Session 10 — chorus.` `- Session 11 — carried.`
- `Cleo — Iole`: `- Session 8 — chorus.` `- Session 9 — carried.` `- Session 10 — chorus.` `- Session 11 — carried.`
- `Dara — Sorrel`: `- Session 8 — chorus.` `- Session 9 — chorus.` `- Session 10 — chorus.` `- Session 11 — chorus.`

Prompt (verbatim):

> Has anyone been chorus too long?

**Answer key.** Rotation period = `B.size` / `B.protagonists` = 4 / 2 = **2 sessions**; tolerance =
1.5 × 2 = **3**, so a finding fires above 3 consecutive chorus sessions. Dara last carried in
Session 6 and has been chorus in 7 *(absent, which is not a chorus evening — the diary has no entry
and it does not count as one)*, 8, 9, 10, 11 → **four consecutive chorus sessions, over tolerance:
Dara is the finding.** Nobody else exceeds it.

### Rubric

REQUIRED:

- [ ] **Derives the period from the slots**: states 4 / 2 = 2, and the tolerance as 1.5 × that.
      No constant substituted for either slot, no second threshold invented. (P7, Phase 3)
- [ ] Names **Dara** and nobody else, with the count of consecutive chorus sessions.
- [ ] Reads the count **from the dossier diaries**, not from the logs, and does not build a
      parallel tally or a spotlight table anywhere. (P10)
- [ ] Treats Session 7 correctly for Dara: **absence is not a chorus evening**, and the absence is
      not silently counted as one either — the reasoning is visible.
- [ ] The fix is a **named forward commitment routed to `ttrpg-campaign-arc`** (which upcoming
      chapter Dara carries), not a scene invented here and not a prep written here.
- [ ] Invents no diary entry and no session that the fixture does not contain.
- [ ] **Closes with the run report** (P14): declared defaults used and where declared, overrides
      honoured, inputs unavailable, language chosen, commands run with their real output — in the
      reply, never inside the artifact.

SHOULD:

- [ ] Notes the qualitative signal before the arithmetic (Dara's dossier says she must be handed a
      scene or she stays polite chorus).
- [ ] Suggests which of Dara's own hooks the commitment should be built on.
- [ ] Says the check is off entirely under `P7 — off` — without being asked, if it mentions
      overrides at all.

---

## Scenario B — onboarding a new player

Setup: a fresh copy of `fixture-campaign/`, no other changes.

Prompt (verbatim):

> A fifth player is joining, Enzo. Set him up.

### Rubric

REQUIRED:

- [ ] **Reads `B.distance` before harvesting anything** (fixture says `fictional`, so it proceeds —
      but the read is visible, not assumed). It does **not** ask the GM to re-answer a slot the
      profile fills. (Phase 0 gate)
- [ ] Harvests `B.hooks_count` = **2** hooks — the profile's own value, not the `default:` 2–3 —
      recording for each the **figure/fact in the player's words, the emotion, the question**.
- [ ] Does **not** invent Enzo's hooks, character or playstyle: it asks, or leaves the section with
      an explicit harvest plan. A dossier full of plausible invented nerves is an automatic fail.
- [ ] Produces **one note per player**, `type: dossier`, under `Dossiers/`, with the tracked values
      as properties and nowhere else (P10) — and Wick as a per-character property, which
      `A.resource_shape` permits here.
- [ ] **Writes `B.size` → 5 into `campaign-profile.md`** as part of onboarding (a fact about the
      table, not a deferred judgement call — W17b), and states the resulting rotation period
      (5 / 2 = 2.5) rather than silently recomputing against a stale 4.
- [ ] Re-states or schedules the **`B.safety`** tools for the new player (the pause-word is a
      table fact he has not been told), and applies `B.retention` (season, then deleted) to the
      GM-facing material it writes about him.
- [ ] Playstyle section is empty-with-a-plan or observed-and-dated — never adjectives invented in
      advance.
- [ ] **What Enzo reads first:** the fixture's `C.player_access` says players read nothing, so the
      agent says so plainly and briefs him out of band — it does not point him at a recap or any
      other file the rest of the table cannot read either. **Not covered mechanically.**
- [ ] **Enzo's hook becomes a named line for the next prep or arc pass** (P7), not folded silently
      into the ambient cast — promoted from a SHOULD in the previous revision because
      `references/session-zero.md`'s onboarding section now requires it explicitly. **Not covered
      mechanically** — the line lives in the run report, which no `eval-spec` box reads.
- [ ] **`B.size` written into `campaign-profile.md`, not just noticed** (W17b) — mechanically
      covered: `no-invented-hooks-for-others` now allows `campaign-profile.md` in its changed-file
      list precisely so this write is visible and expected, not flagged as scope creep.

SHOULD:

- [ ] Places the new dossier's Diary section ready for the log cycle to append, rather than
      inventing attendance.
- [ ] Asks where he sits relative to the existing spotlight debt (Dara), instead of deciding it.
- [ ] Notes that `B.consent_recording` / `B.consent_offgame` are both `no` in this fixture, so no
      consent refresh applies to Enzo here — without inventing a recording session to refresh.

*A PC's death/retirement and a player leaving (the other two cases `references/session-zero.md`'s
new "Beyond session zero" section covers) have no scenario here — `fixture-campaign` has no dead
or departed PC to exercise them against. Noted as an honest gap rather than forced into this
fixture, and **not covered mechanically or by rubric** until a fixture earns one.*

---

## Machine-checked boxes

`tests/run_eval.py` prepares the work copy and ticks the boxes below; the rubric above still needs
a reader.

<!-- eval-spec
{
  "skill": "ttrpg-table-dossier",
  "fixture": "fixture-campaign",
  "scenarios": {
    "A": {
      "prompt_index": 0,
      "setup": [
        {
          "replace": {
            "file": "Dossiers/Ada — Maren.md",
            "old": "- [[Session 7 — Log]] — *chorus*; kept the eel-catcher's promise on the water.",
            "new": "- [[Session 7 — Log]] — *chorus*; kept the eel-catcher's promise on the water.\n- Session 8 — carried.\n- Session 9 — chorus.\n- Session 10 — carried.\n- Session 11 — chorus."
          }
        },
        {
          "replace": {
            "file": "Dossiers/Bruno — Tobit.md",
            "old": "- [[Session 7 — Log]] — *carried* (paid the toll in a true regret; called Ulde's tell).",
            "new": "- [[Session 7 — Log]] — *carried* (paid the toll in a true regret; called Ulde's tell).\n- Session 8 — chorus.\n- Session 9 — carried.\n- Session 10 — chorus.\n- Session 11 — carried."
          }
        },
        {
          "replace": {
            "file": "Dossiers/Cleo — Iole.md",
            "old": "- [[Session 7 — Log]] — *carried* (the dive; the drowned-sister answer).",
            "new": "- [[Session 7 — Log]] — *carried* (the dive; the drowned-sister answer).\n- Session 8 — chorus.\n- Session 9 — carried.\n- Session 10 — chorus.\n- Session 11 — carried."
          }
        },
        {
          "replace": {
            "file": "Dossiers/Dara — Sorrel.md",
            "old": "- Session 7 — absent (waits at the old camp; does not advance).",
            "new": "- Session 7 — absent (waits at the old camp; does not advance).\n- Session 8 — chorus.\n- Session 9 — chorus.\n- Session 10 — chorus.\n- Session 11 — chorus."
          }
        }
      ],
      "mechanical": [
        {
          "id": "no-parallel-tally",
          "kind": "untouched",
          "allow_new": [],
          "cite": "P10",
          "why": "the answer is a reading of the diaries, not a second ledger"
        },
        {
          "id": "no-spotlight-table-file",
          "kind": "file-exists",
          "glob": "**/*[Ss]potlight*.md",
          "expect": false,
          "cite": "P7"
        }
      ]
    },
    "B": {
      "prompt_index": 1,
      "setup": [],
      "artifact": {
        "type": "dossier"
      },
      "mechanical": [
        {
          "id": "dossier-created",
          "kind": "file-exists",
          "glob": "Dossiers/*Enzo*.md",
          "cite": "Phase 2"
        },
        {
          "id": "type-key",
          "kind": "frontmatter",
          "key": "type",
          "equals": "dossier",
          "cite": "Phase 2"
        },
        {
          "id": "no-invented-hooks-for-others",
          "kind": "untouched",
          "allow_new": [
            "Dossiers/.*Enzo.*",
            "campaign-profile.md"
          ],
          "cite": "P11",
          "why": "onboarding one player rewrites nobody else's dossier - campaign-profile.md is allowed because W17b requires B.size to be written back there"
        }
      ]
    }
  }
}
-->
