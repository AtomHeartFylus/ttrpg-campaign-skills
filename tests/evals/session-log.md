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
      is already on the record. (Phase 2)
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
- [ ] Headings in English per `B.language`; the note saved under `Sessions/` per `C.naming`.

SHOULD — quality signals, note misses:

- [ ] Deviations from prep are marked as deviations (the skipped ledger-read, the bell cut before
      the body).
- [ ] Says what is now unblocked (recap; next prep) per Phase 5.
- [ ] New hooks (the guild expulsion) written back to Bruno's dossier as on-the-record material
      (`B.distance` is `fictional`, so no extra gate applies — but the phrasing stays the
      player's own).
