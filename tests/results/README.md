# Recorded eval runs

`tests/run_eval.py --record` writes one JSON file per graded run:
`<date>-<eval>-<model>.json`, holding which mechanical boxes passed, which files the agent
changed, and which artifact it produced.

Why keep them in the repo: "run the evals before trusting a new model with your campaign" only
means something if last time's result is still readable. A run recorded here answers *which model,
which day, which boxes* — a memory of "it seemed fine" answers nothing.

What they are **not**: a pass/fail verdict on the skill. The JSON's own field names say so:
`mechanical_passed` is exactly what it claims, the half a machine can tick, and `judged` starts
`null` until a human fills it in (a pointer to where the verdict lives, e.g. this same commit's
message or a companion file — never a bare boolean standing in for a reading nobody did). The
rubric in `tests/evals/` still needs a reader, and a run with every mechanical box green can still
be a bad prep. Note the human verdict in the commit message that adds the file, or in a companion
file it points at — but `judged` must stop being `null` before the record is treated as finished.

These files are cheap and disposable — delete them freely when they stop being informative, but do
not edit one to make it look better. A record you have edited is not a record.
