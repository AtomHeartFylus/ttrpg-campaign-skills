# Slot degradation — session-audio

Non-gating Phase 0 slots: what the skill does when each is empty or deferred.
Gate slots (`B.consent_recording`, `B.consent_offgame`, `C.capture_paths`, `B.distance`)
live in the SKILL.md Phase 0 table and block or redirect execution. Everything below is
graceful degradation — the skill continues, with reduced scope.

| Slot | Used for | If empty |
|---|---|---|
| `C.player_access`, `C.gm_private` | what players may read of the repo; **where the off-game note is allowed to live** | treat transcripts and the off-game note as GM-only |
| `B.retention` | how long transcripts and off-game entries are kept, and who can trigger a deletion | say plainly that this material is being kept indefinitely, and offer to set the rule — do not quietly assume forever |
| `B.language` | the language the transcription runs in | infer it from the notes around the repo, say which you chose and offer to record it here; ask only when there is nothing to infer from |
| `C.naming`, `C.links`, `C.frontmatter`, `C.verify` | file naming, link syntax, frontmatter, verification command | follow the repo's existing convention; skip link verification |
| `E.never_without_asking`, `E.overrides` | whether external/cloud tools may be used; whether files may be created without asking | ask before uploading anything and before creating folders |
| `D.shape` | one-shot / series / open sandbox — see the branch in SKILL.md | proceed; this skill is the least shape-sensitive in the package |
