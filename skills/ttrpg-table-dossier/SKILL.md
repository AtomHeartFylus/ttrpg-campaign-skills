---
name: ttrpg-table-dossier
description: "Run session zero and produce one dossier note per PLAYER — the people layer of the campaign: playstyle craft notes, harvested hooks, safety tools, attendance convention and the spotlight budget across sessions. Use when starting a table, onboarding a player, collecting hooks or safety tools, or checking whether someone has been chorus too long. Does not write the prep that spends the spotlight (see ttrpg-session-prep), record what happened at the table (see ttrpg-session-log), or set the repo conventions it obeys (see ttrpg-campaign-setup)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Table dossier

Produces the notes about the **people at the table**: the session-zero decisions and one dossier per
player. These are the input of every prep (`ttrpg-session-prep` reads them in Phase 1) and the
output of every log. The campaign's mechanics live elsewhere; this is where the table lives.

> **One note per PLAYER, not per character.** The person is the constant across character death,
> retirement and system change; the character is a section or a linked note. A vault organised by
> character loses the accumulated knowledge of how that human plays the moment their PC dies.

---

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

**Supporting reference:** [references/session-zero.md](references/session-zero.md) — the six
decisions of a session zero and how each one ends as a written profile slot. Read it only when a
campaign is starting, a player is joining, or an unsettled question has to be reopened; the rest of
this skill runs far more often than that.

## Phase 0 — Read the campaign profile

| Slot | Used for | If empty |
|---|---|---|
| §1 System | which character-side values are worth tracking as properties | track only what the GM names |
| §2 Dramatic resource | the per-player tracked value and its asymmetries | no resource property; drop those lines |
| §3 Tone | the tone contract and the hard lines / lines & veils to agree on | make the tone contract the first session-zero item, then write the answer back into §3 |
| §7 Table conventions | table size → spotlight rotation; cadence → budget window; absent-player rule; safety tools and refresh | these *are* session zero's output — decide them here and write them back |
| §8 Player-facing repo access | where playstyle notes may live | assume players read nothing; still keep playstyle GM-side |
| §9 Repo conventions | dossier folder, frontmatter properties, link syntax, verification command | run `ttrpg-campaign-setup` first — do not invent a layout |
| §10 Working agreements | bluntness of the craft notes; what not to do without asking | write honestly, save in the repo, ask before renaming |

## Phase 1 — Read before writing

1. **The existing dossiers** — never start a player's note from scratch if one exists; update it.
2. **The last 3–4 session logs** — who carried scenes, who has no line in them, which hooks fired.
   Logs are the authority on what happened (P11); memory flatters the loud players.
3. **The campaign state hub** — current state, open per-player obligations.
4. **The profile's tone and safety slots** — a session zero that re-opens settled questions wastes
   the table's patience; one that skips unsettled ones detonates later.

## Phase 2 — Session zero (only when the campaign or a player is starting)

Six decisions — expectations, tone contract, safety tools, repo access, attendance, hook harvest —
each of which must end as a **written profile slot or dossier section**, never as something the
table remembers agreeing to. The agenda, the wording of each question and the rules for safety-tool
refresh are in [references/session-zero.md](references/session-zero.md).

If the campaign is already running, skip to Phase 3; reopen only the decisions the profile leaves
empty.

## Phase 3 — The dossier

```markdown
---
<frontmatter per profile §9: player tag, aliases>
<tracked properties per profile §1/§2: the state values, one place only — P10>
---

# <Player>

> [!info] What this note is
> (one line: the player and their character(s); state lives in the properties above)

## Character
(who they are in the fiction, what §1 says about them, links to the entity notes — no state here)

## Hooks / exposed nerves
(harvested, not hoped for — see below)

## Playstyle           <!-- GM-facing craft notes -->

## Diary
(one entry per session they played, newest work appended by ttrpg-session-log's downstream step)
```

### Tracked properties are the single source of truth (P10)
Every per-player value the system tracks — advancement if §1 has any, the dramatic resource (§2),
rewards held, status — lives **only** in this note's frontmatter, and is read everywhere else through a view or a
query. No roster table in the hub, in an index or in a prep document. The one admitted freeze is the
*exit state* section of a session log.

### Hooks are harvested, never hoped for
At session zero ask each player, directly and on the record, for **2–3 people, obligations or
unfinished pieces of their character's life** (more only if the campaign declares a different count) tied to whatever the campaign will press on (the sin,
the crime, the debt, the failure — in the profile's own terms). Write down:

- the **figure or fact**, in the player's words;
- the **emotion it is meant to provoke in this player**;
- the **question it lets you put to them** that they cannot answer immediately.

A hook records a **nerve, not a scene**. It is not an NPC to place on a map: prep builds a
situation that runs the *same mechanism*, and the player makes the moral connection themselves —
which lands harder than the literal cameo. Casting rules for real or public figures, if the
campaign has any, belong in the campaign overlay, not here.

**Missing-hook check:** a player with an empty hooks section is a player prep cannot aim at.
Make harvesting it an explicit early scene — do not wait for it to emerge naturally, it does not.

### Playstyle — honest GM-facing craft notes
The most valuable section in the vault and the one people soften into uselessness. Write what you
would tell a co-GM taking over your table tomorrow:

- **Who charges in**, who waits, who solves laterally, who negotiates before drawing.
- **Who must be handed a scene** — will not take spotlight, will play it beautifully when given it.
- **Who is chorus**, and whether by preference or by neglect. The distinction is the whole point.
- **What makes this player light up** — the exact register: tactics, moral dilemma, comedy, lore,
  a scene alone with an NPC, being asked to decide for the group.
- **What makes them go quiet**, and what they will not do at the table.
- **Out-of-character constraints** that shape prep: arrives late, leaves early, unreliable, loud.

Adjectives are worthless here; write **observed moves**, dated to the session where you saw them
("S4: took the deal that cost him and argued the group into it"). This section is the direct input
of the prep red team (P9): a table's derailments are predictable from its playstyle notes.

**Where it lives** depends on profile §8. If players may read the repo, playstyle notes go in a
GM-only location — a private folder, a separate repo — and the dossier links to them. Never soften
the notes to make them safe to read; move them instead.

### Spotlight budget across sessions (P7)
2–3 protagonists per session, the rest chorus, rotating. This skill owns the **budget**, prep owns
the spending.

- **No spotlight table.** The ledger is derived: each dossier's Diary says which sessions that
  player carried; count from there.
- **Rotation window:** with a table of *T* players and ~2.5 protagonists a session, everyone should
  carry a session roughly every *T / 2.5* sessions. Flag anyone past **1.5×** that window.
- **Qualitative alarms**, which fire before the arithmetic does: their last diary entries are all
  reactions to other people's scenes; they have no quoted line in the last two logs; they stopped
  proposing; they are the one who fills silences with jokes rather than choices.
- **The fix is a named commitment**, not good intentions: this player is a protagonist of the next
  session, and prep is told which of their hooks it is built on. The lesson of the player who was
  chorus four sessions running, stopped proposing anything, and had to be re-recruited to the
  campaign after having never once complained.
- Single-session play: the budget collapses into a within-session check — every player gets one
  scene where the outcome depends on them.

### Attendance convention (profile §7)
Apply what §7 declares: one in-fiction explanation for absent players, agreed once and used without
negotiation, plus the rule on whether absentees advance. Deciding either in the moment turns
attendance into a negotiation and absence into a grievance. If the slot is empty, ask once and
write it back — the requirements a good convention must meet are in
[references/session-zero.md](references/session-zero.md). Single-session play: skip it.

## Phase 3bis — Updating dossiers after play

**`ttrpg-session-log` owns this step.** It reconstructs the evening, is the authority on what
happened (P11), and its own state phase already specifies which properties move, that only players
present advance (per §7), and that new hooks and playstyle changes get written. Do not re-interview
the GM and do not restate that procedure. Take the finished log as input.

What this skill adds, once the log has done its part:

- **Register of the diary entry:** GM-facing and concrete — the choice they made, what it cost them,
  what they now carry. Not a summary of the session (the log is that), not praise.
- **Hook lifecycle:** mark which hook fired and how it landed; keep unfired ones visibly open; an
  obligation the character took on is a new hook, recorded as one.
- **Playstyle discipline:** revise **only when the table surprised you**, and add the move dated to
  its session. A section rewritten every week stops recording anything.
- **Spotlight ledger:** no separate bookkeeping — the diary entry itself says whether they carried
  the session or were chorus. Run the rotation check (above) every few sessions, not every week.

## Phase 4 — Verify

- One note per player, at the path §9 declares; no dossier organised around a character.
- Every tracked value exists in exactly one place — the properties of this note (P10) — and nowhere
  in the hub, an index or a prep document.
- Every player has a non-empty hooks section, or an explicit plan for harvesting it.
- Playstyle sections contain observed, dated moves — not adjectives — and sit where §8 permits.
- Session-zero decisions were written back into profile slots §3, §7 and §8, not left in chat.
- The attendance convention and the absentee-advancement rule are recorded and unambiguous.
- Spotlight check run: nobody past 1.5× the rotation window without a named commitment.
- Links follow §9; run the profile's verification command — invariant as declared.

## What NOT to do

- Do not write a dossier per character.
- Do not water down playstyle notes to make them player-safe — relocate them instead.
- Do not record hooks as NPCs to place, or promise a literal cameo of every one.
- Do not build a spotlight table; derive the ledger from the diaries.
- Do not equalise spotlight across all players — thin slices for everyone means a scene for nobody.
- Do not re-decide the absent-player convention each session, and do not advance an absentee
  against the profile's rule.
- Do not copy a tracked value into the hub, an index or a prep document.
- Do not re-run the session-log interview here; take the finished log as input.
- Do not skip the safety-tools refresh because nobody has ever used the tool.
