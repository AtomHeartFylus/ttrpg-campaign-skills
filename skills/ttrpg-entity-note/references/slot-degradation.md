# Slot degradation — entity-note

Non-gating Phase 0 slots: what the skill does when each is empty or deferred.
Gate slots (`B.distance`, `B.frame`, `D.shape`, `C.root` / `C.granularity` / `C.naming` /
`C.links` / `C.frontmatter` / `C.verify`) live in the SKILL.md Phase 0 table and block or
redirect execution. Everything below is graceful degradation — the skill continues, with
reduced scope.

| Slot | Used for | If empty |
|---|---|---|
| `B.hooks_staging`, `B.safety` | parallels vs literal appearances; the tools to refresh before a nerve-touching entity reaches the table | stage as parallels; ask once before building one |
| `A.ruleset` | whether this entity needs a stat/mechanics note, and in what form | write fiction only; note that mechanics are undefined |
| `D.tone` | the register of the description and the question the entity must pose | ask once, then proceed |
| `D.canon_source` | entities the canon already fixes: place them where the source places them | treat every entity as original |
| `D.guide` | whether this entity touches the guide's arc (a line for the guide to have about it) | drop that line |
| `D.backbone`, `D.official_material`, `D.deviation_policy` | published material → attribution link + record the deviation | treat as homebrew |
| `B.language` | the language the note is written in | write in the language of the notes around it, say which you chose, and offer to record it |
| `C.player_access`, `C.gm_private` | what players may read; where GM-only material lives | keep every secret in a clearly GM-only section |
| `E.deliverable`, `E.never_without_asking`, `E.retroactivity`, `E.overrides` | deliverable; renaming rules; retroactivity; which strong defaults this table switched off — see the branch in SKILL.md | save in the repo; never rename an existing note; all defaults in force |
