<!-- The change procedure is docs/AUTHORING.md §7; the decisions already taken are AGENTS.md. -->

## What changes, and the lesson behind it

<!-- One paragraph. If this came from something that broke at a table, say what broke: that
     sentence is what makes the rule stick, and it belongs in the CHANGELOG entry too. -->

## Checklist

- [ ] `python scripts/check_contract.py --strict` exits 0 (no check was weakened to get there)
- [ ] `python -m unittest discover -s tests/checker` passes; a **new check has a new negative fixture**
- [ ] `python tests/check_fixture.py` passes (the seeded defects are still seeded)
- [ ] No base skill names a game system, setting, mechanic or character (agnosticism self-test, AUTHORING §1)
- [ ] Touched skills bumped `metadata.version`; CHANGELOG entry added for anything a fork would notice
- [ ] Schema change? `sync_bundles.py` run, a **Migration** note written, some skill actually reads the new slot
- [ ] Behavioural change? the skill's eval was re-run or its rubric updated in this commit
- [ ] Skeleton or required element changed? `references/example-*.md` updated in this commit

## Scope

- [ ] This is not one of the deliberate non-goals (encounter balancing, rules lookup, character
      sheets, VTT integration) — see README
