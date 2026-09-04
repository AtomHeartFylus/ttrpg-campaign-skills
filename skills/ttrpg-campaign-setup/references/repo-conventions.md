# Repository conventions — worked detail

Companion to Phase 3 of `SKILL.md`. Everything here is written **into profile slots**; this file is
how to fill them concretely, not a second place to store the answers.

---

## The folder skeleton, annotated

Create only what the answers justify. A folder with no declared purpose is a folder that collects
strays.

```
<repo root>/
  campaign-profile.md        # the contract itself; C.root declares everything below
  <state hub>.md             # C.hub — single source of truth for current state (P10)
  <sessions>/                # prep + log, one pair per session, progressively numbered
  <people>/                  # one note per PLAYER — owned by ttrpg-table-dossier
  <entities>/                # one note per NPC / creature / faction
  <places>/                  # one note per location, at the granularity C.granularity implies
  <items>/                   # only if the ruleset makes individual items significant
  <official>/ <reworked>/    # only if D.backbone declares a published source it deviates from
  <player-facing>/           # only what C.player_access says players may read
  <gm-private>/              # C.gm_private — required as soon as players can read the repo
  <recaps>/                  # only if D.recap declares an opening recap form
  assets/                    # media; declare in .gitignore what is too large to version
  scripts/                   # whatever C.verify names
```

Rules that survive contact with a real vault:

- **Names in the repo's language.** If the table plays in one language and the repo is written in
  another, the profile says which is which and the folder names follow the repo's.
- **One folder per kind, forever.** The second folder for the same kind of note is how a vault
  dies: two half-populated homes, links pointing at both, and no way to tell which is current.
- **The map goes in the profile as a table**, folder → what belongs in it. The test: an agent that
  has never seen this vault can answer "where does this new note go?" from the profile alone.
- **Capture folders only if recording consent is `yes`.** Raw audio is ignored by version control,
  transcripts are versioned. No consent → the folders do not exist, and their absence is the point.

## The state hub

The hub answers, at a glance: where the party is, what happened last, what is open, what is next.
It holds nothing that is a property of an entity note.

```markdown
## Now
Party is <where>, <when>, immediately after <last event>.

## Open threads
- [ ] <thread> — owed to <entity>, opened session <n>
- [ ] <thread> — deadline: <in-fiction condition>

## Party state
<live view / query over the character notes — NOT a typed table>

## Next
<the immediate pressure, one line>
```

- If the tooling has no query mechanism, link the entity notes and say the values live there. A
  link that costs one click beats a table that is confidently wrong.
- The single legitimate frozen snapshot in the whole repo is the **exit state** of a session log
  (P10): it is history, not state.
- A one-shot has no hub; the prep note is the hub. Record that decision rather than leaving an
  empty file that looks unmaintained.

## Frontmatter, tags, links, names

**Tag families.** Namespaced `<kind>/<subkind>`, declared as a closed list in the profile:

```yaml
tags: [entity/npc, place/city, thread/open]
```

A tag that exists in exactly one note is a typo until proven otherwise. Review the list when it
grows; an open-ended tag vocabulary is a search that stops working.

**Properties vs. body.** Every *tracked* value is frontmatter; prose is body (P10).

```yaml
---
type: entity/npc
status: alive
location: "<link to the place note, in the exact syntax recorded in C.links>"
<tracked resource>: 12
---
```

**Link syntax, written literally.** Record the exact forms, including the awkward ones — a plain
link, an aliased link, a link inside a table cell, an embedded attachment, and any character that
must be escaped. Ambiguity here produces breakage that no error message announces.

**File naming.** Record allowed separators and **forbidden characters**. The lesson: a vault where
an en-dash was typed instead of a hyphen in one note title broke every link to it, silently, and
the mistake was invisible in rendered text.

**Search before creating.** Update the existing note; a near-duplicate splits a history in two.

**Link, don't copy** — except the prep document, which inlines what the GM needs at the table (P1).
Record that exception in the profile so a later tidy-up does not "fix" it.

## Verification command and invariant

The invariant is usually **0 broken links, embedded attachments included**. What matters is that
the command exists, runs, and has a baseline you have seen with your own eyes.

- Run it at setup and report the actual number. A checker that is already red at setup is not an
  invariant, it is decoration.
- Record the command verbatim in the profile, with the invariant beside it, because every skill in
  this package ends its verify phase by running it.
- No checker available → write `none — invariant unverifiable`. Naming a command that does not run
  is worse than admitting there is none: the next agent will report a pass it never got.

## Portability checklist

- Profile, conventions, hub, dossiers and working agreements: all files, all in the repo.
- Campaign-specific skills and overlays: canonical copy **in the repo**, installed from there.
  Fix the canonical copy; never edit the installed one.
- Nothing in an account-bound assistant memory, a harness setting, a local config, or a chat.
- Test: a fresh agent, another machine, a different model, only a clone and no history — can it
  prepare the next session? Anything that fails this is a bug in the repo, not in the agent.
