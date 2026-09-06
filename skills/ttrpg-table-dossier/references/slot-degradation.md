# Slot degradation — table-dossier

Non-gating Phase 0 slots: what the skill does when each is empty or deferred.
Gate slots (`B.distance`, `B.size` / `B.protagonists`, `B.safety`, `D.shape`) live in the
SKILL.md Phase 0 table and block or redirect execution. Everything below is graceful
degradation — the skill continues, with reduced scope.

| Slot | Used for | If empty |
|---|---|---|
| `A.ruleset`, `A.resource`, `A.resource_shape`, `A.resource_asymmetry` | which character-side values are properties — **`A.resource_shape` decides whether the resource is per-player at all** | track only what the GM names; no resource property |
| `D.tone` | the tone contract and the hard lines / lines & veils to agree on | make it the first session-zero item, then write the answer back |
| `B.cadence`, `B.absence` | the budget window; the absent-player convention and whether absentees advance | decide both here and write them back |
| `B.hooks_count`, `B.hooks_staging` | how many nerves per player, and how they are staged | use the `default:` the slot itself declares (2–3), say you did, and offer to record the real number; staging defaults to parallels |
| `D.identity` | the rule for what a recap calls this protagonist — this note is where the **per-character** value lives, for `ttrpg-table-recap` to read | leave the field out; the recap asks once and writes the answer back here |
| `B.retention` | how long playstyle notes and harvested hooks about a real person are kept, and who can have an entry removed | say plainly that these notes are kept indefinitely, and offer to set the rule — under `B.distance` = `self-insert` / `close`, ask before writing rather than after |
| `C.player_access`, `C.gm_private`, `C.root`, `C.frontmatter`, `C.links`, `C.verify` | where playstyle notes and hook records may live; dossier folder, properties, link syntax, verification | assume players read nothing and keep playstyle GM-side; run `ttrpg-campaign-setup` — do not invent a layout |
| `C.blocks` | how this vault writes the callouts the skeleton shows | keep the roles, render them as plain headings and blockquotes |
| `E.review`, `E.never_without_asking` | bluntness; what not to do without asking | write honestly, save in the repo, ask before renaming |
