# Contributing

The rules for *writing* a skill are in [`docs/AUTHORING.md`](docs/AUTHORING.md); the decisions
already taken are in [`AGENTS.md`](AGENTS.md). Read those before proposing a change to a skill —
most review comments here are a line from one of them.

This file is the shorter question: how a change gets in.

## Set up in one minute

```sh
git clone <this repo> && cd ttrpg-campaign-skills
sh scripts/install-hooks.sh        # pre-commit: bundle sync + contract check
python scripts/check_contract.py   # must exit 0; no dependencies to install
```

Everything is **stdlib Python 3.9+ and nothing else**, on purpose: validating a clone must never
require a tool installed somewhere else on the machine.

## The gate

| Command | What it proves |
|---|---|
| `python scripts/check_contract.py --strict` | the package is well-formed (16 checks) |
| `python -m unittest discover -s tests/checker` | each check and rule still fires on its own negative fixture |
| `python scripts/validate_profile.py tests/fixture-campaign/campaign-profile.md` | the example campaign satisfies the schema it demonstrates |
| `python scripts/validate_overlay.py tests/fixture-overlay --strict` | the example overlay satisfies the overlay rules |
| `python tests/check_fixture.py` | the deliberately seeded defects are still seeded |
| `python tests/smoke_install.py` | what a user receives is what the README promises |
| `python tests/run_eval.py --grade <eval> --work <dir>` | the skill still *behaves*, for the boxes a machine can tick |

CI runs all of them on Linux, macOS and Windows. **Never weaken a check to get green:** a check
that fires is either a real defect or a missing declaration in the schema.

## What a good change looks like

- **One lesson, one home.** A general rule goes to `docs/PRINCIPLES.md` and is cited by tag; it is
  never restated inside a skill.
- **Nothing campaign-specific in a base skill.** No system, setting, mechanic or character name.
  Everything variable is a slot in `templates/campaign-profile.md`; everything irreducible is an
  overlay in your own campaign repo.
- **Every slot has a reader.** Adding a slot without a skill that branches on it fails `DEAD-SLOT`,
  and rightly: it is a question asked for nobody.
- **A behavioural change carries its eval.** A new phase, required element or branch re-runs that
  skill's eval or updates its rubric in the same commit; a wording fix needs the checker alone.
- **A skeleton change carries its example.** `references/example-*.md` is updated with the skill it
  demonstrates — a stale example outteaches the rules it contradicts.
- **Version and changelog.** Bump `metadata.version` in the skill you touched; add a CHANGELOG
  entry with its **lesson** for anything a fork would notice; a schema change always carries a
  **Migration** note. `scripts/check_release.py` checks this over the diff.

## What will be declined

The package is an extraction from real play, not a wish list. Encounter balancing, rules lookup,
character sheets and VTT integration are **deliberate non-goals** — they are where system
agnosticism genuinely breaks. The known gaps (item/economy ledger, scheduling, player-facing
handouts, endgame and archival) are waiting for a second campaign to earn them, not for a
plausible design.

If your table needs something specific, the answer is usually a profile slot or an overlay in your
own repo — and if an overlay grows past a page, that *is* a good issue: the base skill is missing
a slot.

## Reporting something sensitive

See [`SECURITY.md`](SECURITY.md). Material about real people at a table is covered by
[`docs/PRIVACY.md`](docs/PRIVACY.md).
