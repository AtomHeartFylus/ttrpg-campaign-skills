# Design principles

The invariants every skill in this package is built on. Each was paid for at a real table.
Skills **reference these by name** instead of restating them, so a lesson is fixed in one place.

> **Requirement or convention?** These principles were distilled from *one* long campaign. Treat
> **P1, P2, P3, P10, P11** as requirements: violating them produces documents that fail at the
> table or state that silently desynchronises. Treat **P5, P6, P7, P8, P9, P12** as strong house
> conventions of a fiction-first table — excellent defaults, and legitimately overridable by a
> campaign that declares the override in its profile rather than drifting away from it in silence.
> A skill must not present a convention as if it were a law of the game.

---

### P1 — Self-sufficiency of the play document

The document the GM holds during play must contain *everything* needed to run the session
— descriptions, read-aloud text, quotes, the tables and rules used *that night* — inlined.
The only admitted exception is **stat blocks**, which stay linked.

*Why:* under pressure, with a full table talking, jumping between files is not an option.
*Failure mode:* "see the module for the description" — at the table it becomes improvised filler.
*Note:* this is a deliberate exception to the general "link, don't copy" rule of a wiki-style
vault. It applies to prep documents only.

### P2 — Two levels of reminders, single source of truth

Triggers that are easy to lose in the flow live on exactly two levels:
**global threads** in a callout at the top (what must not be lost sight of *all night*), and
**scene triggers** in a checkbox box opening each scene (what is easy to forget *right here*).
No trigger appears on both levels. Any value (a DC, a cost) exists in exactly one place.

*Why:* duplication means that changing a number leaves a stale copy somewhere.
*Test:* open any scene — its box alone answers "what do I risk forgetting here?"; the top
callout alone answers "what must I keep in mind all evening?".

### P3 — Read-aloud contains only what the senses perceive

Text meant to be read to the players contains only what the characters can see, hear, smell.
Hidden truths, narrator judgements and anything the players should *discover* move into a GM
note, with an indication of how to seed the clues.

*Why:* a reveal delivered inside the read-aloud is a discovery stolen from the table.
*Test:* a GM who never read the source can run the scene from the prep alone — and the players
still have to work for what is meant to be earned.

### P4 — NPCs are subjects, not objects — proportionally

Every NPC the players interact with whose will is not obvious declares a **playable intention**:
*what it wants* (surface want, and beneath it the hidden truth when they differ) and
*how to make it respond* (what each line pushes toward; what it does if the players stall,
walk away, or contradict it). The surface want must also surface *to the players*, as a
speakable line or a described gesture.

**Scale the burden.** A full box only for NPCs whose misread will breaks a scene, or hooks that
die if they only recite a line. Type-level behaviour, not per-individual, for crowds from an
encounter table. One shared framing note, not N boxes, for a large cast of interlocutors.
Obvious motives, hazards and pure atmosphere get nothing. A deliberately will-less NPC is
marked as a choice.

*Why:* an NPC written as an object leaves the GM unable to improvise coherent reactions.

### P5 — Every scene declares its dramatic question and a non-combat exit

Each scene states: the **question** it poses that the players cannot answer instantly; what a
**rewardable moment** looks like *in this scene* (so the reward goes to choices and portrayal,
never to tactical cleverness); and the **exit condition that is not "enemy at zero HP"**
(cross, convince, endure, protect, renounce).

*Why:* the natural gravity of a table is to reward action, because action is easy to adjudicate.
*Corollary:* combat happens only when the story or the mechanics need it, and always with an
objective other than depletion, plus an explicit exit condition. Boss set-pieces earn the night;
everything else is an obstacle.

### P6 — White space is written, or it does not happen

Every session plans 1–2 explicit **conversation scenes**: no checks, no combat, no mechanical
pressure — only context and a couple of trigger questions.

*Why:* if the white space is not in the file, at the table it gets filled with combat or plot
advancement, which are easier to improvise.

### P7 — Spotlight is rotated, not shared equally

Each session has **2–3 protagonists**; the rest are chorus, rotating across sessions.
The spotlight is **distributed into the document**, never a summary table: the cross-session
arc belongs to the global callout, the per-scene focus is a marked line in that scene's box.

*Why:* with a large table, equal time means everyone gets a thin slice and nobody gets a scene.
Nobody scrolls to the bottom of the page mid-session to find out whose moment it is.

### P8 — Content margin

Prep more than one session can cover: 1–2 **optional scenes** beyond the main path, tagged as
such. The main path alone must already make a satisfying session. If an optional scene is skipped
and carried a hook, the prep says how the seed can be recovered later — or declares it lost.

### P9 — Red-team the derailments, fed by the logs

Before finishing prep, predict the **3–5 most likely derailing choices of *this* table for *this*
session**, each with a **response pressure** — never a wall, always a consequence (the enemies
*pursue*, the door *stays the only exit*, the soul *calls them by name as they leave*).
Past logs are the best predictor, so this gets sharper every session. Note recurring patterns of
your table (e.g. a group that habitually looks for the lateral, procedural solution) as standing
red-team questions.

### P10 — One source of truth for state

Every tracked value (level, resources, position, open threads) is written in **exactly one place**
— the character/entity note — and read everywhere else through a live view or a query.
Static roster tables in indexes and prep documents are forbidden: they desynchronise on the first
update. The single exception is the **exit state** section of a session log, which deliberately
freezes a historical snapshot of that night.

### P11 — The cycle is closed, and the log is the authority

`prep → play → log → recap → next prep`. What does not make it into the log is lost within a month.
The log is the input of the recap and of the following prep. Recordings and transcripts are memory
aids, **not minutes**: names and campaign terms come out mangled, speaker turns are unreliable.
On divergence, the log wins.

### P12 — Fiction-only in player-facing text

Anything read to the table exists from the point of view of the *journey*, never of the *evening*:
no mechanics, no meta, no fourth wall, no "next time on". A skipped scene did not happen.

*Test:* does this sentence exist for the characters, or only for the people in the room?

---

## Using these in a skill

- Cite as `P4 (NPCs as subjects)` — do not restate the rationale.
- A skill that needs an exception to a principle must say so explicitly and why
  (as `ttrpg-session-prep` does for P1 vs. link-don't-copy).
- If a lesson from play generalises across campaigns, it belongs **here** and the skills reference
  it. If it only holds for one campaign, it belongs in that campaign's profile or overlay.
