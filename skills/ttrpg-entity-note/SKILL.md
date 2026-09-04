---
name: ttrpg-entity-note
description: "Create or update the single note for one campaign entity — an NPC, place, faction, item or creature. Use when asked to add, write, flesh out or fix the note for a character, location, group, artefact or creature in a campaign repo. Covers searching before creating (update what exists), the admission test that decides whether the entity earns a note at all, playable intention proportional to its role, connecting it to a player's exposed nerve as a parallelism rather than a cameo, the stat-block link policy, link density and reachability, frontmatter and folder placement. Does not write the session it appears in (see ttrpg-session-prep), record what it did at the table (see ttrpg-session-log), or plan the arc it belongs to (see ttrpg-campaign-arc)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.1"
---

# Entity note

Produces **one note for one entity**, small and linked, that prep can draw from and that the
repository's concept graph can reach. It is read cold, months later, by someone who has forgotten
why this entity was invented.

> **P1 does not apply here.** Prep documents inline everything; entity notes are wiki notes and obey
> the repository's normal *link, don't copy* rule. The one thing never inlined **anywhere** is a
> stat block outside its own note.

---

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

**Find it before declaring it missing.** Search the repo/vault root for a file named
`campaign-profile.md` (`rg --files -g campaign-profile.md`, or the equivalent) before concluding
there is none. A profile that exists but was not found re-interviews a GM who already answered.

| Slot | Used for | If empty |
|---|---|---|
| `B.distance` | **the ethics gate** — whether this entity may be built on a player's exposed nerve at all | **ask which of the three this table is before touching a hook**; never assume `fictional` |
| `B.frame` | **the cultural frame a figure must sit inside to land with this table**, and which real or public figures are admissible | do not guess a frame and cast no real or public figure; ask once |
| `B.hooks_staging`, `B.safety` | parallels vs literal appearances; the tools to refresh before a nerve-touching entity reaches the table | stage as parallels; ask once before building one |
| `A.ruleset` | whether this entity needs a stat/mechanics note, and in what form | write fiction only; note that mechanics are undefined |
| `D.tone` | the register of the description and the question the entity must pose | ask once, then proceed |
| `D.canon_source` | entities the canon already fixes: place them where the source places them | treat every entity as original |
| `D.guide` | whether this entity touches the guide's arc (a line for the guide to have about it) | drop that line |
| `D.backbone`, `D.official_material`, `D.deviation_policy` | published material → attribution link + record the deviation | treat as homebrew |
| `D.shape` | one-shot / series / open sandbox — see the branch below | ask once; do not assume `series` |
| `B.language` | the language the note is written in | match the notes already in the repo |
| `C.player_access`, `C.gm_private` | what players may read; where GM-only material lives | keep every secret in a clearly GM-only section |
| `C.root`, `C.granularity`, `C.naming`, `C.links`, `C.frontmatter`, `C.verify` | folder, file naming, link syntax, tag families, verification command | ask where the note goes; do not invent a folder |
| `E.deliverable`, `E.never_without_asking`, `E.retroactivity`, `E.overrides` | deliverable; renaming rules; retroactivity; which defaults are off | save in the repo; never rename an existing note |

If the search finds no profile, run `ttrpg-campaign-setup` first — do not guess conventions.

**`D.shape` branch — mandatory.** `series` → as written. `one-shot` → the entity has one appearance
and no arc: keep the admission test (P13) in full, drop *Appearances* and any tracked state that
only matters across sessions, do not plan a return. `open sandbox` → as written, plus one line for
**which front it belongs to** and what it does if the party never comes. **Empty → ask once.**

## Phase 1 — Search before creating

**Creating a duplicate is the most common failure of this skill.** Before writing a line:

1. Search the repo for the name, every plausible spelling, and any alias
   (`rg -i "<name>"` across the `C.root` folder map — notes, indexes, session logs, prep docs).
2. Search for the **role**, not just the name: an unnamed "the innkeeper who owes them a favour"
   may already exist under another label in a session log.
3. If a note exists → **update it in place.** Add sections, never fork a second note. Never rename
   or move it without asking (`E.never_without_asking`) — links break silently.
4. If the entity appears in published material (`D.official_material`), read that entry first; the note records what
   you changed and **why** (that reason is what future prep must stay consistent with — the arc's
   deviation ledger, see `ttrpg-campaign-arc`).
5. Read every session log where the entity already appeared — the log is the authority on what it
   did and said (P11), and the note must not contradict it.

## Phase 2 — The admission test (P13)

Before the entity gets a note, answer **explicitly**, in writing: *why is it here* — what put it in
this place, in this condition, under this pressure, in the internal logic of the setting; *what does
it represent* — the mechanism, not the label ("a corrupt official" is a label; which complicity,
appetite or fear made it possible is the mechanism); *what question does it pose to the table* that
the players cannot answer immediately.

**The verdict is binding:**

- Three answers → it earns a note, and prep can build a scene on it.
- The third answer is obvious ("it was evil", "it's a shopkeeper") → the entity is **decorative, not
  narrative**. Admit it as **background colour without dialogue**: one line in the location or
  faction note, no note of its own, no scene built on it. Do not promote it later without redoing
  the test.
- It only works as a joke or a moment of recognition → same treatment. Recognition is a spice.

Write the three answers *into the note*. They are its spine, not scaffolding to delete: in six
months they are the only thing that explains why this entity exists.

## Phase 3 — Structure

```markdown
---
<frontmatter per C.frontmatter: the tag family for this entity type>
<tracked state as properties — only if this entity is the single source of truth for it (P10)>
---

# <Name>

<Two or three lines: what it is, where it stands, what a PC perceives first.
 Link the place, the faction, the theme.>

## Why it is here
## What it represents
## The question it poses          <!-- the admission test, Phase 2 -->

## Playable intention             <!-- P4, only if its will is not obvious -->
- **Wants (surface):** <the want the players can perceive>
- **Beneath it:** <the hidden truth, when it differs from the surface want>
- **Surfaces as:** <a speakable line, or a described gesture>
- **If they stall / walk away / contradict it:** <what it does>

## At the table                   <!-- delivery: voice, one repeatable gesture, register -->
## Connections                    <!-- links: place, faction, theme, related entities -->
## Mechanics                      <!-- link to the stat/rules note; local trait in one line -->
## Appearances                    <!-- append-only: link each session log where it acted -->
```

Sections with nothing to say are **deleted, not left empty**: a note padded with headings reads as
if the entity were prepared when it was not.

## Phase 4 — Required elements

### Playable intention, proportional (P4)
Full block only for an entity whose misread will breaks a scene, or a hook that dies if it only
recites a line. One line of want for recurring background figures; type-level behaviour for crowds
and rank-and-file; nothing for obvious motives, hazards and pure atmosphere. A deliberately
will-less entity says so, as a choice. Places and items carry intention only when the fiction
treats them as wilful; otherwise they carry **pressure** — what they do to whoever stays.

### Parallelism, distance and casting
**Read [references/parallelism.md](references/parallelism.md) before building an entity on a
player's exposed nerve.** It owns the full rule; the load-bearing summary:

- **`B.distance` is read first, before the hook.** `fictional` → the hook is a fact about a
  character, build freely. `close` / `self-insert` → it is a fact about a **person**: use only
  material the player put on the record in their own words, refresh `B.safety` before the entity
  reaches the table, keep the GM-facing record in `C.gm_private`, and never let the entity embody a
  claim about the player they did not author. **Empty → ask; do not default to `fictional`.**
- **The default staging is a parallel, not a cameo:** the *same mechanism* of the flaw wearing a
  different face, so **the player makes the connection themselves**. `B.hooks_staging` may declare
  literal appearances instead; empty → parallels.
- **The frame is `B.frame`** — the single home of the cultural-proximity and casting rule: which
  register a figure must belong to to land with this table, and which real or public figures are
  admissible. A named subject outside it → cast the nearest parallel inside it. **Empty → ask once;
  cast no real or public figure until it is answered.**
- **Stated exception:** a figure that *is* the moral question in itself is met directly. Test:
  remove the name and ask whether the scene still stands.
- In the note record **whose nerve**, **which emotion**, **which question** — never a scene script.
- If the profile declares no dossier hooks, **skip this entirely.** Do not invent a player's nerve.

### Stat blocks stay in their own note (P1)
The full stat block lives in the mechanics note for that creature/NPC and is **linked**, never
copied into an entity note and never inlined into prep. One distinguishing mechanical trait may be
written here in one line — short, and needed at the table — with the rest linked. If `A.ruleset`
declares no stat format, describe the threat in fiction and say mechanics are open.

### Link density and reachability
**An entity note that links to nothing is orphaned from the campaign's concept graph** — it will
never surface while preparing the session that needed it. Minimum, in the `C.links` syntax: the
**place** it belongs to, its **affiliation** (faction, patron, owner), at least one **thematic**
link, and every **entity** it has a relationship with. Reciprocate the important ones. Reachability,
not just outbound links: it must be reachable from a hub or an index — where indexes are generated
by query, the frontmatter tag *is* the reachability. No static roster table (P10).

### State and secrets
Any tracked value this entity owns (position, disposition, resources, status) is written **here and
nowhere else** (P10). Secrets, hidden truths and planned reveals go in a clearly marked GM-only
section — and if `C.player_access` says players may read this folder, the secret moves to
`C.gm_private` and this note links to nothing that leaks it. Never improvise that location:
`C.gm_private` empty while players have access → stop and ask.

### Naming and placement
File name, separators and forbidden characters per `C.naming`; folder per the `C.root` map. Aliases
for the names the table actually uses, so links resolve. Two entities colliding on name →
disambiguate the new one, never rename the old (`E.never_without_asking`).

## Phase 5 — Verify

- Searched first: no second note exists for this entity under any spelling, alias or role.
- All three admission answers are written and the third is not obvious; a failed entity was demoted
  to background colour instead of being written up.
- Playable intention present where the will is not obvious, absent where the motive is obvious, and
  a will-less entity is marked as a choice.
- Any nerve-touching entity records whose nerve, which emotion, which question — and is a
  parallelism unless the direct encounter passes the remove-the-name test.
- `B.distance` was read **before** the hook; under `close` / `self-insert` the GM-facing material
  sits in `C.gm_private`, the safety refresh is scheduled, and nothing asserts something about the
  player they did not say themselves. Empty slot → the question was asked, not assumed.
- Any real or public figure sits inside `B.frame`; nothing was cast against an empty frame.
- No stat block inlined; the mechanics link resolves.
- Links: place + affiliation + theme + related entities, in the profile's syntax; the entity is
  reachable from a hub or an index; no static roster table was edited.
- Tracked state exists in this note only; secrets sit where `C.player_access` / `C.gm_private` allow.
- Run the `C.verify` command — invariant as declared (typically **0 broken links**). If the profile
  declares none, say the links were not verified; do not imply they were.

## What NOT to do

- Do not create a note before searching; do not fork a second note for an entity that exists.
- Do not rename, move or reorganise existing notes without asking.
- Do not write up an entity that fails the third question — demote it to background colour.
- Do not inline a stat block, and do not copy published material into the note; link and attribute.
- Do not stage the literal figure a player named when the same mechanism with another face would
  make the player do the connecting.
- Do not use a reference outside `B.frame`, and do not invent a player's nerve.
- Do not build an entity on a player's hook while `B.distance` is empty — ask first — and do not
  treat a `close` or `self-insert` table's material as if it belonged to a character.
- Do not reconstruct the cultural frame from the tone slot or the overlay; `B.frame` owns it.
- Do not leave the note orphaned: no links in, no links out, no tag.
- Do not copy tracked state into an index, a hub or a prep document.
- Do not leave empty headings as evidence of work that was not done.
