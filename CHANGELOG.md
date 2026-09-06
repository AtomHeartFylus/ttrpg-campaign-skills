# Changelog

This package is **meant to be forked**: your campaign clones it, fills a profile, maybe adds an
overlay. This file is how a fork learns what moved upstream — each entry names what changed,
**why** (the lesson), and what a fork or an existing campaign must do about it, if anything.
Skill versions live in each skill's `metadata.version`, the package's own number in `VERSION`;
entries here are grouped by change, newest first. A schema change always carries a **Migration**
note. What each part of a version means, and how a release is cut: [`docs/RELEASING.md`](docs/RELEASING.md).

## Unreleased

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
