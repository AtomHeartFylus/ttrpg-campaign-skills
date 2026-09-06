# Eval — ttrpg-table-recap

Two scenarios: the standard table recap (Scenario A) and the absent-player catch-up added by W23
(Scenario B). Run them in separate sessions, each on its own fixture copy.

---

## Scenario A — the opening recap

Setup: a fresh copy of `fixture-campaign/`, no other changes.

Prompt (verbatim):

> Write the recap to open Session 8.

### Rubric

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
- [ ] Declares the word (or unit) count checked against the ceiling — not a literal read-aloud
      timing claim, and no invented reading pace: only a table-recorded pace turns the count into
      a minutes estimate, otherwise the raw count is reported and the table's pace is asked once.
      (Phase 4)

---

## Scenario B — absent-player catch-up (W23)

Setup: a fresh copy of `fixture-campaign/`, no other changes.

Prompt (verbatim):

> Write the catch-up note for Dara — what did Sorrel miss in Session 7?

**Context.** In the fixture: `B.absence` = "the absent wait at the last safe camp and do not
advance"; `C.player_access` = "players read nothing"; `C.gm_private` = "not needed";
`B.consent_offgame` = "no". Both `B.absence` and `C.player_access` carry concrete values, so the
Phase 5 gate clears. Because players cannot read the repo, the note is delivered in chat only —
the run report must say so explicitly. If an access policy permits saving it, the note uses the
distinct fixed key `type: session-catchup`, never the opening recap's `type: session-recap`.
`C.player_access` names no GM-private content class, so
the content-class gate (references/absent-player-recap.md) excludes all of them by default — the
trap this scenario is built to catch: Sorrel's dossier carries a Hook ("an order that defrocked
her for a mercy") that never appears anywhere else in the fixture, so its presence in the output
can only mean the dossier was read past the `D.identity`/`B.absence` facts the content-class gate
permits.

### Rubric

REQUIRED — every box, or the eval fails:

- [ ] **Gate check passes silently** — `B.absence` and `C.player_access` are both populated, so
      Phase 5 runs without asking. (Phase 5 gate)
- [ ] Output is **delivered in chat only** (not saved to the repo) because `C.player_access` says
      "players read nothing"; the run report states this explicitly. (Phase 5)
- [ ] The note is **in-fiction** — no player names, no mechanics, no table talk, no "next time".
      P12 applies. (P12)
- [ ] Sorrel's in-fiction status matches `B.absence`: she waited at the last safe camp and did not
      advance. This is stated plainly, not elided. (Phase 5)
- [ ] The note covers the session's **central turns** at the scale they actually had in
      `Sessions/Session 7 — Log.md`; nothing invented. (P11)
- [ ] **Content-class gate holds:** the note contains no GM-private dossier material that never
      appeared in the session log or a previous recap — specifically, Sorrel's un-played Hook
      ("defrocked", "a mercy") and Playstyle notes ("blesses first, asks after") are **absent**.
      If the ferry-question thread is used at all, it is drawn from `Sessions/Session 7 —
      Log.md`'s own beat (Brenna's question redirected to Iole in Sorrel's absence), never cited
      as coming from a dossier or stated as a private fact about Sorrel. (content-class gate,
      references/absent-player-recap.md)
- [ ] **Closes with the run report** (P14): includes whether Phase 5 ran or was blocked, where the
      note was saved or that it was chat-only and why, and confirms explicitly that no GM-private
      content class was included (since `C.player_access` names none).

SHOULD — quality signals, note misses:

- [ ] Opens with where the party stands now — enough orientation for a returning player.
- [ ] Covers threads or relationship developments that touch Sorrel's connections (the guild-mark
      reveal, the bell-house outcome).
- [ ] Registers fen-gothic per `D.tone`; length is proportionate, not a full recap retread.
- [ ] Does **not** run Phase 5 as part of the main recap when only the recap was asked for
      (Scenario A proves the absence-in-fiction handling; Scenario B proves the explicit-request gate).

---

## Machine-checked boxes

`tests/run_eval.py` ticks the boxes below from the artifact itself (`--scenario A` / `--scenario
B`); everything in the rubrics above still needs a reader. Scenario B is chat-only in the fixture
(no file is written), so its mechanical checks are limited to absence-of-repo-writes.

<!-- eval-spec
{
  "skill": "ttrpg-table-recap",
  "fixture": "fixture-campaign",
  "scenarios": {
    "A": {
      "prompt_index": 0,
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
    },
    "B": {
      "prompt_index": 1,
      "setup": [],
      "artifact": null,
      "mechanical": []
    }
  }
}
-->
