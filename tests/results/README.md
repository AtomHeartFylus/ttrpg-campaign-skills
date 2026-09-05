# Recorded eval runs

`tests/run_eval.py --record` writes one JSON file per graded run:
`<date>-<eval>-<model>.json`, holding which mechanical boxes passed, which files the agent
changed, and which artifact it produced.

Why keep them in the repo: "run the evals before trusting a new model with your campaign" only
means something if last time's result is still readable. A run recorded here answers *which model,
which day, which boxes* — a memory of "it seemed fine" answers nothing.

What they are **not**: a pass/fail verdict on the skill. The mechanical boxes are the half a
machine can tick; the rubric in `tests/evals/` still needs a reader, and a run with every
mechanical box green can still be a bad prep. Note the human verdict in the commit message that
adds the file.

These files are cheap and disposable — delete them freely when they stop being informative, but do
not edit one to make it look better. A record you have edited is not a record.
