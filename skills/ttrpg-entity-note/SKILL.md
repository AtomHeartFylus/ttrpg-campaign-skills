---
name: ttrpg-entity-note
description: "Create or update the single note for one campaign entity — an NPC, place, faction, item or creature. Use when asked to add, write, flesh out or fix the note for a character, location, group, artefact or creature in a campaign repo. Covers searching before creating (update what exists), the admission test that decides whether the entity earns a note at all, playable intention proportional to its role, connecting it to a player's exposed nerve as a parallelism rather than a cameo, the stat-block link policy, link density and reachability, frontmatter and folder placement. Does not write the session it appears in (see ttrpg-session-prep), record what it did at the table (see ttrpg-session-log), or plan the arc it belongs to (see ttrpg-campaign-arc)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Entity note

Produces **one note for one entity**, small and linked, that prep can draw from and that the
repository's concept graph can reach. It is read cold, months later, by someone who has forgotten
why this entity was invented.

> **P1 does not apply here.** Prep documents inline everything; entity notes are wiki notes and
> obey the repository's normal *link, don't copy* rule. The one thing that never gets inlined
> **anywhere** is a stat block outside its own note.

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

| Slot | Used for | If empty |
|---|---|---|
| §1 System | whether this entity needs a stat/mechanics note, and in what form | write fiction only; note that mechanics are undefined |
| §3 Tone | the register of the description and the question the entity must pose | ask once, then proceed |
| §4 Canon source | entities the canon already fixes: place them where the source places them | treat every entity as original |
| §5 Recurring guide | whether this entity touches the guide's arc (a line for the guide to have about it) | drop that line |
| §6 Structure | whether the entity comes from published material → attribution link + record the deviation | treat as homebrew |
| §7 Table conventions | how hooks are staged; language of play; what this table recognises | stage hooks as parallels by default; do not guess the cultural frame |
| §8 Player-facing outputs | what players may read; where GM-only material lives | keep every secret in a clearly GM-only section |
| §9 Repo conventions | folder, file naming, link syntax, frontmatter tag families, verification command | ask where the note goes; do not invent a folder |
| §10 Working agreements | default deliverable; renaming rules; retroactivity | save the note in the repo; never rename an existing note |

If the profile is missing, run `ttrpg-campaign-setup` first — do not guess conventions.

## Phase 1 — Search before creating

**Creating a duplicate is the most common failure of this skill.** Before writing a line:

1. Search the repo for the name, every plausible spelling, and any alias
   (`rg -i "<name>"` across the folder map from §9 — notes, indexes, session logs, prep docs).
2. Search for the **role**, not just the name: an unnamed "the innkeeper who owes them a favour"
   may already exist under another label in a session log.
3. If a note exists → **update it in place.** Add sections, never fork a second note.
   Never rename or move the existing note without asking (§10) — links break silently and the
   graph loses it.
4. If the entity appears in published material (§6), read that entry first; the note records what
   you changed and **why** (that reason is what future prep must stay consistent with — the arc's
   deviation ledger, see `ttrpg-campaign-arc`).
5. Read every session log where the entity already appeared. The log is the authority on what it
   did and said (P11); the note must not contradict it.

## Phase 2 — The admission test

Before the entity gets a note, three questions must have **explicit** answers:

1. **Why is it here** — what put it in this place, in this condition, under this pressure, in the
   internal logic of the setting. Not "it lives here": what the world's own rules make of it.
2. **What does it represent** — which social, cultural or moral mechanism it embodies. Not a
   label ("a corrupt official") but the machinery: which complicity, which appetite, which fear
   made it possible.
3. **What question does it pose to the table** — the moral or practical question it opens that the
   players *cannot answer immediately*. This is P5 applied to an entity instead of a scene.

**The verdict is binding:**

- Three answers → it earns a note, and prep can build a scene on it.
- The third answer is obvious ("it was evil", "it's a shopkeeper") → the entity is **decorative,
  not narrative**. Admit it as **background colour without dialogue**: one line in the location or
  faction note, no note of its own, no scene built on it. Do not promote it later without redoing
  the test.
- It only works as a joke or a moment of recognition → same treatment. Recognition is a spice, not
  a scene.

Write the three answers *into the note*. They are the note's spine, not scaffolding to delete:
in six months they are the only thing that explains why this entity exists.

## Phase 3 — Structure

```markdown
---
<frontmatter per profile §9: the tag family for this entity type>
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

Sections with nothing to say are **deleted, not left empty**. A note padded with headings reads as
if the entity were prepared when it was not.

## Phase 4 — Required elements

### Playable intention, proportional (P4)
Full block only for an entity whose misread will breaks a scene, or a hook that dies if it only
recites a line. One line of want for recurring background figures. Type-level behaviour for
crowds and rank-and-file. Nothing for obvious motives, hazards and pure atmosphere. A deliberately
will-less entity says so, as a choice. Places and items carry intention only when the fiction
treats them as wilful; otherwise they carry **pressure** — what they do to whoever stays.

### Parallelism, not cameo
When an entity is built to touch a player's **exposed nerve** — the hooks recorded in their dossier
(see `ttrpg-table-dossier`), staged as profile §7 declares — the default is a **parallel**: build the
*same mechanism* of the flaw wearing a different face. An anonymous figure, or a different one, that runs the same machinery lands harder
than the literal figure the player named, because **the player makes the connection themselves**
and a connection you hand over is one they do not have to make.

In the note, record: **whose nerve** it addresses, **which emotion** to provoke, **which question**
to put to that player. Never a script of the scene — the form of the scene belongs to prep.

- **Cultural proximity is a requirement, not a preference.** The figure, archetype or reference
  must be recognisable *to this table* — the frame is set by profile §3 (tone) and §7 (language of
  play and table composition), and by the campaign overlay if it declares casting rules. A
  reference the table does not recognise produces silence, and silence reads as a failed scene.
  When a player's named reference sits outside that frame, find the **nearest parallel**: same
  mechanism of the flaw, a face this table knows.
- **Stated exception** (and the case §7 calls a literal appearance): a figure that *is* the moral
  question in itself — where the whole scene
  rests on that specific person — is met directly. The test: remove the name and ask whether the
  scene still stands. If it collapses, the direct encounter is the right call.
- If the profile declares no dossier hooks and no cultural frame, **skip this entirely**. Do not
  invent a nerve for a player.

### Stat blocks stay in their own note (P1)
The full stat block lives in the mechanics note for that creature/NPC and is **linked**, never
copied into an entity note and never inlined into prep. If the entity has one distinguishing
mechanical trait, write that trait here in one line — short, and needed at the table — and link
the rest. If §1 declares no stat format, describe the threat in fiction and say mechanics are open.

### Link density and reachability
**An entity note that links to nothing is orphaned from the campaign's concept graph** — it will
never surface while preparing the session that needed it. Minimum, in the profile's link syntax
(§9): the **place** it belongs to, its **affiliation** (faction, patron, owner), at least one
**thematic** link (the theme, mechanic or region it embodies), and every **entity** it has a
relationship with. Reciprocate the important ones from the other side.
Reachability, not just outbound links: the entity must be reachable from a hub or an index. If the
profile's indexes are generated by query, the frontmatter tag *is* the reachability — get it right.
Do not add the entity to a static roster table (P10).

### State and secrets
Any tracked value this entity owns (position, disposition, resources, status) is written **here and
nowhere else** (P10); everywhere else reads it. Secrets, hidden truths and planned reveals go in a
clearly marked GM-only section — and if the profile declares that players may read this folder
(§8), the secret moves to the GM-only location §8 declares, and this note links to nothing that
leaks it. Never improvise that location.

### Naming and placement
File name, separators and forbidden characters per §9; folder per the §9 map for this entity type.
Aliases for the names the table actually uses, so links resolve. If two entities would collide on
name, disambiguate the new one — never rename the old one without asking (§10).

## Phase 5 — Verify

- Searched first: no second note exists for this entity under any spelling, alias or role.
- All three admission answers are written, and the third is not obvious. A failed entity was
  demoted to background colour instead of being written up.
- Playable intention present where the will is not obvious, absent where the motive is obvious,
  and a will-less entity is marked as a choice.
- Any nerve-touching entity records whose nerve, which emotion, which question — and is a
  parallelism unless the direct encounter passes the remove-the-name test.
- No stat block inlined; the mechanics link resolves.
- Links: place + affiliation + theme + related entities, in the profile's syntax; the entity is
  reachable from a hub or an index; no static roster table was edited.
- Tracked state exists in this note only; secrets are in a GM-only section consistent with §8.
- Run the profile's verification command (§9) — invariant as declared (typically **0 broken
  links**). If the profile declares none, say the links were not verified; do not imply they were.

## What NOT to do

- Do not create a note before searching; do not fork a second note for an entity that exists.
- Do not rename, move or reorganise existing notes without asking.
- Do not write up an entity that fails the third question — demote it to background colour.
- Do not inline a stat block, and do not copy published material into the note; link and attribute.
- Do not stage the literal figure a player named when the same mechanism with another face would
  make the player do the connecting.
- Do not use a reference this table will not recognise, and do not invent a player's nerve.
- Do not leave the note orphaned: no links in, no links out, no tag.
- Do not copy tracked state into an index, a hub or a prep document.
- Do not leave empty headings as evidence of work that was not done.
