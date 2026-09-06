# Slot degradation — continuity-audit

Non-gating Phase 0 slots: what the skill does when each is empty or deferred.
Gate slots (`D.shape`, `B.cadence`, `B.retention`, `C.verify`) live in the SKILL.md Phase 0
table and block or redirect execution. Everything below is graceful degradation — the skill
continues, with reduced scope.

| Slot | Used for | If empty |
|---|---|---|
| `E.audit_cadence` | **how often this audit runs** — the only slot that answers it. Not the spotlight rotation check, which follows `B.protagonists` | use the **`default:` the slot itself declares**, **say in the report you used it**, and offer to record the table's real cadence |
| `A.resource` | which values are tracked and therefore duplicable | skip the resource checks |
| `D.backbone`, `D.deviation_policy` | the deviation ledger prep must stay consistent with | skip the deviation-drift check — a fully homebrew campaign has no ledger and its absence is not a finding |
| `B.absence` | absent-player rule → expected state divergence, not a bug | flag attendance divergences as questions, not findings |
| `C.player_access`, `C.gm_private` | what players may read, and where GM-only material must live | assume no note is player-readable |
| `C.state_locations`, `C.hub`, `C.root`, `C.naming`, `C.links`, `C.arc_note`, `C.thread_ledger` | single-source-of-truth locations, folder map, naming, link syntax, where the ledgers live | audit only what the user names; report the rest as unverifiable |
| `E.retroactivity` | **whether past material may be corrected, and where corrections are recorded** | assume retroactivity is **not** granted; propose only the typo class |
| `E.review`, `E.never_without_asking` | review bluntness, and what may not be touched without asking | be plain; propose, never apply |
