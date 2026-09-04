# Changelog

This package is **meant to be forked**: your campaign clones it, fills a profile, maybe adds an
overlay. This file is how a fork learns what moved upstream — each entry names what changed,
**why** (the lesson), and what a fork or an existing campaign must do about it, if anything.
Skill versions live in each skill's `metadata.version`; entries here are grouped by change, newest
first. A schema change always carries a **Migration** note.

## Unreleased

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
