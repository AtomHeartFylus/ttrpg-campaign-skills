# Slot degradation — session-prep

Non-gating Phase 0 slots: what the skill does when each is empty or deferred.
Gate slots (`D.shape`, `B.distance`, `B.safety`, `B.size` / `B.protagonists`) live in the
SKILL.md Phase 0 table and block or redirect execution. Everything below is graceful
degradation — the skill continues, with reduced scope.

| Slot | Used for | If empty |
|---|---|---|
| `A.ruleset`, `A.adjudicated`, `A.houserules` | which mechanics to inline in a scene | inline nothing mechanical; keep scenes fiction-first |
| `A.fiction` | what this table **never rolls for** — those beats are staged as pure fiction, with no check and no difficulty value in the scene | mechanise nothing you were not asked to; when in doubt, leave the beat to the fiction |
| `A.resource` (+ `A.resource_loss` / `A.resource_gain`, `A.resource_scale`) | the spend/regain triggers section, and the units a cost is written in | drop that section entirely — do not invent a resource |
| `D.tone` | register of read-aloud text; the recurring thematic pressure | ask once, then proceed |
| `D.canon_source` | quote blocks and their delivery mode | no quote blocks |
| `D.guide` | the one prepared beat per session | no beat section |
| `D.backbone`, `D.official_material` | which official module/chapter this session leans on | treat as fully homebrew |
| `B.length` | content margin (P8) | prep the main path only, no optional scenes |
| `B.absence` | the in-fiction convention for absent players | ask once, then record it in the profile |
| `B.frame` | the cultural frame any real, public or historical figure must sit inside — it applies to a figure **staged directly here**, not only to one with a note | cast no real or public figure; ask once. `ttrpg-entity-note` owns the rule, this skill obeys it |
| `C.root`, `C.links`, `C.frontmatter`, `C.verify` | where the note goes, link syntax, frontmatter, verification command | write the file where told, skip link verification |
| `C.blocks` | how this vault writes the callouts and checkboxes the skeleton shows | keep the roles, render them as plain headings and blockquotes |
| `C.inline_exception` | which material may be inlined here beyond the P1 default | apply the P1 default: inline everything but stat blocks |
