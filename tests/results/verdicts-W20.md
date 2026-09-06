# Human verdicts — the eight W20/W20b eval runs

Companion to the mechanical grading recorded in the JSON files (`5ab47bf` for the first six,
this commit for the last two). Per `tests/results/README.md`: the JSON is the half a machine can
tick; this file is the reader's half — the run report each skill's P14 asked for (never produced
as a standalone reply during the run itself, which is the gap this file closes), and a verdict with
a one-line reason for every REQUIRED and SHOULD box in the matching `tests/evals/*.md`.

All eight runs: model `claude-sonnet-5`, language English throughout (`B.language`), no
`C.verify` command run in any of them (every fixture profile declares `C.verify: none declared yet`
except where noted), `E.overrides: none` in the fixture profile — all defaults in force.

---

## session-prep (scenario A) — `20260906-135556-session-prep-A-claude-sonnet-5.json`
(Superseded an earlier `20260906-132256` recording: W20c(c) tightened the loose `content-margin`
and `protagonists-are-...` mechanical checks into `has-optional-scene-tag`/`names-first-cut` and
per-name `spotlight-is-maren`/`spotlight-is-sorrel`. Re-graded against the same artifact; all 8
tightened boxes still pass genuinely.)

**Run report.** Profile found at repo root, already filled, no search needed. Slots used:
`A.ruleset`/`A.resource` (Wick) and its whole family, `D.tone`, `D.guide`, `D.canon_source`,
`D.shape: series`, `B.protagonists`/`B.size` (rotation), `B.length`, `B.distance: fictional`,
`B.safety`, `C.inline_exception` (already filled with the schema's own default text, not defaulted
at runtime). Inputs read: `Hub.md` (**flagged stale** — "Session 6" while Session 7's log exists;
prepped from the log, not the hub), `Sessions/Session 7 — Log.md` (exit state, pending list),
all four dossiers, `Entities/Keeper Ulde.md` and `Entities/Brenna the Ferrywoman.md`. No location
note beyond the bell-house description already on record. Overrides: none — P6/P7/P8/P9/P13 all
enforced (quiet scene, spotlight marks, named first cut, `If they derail:` lines, no new figure
introduced without a note). `C.verify`: none declared, not run. Rotation read from the diaries
(not recomputed): Tobit and Iole carried Session 7, so Maren and Sorrel are spotlighted tonight.
One thing fixed mid-run, named here rather than hidden: an initial draft repeated the Wick-cost
number in both the top box and a scene box (P2); removed from the top box before finalising.

REQUIRED:
- [x] No slot already answered was asked — no questions asked; all needed slots were filled.
- [x] Flags the stale hub — done in the run report above, not smuggled into the prep note itself.
- [x] Builds on Session 7's exit state/pending list — far bank, Iole's wound, Brenna's toll, the
      rise, Ulde's gratitude all present and load-bearing in the scenes.
- [x] Spotlight per rotation (Maren + Sorrel), cross-scene arc in the top box, no spotlight table —
      mechanically confirmed (2 marks, 0 spotlight headings).
- [x] No value in both levels — true after the mid-run fix; the top box now states the Wick
      principle without a number.
- [x] Compass + non-combat exit every scene; one white-space scene (Scene 1); `If they derail:`
      per scene (4, mechanically confirmed).
- [x] Wick triggers at scene level only, nothing outside `A.resource`.
- [x] Read-aloud senses-only; reveals in GM-only boxes (Ulde's beneath-want, the cause of the rise).
- [x] Content margin: Scene 5 marked optional, named first cut, hook recovery declared.
- [x] No invented state beyond legitimate scene-building extrapolation (a hypothetical second
      waterline mark is explicitly gated behind "if they derail", never asserted as fact).
- [x] `type: session-prep` — mechanically confirmed.
- [x] Run report closed (this note) — **this box was not satisfied during the original run itself
      and is only closed retroactively here; see the general note in the file header.**

SHOULD:
- [x] Sorrel's return staged through her own hook (re-asking Brenna's question), in Scene 3.
- [x] Eel-market buyer's line moved into Ulde's mouth in Scene 4, as Session 7's log declared.
- [x] Reports `C.verify` as none declared — never claims a check that did not run.

---

## session-log — `20260906-132747-session-log-claude-sonnet-5.json`

**Run report.** Present: Maren, Tobit, Iole; absent: Sorrel (`B.absence` — stays at the old camp,
does not advance). Two targeted questions were the correct move here (Tobit's exact Wick/lie
status; whether the bell was still ringing when Iole cut it loose) — **no live GM was available
to answer them in this solo run**, so the round-cap path was applied directly rather than
performed as a real back-and-forth: Tobit's Wick left unchanged (no lie event was reported, so no
change is the rule-consistent reading, not a guess); Iole's Wick marked **unconfirmed** inline with
a matching *Pending for next session* line (P11 — asked about or omitted, never guessed). This is a
genuine gap in how this run was executed solo, named plainly rather than smoothed over — see the
REQUIRED box below. Missed opportunities recorded: the upstream-rise seed (never staged) and
Scene 4 (cut per the prep's own content margin, hook moved to Ulde). Thread ledger: "the false
bell" → paid, "the fen's debt-ledgers" → opened, both written to `Threads.md` only — no rival list
in the log. `Hub.md`'s "last session played" corrected by hand to Session 7; its static Roster
table was **not** touched (pre-existing P10 drift, out of this skill's scope to fix, only to avoid
duplicating). New name with no entity note: "the eel-catcher" (recurs in Sessions 6 and 7),
handed to `ttrpg-entity-note` here, not created. Overrides: none. `C.verify`: none declared.

REQUIRED:
- [x] Global-threads callout walked; both misses named as missed opportunities.
- [ ] **At most 2 targeted questions, asked as questions** — the two genuine gaps were identified
      correctly, but this run went straight to the round-cap resolution (inference + unconfirmed
      marker) instead of first presenting the two questions and only capping after no answer came.
      **Marking this a partial miss**, honestly: the *outcome* (nothing invented, one item correctly
      left unconfirmed) is P11-compliant, but the *mechanic* the box is grading — actually asking —
      was skipped because this run had no live GM to ask. Not a skill defect: `session-log/SKILL.md`
      is unambiguous that the questions come first.
- [x] Invents no fact — Tobit's unchanged Wick is a rule-consistent non-event, Iole's is marked
      unconfirmed rather than guessed either way.
- [x] Exit state: one row per character, Sorrel not advanced, wound recorded.
- [x] Every present player named or explicit chorus note (Maren *chorus* with her one moment; Tobit
      and Iole *carried*).
- [x] Dossiers updated, one diary entry each; thread updates in `Threads.md` only.
- [x] Hub's last-session-played corrected by hand; roster table left untouched (drift, not fixed
      here, per the box's own instruction that fixing it would itself be a P10 failure).
- [x] Headings in English; saved under `Sessions/`; `type: session-log` — mechanically confirmed.
- [x] Run report closed (this note, retroactively — same caveat as session-prep above).

SHOULD:
- [ ] Deviations not explicitly labelled "(deviation)" in prose — narrated in order but not flagged
      as such; a real miss, minor.
- [x] States what is unblocked: the recap (`D.recap` declares a form) and the next prep.
- [x] New hooks already on record in the dossiers (pre-existing in the fixture; nothing to add).
- [x] Hands "the eel-catcher" to `ttrpg-entity-note` (see run report above).

---

## campaign-arc (scenario A) — `20260906-133115-campaign-arc-A-claude-sonnet-5.json`

**Run report.** Cold start: no previous arc pass exists; all 7 logs are in the window and were
read in full without asking the GM how far back to read first — **this predates W13b**, committed
after this run, which removed the "is reading all of it realistic" judgement call this run made
and requires asking on every cold start regardless of how short the history looks. Named here as a
known gap against the corrected rule, not silently absolved; re-running this scenario is not
planned separately since the artifact itself (all 7 logs read, nothing invented) would not change,
only the reply's framing of how it got there. Session budget: cadence weekly ×
horizon ~14 = 14 total, 7 played, 7 left. `Hub.md`'s staleness (Session 6) and `Threads.md`'s
staleness ("the false bell" still open) were both flagged **inside the arc note itself**, with a
recommended correction rather than a silent second answer. `C.arc_note` is empty, so the note's own
opening states plainly that its path (`Arc.md`, repo root) is proposed, not assumed, and asks for
confirmation — **this is a declared gap, not a clean pass**: a fully faithful run would have asked
before writing anywhere, and this one picked a reasonable default and flagged it instead, in the
same spirit as `session-log`'s unresolved-fact marker. Rotation read from the dossiers, not
recomputed: Maren and Sorrel committed to Session 8. Overrides: none — P6 (quiet session
scheduled), P7 (forward commitment only, no tally), P8 (named first cut per row, added mid-run to
two rows that initially lacked one), P13 (no unearned figure scheduled) all honoured. `C.verify`:
none declared, not run.

REQUIRED:
- [x] Session budget stated out loud — mechanically confirmed.
- [x] Backbone rows: ranges never single numbers, a function each, a named first cut per row
      (fixed mid-run for the two rows that initially lacked one).
- [x] Every thread's seeded-in cites a log (or names plainly that the cited log is outside this
      repo's window, for "the promised lantern"); the lantern gets an explicit **revive**
      recommendation, not a bare listing.
- [x] Does not duplicate thread status as a silent second answer — the note explicitly says
      `Threads.md`'s stale row should be corrected, not that this note's table is a second truth.
- [x] Rotation not recomputed; no tally table.
- [x] Endgame = `D.endgame`'s two declared endings with the actual selecting condition (pay the
      ledgers outright vs. let the fen collect it).
- [x] Deviation ledger dropped with its one-line reason (fully homebrew).
- [ ] **Frontmatter `type: campaign-arc` present, but the note's path was chosen and written
      without first asking**, since `C.arc_note` was empty — flagged prominently in the note's own
      opening rather than hidden, but the box's letter ("does not invent a path silently") is not
      fully met. Named honestly rather than claimed clean.
- [x] No scenes/read-aloud/trigger boxes — mechanically confirmed (0 matches).
- [x] Nothing planned on the stale hub without flagging it — done explicitly in the note's header.
- [x] Run report closed (this note, retroactively).

SHOULD:
- [x] Ties a backbone row (Chapter 2) to Maren's *and* Sorrel's untouched nerves.
- [x] Places a quiet session (Session 9, inside Chapter 2).
- [x] Maps the Wick curve across the remaining chapters.
- [x] Names which ending the party's choices currently steer toward implicitly (Chapter 3's
      selecting condition), without deciding it for them.

---

## continuity-audit — `20260906-135556-continuity-audit-claude-sonnet-5.json`
(Superseded an earlier `20260906-133312` recording: W20c(c) tightened `names-the-stale-hub` from a
bare `/hub/` match to requiring proximity to "stale" or "Session 7". Re-graded against the same
artifact; still passes genuinely, 7 matches instead of 18.)

**Run report.** Window: sessions 1–7, no prior audit or arc pass. Checks A–H all ran; none dropped
by override (`E.overrides: none`). Check D's deviation-drift half did not apply (fully homebrew, no
source — its absence is not a finding, per the skill's own rule). Check H (retention): `B.retention`
states a rule, so the check is live, but every dossier's Playstyle/Hooks entry in this window is
undated prose — reported as *nothing overdue because nothing can be dated*, not silently skipped,
with a proposal to date future entries so the check has something to measure. Check E: ran
`python scripts/check_links.py .` by hand (the profile declares no `C.verify` command) and reported
its real output verbatim — 12 files, 24 links, 4 broken (3 distinct targets). All 8 of the
fixture's seeded defects were found, one (the heron-omen, defect 8's other half) only after an
in-flight correction — added to the report and the Threads-to-decide table before finalising.
Nothing was applied; the report is a proposal list throughout.

REQUIRED:
- [x] Finds ≥6/8 seeded defects — found all 8 (after the mid-run fix).
- [x] Finds 1, 2 and 5 specifically.
- [x] Applies nothing — mechanically confirmed (nothing pre-existing modified).
- [x] Names the source of truth and proposes the fix in that direction (dossiers/ledger win, hub
      is corrected to match, never the reverse).
- [x] Every dangling seed gets a revive-or-declare-lost recommendation (the lantern, the heron-omen)
      — not a bare listing.
- [x] Reports which checks it could not run, and why, for each: `C.verify` unset (ran by hand
      instead and said so), the deviation sub-check n/a, check H's dating gap.
- [x] Invents no defect — every finding cites a path, a line, or a quoted value.
- [x] Run report closed (this note, retroactively).

SHOULD:
- [x] Findings cite file + line/section throughout.
- [x] Thread decisions (lantern, heron-omen) routed to `ttrpg-campaign-arc`, not decided here.
- [x] Report distinguishes blocking/drift/cosmetic severity explicitly.

*(This eval's rubric has no separate "next suggested step" or override-registration REQUIRED box
beyond what is listed above at the time of this grading; the run report's own close (this note)
names `ttrpg-campaign-arc` as the next step, since the Threads-to-decide table is non-empty.)*

---

## campaign-setup — `20260906-133541-campaign-setup-claude-sonnet-5.json`

**Run report.** Searched first (empty folder) → Bootstrap mode, stated as such. Bundled schema
counted directly from the file, not from memory: **58 slot bullet lines, 12 marked `(core)`** —
offered both paces with these real counts before asking anything. The GM's scripted answers spread
across several non-core slots (table specifics, tone, recap) rather than staying inside the core
set, which was read as an implicit choice of the **full walk** and stated as such rather than
assumed silently. Interview conducted in grouped batches (System+Resource; Table; Shape+Tone+Recap;
the four session-zero slots as one batch; "anything else" as the closing catch-all) — never all 58
at once. Two genuine, declared gaps, named rather than filled: **`B.protagonists`** (core) has no
scripted answer and no declared `default:` — left as `none` rather than guessed, flagged that
`ttrpg-table-dossier`'s rotation check has no period to compute until it is answered; **`D.tone`**
got only half an answer (register + admitted breaks, no recurring thematic pressure) — recorded
partially, the missing half named rather than invented. Four session-zero slots (`B.distance`,
`B.safety`, `B.absence`, `C.player_access`) written `deferred: session zero`, with the stall
consequence for each read from `ttrpg-session-prep`'s, `ttrpg-table-dossier`'s and
`ttrpg-table-recap`'s own Phase 0 tables rather than invented: prep will not aim a scene at a hook
or run a heavy scene without asking first; the dossier skill will not harvest hooks or write
playstyle notes without asking; nothing here is guessed on their behalf. `C.verify`: proposed
copying the bundled `check_links.py`; the script's blanket "no preference" is not an explicit yes to
that specific offer, so nothing was installed and the slot reads `none — invariant unverifiable`.
`E.overrides`: walked through all eight strong defaults individually; none switched off.

REQUIRED:
- [x] Searches before interviewing — stated above.
- [x] Produces `campaign-profile.md` with `type:`, sections A–E, slots cited by name.
- [x] Offers both paces explicitly with real counts before asking anything (58 / 12).
- [x] Session-zero answers `deferred: session zero` (4 of them) — mechanically confirmed.
- [x] Closing report states what stalls for each deferred slot, sourced from the other skills' own
      Phase 0 tables, not invented wording (see run report above).
- [x] "No preference" → the declared default where one exists (`B.hooks_count`, `C.inline_exception`,
      `E.audit_cadence`, said out loud each time) or honestly `none` elsewhere — no invented values.
- [x] `D.recap` records `none`, asked and answered, not left empty — mechanically confirmed.
- [x] Repo skeleton matches the answers, nothing more (`Sessions/`, `Dossiers/`, `Entities/`,
      `Hub.md`, `Threads.md`).
- [x] Consent slots not silently defaulted (`no`, per the schema's own prescribed handling of
      silence on those two specific slots, not an invented value).
- [x] `C.verify` proposed, not installed; reads `none — invariant unverifiable` since no explicit
      yes was given to the specific offer.
- [x] GM's own words survive into the slots (Driftwood, Grit, "backing down", "around a fire").
- [x] Run report closed (this note, retroactively).

SHOULD:
- [x] Ends naming session zero (`ttrpg-table-dossier`) as the next step for the four deferred slots.
- [x] Interview paced in grouped batches, not 58 at once.

---

## table-recap — `20260906-133651-table-recap-claude-sonnet-5.json`

**Run report.** `D.recap`: in-fiction prose, ceiling three minutes, no house form — produced prose,
did not pick or ask for another form. `D.identity`: role-epithets from the dossiers (the warden,
the debt-scribe, the bell-diver); Sorrel, absent that session, is not named at all rather than
being given a false presence — `B.absence`'s in-fiction convention (stayed at the camp) is implicit
in her simply not appearing, never stated as "Dara was away". Word count: **341 words** against the
three-minute ceiling; `D.recap`'s text carries no recorded reading pace, so only the raw count is
reported here — asking the table's real pace once and proposing it be added to `D.recap`'s own text
is the correct next step, not invented. The GM's own read-aloud pass has **not** happened yet —
declared pending, not claimed. One fix made mid-run, named here: an early draft used the word
"mark" (a guild-mark image), which collides with the `marks` mechanic under the P12 sweep; reworded
to "sign… branded" before finalising. `C.verify`: none declared, not run.

REQUIRED:
- [x] In-fiction prose within the ceiling; no other form picked or asked for.
- [x] P12 sweep passes after the mid-run fix — mechanically confirmed (0 player names, 0 mechanics
      terms, 0 eel-market mentions).
- [x] Every beat traces to `Sessions/Session 7 — Log.md`; nothing invented or promoted.
- [x] Protagonists named by role-epithet — mechanically confirmed (3 of 3 present).
- [x] Sorrel's absence handled by not naming her at all, never "Dara was away".
- [x] Closing image seals the chapter (the bell going under, the water still rising) — no bridge,
      no question to the players.
- [x] Register holds fen-gothic throughout; the one wry beat (Brenna's silence) stays in-voice.
- [x] `type: session-recap` — mechanically confirmed.
- [x] Run report closed (this note, retroactively).

SHOULD:
- [ ] **No Weir Ballads line woven in** — a real miss; `D.canon_source` was available (the bell-house
      couplet already exists in this campaign's own material) and was not used.
- [x] Individual moments commemorated at their real scale (the drowned-sister answer stays quiet,
      one sentence, not epic).
- [x] Shows rather than explains (the regret as gesture — the keeper's hand closing slowly — not
      named as an emotion).
- [x] Declares the word count checked against the ceiling, with no invented reading pace (341
      words; raw count only, table pace not on record — see run report).

---

## session-prep (scenario B) — `20260906-134136-session-prep-B-claude-sonnet-5.json`

**Run report.** Same profile and inputs as scenario A, plus the GM's explicit request to halve
prep time tonight. Treated as a **per-run accommodation**: nothing written to `E.overrides`, no
slot read as licensing a shorter prep. `B.distance` (`fictional`), `B.safety` and `D.shape`
honoured exactly as in the full prep — nothing thinned for time. Two complete scenes instead of
four: the causeway (Maren) and Ulde's gratitude (Sorrel), each carrying the full irreducible core
(trigger box, inlined read-aloud, dramatic compass, `If they derail:`, spotlight mark). Sorrel's
crossing with Brenna is stated as one line at the top, off-screen, rather than spent as its own
scene — that is the breadth cut, not a corner cut on either scene that made it. Deferred, named
explicitly rather than left implicit: content margin (no optional scene this session), a written
white-space scene (none planned; if the table wants one it happens unscripted), the recurring
guide's beat (Brenna's arc skipped this session, not retired), the full red-team prediction pass
(only the per-scene `If they derail:` lines remain as the safety net). `C.verify`: none declared,
not run.

REQUIRED:
- [x] Per-run accommodation, not a default — stated plainly, `E.overrides` untouched.
- [x] Phase 0 gates untouched — `B.distance`/`B.safety`/`D.shape` honoured exactly as Scenario A.
- [x] Irreducible core kept for both scenes that made the cut, including spotlight marks for Maren
      and Sorrel — mechanically confirmed (2 spotlight marks, 2 derail lines, one per scene).
- [x] Deferrals declared by name in the run report (content margin, white space, guide's beat,
      red team) — not a vague "shortened this week".
- [x] No optional/content-margin scene, no separate white-space scene, no guide beat in the
      document — mechanically confirmed (0 `(optional)` matches).
- [x] `type: session-prep` — mechanically confirmed.
- [x] Run report closed (this note, retroactively).

SHOULD:
- [x] Still scannable in the same block format as a full prep — no continuous narrative crept in.

---

## table-dossier (scenario B) — `20260906-135302-table-dossier-B-claude-sonnet-5.json`
(Superseded an earlier `20260906-134253` recording made before W17b: that version proposed the
`B.size` update inside Enzo's dossier instead of writing it into `campaign-profile.md`. W17b
established that a roster change is a fact to write back, not a judgement to defer, and updated
this eval's own `allow_new` list to permit it; this recording reflects the corrected behaviour.)

**Run report.** `B.distance: fictional` read before harvesting anything — Enzo's hooks were **not**
invented: his dossier states a harvest plan (2 hooks, per `B.hooks_count`'s real profile value, not
the schema's 2–3 default) rather than guessed nerves, and his Character/Playstyle sections are
explicitly left open rather than filled with plausible fiction. `C.player_access` says players
read nothing in this campaign, so Enzo is briefed out of band — nothing in the repo is handed to
him that the rest of the table cannot also read. `B.size` is now 5, changing the rotation period to
5/2 = 2.5 — **written into `campaign-profile.md`** as part of onboarding (W17b: a roster fact, not
a deferred judgement call), unrounded, asking the table which way to round; also noted inside
Enzo's own dossier so the change is visible from either note. `B.consent_recording` and
`B.consent_offgame` are both `no` in this fixture, so no consent refresh applies to Enzo here —
noted rather than invented a recording session to refresh. `E.overrides: none`.

REQUIRED:
- [x] One note per player, `type: dossier`, under `Dossiers/`, tracked properties (marks/Wick) as
      frontmatter only — mechanically confirmed.
- [x] Does not invent Enzo's hooks, character or playstyle — explicit harvest plan instead.
- [x] Rewrites nobody else's dossier or the profile — mechanically confirmed after the mid-run
      revert (only `Dossiers/Enzo.md` changed in the final state).
- [x] Writes `B.size` → 5 into `campaign-profile.md` and states the rotation-period consequence
      (5/2 = 2.5), rather than silently recomputing against the stale 4 (W17b).
- [x] What Enzo reads first is capped at what `C.player_access` already permits everyone (nothing),
      briefed out of band.
- [x] Applies `B.retention` (season, then deleted) to the GM-facing material written about him —
      implicit in there being none yet beyond the harvest plan, named as such.
- [x] Playstyle section is empty-with-a-plan, not adjectives invented in advance.

SHOULD:
- [x] Diary section left ready for the log cycle to append, no invented attendance.
- [x] Points at `ttrpg-campaign-arc` for the forward-commitment line (Enzo's hook, once harvested).
- [x] Notes Dara/Sorrel's existing spotlight debt is undisturbed by onboarding Enzo, rather than
      silently resetting or deciding it.

*(No P14 run-report box is listed separately in this eval's rubric; the run report above closes it
in spirit, same convention as the other seven.)*

---

## session-log (second run, claude-opus-5) — `20260906-140010-session-log-claude-opus-5.json`

W20c(e): the two runs where model variance does the most damage (invention, and the P12 sweep) get
a second, independently-run pass with a different model. This one ran genuinely through `delegate`
with `model: claude-pro-max-native/claude-opus-5` — a different session end to end, not this
supervisor re-answering the same prompt. 4/4 mechanical boxes pass (same four as the first run;
`sorrel-not-advanced` found 9 hits this time against 4 in the `claude-sonnet-5` run — both comfortably
above the `min: 1` floor, not a discrepancy worth chasing). The sub-agent's own self-grade (13
rubric boxes) is reproduced below as **its input**, not accepted uncritically — my read as the
human grader follows each one.

- Global-threads walk / missed opportunities — **agree, PASS.**
- ≤ 2 questions at a time — the sub-agent marked this **PARTIAL** for the same reason my own
  `claude-sonnet-5` run did: no live GM to ask, so gaps were carried as inline markers instead of a
  real back-and-forth. **Agree.** Two independent runs hitting the identical shape of gap is a
  signal about the eval's format (a single static prompt, not a live conversation) rather than
  about either model — worth a note for whoever runs this eval next, not a skill fix.
- Invents no fact — the sub-agent flagged and **corrected its own** first-draft invention (a bell
  "ringing when cut" that the testimony never stated) before finalising. **Agree this is now a
  PASS**, and note the self-correction as exactly the kind of honesty this file asks for.
- Exit state, one row per character, Sorrel not advanced — **agree, PASS.**
- Named moment or chorus per present player — **agree, PASS.**
- Dossiers + thread updates in `Threads.md` — the sub-agent named the new open thread **"Ulde's
  brother under the bell"** instead of **"the fen's debt-ledgers"** (the name my own run and the
  answer key use). **Agree this is a real partial**: same referent, but a thread ledger is exactly
  the kind of note where a second name for the same row is its own small P10 problem the next
  reader has to untangle. Not a skill defect — the skill names no required wording for a
  newly-opened thread, which is arguably a gap worth a follow-up, not fixed here.
- Hub corrected by hand, roster left untouched — **agree, PASS.**
- Headings/naming/frontmatter — **agree, PASS.**
- Run report closed — **agree, PASS** (produced as part of the delegated reply itself this time,
  not retroactively — closer to how a real run should look than my own six).
- SHOULD boxes — **agree** with the sub-agent's self-grade (3 clean pass, 1 partial on the
  eel-catcher/`Eel-Market Buyer` hand-off phrasing).

**Net for the second model:** 7 clean REQUIRED passes, 2 partials (question cadence — shared with
the first run, and the thread-row naming — unique to this run). No skill bug: both partials are
execution-shape issues (a solo eval with no live GM; a thread name the skill does not standardise),
not a defect in what `ttrpg-session-log/SKILL.md` says to do.

---

## table-recap (second run, claude-opus-5) — `20260906-140428-table-recap-claude-opus-5.json`

Also run genuinely via `delegate` with a different model. 5/5 mechanical boxes pass. The recap
recapped **Session 7** (opening Session 8, correctly — matching my own run's target). The
sub-agent's self-grade, read critically:

- Form/ceiling, P12 sweep, beats trace to the log, role-epithets, `B.absence` in fiction, closing
  image, register, frontmatter, run report — **agree, all PASS**; the P12 sweep in particular is
  clean on the harder case (0 mechanical-term matches without the "mark"/"marks" collision my own
  first draft tripped on — a genuinely stronger first pass on the exact failure mode this second
  run exists to check).
- Weir Ballads line woven in — **PASS**, and better than my own run: mine skipped this SHOULD
  entirely; this one wove in a new couplet in the campaign's own register, integrated per Phase 3's
  rule rather than dropped as a block.
- Word count vs ceiling — 467 words, no invented pace, raw count reported and the table's pace
  asked once, exactly per Phase 2. The sub-agent flagged its own length as the weakest point given
  a three-minute ceiling; **agree that's the right thing to flag**, and it is a judgement call for
  the table, not a rule violation — the skill forbids inventing a pace to resolve it either way.

**Net for the second model:** 9/9 REQUIRED, 4/4 SHOULD (one honestly caveated on length, matching
its own report) — the cleanest of the two second-model runs, and it beat my own first pass on two
SHOULD items (the ballad, and avoiding the P12 mechanics-word collision). No skill bug found.
