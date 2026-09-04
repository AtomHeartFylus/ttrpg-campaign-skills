---
name: ttrpg-table-recap
description: "Write the in-fiction recap that is read aloud to open the next session — the previous evening retold from inside the story, in the form the campaign profile declares (prose, verse, or none). Use when asked to write, update or polish the opening recap, 'previously on', or session poem/chronicle for a session already logged. Does not record what happened (see ttrpg-session-log) or prepare the coming session (see ttrpg-session-prep)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.4"
---

# Table recap

Produces the text read aloud **at the opening of the next session**, before play starts. Its
input is the session log; its audience is the players, in character, with the lights already down.

> **P12 — fiction-only.** Everything here exists from the point of view of the *journey*, never of
> the *evening*. No mechanics, no meta, no fourth wall, no "next time on". **A scene that was
> skipped did not happen.** P12 is a *strong default*, not a law: a table that declares `P12 — off`
> in `E.overrides` gets the recap it asked for, and this skill says so instead of arguing.

---

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled in this folder.
> A complete worked recap for an **invented** campaign, annotated, is in
> [references/example-recap.md](references/example-recap.md) — read it once to calibrate posture
> and register; it is a shape, never prose to reuse. It opens the session after the one
> `ttrpg-session-log`'s example records.

## The posture

**You are writing the work, not summarising an evening.** Recap N is a chapter of a single text
that, read end to end at the close of the campaign, must stand on its own as the chronicle of this
journey. That is the standard: every line is weighed as if it had to last, not as if it had to fill
a slot before play starts.

Two consequences, in force unless `E.overrides` says otherwise:

- A recap is not a list of events with atmosphere applied on top. It selects, shapes and judges.
- Anything that only makes sense to the people in the room does not exist — not "trimmed for
  length", but outside the world.

## Phase 0 — Read the campaign profile

**Find it before declaring it missing.** Search the repo/vault root for a file named
`campaign-profile.md` (`rg --files -g campaign-profile.md`, or the equivalent), and **if that comes
back empty, search by frontmatter** (`rg -l "type: campaign-profile"`): the schema declares that
type, `ttrpg-campaign-setup` explicitly tolerates a renamed profile, and no other skill may call a
renamed profile an absent one. A profile that exists but was not found re-interviews a GM who
already answered.

| Slot | Used for | If empty |
|---|---|---|
| `D.recap` | **the form** of the recap (in-fiction prose / a verse form / none), who reads it, and the **reading-time ceiling** | if it says **none**, stop: report that this campaign declares no opening recap and offer to record the choice in `D.recap`. Never pick a form yourself. For the ceiling alone, see the branch below |
| `D.identity` | **what the text calls each protagonist** — real name, role or epithet | apply the per-character value from that player's dossier; if that is empty too, ask once and write the answer to both |
| `D.tone` | register, admitted breaks, the recurring thematic pressure | ask once for the register, then proceed |
| `D.canon_source` | quotes woven into the recap, and their status in-world | no quotes |
| `D.guide` | a figure who keeps their own name and voice | treat every NPC by the name the fiction gives them |
| `D.shape` | one-shot / series / open sandbox — see the branch below | ask once; do not assume `series` |
| `B.language` | language of player-facing text | write in the language of the notes around it — the session log first — say which you chose, and offer to record it |
| `B.size` | how many were present shapes the telling | take the roster from the log |
| `C.root`, `C.naming`, `C.frontmatter`, `C.links`, `C.verify` | path, file name, frontmatter, link syntax, verification command | write where told |
| `C.blocks` | how this vault writes the quote block the recap is delivered in | keep the role, use a plain blockquote |
| `E.overrides` | which strong defaults this table switched off — see the branch below | all defaults in force |
| `E.deliverable`, `E.review` | saved note or draft in chat; how blunt to be about a weak recap | save the note in the repo and be plainly honest |

**`E.overrides` branch — mandatory.** Read the slot before writing a line, obey it, and say once in
the output which override you honoured. Two overridable defaults reach this skill:

| Override | What stops being required here |
|---|---|
| `P12 — off` | the fiction-only rule. Mechanics, meta and "previously, at our table" are admitted; the *journey* framing above becomes optional, and the piece may address the room. Do not smuggle it back as a style note |
| `P13 — off` | the admission test on anything the recap introduces; it may name a figure or place that has not earned a note |

P1, P2, P3, P10 and P11 are **not** overridable: the recap still contains only what the fiction can
carry from the log, and the log stays the authority (P11).

**`D.shape` branch — mandatory.** `series` → as written: this recap opens the next session.
`one-shot` → **there is no next session to open, so the default output is nothing.** Say so;
produce a text only if the GM asks for a closing chronicle, and write it as an **ending** — sealed,
no thread left deliberately live — not as an opening. `open sandbox` → as written, but the recap
covers the last session *played* and may account for fronts that moved off screen. **Empty → ask
once**; do not assume a series exists to open.

If `D.recap` declares a **verse form or a house voice with specific prosody**, the prosodic rules
themselves belong to the **campaign overlay**, not here. This skill owns everything
that is true of any form; the overlay owns the metre, the rhyme scheme and the house lexicon.

## Phase 1 — Read before writing

1. **The session log** for the session being recapped (locate it by its `type: session-log`
   frontmatter when names vary). Take the narrative beats from *What actually
   happened*, **filtering out everything that belongs to the table and not to the fiction**: rewards
   handed out, dice, scenes not played, prep retrospectives, missed opportunities.
2. **The previous recaps**, most recent first. This is a continuity read, not a courtesy: the same
   figure keeps the same epithet, the register does not drift, and an image already used is either
   reprised deliberately or avoided.
3. **The player dossiers** of those present, for each protagonist's **in-fiction identity**.
   `D.identity` declares the *rule* (real name, role, or epithet); the **per-character value** lives
   in that player's dossier. Apply the rule, take the value. No value recorded → ask once and write
   it back, so recap N+1 inherits it. `D.identity` itself empty → ask which rule this campaign uses,
   before inventing epithets for a table that uses plain names.
4. **Who was present.** Absence is handled by the `B.absence` in-fiction convention — the text
   either accounts for the missing character the way the table agreed, or does not name them. It
   never says a player was away.

## Phase 2 — Write

```markdown
---
type: session-recap    <!-- fixed package key, identical in every campaign: how the next prep
                            and the audit FIND this artifact -->
<frontmatter per C.frontmatter: session tag, recap tag>
---

> [!quote] To be read aloud at the opening of Session N+1   <!-- quote block per C.blocks -->

<the recap itself, in the form declared by D.recap, in the language of B.language>

<link back to the session log, per C.links>
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

**Length ceiling: `D.recap` declares it. Read the recap aloud and time it against that value.**
The ceiling is a slot, not a constant: a thirty-second cold open and a sung chronicle are both
legitimate, and the profile is where the table says which. Past the declared ceiling attention is
gone and the opening you wanted is spent. Some forms are measured in a form-native unit instead of
minutes (a fixed number of strophes, one page); if `D.recap` gives one, time against that.

**If `D.recap` states no ceiling**, use the **`default:` the slot itself declares** (three to five
minutes) — the number belongs to the profile, not to this skill — **say in the output that you used
it**, and offer to record the table's real ceiling in the slot. The form itself is
never defaulted this way: no form, no recap.

If the log has more material than fits, cut beats; never compress every beat into a summary.

## Phase 3 — Required elements

### In-fiction identity, per `D.identity` (P12)
Protagonists are named by the rule `D.identity` declares — real name, role, epithet or
periphrasis — taking each per-character value from that player's dossier. The mapping
character → identity is **stable across recaps**; changing it silently breaks the chronicle.
NPCs and places keep the names they have in the world.

**Player names are a separate question from `D.identity`.** Where `B.distance` is `self-insert`, a
protagonist's in-fiction name may legitimately *be* the player's own — that is the campaign's
premise, not a P12 breach. What P12 forbids is naming the **person in the room as a person** ("the
player who rolled badly"). Anywhere else, or with `B.distance` empty, keep player names out.

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

### Register per `D.tone`, held all the way
The campaign's dominant register governs the whole text, including its comic moments: humour comes
from the *contrast*, delivered in the same voice, not from switching to a lighter register for a
paragraph. Admitted breaks are declared in `D.tone` — respect their limits.

### Canon quotes (`D.canon_source`), woven in
If the profile declares a canon source, a quote is **integrated into the fabric** of the recap, not
dropped in as a block that snaps the form. Let the text arrive at it, let the source speak, then
resume. One or two lines; for a longer passage take its opening and closing fragments as a frame.
Mark quotations the way the repo's conventions declare (typically italics). If `D.canon_source`
says the source does not exist in-world, quote nothing.

### The closing image seals it
End on an image or a moral weight that closes the chapter — something that stays in the room for a
second after the reading stops. Never a bridge to the coming session, never a question to players.

### If `D.recap` declares a form constraint
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
- **P12 sweep — while `E.overrides` leaves P12 in force:** no mechanics, no rewards, no system
  vocabulary, no session number in the body, no
  address to the table, no anticipation of the next session, nothing from a scene that was not
  played, and nobody referred to as a person in the room rather than a figure in the story.
- Every protagonist present is named per `D.identity`, and by the *same* identity as in earlier
  recaps; new values have been written back to the dossiers.
- The text is in `B.language`; the reading-aloud timing was checked against `D.recap`'s ceiling,
  or the fallback was used **and declared**.
- `D.shape` honoured: nothing was written to open a session that a one-shot does not have.
- Every beat in the text can be traced to the session log; nothing invented, nothing promoted from
  a scene that never happened.
- Register matches `D.tone`; the closing image closes and does not bridge.
- If `D.recap` declares a form: the form holds throughout, with no invented words and no filler lines.
- Links follow `C.links` syntax; run the `C.verify` command — invariant as declared
  (typically **0 broken links**).

## What NOT to do

- Do not summarise the evening — write the chapter.
- Do not name players, mechanics or rewards, and do not mention that a scene was skipped — unless
  `E.overrides` declares `P12 — off`, in which case say once that you are writing under it.
- Do not address the table or preview the next session, not even in the closing line (P12).
- Do not invent an epithet for a character who already has one, or drift the register between
  recaps.
- Do not explain a character's inner state that the images already carry.
- Do not inflate a player's moment into generic heroics.
- Do not choose a form the profile does not declare, and do not restate the overlay's prosody here.
- Do not let a form constraint invent a word, buy a filler line, or bend a fact from the log.
- Do not exceed the ceiling `D.recap` declares; cut beats instead of flattening all of them, and
  do not treat the fallback as the rule when the slot has a value.
- Do not invent an epithet for a table whose `D.identity` says it uses plain names.
- Do not write an opening recap for a one-shot; if asked for anything, write an ending.
