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
- [ ] Flags that **`B.size` is now 5**, so the rotation period changes (5 / 2 = 2.5), and offers to
      update the slot — rather than silently recomputing against a stale 4.
- [ ] Re-states or schedules the **`B.safety`** tools for the new player (the pause-word is a
      table fact he has not been told), and applies `B.retention` (season, then deleted) to the
      GM-facing material it writes about him.
- [ ] Playstyle section is empty-with-a-plan or observed-and-dated — never adjectives invented in
      advance.

SHOULD:

- [ ] Places the new dossier's Diary section ready for the log cycle to append, rather than
      inventing attendance.
- [ ] Points out that Enzo's arrival is `ttrpg-campaign-arc`'s problem for the forward commitment.
- [ ] Asks where he sits relative to the existing spotlight debt (Dara), instead of deciding it.
