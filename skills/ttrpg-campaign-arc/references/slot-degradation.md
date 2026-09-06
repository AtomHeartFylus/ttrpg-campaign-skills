# Slot degradation — campaign-arc

Non-gating Phase 0 slots: what the skill does when each is empty or deferred.
Gate slots (`D.shape`, `D.backbone` / `D.unit` / `D.deviation_policy`, `D.endgame`,
`B.cadence` / `B.horizon`) live in the SKILL.md Phase 0 table and block or redirect execution.
Everything below is graceful degradation — the skill continues, with reduced scope.

| Slot | Used for | If empty |
|---|---|---|
| `A.ruleset` | the advancement checkpoints the backbone must respect, in that system's own measure | plan in fiction only, no progression row |
| `A.resource` | the arc-level curve: where it must be lowest, where it can be regained | drop the curve column entirely |
| `D.tone` | where the register must shift, and which breaks are admitted | ask once; do not invent tone shifts |
| `D.canon_source` | which part of the corpus each chapter leans on | drop the canon column and the deviation ledger |
| `D.guide` | the guide's arc across the campaign and where it resolves | drop that row |
| `B.size`, `B.protagonists` | passed through to `ttrpg-table-dossier`'s rotation check — **not recomputed here** | that skill asks; do not substitute a number |
| `C.arc_note`, `C.thread_ledger`, `C.hub`, `C.links`, `C.verify` | where the arc note and ledger live, link syntax, verification command | ask where the note goes |
| `E.review`, `E.never_without_asking` | how blunt the review is; what may not be changed without asking | propose, do not restructure |
