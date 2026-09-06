# Releasing

The package is meant to be forked and installed on several machines, so a version here is not
decoration: it is how a fork knows whether its profile still fits, and how a second machine knows
whether its installed copy is current.

## Two version numbers, on purpose

- **`VERSION`** — the package. One number for the whole bundle, tagged in git as `v<version>`.
- **`metadata.version` in each `SKILL.md`** — that skill. Bumped whenever the skill changes
  (AUTHORING §7 step 4), so an installed folder can be compared against the repo without git.

`scripts/check_release.py` fails a diff that changes a skill without bumping its own version, and
`scripts/check_install.py` compares an installed copy against this repo file by file.

## What each part of the package version means

| Change | Bump |
|---|---|
| a schema change (a slot added, renamed, retyped, or its meaning altered) | **major** |
| a check that fails a repo that used to pass; a removed or renamed skill | **major** |
| a new skill, a new check, a behavioural change inside a skill, a new script | **minor** |
| wording, examples, docs, tests, a fixed false positive | **patch** |

A schema change is major because a fork's filled `campaign-profile.md` is downstream of it: the
fork has to migrate, and **every schema change carries a `Migration:` note in `CHANGELOG.md`**
(enforced by `SCHEMA-MIGRATION`).

**Editing `templates/campaign-profile.md` is not by itself a schema change.** `SCHEMA-MIGRATION`
fires on the *file*, and a check that fires is easy to mistake for a verdict on the number. The
question that decides the bump is the one the table above asks: **does a profile that was valid
before this commit stop being valid after it?** If no slot was added, renamed or retyped and no
validator behaviour changed — stating in the schema a rule that was already enforced, for instance
— nothing downstream breaks, and that is a minor or a patch with a `Migration:` note attached. The
note is about what a reader must *do*, not about how big the number is: a minor may carry one.

## Cutting a release

1. `python scripts/check_contract.py --strict` — clean, warnings included.
2. `python -m unittest discover -s tests/checker` — the validators' own fixtures.
3. `python tests/check_fixture.py` — the seeded defects are still seeded.
4. `python tests/smoke_install.py` (and `--installer ps1` on Windows) — an install is what a user
   receives.
5. Re-run the evals whose skills changed behaviourally (`python tests/run_eval.py --list`), and
   record the result under `tests/results/`.
6. Move the `## Unreleased` section of `CHANGELOG.md` under a `## <version> — <date>` heading,
   keeping every entry's **lesson** and any **Migration** note.
7. Write the new number into `VERSION`, commit, then `git tag -a v<version> -m "<version>"`.
8. Re-run the installer on every machine that carries a copy (`./install.sh ~/.agents/skills`),
   or `python scripts/check_install.py <target>` to see which machine is stale.

## What is *not* released

`docs/`, `templates/`, `tests/` and `scripts/` never travel into an install — the installer copies
`skills/` alone. That is why every skill folder carries its own `references/PRINCIPLES.md` and why
`ttrpg-campaign-setup` carries the schema: a released skill has to stand up alone in a folder,
with no repo around it.
