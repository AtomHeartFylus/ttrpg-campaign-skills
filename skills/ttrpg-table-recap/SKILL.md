---
name: ttrpg-table-recap
description: "Write the in-fiction recap that is read aloud to open the next session — the previous evening retold from inside the story, in the form the campaign profile declares (prose, verse, or none). Use when asked to write, update or polish the opening recap, 'previously on', or session poem/chronicle for a session already logged. Covers the authorial posture, the fiction-only rules, naming characters by their in-fiction identity, continuity of epithets and register with earlier recaps, integrating canon quotes, form constraints, and the reading-aloud length ceiling. Does not record what happened (see ttrpg-session-log) or prepare the coming session (see ttrpg-session-prep)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Table recap

Produces the text read aloud **at the opening of the next session**, before play starts. Its
input is the session log; its audience is the players, in character, with the lights already down.

> **P12 — fiction-only.** Everything here exists from the point of view of the *journey*, never of
> the *evening*. No mechanics, no meta, no fourth wall, no "next time on". **A scene that was
> skipped did not happen.**

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## The posture

**You are writing the work, not summarising an evening.** Recap N is a chapter of a single text
that, read end to end at the close of the campaign, must stand on its own as the chronicle of this
journey — with the player characters as its protagonists. That is the standard to write against:
every line is weighed as if it had to last, not as if it had to fill a slot before play starts.

Two consequences, both non-negotiable:

- A recap is not a list of events with atmosphere applied on top. It selects, shapes and judges.
- Anything that only makes sense to the people in the room does not exist. It is not "trimmed for
  length"; it is outside the world.

## Phase 0 — Read the campaign profile

| Slot | Used for | If empty |
|---|---|---|
| §8 Player-facing outputs | **the form** of the recap: in-fiction prose / a verse form / none; who reads it | if it says **none**, stop: report that this campaign declares no opening recap and offer to record the choice in §8. Never pick a form yourself |
| §3 Tone | register, admitted breaks, the recurring thematic pressure | ask once for the register, then proceed |
| §4 Canon source | quotes woven into the recap, and their status in-world | no quotes |
| §5 Recurring guide | a figure who keeps their own name and voice | treat every NPC by the name the fiction gives them |
| §7 Table conventions | language of player-facing text; table size (how many were present shapes the telling) | write in the language of the log |
| §9 Repo conventions | path, file name, frontmatter, link syntax, verification command | write where told |

If §8 declares a **verse form or a house voice with specific prosody**, the prosodic rules
themselves belong to the **campaign overlay**, not here. This skill owns everything
that is true of any form; the overlay owns the metre, the rhyme scheme and the house lexicon.

## Phase 1 — Read before writing

1. **The session log** for the session being recapped. Take the narrative beats from *What
   actually happened*, **filtering out everything that belongs to the table and not to the
   fiction**: rewards handed out, dice, scenes not played, prep retrospectives, missed
   opportunities.
2. **The previous recaps**, most recent first. This is a continuity read, not a courtesy: the same
   figure keeps the same epithet, the register does not drift, and an image already used is either
   reprised deliberately or avoided.
3. **The player dossiers** of those present, for each character's **in-fiction identity** — the
   name, title or epithet by which the text will call them. If a character has none recorded,
   ask for it once and write it back to the dossier so recap N+1 inherits it.
4. **Who was present.** Absence is handled by the §7 in-fiction convention — the text either
   accounts for the missing character the way the table agreed, or does not name them. It never
   says a player was away.

## Phase 2 — Write

```markdown
---
<frontmatter per §9: session tag, recap tag>
---

> [!quote] To be read aloud at the opening of Session N+1

<the recap itself, in the form declared by §8>

<link back to the session log, per §9>
```

Suggested shape of the telling — adapt, do not pad to fill it:

| Beat | Weight |
|---|---|
| Opening: where they are, how they got there | short |
| The first movement of the evening | short |
| Individual moments worth commemorating | one small unit each |
| The central turn (the confrontation, the choice, the loss) | the longest passage |
| A death, a transformation, an arrival | its own passage |
| Closing: the passage onward, sealed by a final image | short |

**Length ceiling: read it aloud and time it.** The recap has to hold a table that has not started
playing yet — past roughly three to five minutes, attention is gone and the opening you wanted to
create is spent. If the log has more material than fits, cut beats; never compress every beat into
a summary.

## Phase 3 — Required elements

### In-fiction identity, never player names (P12)
Protagonists are named by the identity the fiction gives them — a name, a title, an epithet, a
periphrasis. Player names never appear. NPCs and places keep the names they have in the world.
The mapping character → epithet is **stable across recaps**; changing it silently breaks the
chronicle.

### The fourth wall stays closed (P12)
No address to the table, no announcement of what comes next. The future may exist only as
*geography or dread inside the world* ("what waits beyond the next threshold"), never as a
programme. No mechanics, no session numbering inside the text, no "we didn't get to that part".

### Show, do not explain
The listener makes the connection. Render the gesture, the image, the silence — not the
psychological gloss on it. A character who refuses to believe what they see is written as someone
looking straight through it, not as "he refused to believe".

### Commemorate without inflating
Player moments are honoured at the scale they actually had. Keep them physical and specific;
resist the upgrade into generic heroics. The concrete, slightly ugly version of a feat is worth
more than the polished epic version, and it is the one the player recognises.

### Register per §3, held all the way
The campaign's dominant register governs the whole text, including its comic moments: humour comes
from the *contrast*, delivered in the same voice, not from switching to a lighter register for a
paragraph. Admitted breaks are declared in §3 — respect their limits.

### Canon quotes (§4), woven in
If the profile declares a canon source, a quote is **integrated into the fabric** of the recap, not
dropped in as a block that snaps the form. Let the text arrive at it, let the source speak, then
resume. One or two lines; for a longer passage take its opening and closing fragments as a frame.
Mark quotations the way §9 declares (typically italics). If §4 says the source does not exist
in-world, quote nothing.

### The closing image seals it
End on an image or a moral weight that closes the chapter — something that stays in the room for
a second after the reading stops. Never a bridge to the coming session, never a question to the
players.

### If §8 declares a form constraint
Whatever the form (a metre, a rhyme scheme, a fixed strophe, a house voice), apply these tests —
the prosody itself lives in the overlay:

- **The ear is the judge, not arithmetic.** Read every line aloud. If it scans by counting but
  stumbles when spoken, it is wrong. Approximation that sounds right beats exactness that does not.
- **Never invent a word, a name or a spelling to satisfy the form.** If the constraint cannot be
  met with real language, rewrite the sentence.
- **No filler.** A line whose only job is to complete a scheme is cut, and the passage rebuilt.
  The form must never buy itself a line that says nothing.
- **The constraint may not distort a fact.** Bending an event so it fits the form makes the recap
  contradict the log, which is the authority (P11).
- **Consistency is part of the form:** the scheme, the closing device and the strophe length behave
  the same way in every recap of the campaign.

## Phase 4 — Verify

- Read the whole text aloud, end to end, timed. Anything that trips the tongue is rewritten.
- **P12 sweep:** no mechanics, no rewards, no system vocabulary, no player names, no session number in the body,
  no address to the table, no anticipation of the next session, nothing from a scene that was not
  played.
- Every protagonist present is named by their in-fiction identity, and by the *same* identity as in
  earlier recaps; new epithets have been written back to the dossiers.
- Every beat in the text can be traced to the session log; nothing invented, nothing promoted from
  a scene that never happened.
- Register matches §3; the closing image closes and does not bridge.
- If §8 declares a form: the form holds throughout, with no invented words and no filler lines.
- Links follow §9 syntax; run the profile's verification command — invariant as declared
  (typically **0 broken links**).

## What NOT to do

- Do not summarise the evening — write the chapter.
- Do not name players, mechanics or rewards; do not mention that a scene was skipped.
- Do not address the table or preview the next session, not even in the closing line.
- Do not invent an epithet for a character who already has one, or drift the register between
  recaps.
- Do not explain a character's inner state that the images already carry.
- Do not inflate a player's moment into generic heroics.
- Do not choose a form the profile does not declare, and do not restate the overlay's prosody here.
- Do not let a form constraint invent a word, buy a filler line, or bend a fact from the log.
- Do not exceed the reading-aloud ceiling; cut beats instead of flattening all of them.
