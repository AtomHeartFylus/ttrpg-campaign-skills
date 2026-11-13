# Scene-local visuals: brief-only pilot

Three fresh executions used `openai-codex/gpt-6.1-terra`, the packaged skill entrypoints and
fresh copies of the invented campaign fixture. Workers received the scenarios' verbatim prompts,
not their rubrics. No network, generation or playback tools were available.

| Scenario | Observed output | Mechanical result | Record |
|---|---|---|---|
| session-visuals A | Four compact, scene-local briefs; renamed profile found; only existing prep changed | 3/3 | `20261113-094526-session-visuals-A-openai-codex-gpt-6.1-terra.json` |
| session-visuals F | Four briefs for one session; profile unchanged; only existing prep changed | 3/3 | `20261113-094527-session-visuals-F-openai-codex-gpt-6.1-terra.json` |
| session-prep C | One new Session 8 prep with two local visual briefs, not a separate script | 2/2 | `20261113-094527-session-prep-C-openai-codex-gpt-6.1-terra.json` |

Each record includes paths to the original saved artifact content. Its `judged: null` remains
unchanged: mechanical success is not a complete rubric pass. The reader can inspect both the
briefs and the untouched surrounding material rather than infer quality from a grader vote.

## Checks and inspection

All three invocations of `python tests/run_eval.py --grade ... --record` exited 0. The scenario
keys were explicitly A and F for session-visuals, and C for session-prep. The inspected blocks
place show/change/stop conditions, brief-only status and blank fallback at scene points of use.
No asset, inspection, rights clearance or playback success is asserted. The new prep retains its
read-aloud and mechanics and reports the stale hub rather than silently using it.

The two enriched Session 7 preps were also compared with the pristine fixture using byte-line
`difflib.SequenceMatcher(..., autojunk=False)`. Every non-equal opcode was an insertion: four
regions in A, four in F. Original byte-lines were retained in order. The mechanical grader
separately checked that other files were untouched and no files were created or deleted.
This preservation result applies to these outputs, not to arbitrary future runs.

The authoring agnosticism self-test considered a modern investigative one-shot and diceless
political intrigue. The base procedure delegates setting, tone and conventions to the profile;
the invented example does not impose a setting or rules family on either case. This is an
instruction review, not evidence of behavior in those campaigns.

## Limits

This is a small functional pilot, not a matched baseline comparison, proof of improvement or
validation across models, tables and hosts. Full P14 command accounting and every subjective
rubric box have not been independently certified. Control scenarios B–E were not freshly
executed for this publication snapshot. The optional shared-metadata branch was not exercised;
these outputs use concise local notes. Actual media production/acquisition, rights clearance,
asset inspection, playback on a projector/display and a live session remain untested.
