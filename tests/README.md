# Behavioral evals

`scripts/check_contract.py` proves the skills are **well-formed**. Nothing in it proves they
**work**: that a prep comes out scannable, that a log invents no facts, that the audit finds real
drift. That is what this folder is for.

Two pieces:

- **`fixture-campaign/`** — a complete, invented campaign repo ("The Weir Circuit", system
  "Lantern & Ledger": the same fictional campaign the worked examples in `skills/*/references/`
  use). Its state is *deliberately dirty*: the defects are seeded on purpose and listed, as the
  answer key, in `evals/continuity-audit.md`. **Never "fix" the fixture** — a clean fixture tests
  nothing.
- **`fixture-audio/`** — synthetic diarized machine output for one evening of the same campaign,
  so the audio skill's judgement (gates, storage contract, speaker map, off-game curation) is
  testable without a recording. See its own README for what is seeded into it.
- **`fixture-overlay/`** — one invented overlay for the same campaign: the positive fixture of
  `scripts/validate_overlay.py`, and the package's only worked example of an overlay.
- **`evals/`** — one file per skill under test: a scenario (setup + the prompt to give the agent)
  and a pass/fail rubric a human grader ticks. Six of them end with a machine-readable
  `eval-spec` block (setup steps, the artifact's `type:`, and the boxes a machine can tick).
- **`checker/`** — negative fixtures for `check_contract.py`, `validate_profile.py` and
  `validate_overlay.py`: 85 tests, one per check, plus a coverage test that fails when a new check
  lands without one. `python -m unittest discover -s tests/checker`.
- **`check_fixture.py`** — asserts the eight seeded defects are **still seeded** and that the
  answer key lists exactly them. Run it after anything that touches `fixture-campaign/`.
- **`smoke_install.py`** — installs into a throwaway directory and asserts what a user receives:
  nine folders each with its own `references/PRINCIPLES.md`, the schema inside the setup skill,
  no `docs/` or `tests/` travelling, `--dry-run` writing nothing, `--uninstall` removing exactly
  what was installed, and a re-install replacing a folder wholesale.
- **`results/`** — recorded eval runs (`--record`), so "before trusting a new model" produces
  comparable data instead of a memory.

## The runner

```sh
python3 tests/run_eval.py --list                     # evals, scenarios, mechanical coverage
python3 tests/run_eval.py --setup session-prep       # work copy + setup steps + verbatim prompt
# ... run a fresh agent session in the printed work copy ...
python3 tests/run_eval.py --grade session-prep --work <dir> --record --model <what ran>
```

The runner ticks only the boxes that are **observable facts about a file** (a fixed `type:` key,
per-scene spotlight marks, a forbidden word in a recap, "changed nothing" for the audit). Every
other box still needs a reader, and the runner prints how many are waiting. That split is the
whole point: a grader who only judges the judgement calls actually runs the evals.

`--scenario` selects between the scenarios of a multi-scenario eval. `campaign-arc --scenario B`
doubles as the package's **structural-branch fixture**: its setup rewrites `D.shape` to `one-shot`
in the profile copy, so the refusal branch is exercised without a second fixture campaign to keep
in step.

## Protocol

1. **Copy the fixture** to a temp folder — the agent under eval reads *and writes* there, never in
   the repo: `cp -r tests/fixture-campaign /tmp/weir-eval` (or the platform equivalent).
2. **Fresh agent session**, with the skill under test installed and nothing else primed. Do not
   paste the rubric into the session.
3. Perform the eval's **setup steps** (some evals delete a file first), then give its **prompt**
   verbatim, with the copy as working directory.
4. Grade against the rubric. **Pass = every REQUIRED box ticked.** SHOULD boxes measure quality,
   not correctness; note misses, don't fail on them.
5. A failed box is either a skill bug (fix the skill, then re-run) or a rubric bug (fix the
   rubric). Decide which *before* touching either.

## When to run

- After any **behavioural** change to a skill (a phase, a required element, a branch). A pure
  wording fix needs only `check_contract.py`.
- When adopting a **new model/harness** for campaign work: the evals are the cheapest way to learn
  where the new model needs the skill tightened.

## Current coverage

| Eval | Fixture-backed | Notes |
|---|---|---|
| `evals/session-prep.md` | yes | prep Session 8 from the dirty state |
| `evals/session-log.md` | yes | log Session 7 from testimony (setup deletes the shipped log) |
| `evals/table-recap.md` | yes | recap to open Session 8 |
| `evals/entity-note.md` | yes | promote the eel-market buyer |
| `evals/continuity-audit.md` | yes | the answer key of seeded defects lives here |
| `evals/campaign-setup.md` | no (empty dir) | scripted-GM interview |
| `evals/table-dossier.md` | yes | A: rotation check (setup extends the diaries) · B: onboarding a player |
| `evals/campaign-arc.md` | yes | A: plan the season · B: the one-shot gate must refuse |
| `evals/session-audio.md` | yes (+ `fixture-audio/`) | A: gate 1 refuses · B: consented run from machine output · C: declared not runnable |

All nine skills are covered. **The one declared hole** is `ttrpg-session-audio` Phase 2 end to end
— running a real diarizing tool on a real recording — which needs a consented audio sample this
package will not invent; see Scenario C of that eval for how to run it if you have one.

**Scenarios that must refuse.** Three rubrics are pass/fail on their first box because the correct
behaviour is *stopping*: the arc skill on a one-shot, the audio skill without recording consent,
and — partially — the entity skill when the admission test fails. Silent degradation is invisible
to a form checker and expensive at the table, so it gets its own scenarios rather than a footnote.

## Rules for writing an eval

- The scenario must be runnable by someone who has never seen the fixture: setup steps explicit,
  prompt verbatim, no hidden context.
- Rubric boxes are **observable facts about the artifact or the agent's behaviour** ("the global
  callout contains no per-scene value"), never vibes ("the prep feels usable").
- Every REQUIRED box traces to a phase, a required element or a principle of the skill under test
  — cite it in the box.
- The fixture is shared: an eval may add temp files in its *copy*, but a new **seeded defect** in
  `fixture-campaign/` must be added to the answer key in `evals/continuity-audit.md` **and to
  `check_fixture.py`** in the same commit, or the audit eval starts failing for the wrong reason.
- Setup steps that a machine can perform (`delete`, `replace`) belong in the `eval-spec` block as
  well as in the prose, so the work copy is prepared identically every time. Prose alone drifts
  from what the last grader actually did.
- A rubric box goes in the spec when it is a fact about a file, and stays in the rubric when it is
  a judgement. Do not mechanise a judgement into a keyword count: a box that passes on the wrong
  artifact is worse than a box a human forgets.
