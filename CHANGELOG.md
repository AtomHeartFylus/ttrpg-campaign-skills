# Changelog

This package is **meant to be forked**: your campaign clones it, fills a profile, maybe adds an
overlay. This file is how a fork learns what moved upstream — each entry names what changed,
**why** (the lesson), and what a fork or an existing campaign must do about it, if anything.
Skill versions live in each skill's `metadata.version`, the package's own number in `VERSION`;
entries here are grouped by change, newest first. A schema change always carries a **Migration**
note. What each part of a version means, and how a release is cut: [`docs/RELEASING.md`](docs/RELEASING.md).

## Unreleased

- **Overlay diagnostics survive validation across filesystem drives.** `validate_overlay.py` keeps
  relative paths when `os.path.relpath` can compute them and falls back to an absolute,
  slash-normalized path when the drives differ. *Lesson: CI's checkout and temporary directories
  need not share a Windows drive.* No schema change.
## 2.1.0 — a consent gate an Italian table can pass

- **The two consent gates now declare the form of their answer: the token `yes`/`no` first, then
  what the table said, in the table's own language.** `validate_profile.py` has always gated the
  capture pipeline on `^(yes|y)` — English, and only English — while the package ships `B.language`
  and claims to work for a table that does not play in English. The schema said "an explicit
  `yes`" and never said the word had to be *that* word, and `references/interview.md` told the
  interviewer to "write exactly what you were told": at an Italian table those two instructions
  produce `**sì.** Il consenso è stato dato esplicitamente al tavolo da tutti i presenti` — a real,
  explicit, per-person consent that the validator then rejects as missing. Fixed by declaring the
  form in `templates/campaign-profile.md` (`B.consent_recording`, `B.consent_offgame`), teaching
  the interview to write the token before the verbatim sentence, and rewriting both `CROSS-SLOT`
  messages to say that a consented table is looking at a *form* fix and not at a consent question.
  The validator's behaviour is unchanged — what changes is that the rule it enforces is now
  written where the GM reads it. *Lesson: a consent gate that produces a false negative is worse
  than one that produces none, because the workaround — editing a consent slot until the tool goes
  quiet — is exactly the habit the gate exists to prevent. The package generated that state itself:
  its own interview instruction, followed exactly, wrote a profile its own validator failed.*
  `metadata.version`: `ttrpg-campaign-setup` 1.17 -> 1.18.
  **Migration:** a filled profile whose `B.consent_recording` or `B.consent_offgame` answers in a
  language other than English must put the literal token first — `**yes** — <the sentence you
  already have>` — keeping the existing sentence untouched. **Only the person who holds the
  consent may make this edit**: it records an answer the table gave, and no skill and no agent may
  supply the token on the profile's behalf. A profile that answers `no`, or has not asked yet,
  changes nothing.

## 2.0.0 — behaviour measured, not just form

- **The absent-player catch-up now has its own artifact type, and the recap entrypoint keeps only
  the length rule.** `ttrpg-table-recap`'s privacy-gated Phase 5 used to label a catch-up note
  `type: session-recap`, which let a consumer locating artifacts by fixed type mistake a player
  recovery note for the opening recap. Catch-ups now carry `type: session-catchup`, added to the
  package artifact contract. The detailed one-way length-ceiling procedure moved to
  `references/length-ceiling.md`, leaving the Phase 2 entrypoint with the measurable rule and a
  local pointer; the entrypoint remains under `ENTRYPOINT-BUDGET`. *Lesson: a fixed type is a
  dispatch key, not a loose label — two artifacts with different privacy and audience contracts
  cannot share it merely because one is a variant of the other.* `metadata.version`:
  `ttrpg-table-recap` 2.3 -> 2.4.
  **Migration:** the package artifact contract now includes `session-catchup`; campaigns that
  save an absent-player note should use that key instead of `session-recap`. No profile slot was
  added or renamed, but this is a package contract change and belongs to the next major release.

- **The three `EXAMPLE-DRIFT` warnings and the `EVAL-RECHECK` for `ttrpg-entity-note` are
  consciously accepted, not forgotten.** Against `v1.2.0`, `ttrpg-entity-note` and
  `ttrpg-session-prep` only moved their Phase 0 slot-degradation material verbatim and marked the
  remaining gates; their artifact skeletons and required-element lists did not change. For the
  same reason, `tests/evals/entity-note.md` was not changed: `EVAL-RECHECK` fires on any
  `SKILL.md` diff, while this diff touches no phase, branch or required element. `ttrpg-table-recap`
  added a verification-procedure refinement and a separate `session-catchup` artifact, neither of
  which belongs in the main recap example. Updating `references/example-recap.md` merely to silence
  the heuristic would make it less faithful to the skeleton it demonstrates. The warnings remain a
  review prompt, not release blockers; the future question is whether `session-catchup` earns its
  own worked example.
  *Lesson: `EXAMPLE-DRIFT` and `EVAL-RECHECK` compare changed files, not skeleton content, so a
  recurring warning needs a recorded content-level decision or it becomes noise that reviewers
  learn to skip.*

- **The bundled link checker no longer trusts a path outside the campaign root.**
  `scripts/check_links.py` (bundled byte-identically at
  `skills/ttrpg-campaign-setup/references/check_links.py`, the `C.verify` tool this skill
  proposes) resolved a slash wikilink or a relative markdown link that climbed above the root with
  `../` — or started with `/`, which `os.path.join` silently treats as filesystem-absolute — by
  checking whatever real file that path happened to reach, anywhere on the machine that ran the
  check. Both forms are now rejected as `broken` whenever the resolved target normalizes to
  outside the campaign root, even when a file genuinely exists there; a leading `/` is now treated
  as rooted at the *campaign* root, matching how a slash wikilink already worked. Markdown links
  also gained the optional-title forms CommonMark allows — `[text](path.md "Title")`,
  `[text](path.md 'Title')`, `[text](<path.md> "Title")` — which previously failed to match the
  link regex at all and were silently never checked. *Lesson: a link checker that walks directories
  by hand (for the case-mismatch check) has to say explicitly where it refuses to walk, or `../../`
  is a working escape hatch out of the one boundary the tool exists to enforce — and a regex that
  cannot parse a valid link form is a link this checker was silently not checking, which is worse
  than reporting it broken.* `metadata.version`: `ttrpg-campaign-setup` 1.16 -> 1.17 (the bundled
  copy changed; its own `SKILL.md` text did not). No migration: no slot changed, `C.verify`'s
  contract ("0 broken links") is unchanged.

- **W23 follow-up — the catch-up phase read `C.player_access` as a save location and never as
  a content-class filter.** `ttrpg-table-recap`'s Phase 5 correctly gated *whether* the note ran on
  `B.absence`/`C.player_access`, but once it cleared, the reference procedure pointed the writer at
  "the dossiers" undifferentiated — Playstyle, Hooks and (had consent allowed one) the off-game
  note were exactly as reachable as the `D.identity` mapping and the `B.absence` fact the note
  actually needs. `references/absent-player-recap.md` now reads `C.player_access` and
  `C.gm_private` as a **content-class policy**: dossier Playstyle, dossier Hooks, off-game entries
  and raw transcript facts are excluded from a Phase 5 note **by default**, and only an explicit,
  named permission in `C.player_access` admits one of them — an ordinary "players may read recaps
  and logs" value reaches none of the four. No consent is inferred and no new gate was added:
  `B.absence`/`C.player_access` still gate whether Phase 5 runs at all, unchanged. *Lesson: a
  two-slot go/no-go gate at the top of a phase can be exactly right and still leave the phase's
  body reading a source (a player dossier) that carries several content classes at once with no
  per-class rule — gating access to the phase is not the same question as gating what the phase,
  once running, is allowed to pull out of what it reads.* `metadata.version`:
  `ttrpg-table-recap` 2.1 -> 2.2. No migration: no slot added, `C.player_access`/`C.gm_private`
  already existed and are read the same way everywhere else that reads them.

- **W23 — the absent-player catch-up is a gated phase, not a freebie (retroactive entry).**
  `ttrpg-table-recap` gained Phase 5 (`references/absent-player-recap.md`), run only on explicit
  request ("write the catch-up for Dara"), never automatically. It is gated on two slots read as
  content-class policy, not merely "where to save": `B.absence` (the in-fiction convention for
  absent characters) and `C.player_access` (what players may read). Either empty or `deferred:
  <when>` blocks the phase and is reported in the run report; the phase never guesses a value for
  either. `E.overrides`'s `P12 — off` now explicitly applies to both the main recap and the
  absent-player note. *Lesson: a "just tell the absent player what they missed" feature looks
  harmless until it is asked to summarise session content for someone who was not at the table —
  at that point it is a privacy decision (what crosses from the room to a person who wasn't in it),
  not a formatting one, and it needs the same two-slot gate as everything else in this package that
  touches who gets to read what.* `metadata.version`: `ttrpg-table-recap` 1.9 -> 2.0. No migration:
  no slot added, both slots already existed in the schema.

- **W22 — the substrate is a capability contract, not a tool contract (retroactive entry).**
  Reworded `AGENTS.md`, `README.md`, `SECURITY.md` and `docs/PRIVACY.md` to state precisely what
  this package requires of its storage: a local folder an agent can list, read and write, with
  stable file paths — not version control. Version control stays a **strong recommendation** (the
  only reliable recovery path from a bad write, and the only basis for enforcing `C.portability`),
  but a GM working from a plain, unversioned folder can use every skill; they accept that a bad
  write becomes permanent. `ttrpg-campaign-setup`'s Phase 0 wording changed from treating missing
  version control as blocking the portability rule to flagging and recommending it. *Lesson: the
  package had quietly hardened "recommended" into "required" in several places (`git`, "your git
  history", "version-control-ignored folder") without that ever being a decision anyone took —
  `SECURITY.md`'s threat model and `docs/PRIVACY.md`'s retention guidance both need to describe
  what actually happens to an unversioned folder, not assume a safety net that a real table may not
  have.* `metadata.version`: `ttrpg-campaign-setup` 1.14 -> 1.15. No migration: no slot changed.

- **W21b — first-run bootstrap without a full profile.** Added conversational
  "draft in chat" sub-mode when `E.deliverable` is set to `draft in chat` (or no repo path is
  writable yet), producing the filled profile as a chat artifact. It opens with an explicit
  no-profile declaration listing the slots to be asked, closes with a run report detailing asked/deferred
  slots, and explicitly offers to record confirmed answers into the profile only with consent.
  *Lesson: forcing a file write on a fresh user who is still exploring or lacks a configured repo
  stalls the onboarding — giving them an in-chat draft option makes the initial walk interactive and low-friction.*
  `metadata.version`: `ttrpg-campaign-setup` 1.15 -> 1.16. No migration: no slot changed.

- **The eval harness stops claiming more than it measured (W20c).** `tests/run_eval.py`'s
  recorded JSON renamed its top-level `passed` key to `mechanical_passed` and added `judged: null`
  — a record is no longer one boolean away from reading as a verdict nobody gave, matching what
  `tests/results/README.md` already said in prose. Three mechanical checks that could not fail were
  tightened: `session-prep`'s `content-margin` (passed on the bare word "optional" anywhere, split
  into `has-optional-scene-tag` + `names-first-cut`) and `protagonists-are-...` (passed on both
  names appearing anywhere, split into per-name `spotlight-is-maren`/`spotlight-is-sorrel`);
  `continuity-audit`'s `names-the-stale-hub` (matched on the bare word "hub", 18 times in a report
  that only describes check B; now requires proximity to "stale" or "Session 7"). Two behaviours
  added this lotto (`campaign-arc`'s cold-start ask, `continuity-audit`'s check H) have no
  mechanical box at all; their rubric boxes now say **"not covered mechanically"** explicitly
  rather than leaving a reader to assume a green run exercised them.
  *Lesson: a check that cannot go red is not a check, and a `passed` field that only ever reflects
  a machine's half of the grading is the same false-precision the package refuses everywhere else
  — W20's own six green runs could not see either problem because they never needed check H's
  coverage or a report that gamed `content-margin`.* No `metadata.version` bump: harness and eval
  files, not skills.
- **Human verdicts for the W20 runs, closing what W20 itself left open.** Commit `5ab47bf`
  recorded six mechanical gradings with a one-line commit message; per `tests/results/README.md`
  the human half — including the P14 run-report box, which no file check can see — was never done.
  `tests/results/verdicts-W20.md` now carries, for all eight recorded runs (the original six, plus
  `session-prep` scenario B and `table-dossier` scenario B, run to close W9/W9b/W9c and W17's newly
  REQUIRED boxes that the first pass never exercised): the run report each skill's P14 asked for,
  written for the first time rather than only reasoned about internally, and a pass/partial verdict
  with a one-line reason for every REQUIRED and SHOULD box. Two genuine partials surfaced and are
  named rather than smoothed over: `session-log`'s round-cap mechanic was resolved by inference
  instead of literally asking two questions first (no live GM was available in a solo run), and
  `campaign-arc`'s note path was picked and flagged rather than asked before writing (closed for
  future runs by W13b/W14b's own fixes below). `session-log` and `table-recap` — the two evals
  where model variance costs the most (invention; the P12 sweep) — were additionally re-run with a
  different model (`claude-opus-5` via a genuine sub-agent dispatch, not this session re-answering
  its own prompt) and recorded the same way; both passed, one surfaced and self-corrected an
  invented fact before finalising, the other wove in a canon quote and avoided a P12 word collision
  the first run had tripped on.
- **W14b — continuity-audit check H described a field the package does not produce.**
  `references/checks.md` claimed dossier **Hooks** entries were dated like Playstyle notes; only
  Playstyle notes carry a date (`ttrpg-table-dossier`'s own text). Check H now reports undated
  material as **not measurable**, a different, always-distinct outcome from "nothing overdue" (a
  measurement that actually ran and found nothing) — Hooks entries are always not-measurable, not
  occasionally so. Also removed: the clause letting a subject's own removal request be "applied
  directly" as an exception to "nothing is applied until approved" — that duplicated a rule already
  owned by `ttrpg-session-audio` (off-game note, speaker map) and `ttrpg-table-dossier` (the
  dossier) and made the audit a writer inside an artefact it does not own. Check H now lists the
  material and cites the owning skill's rule, the same shape W15 already used for a name hand-off.
  *Lesson: "nothing overdue" and "nothing measurable" look identical in a short report and are
  opposite claims on a check that touches real people's data — collapsing them is exactly the kind
  of invariant P14 forbids stating without having measured it.* `metadata.version`:
  `ttrpg-continuity-audit` 1.11 -> 1.12. No schema change.
- **W13b — the arc's cold-start clause judged what was "realistic" instead of always asking.**
  `campaign-arc/SKILL.md` Phase 1.2 read "once the log count is large enough that reading all of it
  is not realistic" — the same mood-based trigger W7 had just removed elsewhere ("or visibly has
  one evening in them"). The trigger is now the cold start itself: no previous arc pass exists ⇒
  always ask how far back to read, and a short history simply gets "all of it" as the answer
  instead of the skill deciding that for itself. `tests/evals/campaign-arc.md`'s cold-start box
  updated to require the ask even against the fixture's short 7-log history, and marked **not
  covered mechanically**. *Lesson: replacing one hardcoded number with a a skill's own judgement
  call about what counts as "too many" is the same failure with an extra step — the fix W13
  shipped for the number left the judgement behind.* `metadata.version`: `ttrpg-campaign-arc`
  1.8 -> 1.9. No schema change.
- **W19b — the copyright pointer in session-prep overclaimed what it could enforce.**
  `session-prep/SKILL.md` said `C.player_access` "must never expose it to a player", dropping
  `SECURITY.md`'s own qualifier ("to players who have not bought the source") into an absolute the
  skill has no way to check. Restored the qualifier in the skill's own text. *Lesson: compressing a
  cross-reference for space is a wording fix until it quietly turns a qualified position into a
  promise nothing enforces.* `metadata.version`: `ttrpg-session-prep` 1.11 -> 1.12. No schema
  change; wording only, checker alone covers it.
- **W17b — onboarding noticed `B.size` changed and never wrote it down.**
  `references/session-zero.md`'s new-player section said the rotation now divides by a different
  number and stopped there — nothing told the skill to write `B.size` back into
  `campaign-profile.md`, and Verify never checked it, so the count goes stale in silence from that
  session on. Session zero now writes `B.size` back as part of onboarding (a fact about the table,
  not a deferred judgement call) and Phase 4's Verify gained a matching bullet.
  `tests/evals/table-dossier.md` Scenario B's `no-invented-hooks-for-others` check now allows
  `campaign-profile.md` in its changed-file list for exactly this write, and its rubric box was
  promoted from "flags" to "writes". *Lesson: "the rotation period changes" is not the same
  sentence as "and here is where that number now lives" — W17 wrote the first and assumed the
  second followed from it.* `metadata.version`: `ttrpg-table-dossier` 1.6 -> 1.7. No schema change.
- **Six evals actually run, `tests/run_eval.py` gains a check kind the harness needed to grade one
  of them.** `session-prep` (A), `session-log`, `campaign-arc` (A), `continuity-audit`,
  `campaign-setup` and `table-recap` were each run end to end by an agent following the current
  `SKILL.md` (not simulated), graded and recorded under `tests/results/`. Grading `session-log`
  surfaced a real harness bug: its `dossiers-updated` mechanical box could never pass, because
  `grade()` scopes the text every `regex` check reads to the `type:`-matched artifact alone, and a
  dossier is `type: dossier`, never `type: session-log` — the box was checking a file it could not
  see. New check kind `regex-changed` (scans every changed `.md` file, not just the artifact) fixes
  it without touching every other eval's `regex` boxes, several of which rely on the narrower scope
  on purpose (a `max: 0` box that must not accidentally match a sibling file). Two more findings
  were fixed in the artifacts themselves during the run, not the skill or the harness: a P2
  duplicate value between a prep's global box and a scene box, and a missed dangling seed in an
  audit report — both execution slips, not defects in what the skills say to do.
  *Lesson: a mechanical box is itself code, and this one had never been run for real, so its own
  scoping bug was invisible until an actual grading pass hit it — the same reason `tests/checker`
  demands a fixture per check.* No `metadata.version` bump: `tests/run_eval.py` and one eval's
  `eval-spec` are harness, not a skill.
- **The package states its position on a publisher's copyright.** `SECURITY.md` gains "Copyright
  of imported material": `ttrpg-session-prep` inlines a published module's text directly into the
  prep (Phase 1.2), and neither `SECURITY.md` nor `docs/PRIVACY.md` had ever said whose text that
  still is. The position, in one paragraph and no legal advice: the campaign repo is private
  working material, the publisher's text enters it as a citation for table use, never for
  redistribution, and `C.player_access` must never expose it to a player who has not bought the
  source. Phase 1.2 gains a matching one-line pointer. *Lesson: P15 already treated module text as
  untrusted-for-instructions; nothing had ever addressed the separate question of whose text it
  still is once it is inlined — a red-team pass caught the gap the main review missed because
  neither is a slot or a check, only a sentence nobody had written yet.* `metadata.version`:
  `ttrpg-session-prep` 1.9 -> 1.10. Wording only, no schema change: `check_contract.py` alone
  covers it (AUTHORING §7).
- **README: prerequisites, repo scope, and the missing skill in the cycle diagram.** §Install
  now opens with what you need before anything else — `git`, a shell, Python 3.9+ stdlib-only
  — and what each is for. §"Adopting them for your campaign" states plainly that one campaign is
  one repo with one profile, and a second table is a second repo, never a merge. The cycle diagram
  gains `ttrpg-entity-note`, which never had a place in it despite being one of the nine skills.
  *Lesson: three separate readers hit three separate gaps in the same file — what to install
  before trying anything, whether two tables share one profile, and where the tenth-looking skill
  actually sits — none of which needed a behavioural change, only a sentence each.* No skill
  version bump: README only, no schema change.
- **Three player-lifecycle events the dossier skill never named:** `references/session-zero.md`
  gains "Beyond session zero" — a new player joining mid-campaign (a partial session zero: what
  they read is capped at what `C.player_access` already permits everyone, their hook becomes a
  named line for the next prep or arc pass instead of silent ambient cast, consent refresh is a
  pointer to `ttrpg-session-audio`, never restated); a PC's death or retirement (the dossier stays
  — it is the player's — only the `## Character` section closes, dated and logged, and a new one
  opens beside it); a player leaving (the dossier closes, dated, never deleted, and its GM-facing
  material still answers to `B.retention`). `SKILL.md`'s skeleton, Verify and What NOT to do gain
  matching lines. `tests/evals/table-dossier.md` Scenario B promotes the forward-commitment line
  and the player-access cap from SHOULD to REQUIRED, and adds a box for the consent-refresh
  non-case (`B.consent_recording`/`B.consent_offgame` both `no` in the fixture); death and
  departure have no fixture PC to exercise them against, noted as a gap rather than forced.
  *Lesson: onboarding was already tested (Scenario B) but under-specified — nothing said what a
  newcomer may read or that their hook must reach the next prep, so a run could brief them fully
  from GM-only notes and still pass; death and departure were not named at all, and a dossier
  closed on a character's death would have erased a player's whole rotation history with them.*
  `metadata.version`: `ttrpg-table-dossier` 1.4 -> 1.5. No schema change.
- **Retention is now verified, not just declared:** `ttrpg-continuity-audit` gains check H —
  it walks the GM-facing material about real people that `B.retention` already governs (dossier
  Playstyle/Hooks entries, off-game notes, speaker maps, transcripts) and reports anything past the
  stated rule as a change-list item, same as every other finding: never deleted by the skill
  itself, except an explicit removal request from the person described, which is applied directly
  because the request **is** the approval. Off when `B.retention` is empty or `deferred` — reported
  as unverified, never guessed at. `tests/evals/continuity-audit.md` gains a box: the fixture's
  retention rule is stated but its dossier entries carry no per-entry date, so the correct call is
  "nothing overdue / cannot verify," not an invented finding.
  *Lesson: `B.retention` had readers that promised to keep the rule (`ttrpg-session-audio`,
  `ttrpg-table-dossier`) and nothing that ever checked whether they had — a promise with no audit
  is the same gap W16 just closed for a material promise, one layer up.* `metadata.version`:
  `ttrpg-continuity-audit` 1.9 -> 1.10. No schema change.
- **The arc note has a cold start:** `ttrpg-campaign-arc` Phase 1.2 gains a clause for the case
  with no previous arc pass: a short history is read whole, same as always; once the log count is
  not realistically readable in full, the skill **asks the GM** how far back to read rather than
  picking a window on its own authority, populates the thread tracker and deviation ledger from
  the hub plus that window, and names every earlier, unread log as **unverified backlog** in the
  run report — never silently dropped. `tests/evals/campaign-arc.md` gains a box proving the
  trivial case (7 logs, no window needed) invents nothing; the windowed branch itself has no
  fixture large enough to exercise, noted as such rather than claimed.
  *Lesson: "every session log since the last arc pass" had an unstated ceiling — a campaign with
  no arc note and eighty logs behind it would have made the agent choose a number on its own, which
  is exactly the hardcoded-constant failure the rest of the package refuses everywhere else.*
  `metadata.version`: `ttrpg-campaign-arc` 1.6 -> 1.7. No schema change.
- **A promised material thing is a thread, not a gap:** the open-thread tracker
  (`ttrpg-campaign-arc/references/arc-elements.md`) and check C
  (`ttrpg-continuity-audit/references/checks.md`) now say explicitly that a promised object,
  reward, favour or payment is a thread like any other — seeded-in, owner, what would pay it off,
  status — hunted by the same check that finds a narrative thread gone quiet. No item or economy
  ledger is introduced: currency, inventory and price stay out of scope, exactly as before.
  README's "Known gaps" now says what is covered (the promise, as a thread) against what still
  is not (a running total or a price list). *Lesson: "no item ledger" read as a bigger gap than it
  is — the promise half of it was already the tracker's job, it just never said so, so a GM read
  the disclaimer and looked for a ledger this package was never going to build.* `metadata.version`:
  `ttrpg-campaign-arc` 1.5 -> 1.6, `ttrpg-continuity-audit` 1.8 -> 1.9. No schema change.
- **The log interview has an exit:** "maximum 2 questions at a time" had no ceiling on how many
  rounds, so a session with five gaps meant roughly three rounds of back-and-forth every week.
  Phase 2 now caps the back-and-forth at two rounds (this skill's own conversational pacing, never
  a campaign fact, stated plainly; a GM who wants a different number for a session says so once);
  past the cap, it stops asking and writes the log with the remaining gaps marked `unconfirmed`,
  named in the run report. P11 unchanged: an unconfirmed fact is still asked about or omitted,
  never invented. `tests/evals/session-log.md` gains a note on the expected cap behaviour (the
  scenario's testimony resolves within it, so the cap itself is not exercised there).
  *Lesson: a per-question limit without a per-conversation one protects the GM from one long
  question and not from ten short ones.* `metadata.version`: `ttrpg-session-log` 1.6 -> 1.7. No
  schema change.
- **Two Verify instructions an agent could not actually run are now deterministic proxies:**
  `table-recap` said "read the recap aloud and time it" — replaced by a measurable proxy: word (or
  form-native-unit) count checked against `D.recap`'s ceiling, turned into a minutes estimate only
  when the table has a **recorded** reading pace (in its own `table-recap` overlay); otherwise the
  raw count is reported, the table's pace is asked once, and recording it in the overlay is
  proposed — the schema has no slot for it, and a number this skill invented to fill that gap would
  be exactly the hardcoded constant "empty slot ≠ default" forbids. Actually reading aloud stays
  the GM's action, declared as such rather than claimed by the skill. `session-audio` said
  "spot-check two timecodes" — replaced by a mechanical check (timecodes monotonic; the last cue at
  or before a GM-stated duration, when given), with opening the audio at a position left as the
  explicit human action it always was. `tests/evals/table-recap.md` and `session-audio.md` rubrics
  updated to match. *Lesson: an instruction phrased as an action only a human can perform is either
  skipped or silently simulated by an agent — P14 forbids declaring a measurement that did not
  happen — but the first fix for `table-recap` swapped one unrunnable claim for an invented
  constant; a proxy is only honest if every number in it is either measured or on record.*
  `metadata.version`: `ttrpg-table-recap` 1.6 -> 1.8 (1.7 then this correction), `ttrpg-session-audio`
  1.4 -> 1.5. No schema change.
- **Adoption mode proposes the `type:` contract instead of never mentioning it:** Phase 4 gains a
  step that inventories recognisable package artifacts already in an adopted repo, counts them per
  type, and **proposes** (never silently applies) an additive `type:` frontmatter pass — the same
  fixed key every other skill locates artifacts by, never by filename. Declining is recorded as a
  known gap; the GM is told plainly that prep/recap/audit will not find these artifacts without it.
  Also states that the rotation check counts from the next *recorded* session, not history it never
  read. Phase 4's full procedure moved to a new `references/adoption.md` (needed one way only, in
  this mode) to stay under `ENTRYPOINT-BUDGET`; the entrypoint keeps a condensed pointer.
  *Lesson: an adopted repo satisfied every §C convention question and still stayed invisible to
  every other skill, because none of them find anything except by `type:` — describing a
  convention and applying its one load-bearing key are not the same step.*
  **Known gap, not closed here:** `tests/evals/campaign-setup.md` has only a bootstrap scenario;
  adding a machine-checked box for this needs a new adoption-mode scenario and fixture, which is
  more than this fix's scope — left for a follow-up rather than force a box nothing exercises.
  `metadata.version`: `ttrpg-campaign-setup` 1.7 -> 1.8. No migration: no slot changed.
- **The existing validators are no longer invisible:** `ttrpg-campaign-setup` Phase 5 now runs
  `python scripts/validate_profile.py <profile>` when a clone of this repo is reachable (falling
  back to the manual slot-id diff otherwise), instead of only ever describing the manual diff;
  Phase 3.6 does the same with `validate_overlay.py` once an overlay exists. README's "Checking
  your own campaign" section says outright that both scripts live in the clone, not in an install.
  *Lesson: a script that reads the schema instead of a hand-written diff was sitting unused because
  nothing pointed an agent at it — the fix that mattered was a sentence, not a feature.*
  `metadata.version`: `ttrpg-campaign-setup` 1.6 -> 1.7. No migration: no slot changed.
- **Reduced prep does not touch the Phase 0 gates:** independent review caught that W9's text never
  said so explicitly — `references/reduced-prep.md` and the entrypoint pointer now state plainly
  that `B.distance`, `B.safety` and `D.shape` ask or stop exactly as in a full prep; a reduced prep
  that eroded them by budget pressure would be the same consent/refusal failure the package treats
  as unassailable everywhere else (`04-detrattore.md` §13), not a smaller version of this skill.
  `tests/evals/session-prep.md` Scenario B gains a matching box. `metadata.version`:
  `ttrpg-session-prep` 1.7 -> 1.8. No schema change.
- **Reduced prep, invoked by the GM, not a smaller default:** `session-prep` Phase 3 gains a
  pointer to new `references/reduced-prep.md`: when the GM explicitly asks for a shorter prep this
  session (never on this skill's own initiative, never on an empty slot), it produces the
  irreducible core — trigger box, opening read-aloud, dramatic compass, `If they derail:` line per
  scene, spotlight per `B.protagonists` — and **declares by name** what it deferred: content
  margin, a written white-space scene, the recurring guide's beat, the full red-team prediction
  pass. Per-run, not a default: `E.overrides` does not change, and no number here is this skill's
  own invention. `tests/evals/session-prep.md` gains Scenario B (explicitly requested reduced
  prep) with a REQUIRED box that the deferrals are named, not just made; eval-spec restructured to
  the multi-scenario form already used by `campaign-arc`.
  *Lesson: the only escape from an all-or-nothing required-elements list was switching a principle
  off forever; a GM with forty minutes tonight needed a smaller ask for tonight, not a permanent
  one.* `metadata.version`: `ttrpg-session-prep` 1.6 -> 1.7. No schema change.
- **`E.overrides` explained, and reopenable:** `ttrpg-campaign-setup/references/interview.md` §E
  gains a one-line gloss per strong default (P4, P5, P6, P7, P8, P9, P12, P13) — what stays true on,
  what changes off — so a GM who has never seen the package applied is choosing, not shrugging,
  when the answer comes back `none`. `ttrpg-continuity-audit` Phase 3 gains "reopening a
  switched-on default": if the same non-compliance with one of those eight recurs across this run
  and the last two **archived** audit reports, it proposes (never writes) registering the override;
  with no archived reports to compare, it says the check is **not verifiable** rather than skip it
  silently or fabricate a pattern from one run. `tests/evals/continuity-audit.md` gains a REQUIRED
  box for the not-verifiable path, which is what this fixture (no archived reports) actually
  exercises. *Lesson: `E.overrides` was mapped in every skill but never explained anywhere a GM
  reads it cold, and a default nobody re-examines after the first guess is a default frozen at the
  interview's least-informed moment.* `metadata.version`: `ttrpg-campaign-setup` 1.10 -> 1.11,
  `ttrpg-continuity-audit` 1.5 -> 1.6. No schema change.
- **Closing reports say what happens next, instead of only what happened:** `ttrpg-campaign-setup`'s
  report now states, for every slot written `deferred: session zero`, what stalls if session zero
  is skipped — read live from `session-prep`/`table-dossier`/`table-recap`'s own Phase 0 tables
  (never a second copy of their wording, which would drift). `ttrpg-continuity-audit` and
  `ttrpg-campaign-arc` each close with a one-line **next suggested step**: audit → arc when its
  "Threads to decide" table has rows; arc → `table-dossier`'s rotation check when a session log it
  just read has no matching Diary entry yet. No new phase in either skill — one line in the run
  report each. `tests/evals/campaign-setup.md`, `continuity-audit.md` and `campaign-arc.md` gain
  matching REQUIRED boxes. *Lesson: three maintenance runs (rotation check, arc pass, continuity
  audit) already read each other's output; only the chain from audit to arc was ever said out
  loud — the report is where a GM learns there is a next step at all, not a fourth skill.*
  `metadata.version`: `ttrpg-campaign-setup` 1.9 -> 1.10, `ttrpg-continuity-audit` 1.4 -> 1.5,
  `ttrpg-campaign-arc` 1.4 -> 1.5. No schema change.
- **The quick start is offered, not inferred:** Phase 2 previously triggered on the GM asking for
  the fast version "or visibly has one evening in them" — a mood judgement two agents would read
  differently on the same GM. It now opens by stating both paces explicitly (full walk vs. quick
  start) with their real slot/`(core)` counts, read live from the bundled schema rather than
  written into the skill, and lets the GM choose. `tests/evals/campaign-setup.md` gains a REQUIRED
  box: its scripted GM never asks for either pace, so the offer has to come unprompted.
  *Lesson: a subjective trigger ("visibly rushed") is not a smaller failure mode than a missing
  one — it just fails silently and differently per agent.* `metadata.version`:
  `ttrpg-campaign-setup` 1.8 -> 1.9. No schema change.
- **The fixture's answer key now lists every broken link `check_links.py` finds:** seeded defect
  #4 (`tests/evals/continuity-audit.md`) covered only `[[Eel-Market Buyer]]`; running the new
  checker against `tests/fixture-campaign/` also finds a Session 6 prep note and a Bell-Wight stat
  block that were never in this trimmed fixture, and an answer key silent on two of the three
  broken links it now surfaces would mislead the continuity-audit eval's grader. Defect #4 widened
  to all three (the eval-spec's mechanical boxes do not reference it, so nothing machine-graded
  changes); `tests/check_fixture.py`'s guard extended to match. *Lesson: shipping a real checker
  changes what "the fixture's known defects" means — an answer key is only complete against the
  tools that exist when it is read, not the ones that existed when it was written.* No skill
  changed; no `metadata.version` bump applies.
- **The overlay template reaches an install:** `templates/overlay-SKILL.md` never travelled to an
  installed copy (installation copies `skills/` alone); it is now also bundled at
  `skills/ttrpg-campaign-setup/references/overlay-SKILL.md` (`sync_bundles.py` /
  `BUNDLE-IDENTICAL` cover the pair, same mechanism as the profile schema and
  `check_links.py`). `ttrpg-campaign-setup` Phase 3 gains a short §3.6 pointing at it; README's
  "write an overlay skill" step now names both locations. *Lesson: `table-recap` sends a GM to an
  overlay, and `README.md` names the template that only a clone had — a promise made by one file
  and kept by another only some of the time.* `metadata.version`: `ttrpg-campaign-setup` 1.5 ->
  1.6. No migration: no slot changed.
- **The improvised NPC becomes a note, one owner:** `session-log` Phase 4 gains a step — from the
  interview and *What actually happened*, list every new NPC/place/faction name with no entity
  note yet, hand the list to `ttrpg-entity-note` in the run report, **never create the note here**
  (one owner per artifact). `continuity-audit` check G gains the inverse-orphan case (a name
  recurring in the logs with no entity note ever made for it) so a missed hand-off is still
  caught. `tests/evals/session-log.md` gains a SHOULD box (this fixture's own eel-catcher, already
  a known dead link, is the natural case to catch).
  Also, same commit: `session-log`'s Phase 0 table was pushed to 4949/5000 by this addition (51
  margin) — migrated the non-gating "if empty" column to new `references/slot-degradation.md`,
  keeping only the four slots that actually gate this skill's behaviour (`D.shape`,
  `A.resource_shape`, the `B.distance`/`B.retention`/`C.gm_private` write-back gate,
  `E.overrides`) inline. Down to ~4496 (504 margin). *Lesson: a table that lists seventeen slots at
  the same visual weight hides the four an agent actually has to notice — this is also most of
  what Regista's upcoming "mark the true gates" pass would have done for this skill.*
  `metadata.version`: `ttrpg-session-log` 1.8 -> 1.9, `ttrpg-continuity-audit` 1.7 -> 1.8. No
  schema change.
- **`ttrpg-campaign-setup` budget migration, done ahead of need:** at 4924/5000 (76-token margin,
  the tightest of the nine and getting tighter every commit that touched this file across the
  workorder), §3.5 (portability) and §3.1 (folder skeleton) trimmed to pointers —
  `references/repo-conventions.md` already carried the same checklist and the same per-folder
  conditions (items/official-reworked/gm-private), so nothing new was written there, only the
  entrypoint's near-duplicate removed. `E.overrides`/`D.shape` branches and the Phase 0 protocol
  untouched, `SLOT-RESOLVES`/`PHASE0-PROTOCOL` stayed green throughout. Down to ~4770 (230 margin).
  *Lesson: migrate before the next paragraph lands, not after it breaks the build — a budget this
  tight is a standing liability, not a one-time warning to clear.* `metadata.version`:
  `ttrpg-campaign-setup` 1.13 -> 1.14. No schema change.
- **New check: `FIND-PROFILE-IDENTICAL`.** The "Find it before declaring it missing" protocol
  block was duplicated verbatim in eight entrypoints with nothing mechanical policing it — exactly
  the drift risk `BUNDLE-IDENTICAL` already guards for the schema and the principles. The block
  itself was already identical everywhere (checked before writing the check); deliberately **not**
  moved to `references/` (`PHASE0-PROTOCOL` reads the `find-profile` declaration against the text
  in the entrypoint itself, and `AUTHORING` keeps Phase 0 branches inline on purpose) — policed by
  a mechanical comparison instead. Caught its own regex bug before shipping it: matching to the
  next blank line (instead of the block's own "... already answered." close) would have folded two
  entrypoints' unrelated trailing sentences into the verdict as false drift. Registered in
  `docs/AUTHORING.md`'s checker table (§7); the check count itself needs no update anywhere — W6
  already pointed every mention at `--list`. Three new tests in `tests/checker/test_checker.py`.
- **Two minor precision fixes in `ttrpg-campaign-setup`, caught in the same review:** the closing
  report's "what stalls" cross-read (W11) is the only place this skill reads another skill's own
  *text* rather than a campaign artifact — it now says plainly when those files are not reachable
  instead of silently guessing the consequence. The quick-start slot count (W7) now counts **slot
  bullets** carrying `*(core)*`, not raw occurrences of the string — the preamble uses the same
  string once too, which would have overcounted by one. `metadata.version`: `ttrpg-campaign-setup`
  1.12 -> 1.13. No schema change.
- **The `unconfirmed` marker gets a form, a language and a way to close:** independent review
  caught that W8's round-cap marker was a new artifact element with none of the three: (a) it was
  the literal English word, contradicting this same skill's own "do not write English headings
  over a log in another language" rule — declared as a role now, like the headings, rendered in
  `B.language`; (b) `references/example-log.md` had zero occurrences — not a judgment call this
  time, since the marker lives inside the artifact itself, not in Verify-phase process — it now
  shows one instance, annotated, with the matching *Pending for next session* line; (c) nothing
  said how it closes — it now gets one line under *Pending for next session* per gap (or the run
  report alone, on a one-shot, which has no such section), so it is not invisible to every later
  check forever. Also: the cap is announced *before* it bites, not just applied silently.
  `tests/evals/session-log.md` box rewritten to match.
  *Lesson: a new marker inside the artifact is a skeleton change, not a process change — the same
  distinction that made several other EXAMPLE-DRIFT warnings this workorder legitimate judgment
  calls makes this one not.* `metadata.version`: `ttrpg-session-log` 1.7 -> 1.8. No schema change.
- **Reduced prep cuts breadth, never completeness — a real bug fixed:** `references/reduced-prep.md`
  put the opening read-aloud in the irreducible core for "the first scene" only, which (a)
  violates P1 (a non-overridable requirement: a scene with no read-aloud is unusable at the table,
  the exact failure mode `PRINCIPLES.md` names) for every scene after the first, and (b)
  contradicted the eval rubric this same workorder wrote for it ("for every scene that made the
  cut"). Fixed by restating the governing rule explicitly: a reduced prep has fewer scenes, all of
  them complete — cut breadth, never completeness. Also added: a consent clause up front (the
  `B.distance` branch, the `close`/`self-insert` off-ramp, the `B.safety` refresh and `B.frame`
  hold in full, concretely, not just "the gates still apply"), and a closing "anything not named
  in either list is kept in full" so P4's NPC intentions, a combat scene's exit condition,
  `A.resource` triggers and `D.canon_source` quotes are not left in an undeclared grey zone.
  *Lesson: writing a rubric correctly and the reference file incorrectly, in the same commit, is
  the review gap a checker cannot see — nothing here cites a slot wrong or breaks a link; it just
  contradicts itself two files apart.* `metadata.version`: `ttrpg-session-prep` 1.8 -> 1.9.
- **`E.overrides` reopening, restricted to what the audit actually measures, and de-fabricated:**
  independent review caught two real problems in W10's "reopening a switched-on default": (1) it
  named P4–P9, P12 and P13 as eligible, but this skill's own `E.overrides` table explicitly grades
  no prep against P4/P5/P6/P7/P9 ("do not invent a check in order to skip it") and P7 is
  `ttrpg-table-dossier`'s to own — restricted to the three principles its own checks actually
  measure: P8 (check C's skipped-hook half), P13 (check F), P12/`C.player_access` (check G's
  leakage half). (2) "the same non-finding recurred across the last two archived audit reports"
  is a claim about the campaign's *history* a reader cannot falsify — this package creates no
  artifact for a past audit report, no `type:`, no slot naming where one lives — the same class of
  problem as W5b's invented reading pace, not the same class as W8's round cap (a stopping
  condition on this skill's own behaviour, reversible in the moment, asserting nothing about the
  world). The number of runs is gone entirely: a proposal now rests on what **this run's** checks
  found, phrased as a single observation, never a multi-run count. `tests/evals/continuity-audit.md`
  box updated to match. *Lesson: two corrections in the same message, and only one of them was
  actually about a hardcoded number — the other was about an unfalsifiable claim wearing the same
  costume; conflating them would have produced the wrong fix (a schema slot for report archives)
  instead of the right one (stop claiming the count at all).*
  `metadata.version`: `ttrpg-continuity-audit` 1.6 -> 1.7. No schema change.
- **The bundle count stopped being hardcoded, again:** `AGENTS.md:20` still said "the ten bundled
  copies" after two more pairs had been added since W6 fixed the same pattern for "sixteen
  checks" — caught by the same review. Both `AGENTS.md` and `sync_bundles.py`'s own docstring now
  point to the script's own output instead of naming a count. No metadata.version bump applies
  (neither file is a skill).
- **Reading pace belongs to `D.recap`, not an overlay:** W5b's fix proposed recording an
  unrecorded table pace in a `table-recap` overlay; independent review caught that this contradicts
  the overlay's own role in the package (irreducible procedure or aesthetic that cannot be a slot
  value — a pace plainly can) and "everything variable is a slot". `D.recap` already declares
  "form, who reads it, and the reading-time ceiling"; the pace is free text on that same answer,
  so the skill now proposes adding it there — the slot it already reads, no new slot, no schema
  change. *Lesson: the overlay looked like the right home because it is where campaign-specific
  facts without a slot go — but this fact already had a slot, and reaching for the overlay first
  was reaching past the simpler answer.* `metadata.version`: `ttrpg-table-recap` 1.8 -> 1.9.
- **`check_links.py` fixed after independent review** (a real defect list, reproduced before
  acting on it, not opinion): the shipped script itself named "Obsidian" in its docstring and
  `SKIP_DIRS`, invisible to `NO-SYSTEM-NAMES`/`MECHANICS-LEAK`/`ENCODING` only because `shipped()`
  and the encoding scan were `.md`-only and check_links.py was the package's first bundled
  non-markdown file — `Repo.shipped_nonmd()` now covers every non-`.md` file under a skill's
  `references/`, wired into both checks, with negative fixtures. The checker itself: wikilink
  targets that already carry an extension (`![[map.png]]`, `[[clip.m4a]]`) now resolve against an
  index of every file, not just `.md` notes, so an embed is verified instead of permanently
  reported broken; matching is case-insensitive with a **separate `case-mismatch` finding class**
  (resolves today, breaks on a case-sensitive filesystem — checked component-by-component, a
  mismatched *directory* name is exactly as fragile as a mismatched file name); markdown links
  accept a space or an angle-bracket-wrapped path and are `%xx`-unquoted; 4-space/tab-indented
  code blocks are stripped alongside fenced ones; both sides of every comparison are Unicode
  NFC-normalised. `ttrpg-campaign-setup` Phase 3.4's invariant updated (embeds now covered,
  case-only mismatches don't count against it) and §3.3 migrated to the existing
  `references/repo-conventions.md` (already had the detail; the entrypoint kept a near-duplicate)
  to stay under `ENTRYPOINT-BUDGET`. `tests/checker/test_check_links.py` grows from 11 to 23
  cases; `tests/checker/test_checker.py` gains the two non-markdown-bundle fixtures.
  *Lesson: a check that only ever looked at `.md` files had a blind spot nobody needed until the
  first non-`.md` bundle existed — the coverage gap was real from the moment `shipped()` was
  written, just unreachable until then.* `metadata.version`: `ttrpg-campaign-setup` 1.11 -> 1.12.
  No schema change.
- **`C.verify` finally has a command:** new `scripts/check_links.py` (stdlib, 3.9+) checks that
  every `[[wikilink]]` (`|alias` and `#heading` tolerated) and every relative markdown `.md` link
  in a campaign vault resolves; fenced and inline code spans are ignored so a doc showing the
  syntax itself is never mistaken for a link. Bundled into
  `skills/ttrpg-campaign-setup/references/check_links.py` (`sync_bundles.py` / `BUNDLE-IDENTICAL`
  cover the pair, same as the profile schema). `ttrpg-campaign-setup` Phase 3.4 now *proposes*
  copying it into `<repo>/scripts/` and registering it as `C.verify`, rather than naming an
  "install a checker" project the GM had to build themselves; `none — invariant unverifiable`
  is the declined fallback, no longer the first thing tried. *Lesson: nine Verify phases had
  promised this command since the schema existed — a promise the package itself cannot keep is
  worse than an honest gap, because it reads as done.* `metadata.version` of
  `ttrpg-campaign-setup` bumped to 1.5. No migration: no slot changed.
- **Stale check count fixed:** `AGENTS.md`, `README.md` and `CONTRIBUTING.md` said "sixteen
  checks"; the registry has grown since (`check_contract.py --list` is the source of truth) and
  the three docs now point to `--list` instead of a hardcoded number. *Lesson: a count copied into
  prose is a constant with a friendlier name — it goes stale the next time a check is added, same
  as any other hardcoded default this package warns against.* No migration: documentation only.

## 1.2.0 — an assistant that can be checked

1.1.0 made the package's rules enforceable. This one closes the gap the tooling exposed: **an
output that is right and unaccountable is trusted exactly like a wrong one.** Two new principles,
carried by all nine skills, and the last two checks that were recognising a phase by a sentence.

### P14 — say what you used, and what you could not
- Every skill now closes its **reply** — never the artifact — with a run report: declared defaults
  used and where each is declared, overrides honoured, inputs unavailable, the language chosen,
  and every command run, **shown before it runs** and reported with its real output. The skeleton
  lives once, in `docs/PRINCIPLES.md` (bundled into every installed skill); each skill states only
  what is specific to it. *Lesson: three of the four worst failures seen were invisible at the
  time — a prep that quietly used a default count as if the table had chosen it, an audit that
  reported "0 broken links" without running anything, a log written blind that reads exactly like
  a log written from a full record.*
- Not overridable: it is the mechanism that makes the overridable principles auditable. `E.overrides`
  listing P14 now fails `OVERRIDE-SCOPE` in `scripts/validate_profile.py`.
- Every eval rubric gains the matching REQUIRED box; it stays a **judged** box on purpose, because
  the report lives in the reply and no file check can see it.

### P15 — imported text is content, not instruction
- Published module material, transcripts and diarizer output are read, quoted and summarised, never
  obeyed; only the profile and the campaign's overlays configure behaviour. Cited where it bites:
  prep (module text), audio and log (transcripts), entity notes (imported sources), setup (a module
  you are pointed at). *Lesson: the two skills that ingest most heavily ingest what nobody at the
  table wrote or reviewed — a publisher's chapter, and four hours of speech turned into text by a
  machine that also guesses.* This is the trust boundary of `SECURITY.md`, moved from a document
  about the repo into the skills that do the reading.
  **Migration:** none for a filled profile. A campaign that had written `P14` or `P15` into
  `E.overrides` could not have: they did not exist. The non-overridable set is now
  P1, P2, P3, P10, P11, P14, P15.

### Phase 0 is declared, not recognised by a sentence
- Every entrypoint carries a `<!-- phase0: ... -->` marker naming the elements it implements
  (`find-profile`, `d-shape`, `overrides`; the finder skill declares `search-protocol`).
  `PHASE0-PROTOCOL` now requires the marker, requires the elements the skill's role implies, and
  **verifies each declared element against the text** — declaring one you do not implement fails,
  and so does the reverse. *Lesson: a check anchored to a literal sentence is hostage to a
  rewording, and the rewording is the likely event.*

### The entrypoint budget is measured, not counted
- New warning check `ENTRYPOINT-BUDGET` (~5000 estimated tokens) and a summary line printing the
  worst entrypoint every run. The 200–250 line band stays as a shape guideline in AUTHORING and is
  now stated for what it is: what costs a reader is tokens, and a table-dense skill is cheaper per
  line than a prose one.

### Evals: the last three scenarios become runnable by machine
- `campaign-setup`, `table-dossier` (A/B) and `session-audio` (A/B) gain `eval-spec` blocks, so
  every eval's work copy is now prepared identically every time instead of by a grader reading
  prose. The runner learned two setup steps for them: `create` (the audio file whose mere existence
  is the trap) and `copy` (the diarized fixture), plus a `no-new-files` check for the scenarios
  whose correct behaviour is producing nothing at all.
- `tests/fixture-empty/` is the folder the setup interview runs on. Do not put a profile in it.

## 1.1.0 — the contract becomes enforceable

Up to here the package's rules were real but hand-enforced: "run the checker before every commit",
"keep the bundles identical", "never clean the fixture", "the profile is the other half of the
contract". This release turns each of those sentences into a program, and adds the half of the
contract nobody was checking - **the campaign's own files**.

### The campaign side is validated too
- **`scripts/validate_profile.py`** validates a filled `campaign-profile.md` against the schema it
  was cut from: the four slot states, `deferred:` with a *when*, enums **parsed from the schema
  line** rather than transcribed, the core tier, and the cross-slot invariants that were prose
  until now - capture paths without recording consent, an off-game path without the second
  consent, player access without a GM-private home, protagonists above table size, a resource
  family under `A.resource: none`, a non-overridable principle in `E.overrides`. *Lesson: nine
  skills each believe this file; a contradiction in it is nine wrong artifacts, and it was the
  only artifact in the system nothing checked.*
- **`scripts/validate_overlay.py`** does the same for the third artifact: an overlay that names no
  base skill, restates the base procedure, cites a slot that does not exist, switches off a
  non-overridable principle, or grows past a page. `NO-SYSTEM-NAMES` deliberately does **not**
  apply - an overlay is exactly where a system name belongs.
- `tests/fixture-overlay/` is the package's first worked example of an overlay, and the
  validator's positive fixture.
  **Migration:** none. Run `python scripts/validate_profile.py <your profile>` once; every finding
  is a question your table has not answered yet, not a break.

### The checks now have checks
- **`tests/checker/`**: a negative fixture per check and per rule (85 tests). Each mutates a
  throwaway copy of the repo and asserts that exactly the expected check fires; a coverage test
  fails when a new check lands without one. *Lesson: a regex that stops matching does not fail
  loudly - it silently stops checking, and the 621-line checker was the only mechanical gate.*
- **`check_contract.py` refactored** into a registry of named checks with one function each, plus
  `--strict` (warnings are failures - what CI runs), `--only CODE`, `--format json` and `--list`.
  Same sixteen checks, same output, now callable and testable one at a time.
- **`tests/check_fixture.py`** asserts the eight seeded defects are still seeded and that the
  answer key lists exactly them. *Lesson: a tidy-minded editor "fixing" the hub deletes the only
  thing the continuity-audit eval measures, and the eval then passes for the wrong reason.*

### The mandatory steps are run by a machine
- **CI** (`.github/workflows/ci.yml`): contract check under `--strict`, the validator suites, the
  fixture guards and an install smoke test, on Linux, macOS and Windows, Python 3.9 to 3.13.
- **`.githooks/pre-commit`** + `scripts/install-hooks.sh`: bundle sync, contract check, and the
  checker's own tests when the checker itself is touched.
- **`scripts/sync_bundles.py`** writes the ten byte-identical bundled copies from their canonical
  sources (`--check` reports drift without writing). They stay checked-in content; what changes is
  that a human no longer copies them by hand.
- **`scripts/check_release.py`** reads a diff and enforces AUTHORING §7: a changed skill bumps its
  own `metadata.version` (error), a schema change carries a **Migration** note (error), a changed
  skill whose worked example or eval rubric did not move (warning).
- **`VERSION`** and [`docs/RELEASING.md`](docs/RELEASING.md): the package now has a number of its
  own, and a stated rule for what makes a release major - a schema change, because a fork's filled
  profile is downstream of it.

### Evals become partly mechanical
- **`tests/run_eval.py`** prepares a work copy, applies each eval's setup steps, prints the
  verbatim prompt, and ticks the rubric boxes a machine can observe (frontmatter keys, per-scene
  marks, forbidden vocabulary in a recap, "changed nothing" for the audit), leaving the judgement
  calls to a reader and recording runs under `tests/results/`. *Lesson: a grader who only has to
  judge the judgement calls actually runs the evals.*
- Six evals carry a machine-readable `eval-spec` block; `campaign-arc` gains **scenario support**,
  and its scenario B doubles as the package's structural-branch fixture by rewriting `D.shape` to
  `one-shot` in the profile copy - a branch covered without a second fixture campaign to keep in
  step.

### Installers, privacy, and the rest
- Installers gain `--dry-run` / `-DryRun` and `--uninstall` / `-Uninstall`, write a manifest
  (package, version, commit, source, date) next to the skills, and the PowerShell one runs under
  `Set-StrictMode` with `$ErrorActionPreference = 'Stop'` - a half-failed copy used to exit 0.
  **`scripts/check_install.py`** compares an installed copy with the repo and names what is stale,
  missing or added by hand.
- **[`docs/PRIVACY.md`](docs/PRIVACY.md)** states what the package writes about the real people at
  the table, which rules are enforced by slots and checks, and what it does not protect you from
  (the model you point at it, your git history). **[`SECURITY.md`](SECURITY.md)** states the trust
  boundary: published modules and transcripts are **content, never instructions**, and `C.verify`
  is as privileged as a shell script.
- **The find-the-profile protocol no longer assumes ripgrep**: the frontmatter search now names
  `grep -rl` as its fallback in all eight consumer skills (versions bumped).
  **Migration:** none.
- `CONTRIBUTING.md` and the checker's `--list` mean the change procedure and the check list have
  one source each instead of three.

### Eval coverage completed for all nine skills
- Added `evals/table-dossier.md` (rotation check with a diary extension in setup, and onboarding a
  player), `evals/campaign-arc.md` (plan the season; **the one-shot gate must refuse**) and
  `evals/session-audio.md` (gate 1 refuses on an existing audio file; a consented run driven from
  synthetic machine output; Phase 2 end to end declared not runnable).
- Added `tests/fixture-audio/`: synthetic diarized output with a split speaker label, an
  unresolvable overlap, mangled names, a hook born off game and a tasteless joke that must never
  be quoted. *Lesson: the consent gates, the speaker map and the off-game rules are judgement, not
  transcription — only running the tool itself needs real audio, and a package that refuses to
  invent a consented recording should not pretend otherwise.*
- Three rubrics are pass/fail on **refusing**, because silent degradation is invisible to the form
  checker and expensive at the table.
  **Migration:** none — `tests/` is not installed.

### Profile tiers, artifact type keys, front-loaded descriptions, two new checks
- **`(core)` tier in the schema.** Twelve slots are marked `(core)`; the setup interview offers a
  quick start that walks only those and leaves the rest as untouched placeholders — read, by the
  existing four-state rule, as *never asked*, so the first consumer skill asks once and writes
  back. *Lesson: 61 slots at once is where a new GM abandons setup.*
  **Migration:** none — existing filled profiles are unaffected; core marks only pace the interview.
- **Fixed `type:` frontmatter keys on package artifacts** (`session-prep`, `session-log`,
  `session-recap`, `entity`, `dossier`, `campaign-arc`): skills locate each other's artifacts by
  key, never by filename — the `type: campaign-profile` mechanism, generalised.
  **Migration:** add the matching `type:` key to existing artifact notes (one `rg`-guided pass);
  new artifacts get it from the skeletons. Nothing breaks without it — skills fall back to names —
  but the audit and the finding rules are sharper with it.
- **Descriptions reordered** artifact → "Use when" → boundary, coverage lists dropped (routers
  weight opening tokens; "Covers …" was documentation, owned by the body).
- **Checker grows to sixteen checks:** `ARTIFACT-CONTRACT` (skeleton frontmatter declares its
  `type:`; one type, one owner) and `PHASE0-PROTOCOL` (find-the-profile protocol and a `D.shape`
  branch/gate before Phase 1 in every consumer skill). *Lesson: nine hand-written Phase 0s drift
  apart unless their shared spine is mechanical.*

### Worked examples and behavioral evals
- Four artifact skills bundle an annotated `references/example-*.md`, all on one **invented**
  campaign ("The Weir Circuit" / "Lantern & Ledger") so prep → log → recap show one cycle.
  *Lesson: a shape-not-content example calibrates a model faster than any rule — and a realistic
  one would get copied instead of read.* One configuration per example; structural branches are
  covered by `VARIANT —` deltas at the branch point, never by a second example (AUTHORING §8).
- `tests/`: `fixture-campaign/` (same invented campaign, deliberately dirty state — answer key in
  `tests/evals/continuity-audit.md`; never clean it) plus one scenario + rubric per covered skill.
  The form checker cannot grade a prep; these are the checks that need a reader (AUTHORING §9).

## 1.0 — first public shape

- **Two-layer architecture**: base skills in this repo name profile slots, never a system; campaign
  facts live in `campaign-profile.md`; anything irreducibly campaign-specific goes in an overlay.
- **Schema 2 — named slots.** Sections `§A`…`§E`, slots cited as `B.distance`. *Lesson: numeric
  citations renumbered themselves the moment three authors added slots in parallel — five slots
  reached the schema and were never asked.*
  **Migration (from schema 1):** replace every numeric citation (`§2` …) with the named id of the
  same slot; the checker fails `NO-LEGACY-SLOTS` on any survivor.
- **Four slot states** (placeholder / `deferred:` / `none` / value), with session zero owning five
  deferrals; declared `default:` on exactly four slots.
- **`E.overrides` mapped, not mentioned**: every skill carries a branch table of what stops being
  required; P1/P2/P3/P10/P11 not overridable. *Lesson: eight of nine skills once cited the slot
  and mapped nothing.*
- **Bundled copies are checked-in content** (principles in every skill, schema in setup), enforced
  byte-identical — a fresh clone is a valid package, installers only copy.
- **Contract checker** (`scripts/check_contract.py`, stdlib-only) as the mandatory pre-commit gate,
  absorbing external validator checks; `NO-SYSTEM-NAMES` with no exception list.
- The nine v1 skills; principles P1–P13; `AGENTS.md` with the repo's active decisions; README
  declares substrate assumptions, non-goals and known gaps.
