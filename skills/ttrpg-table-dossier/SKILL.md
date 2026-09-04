---
name: ttrpg-table-dossier
description: "Run session zero and produce one dossier note per PLAYER — the people layer of the campaign: playstyle craft notes, harvested hooks, safety tools, attendance convention and the spotlight rotation ledger. Use when starting a table, onboarding a player, collecting hooks or safety tools, or checking whether someone has been chorus too long — this skill owns the rotation formula, its tolerance and the ledger, and is the only place that answers that question. Covers how far the characters sit from the players themselves and what that permits, since hook harvest and GM-facing notes about a person are gated on it. Does not write the prep that spends the spotlight (see ttrpg-session-prep), commit which player is protagonist in upcoming sessions (see ttrpg-campaign-arc), record what happened at the table (see ttrpg-session-log), or set the repo conventions it obeys (see ttrpg-campaign-setup)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.1"
---

# Table dossier

Produces the notes about the **people at the table**: the session-zero decisions and one dossier per
player. These are the input of every prep (`ttrpg-session-prep` reads them in Phase 1) and the
output of every log. The campaign's mechanics live elsewhere; this is where the table lives.
**It also owns the spotlight rotation formula, its tolerance and its ledger — the only definition
in the package.**

> **One note per PLAYER, not per character.** The person is the constant across character death,
> retirement and system change; the character is a section or a linked note. A vault organised by
> character loses how that human plays the moment their PC dies.

---

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

**Supporting references** — read the one you need:
- [references/session-zero.md](references/session-zero.md) — the seven decisions of a session zero,
  the distance conversation, and how each ends as a written profile slot. Only when a campaign is
  starting, a player is joining, or an unsettled question is reopened.
- [references/playstyle-and-rotation.md](references/playstyle-and-rotation.md) — craft notes,
  the rotation check and attendance, in full.

## Phase 0 — Read the campaign profile

**Find it before declaring it missing.** Search the repo/vault root for a file named
`campaign-profile.md` (`rg --files -g campaign-profile.md`, or the equivalent) before concluding
there is none. A profile that exists but was not found re-interviews a GM who already answered.

| Slot | Used for | If empty |
|---|---|---|
| `B.distance` | **the ethics gate — read it before harvesting anything.** How far the characters sit from the players themselves | **ask which of the three this table is before the hook harvest**; never assume `fictional` |
| `B.size`, `B.protagonists` | **the rotation formula `B.size / B.protagonists`** — this skill owns it | ask both; they are load-bearing and no constant may be substituted |
| `A.ruleset`, `A.resource`, `A.resource_shape`, `A.resource_asymmetry` | which character-side values are properties — **`A.resource_shape` decides whether the resource is per-player at all** | track only what the GM names; no resource property |
| `D.tone` | the tone contract and the hard lines / lines & veils to agree on | make it the first session-zero item, then write the answer back |
| `D.shape` | one-shot / series / open sandbox — see the branch below | ask once; do not assume `series` |
| `B.cadence`, `B.absence` | the budget window; the absent-player convention and whether absentees advance | decide both here and write them back |
| `B.safety` | which tools, who may invoke them, what happens, **refresh cadence** | decide it here; under `close` / `self-insert` it is mandatory, not optional |
| `B.hooks_count`, `B.hooks_staging` | how many nerves per player, and how they are staged | 2–3 per player, staged as parallels |
| `B.retention` | how long playstyle notes and harvested hooks about a real person are kept, and who can have an entry removed | say plainly that these notes are kept indefinitely, and offer to set the rule — under `B.distance` = `self-insert` / `close`, ask before writing rather than after |
| `C.player_access`, `C.gm_private`, `C.root`, `C.frontmatter`, `C.links`, `C.verify` | where playstyle notes and hook records may live; dossier folder, properties, link syntax, verification | assume players read nothing and keep playstyle GM-side; run `ttrpg-campaign-setup` — do not invent a layout |
| `E.review`, `E.never_without_asking`, `E.overrides`, `E.audit_cadence` | bluntness; what not to do without asking; which defaults are off; how often the rotation check runs | write honestly, save in the repo, ask before renaming |

**`D.shape` branch — mandatory.** `series` → as written. `one-shot` → dossiers collapse to whatever
the pre-game exchange produced; **the rotation ledger does not apply**, becoming a within-session
check (every player gets one scene whose outcome depends on them); attendance: skip. Keep the safety
conversation and the `B.distance` gate in full — a one-shot with self-inserted players is still
aimed at people. `open sandbox` → as written; the rotation counts sessions, not chapters.
**Empty → ask once.**

**`B.distance` gate — mandatory, read before harvesting anything.** This skill harvests a person's
exposed nerves and writes GM-facing notes about them; the slot decides what that is. `fictional` →
hooks and playstyle notes are about a character, proceed as written. `close` / `self-insert` →
**the safety conversation and its refresh are load-bearing, not optional**, and the hook harvest is
a consent conversation rather than a questionnaire: material aimed at a character is aimed at a
person (rules and wording in [references/session-zero.md](references/session-zero.md)).
**Empty → ask which of the three this table is and write it into `B.distance` before the harvest
runs** — do not assume `fictional`: that default treats a named human's exposed nerve as set
dressing, and it cannot be walked back.

## Phase 1 — Read before writing

1. **The existing dossiers** — never start a player's note from scratch if one exists; update it.
2. **The last 3–4 session logs** — who carried scenes, who has no line in them, which hooks fired.
   Logs are the authority on what happened (P11); memory flatters the loud players.
3. **The campaign state hub** — current state, open per-player obligations.
4. **`D.tone`, `B.safety` and `B.distance`** — a session zero that re-opens settled questions wastes
   the table's patience; one that skips unsettled ones detonates later.

## Phase 2 — Session zero (only when the campaign or a player is starting)

Seven decisions — **distance first**, then expectations, tone contract, safety tools, repo access,
attendance, hook harvest — each of which must end as a **written profile slot or dossier section**,
never as something the table remembers agreeing to. Agenda, wording, the distance conversation and
the safety-refresh rules: [references/session-zero.md](references/session-zero.md).

If the campaign is already running, skip to Phase 3; reopen only the decisions the profile leaves
empty.

## Phase 3 — The dossier

```markdown
---
<frontmatter per C.frontmatter: player tag, aliases>
<tracked properties per A.ruleset / A.resource: the state values, one place only — P10>
---

# <Player>

> [!info] What this note is
> (one line: the player and their character(s); state lives in the properties above)

## Character
(who they are in the fiction, what A.ruleset tracks, links to the entity notes — no state here)

## Hooks / exposed nerves
(harvested, not hoped for — gated on B.distance, see below)

## Playstyle           <!-- GM-facing craft notes; relocate per C.gm_private, never soften -->

## Diary
(one entry per session they played, newest work appended by ttrpg-session-log's downstream step)
```

### Tracked properties are the single source of truth (P10)
Every per-player value the system tracks — advancement if `A.ruleset` has any, the dramatic
resource, rewards held, status — lives **only** in this note's frontmatter, read everywhere else
through a view or a query. No roster table in the hub, an index or a prep document; the one admitted
freeze is the *exit state* of a session log. **Check `A.resource_shape` before adding a resource
property here:** it is per-player only when the shape is `per-character`. A **shared party clock**
lives once, on the party's note — copying it into each dossier is the exact P10 violation this
section forbids; a per-faction shape lives on the faction's note.

### Hooks are harvested, never hoped for
**Read `B.distance` first — the gate in Phase 0.** It decides whether the questions below are a
character interview or a consent conversation, and under `close` / `self-insert` it makes the safety
refresh mandatory *before* harvesting. Empty → ask before harvesting, never assume.

Ask each player, directly and on the record, for the number of **people, obligations or unfinished
pieces of their character's life** that `B.hooks_count` declares (default 2–3), tied to whatever the
campaign will press on. Write down the **figure or fact** in the player's words, the **emotion** it
is meant to provoke in this player, and the **question** it lets you put to them that they cannot
answer immediately. Wording and the consent variant: [session-zero.md](references/session-zero.md).

A hook records a **nerve, not a scene** — not an NPC to place on a map. Prep builds a situation
running the *same mechanism*, and the player makes the moral connection themselves, which lands
harder than the literal cameo. `B.hooks_staging` may declare literal appearances; empty → parallels.
**Which real or public figures are admissible, and the cultural frame they must sit inside, is
`B.frame`** — one slot, read by `ttrpg-entity-note` when it builds the figure. Do not restate
casting rules here or scatter them into the overlay. Under `close` / `self-insert` a harvested hook
is a fact about a real person's life: it lives where `C.gm_private` says, and the player may
withdraw one at any time without giving a reason.

**Missing-hook check:** a player with an empty hooks section is a player prep cannot aim at. Make
harvesting it an explicit early scene — do not wait for it to emerge naturally, it does not.

### Playstyle, rotation and attendance
**[references/playstyle-and-rotation.md](references/playstyle-and-rotation.md) owns these three in
full — read it while writing the GM-facing half of a dossier.** The load-bearing summary:

- **Playstyle notes** are observed, **dated** moves, never adjectives ("S4: took the deal that cost
  him and argued the group into it"). They are the direct input of the prep red team (P9). **Where
  they live is `C.player_access` / `C.gm_private`** — never soften them to survive being read,
  relocate them; under `close` / `self-insert` relocation is not optional.
- **Spotlight rotation — this skill owns the formula, the tolerance and the ledger** (P7), and is
  the only place in the package that answers *has anyone been chorus too long?*
  - **One derivation:** the dossier diaries. No spotlight table, no parallel tally from the logs.
  - **One formula:** the rotation period is **`B.size` / `B.protagonists` sessions**. Both are
    slots; **no constant may be substituted for either**, and either empty → ask and write it back.
    `E.overrides` declaring `P7 — off` switches the whole check off.
  - **One tolerance:** flag a player chorus for more than **1.5× the rotation period** consecutive
    sessions. Nothing else in the package may state a competing threshold. Qualitative alarms fire
    before the arithmetic does.
  - **The fix is a named commitment** handed to `ttrpg-campaign-arc`, which schedules which upcoming
    chapter or front that player carries. `D.shape` = `one-shot` → no rotation exists; run the
    within-session check instead.
- **Attendance** applies what `B.absence` declares, decided once, never renegotiated in the moment.
  Empty → ask once and write it back. `D.shape` = `one-shot`: skip it.

## Phase 3bis — Updating dossiers after play

**`ttrpg-session-log` owns this step.** It is the authority on what happened (P11) and its state
phase already specifies which properties move, that only players present advance (per `B.absence`),
and that new hooks and playstyle changes get written. Do not re-interview the GM or restate that
procedure: take the finished log as input. What this skill adds afterwards — diary register, hook
lifecycle, playstyle discipline, and why the diary entry **is** the spotlight ledger — is in
[references/playstyle-and-rotation.md](references/playstyle-and-rotation.md).

## Phase 4 — Verify

- One note per player, at the path `C.root` declares; no dossier organised around a character.
- Every tracked value exists in exactly one place — the properties of this note (P10) — and nowhere
  in the hub, an index or a prep document.
- Every player has a non-empty hooks section or an explicit plan for harvesting it — and
  `B.distance` was read **before** any of it was harvested, not assumed.
- Playstyle sections contain observed, dated moves — not adjectives — and sit where
  `C.player_access` / `C.gm_private` permit.
- Under `close` / `self-insert`: the safety conversation happened and its refresh is scheduled;
  hooks and playstyle notes sit in the GM-private location; every hook is in the player's own words.
- Session-zero decisions were written back into `D.tone`, `B.safety`, `B.absence`, `B.distance` and
  `C.player_access`, not left in chat; the attendance and advancement rules are unambiguous.
- Spotlight check run from the diaries: nobody past **1.5 × (`B.size` / `B.protagonists`)** without
  a named commitment handed to `ttrpg-campaign-arc`. No constant was substituted for either slot.
- Links follow `C.links`; run the `C.verify` command — invariant as declared.

## What NOT to do

- Do not write a dossier per character.
- Do not water down playstyle notes to make them player-safe — relocate them instead.
- Do not record hooks as NPCs to place, or promise a literal cameo of every one.
- Do not build a spotlight table; derive the ledger from the diaries and from nothing else.
- Do not hardcode a protagonist count or a table size — the formula is `B.size / B.protagonists`,
  and an empty slot is asked for, never guessed. Do not let a second "chorus too long" threshold
  exist anywhere: 1.5× the rotation period, defined here, is the only one.
- Do not equalise spotlight across all players — thin slices for everyone means a scene for nobody.
- Do not re-decide the absent-player convention each session, or advance an absentee against it.
- Do not copy a tracked value into the hub, an index or a prep document.
- Do not re-run the session-log interview here; take the finished log as input.
- Do not skip the safety-tools refresh because nobody has ever used the tool — and never treat it
  as optional when `B.distance` is `close` or `self-insert`.
- Do not harvest a hook, or write a GM-facing note about a person, while `B.distance` is empty.
  Ask first; do not assume the fictional case.
