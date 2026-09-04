# The off-game note

Read this **only after `B.consent_offgame` has come back as an explicit yes covering everyone
present that night.** `SKILL.md` owns the gate; this file owns what the note contains once the gate
passes. If the gate did not pass, none of this runs and none of it is written in a softened form.

---

## What it is for, and what it is not

**Roughly half of an evening is out-of-character talk** — tangents, arguments, jokes, life news,
digressions that have nothing to do with the fiction. **Two things in it are worth keeping, and
nothing else is:**

1. **The mood of the table** — the material that later explains why a scene landed or died.
2. **Hooks born off game** — a genuine share of campaign material is invented sideways in a
   digression, and is lost by morning otherwise.

If an entry serves neither, it is not curation, it is a record of what people said about their
lives. Do not write it. This test is what separates the note from surveillance, and it is the
reason the section is allowed to exist at all.

## Where it lives — read, never improvised

`C.player_access` decides. If players can read the repo, the note goes to the `C.gm_private`
location, **or** its existence and contents are agreed openly with the table — those are the only
two options. If `C.gm_private` is empty while players have access, **stop and ask**; do not pick a
folder. The path itself comes from `C.capture_paths` — **but only if that path obeys the access
rule above.** If `C.capture_paths` points at a versioned, player-readable transcript folder while
`C.gm_private` requires otherwise, the access rule wins: stop and ask. Reach is a consent question,
not a layout one, and this is the one place in the package where getting it wrong leaks material
about real people.

## The shape

One note per session, structured **by theme**, with **timecodes pointing back into the timecoded
transcript**. The file name follows `C.naming`, and the skeleton below names *sections*, not
wording: **write every heading, table column and parenthetical label in `B.language`**, keeping the
order and meaning and translating the words. If `B.language` is empty, match the notes already in
the repo and state which language you chose.

```markdown
---
<frontmatter per C.frontmatter: session tag, off-game tag>
---

# Session N — Off-game                         <!-- blocks per C.blocks, headings in B.language -->

> [!info] Curation by theme of the out-of-character talk. Timecodes index the transcript;
> this is not a transcript. Any participant may have any entry removed on request.

## <Theme — a phrase, not a category>
- `00:41:12` <one or two lines: what was said and why it matters>

## Hooks born off game
- `01:22:07` <the idea, and where it could enter the fiction>

## Table mood
- <what the evening felt like; what the group was chewing on; who was tired, who was on>

## Indexed, not quoted
- `02:14:30` crude/personal exchange — indexed only
```

## Rules

- **Curate, do not transcribe.** A theme with two timecodes beats ten verbatim lines. If a section
  is growing into a rewrite of the transcript, cut it back to its index entries.
- **Crude, offensive or personal material is indexed by timecode and never quoted.** The full
  record already exists in the transcript; the curated note does not need to reproduce it, and a
  quoted line in a curated note is the one that gets read out of context.
- **The removal rule: any participant may ask for any entry to be removed, and it is removed
  without discussion, argument or a request for a reason.** Honour a "don't write that down"
  immediately, at the table, before the note exists. **This is precisely why entries are short
  pointers rather than reproductions** — a pointer can be deleted cleanly, and deleting it destroys
  nothing that was worth keeping. A note built of quotations cannot be unwound the same way.
  The rule is stated in the note's own header, so a reader a year later knows it applies.
- Anything said off game that concerns a person at the table and not the campaign gets an index
  entry at most — or nothing, on request.
- **The hooks section is the one that feeds forward.** When a hook is used, the next prep's global
  threads or a hook entry in the player's dossier owns it from then on (P10); the off-game note
  keeps only its birth timecode. For a one-shot (`D.shape`) there is no next prep: put it in the
  single log, or declare it unused.
