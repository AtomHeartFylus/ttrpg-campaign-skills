# Parallelism, casting and distance

Read this whenever an entity is being built to touch a **player's exposed nerve** — the hooks
recorded in their dossier by `ttrpg-table-dossier`. `SKILL.md` owns the note's structure; this
file owns what may be done with a person's material.

If the profile declares no dossier hooks, skip all of it. Do not invent a nerve for a player.

---

## 1. Read `B.distance` first — before you read the hook

`B.distance` says how far the characters sit from the players themselves. It is read **before** the
hook, not after, because it decides whether the hook is fiction or biography.

| `B.distance` | What the hook is | What this skill may do with it |
|---|---|---|
| `fictional` | a fact about a character | build the parallel freely; the sections below are the whole rule |
| `close` | a fact about a person, one screen removed | only material the player put on the record **in their own words**; the entity note records *whose* nerve in a GM-only section; the `B.safety` refresh is scheduled before the entity reaches the table |
| `self-insert` | a fact about a named human being | all of `close`, plus: **the entity may not embody a claim about the player they did not author.** An entity built as a parallel of a real person the player named is a portrait of someone in that player's actual life |
| **empty** | unknown | **ask which of the three this table is.** Write the answer into `B.distance`. Harvest and build nothing against a hook until it is answered — do **not** assume `fictional` |

**Why the empty case asks instead of defaulting.** The cheap default is `fictional`, and it is the
one that does damage: it treats a named human's exposed nerve as set dressing. The expensive
default is asking once.

For `close` and `self-insert`, three rules are load-bearing rather than optional:

- **Material aimed at the character is aimed at the person.** There is no separating layer to
  absorb it. Write the note knowing the subject may one day read it.
- **The safety conversation is refreshed** before this entity reaches the table, not once at
  session zero. `B.safety` declares the tools; this is one of the moments they exist for.
- **No reveal the player did not author.** The entity may press on what the player offered. It may
  not tell them something about themselves, and it may not settle a question about a real person in
  their life on their behalf.

## 2. Parallelism, not cameo

The default staging is a **parallel**: build the *same mechanism* of the flaw wearing a different
face. An anonymous figure, or a different one, running the same machinery lands harder than the
literal figure the player named — because **the player makes the connection themselves**, and a
connection you hand over is one they do not have to make.

`B.hooks_staging` may override this: it declares whether this table wants parallels the player
connects on their own, literal appearances, or both. Empty → parallels.

In the note, record: **whose nerve** it addresses, **which emotion** to provoke, **which question**
to put to that player. Never a script of the scene — the form of the scene belongs to prep. Under
`close` or `self-insert`, that record is GM-facing material about a person: it lives where
`C.gm_private` says GM-only material lives.

### The stated exception: the direct encounter

A figure that *is* the moral question in itself — where the whole scene rests on that specific
person — is met directly. This is also the case `B.hooks_staging` calls a literal appearance.

**The test:** remove the name and ask whether the scene still stands. If it collapses, the direct
encounter is the right call. If it survives, you wanted the parallel.

Under `self-insert`, the direct encounter of a real person from a player's life is agreed with that
player in advance. It is not a surprise; the surprise is the failure mode.

## 3. Cultural proximity — the frame is `B.frame`

**Cultural proximity is a requirement, not a preference.** The figure, archetype or reference must
be recognisable *to this table*. A reference the table does not recognise produces silence, and
silence reads as a failed scene.

**`B.frame` is the single home of this rule.** It declares the cultural, historical or genre
register a figure must belong to in order to land with this table, which real or public figures are
admissible, and how they are handled. Read `B.frame` — do not reconstruct the frame from the tone
slot, from table composition, or from the overlay.

- **When someone names a subject outside the frame, cast the nearest parallel inside it:** the same
  mechanism of the flaw, wearing a face this table knows.
- **`B.frame` empty** → do not guess a cultural frame and do not cast a real or public figure at
  all. Ask once what register a figure must sit in to land here, and write the answer into the slot.
- A campaign overlay may add house casting *aesthetics* on top of `B.frame`. It may not replace it:
  if the overlay is the only place the frame exists, the frame belongs in the profile.

## 4. What to check before the note is done

- `B.distance` was read before the hook, and the branch above was applied.
- Whose nerve / which emotion / which question are all recorded, and none of them is a scene script.
- The entity is a parallel, unless the direct encounter passed the remove-the-name test.
- The figure sits inside `B.frame`, or `B.frame` was empty and nothing was cast.
- Under `close` / `self-insert`: the material sits in the GM-only location, the safety refresh is
  scheduled, and nothing in the note asserts something about the player they did not say themselves.
