# Slot degradation, non-gating

Companion to Phase 0 of `SKILL.md`. The slots that actually gate this skill's behaviour — `D.shape`,
`A.resource_shape`, the `B.distance`/`B.retention`/`C.gm_private` write-back gate, `E.overrides` —
keep their full "if empty" consequence in the entrypoint, because they change *what this skill
does*, every run. Everything below only changes *how a value is recorded*, needed once per empty
slot, not every time the skill runs.

| Slot | Used for | If empty |
|---|---|---|
| `A.ruleset` | what "advancement" means here, in the measure that system uses (a step of progression, a milestone, or none at all) | record no advancement, only fiction |
| `A.resource` | whether Exit state carries a resource value at all | drop those rows — do not invent a resource |
| `A.resource_scale`, `A.resource_zero` | the units the Exit-state value is recorded in, and whether anyone crossed the threshold that ends a character — a zero-crossing is never a footnote, it is the headline of the session | record the bare number the GM reports, and ask what it means before writing any consequence |
| `B.language` | **the language the log is written in**, headings included | write in the language of the surrounding notes, say which you chose, and offer to record it |
| `B.absence` | who advances when absent | ask once: *do absent characters advance?*, then write it back |
| `B.size` | how many per-player moments to expect | ask table size |
| `D.guide` | the "was the prepared beat played, and how did it land?" question | drop that question |
| `D.backbone`, `D.official_material` | which official chapter/module the session covered | record the fiction only |
| `D.recap` | whether a recap follows, so the log's link/property points at it | leave the recap link empty |
| `C.root`, `C.naming`, `C.frontmatter`, `C.state_locations`, `C.hub`, `C.links`, `C.verify` | log path and name, frontmatter, dossier property names, state hub, verification command | write where told; skip link verification |
| `C.blocks` | how this vault writes the callouts and checkboxes the skeleton shows | keep the roles, render them as plain headings and blockquotes |
| `C.thread_ledger` | where a thread's status is updated when this session opens or pays one — the only place it lives (P10) | list the threads in *Pending for next session* and say once there is no ledger; do not start a rival list |
| `E.deliverable`, `E.retroactivity` | saved note vs. draft; whether past logs may be corrected | save the note, correct nothing retroactively |
