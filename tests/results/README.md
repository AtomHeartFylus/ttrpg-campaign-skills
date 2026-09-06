# Recorded eval runs

`tests/run_eval.py --record` writes one JSON file per graded run:
`<date>-<eval>-<model>.json`, holding which mechanical boxes passed, which files the agent
changed or deleted, and which artifact it produced. `work` is **not** the absolute Temp-directory
path the run actually happened in (that path is useless once Temp is cleaned up, and on some OSes
embeds a real username) - it is the work directory's own basename, already namespaced by the eval
name and a random suffix.

When there is anything to show, `--record` also writes a `<date>-<eval>-<model>-files/` folder
beside the JSON, holding the actual CONTENT of every changed/artifact file at grading time (text
saved as text; anything that fails UTF-8 decoding is saved as raw bytes with a `.bin` suffix). A
deleted pristine file has no content to save and is listed in the JSON's `deleted` array (and in
`content` with `"status": "deleted", "saved_as": null`) instead. This is what keeps a record
**judgeable** after the Temp work directory is gone: without it, `changed`/`artifacts` are just
filenames a reader has to take on faith once nothing on disk backs them anymore.

**Chat-only evals are a separate case.** When the correct behaviour is to write no file to the work
copy, `changed` is correctly empty and the sidecar has nothing to preserve. The human runner must
save the verbatim reply beside the JSON as `<date>-<eval>-<model>-reply.md`, with frontmatter naming
`eval`, `model` and `when`, and must say in the JSON or companion verdict that the reply is the
artifact being judged. Never create a file inside the work copy merely to give the harness
something to snapshot: that would invalidate the no-write behaviour under test.

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
not edit one to make it look better. A record you have edited is not a record. The one exception is
an explicit **privacy/retention migration** of legacy metadata: replacing an absolute local `work`
path with its basename and attaching content sidecars is allowed when the mechanical results,
artifacts, verdict pointer and model/date are preserved byte-for-byte in meaning. It is a metadata
migration, not a regrade; record that fact in the change note and never rewrite the artifact content
or a human verdict to improve the result.
