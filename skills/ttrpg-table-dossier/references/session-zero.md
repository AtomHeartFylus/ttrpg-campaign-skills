# Session zero

Read this when a campaign is starting, when a new player joins, or when an unsettled question from
the original session zero has to be reopened. Everything else in `SKILL.md` runs far more often
than this does.

Session zero is not a rules briefing. It is **seven decisions**, each of which must end as a written
profile slot or a dossier section — not as something everyone remembers agreeing to.

---

## The agenda

```markdown
0. Distance           — self-insert | close | fictional: how far the characters sit from the
                        players. Write into B.distance. FIRST, because it changes 3 and 6.
1. Expectations       — what each player wants from this campaign, said out loud, one sentence each
                        (combat, puzzle, drama, comedy, exploration, "I want to be pushed").
                        Record the mismatches: they are the real agenda of the campaign.
2. Tone contract      — the dominant register, the admitted breaks, and what would break it
                        for real (D.tone). Name the heavy themes the campaign will touch.
3. Safety tools       — which tool, who may call it, what happens after it is called, and
                        the refresh cadence. Write into B.safety.
4. Repo access        — what players may read: player-facing reference, recaps, logs, nothing.
                        Write into C.player_access; it decides where GM-facing notes may live,
                        which is C.gm_private.
5. Attendance         — the in-fiction convention for absent players, and whether they advance.
                        Write into B.absence. Decide it now, not the first night someone is out.
6. Hook harvest       — the direct questions that fill each dossier's hooks section.
                        This is the only part that must be done per player, on the record.
```

## Distance — decided first, because it changes the rest

**`B.distance` is asked before anything else is harvested.** It has three values and they are not
degrees of the same thing:

- **`fictional`** — the players portray invented people. Hooks are facts about characters.
- **`close`** — the characters are thin screens over the players: same profession, same city, same
  history with the serial numbers filed off.
- **`self-insert`** — the players portray **themselves, under their own names**. Hooks are real
  people they know and real things that happened to them.

For `close` and `self-insert`, three consequences are **load-bearing, not optional**:

1. **The safety conversation is mandatory and recurring.** Not a formality at session zero: the
   refresh happens again before any arc the tone slot flags as heavy, and before any session built
   on a harvested hook. There is no fictional layer to absorb a scene that goes wrong.
2. **The hook harvest is a consent conversation, not a questionnaire.** Ask what they are willing
   to have the campaign press on — and record, just as explicitly, what is **off the table**. A
   player may withdraw a hook at any time, without giving a reason, and it is removed.
3. **Everything written about them is written knowing they may read it.** Hooks and playstyle notes
   go to `C.gm_private`. They are not softened — they are relocated. Material aimed at a character
   is aimed at a person.

**If `B.distance` is empty, ask. Do not assume `fictional`** — that is the cheap default and the
one that treats a named human's exposed nerve as set dressing. One question at session zero costs
nothing; the wrong assumption cannot be walked back once a scene has landed.

Session zero produces text in **two registers**: what is agreed *with* the table goes into the
profile slots; what you observe *about* each human goes into their dossier, GM-facing.

## Expectations, and the mismatches

Ask for one sentence each and write them down verbatim. The value is not the list — it is where two
players want incompatible things (one wants tactical challenge, one wants to be emotionally
wrecked). Those pairs are what the spotlight budget and the tone contract have to hold together all
campaign; unwritten, they surface as friction that looks personal.

## Tone contract

Fix the dominant register and the breaks it admits (`D.tone`). Then ask the harder question:
*what would break it for real* — the joke, the register, the kind of scene that would make this
campaign stop being the thing they signed up for. Name the heavy themes explicitly; a theme named
in advance is a theme the table consented to.

## Safety tools and their refresh

Record in `B.safety`:

- **which tool**, and how it is invoked;
- **who may invoke it** — everyone, without justifying themselves;
- **what the table does** when it is invoked (rewind, cut, move on), decided in advance rather than
  negotiated in the moment;
- **when it is refreshed:** at session zero, when a new player joins, and *before* any arc the
  profile's tone flags as heavy.

Refresh it out loud even when nobody has ever used it — the lesson of tables where the tool existed
on paper for a year and no player remembered they were allowed to call it. **When `D.tone` declares
heavy themes, or `B.distance` is `close` or `self-insert`, this conversation and its refresh are
mandatory, not optional** — see *Distance* above.

## Repo access

Decide what players may read (`C.player_access`): the player-facing reference, the recaps, the logs,
or nothing. This single answer decides where GM-facing material may live — including the playstyle
notes, which must never be softened to survive being read. If players read the repo,
`C.gm_private` must also be filled in; a skill may never improvise that location.

## Attendance

Agree **once** on one in-fiction explanation covering any absent player: a place they stayed behind
at, a task that keeps them elsewhere, a state they lapse into. It must cost nothing to narrate, be
reversible without ceremony, and never read as a punishment. Decide in the same breath whether
absentees advance, and write both into `B.absence`.

## Hook harvest

The only per-player, on-the-record part, and the one gated on *Distance* above. Ask directly for the
number `B.hooks_count` declares (default 2–3) of people, obligations or unfinished pieces of their
character's life tied to whatever the campaign will press on, in the profile's own terms. Record the
figure or fact in the player's words, the emotion it is meant to provoke, and the question it lets
you put to them. Under `close` / `self-insert`, also record what is **off the table**, and store the
whole thing where `C.gm_private` says. The full rules for what a hook is — and is not — are in
`SKILL.md`, *Hooks are harvested, never hoped for*; which real or public figures may be cast from a
hook is `B.frame`, read by `ttrpg-entity-note`.

## Closing the session zero

Before the table disperses, every one of the seven decisions exists as text in the repo. A decision
that stayed in conversation was not made: three sessions later two people remember it differently,
and the one who is wrong is usually the GM.

## Beyond session zero: a new player, a dead PC, a player who leaves

Three events short of a full session zero, each with its own note discipline.

### A new player joins mid-campaign
This is a **partial** session zero, on the new person alone — do not reopen the settled decisions
for a table that already made them.

- **What they read first** is whatever `C.player_access` already permits everyone else: the recap
  (`ttrpg-table-recap`) and the player-facing reference, never the GM-facing dossiers, hub or prep.
  If `C.player_access` says players read nothing, say so plainly and brief them out of band — do
  not hand them a file the rest of the table cannot read either.
- **How the new PC hooks in:** harvest their hooks exactly as *Hook harvest* above (gated on
  `B.distance`, same consent rules if `close` / `self-insert`), write the new dossier, and add **one
  line for the next `ttrpg-session-prep` or `ttrpg-campaign-arc` pass**: this player is now part of
  the rotation and is owed a scene built on one of their fresh hooks. Do not silently fold them into
  the ambient cast — an unscheduled newcomer is chorus by default.
- **`B.size` gets written back, not just noticed.** A new player changes the number the rotation
  formula (`B.size` / `B.protagonists`) actually divides by. Update `B.size` in
  `campaign-profile.md` itself as part of onboarding — this is a fact about the table, not a
  judgement call to defer — and say so plainly. A rotation period computed against the old count
  is quietly wrong from this session forward, and nothing else in the package checks `B.size`
  against the actual roster.
- **Consent, re-checked, not re-explained:** if `B.consent_recording` or `B.consent_offgame` are in
  force, `ttrpg-session-audio` already refreshes them for anyone newly present — point there,
  do not restate its gate here.

### A PC dies or retires
**The dossier stays open: it belongs to the player, never the character** (the note's own opening
rule). Close only the `## Character` section that ends: append the date and the session log where
it happened, so the record of *why* survives in one place. Open a **new** `## Character` section
for whatever they play next, immediately below the closed one — same dossier, same Diary, same
playstyle notes, because all three are about the player, not the departed PC. A death is not a
reason to touch `B.distance`, `B.safety` or the rotation ledger; none of the three cares which body
the player is currently occupying.

### A player leaves the table
Close the dossier itself: date it, and say in one line why (if the table wants that recorded at
all — it is theirs to decline). It is not deleted on departure. What happens to its GM-facing
material afterward — the playstyle notes and harvested hooks about a person no longer at the table
— is exactly what `B.retention` already governs for everyone; `ttrpg-continuity-audit` checks a
closed dossier against that rule the same as an open one. A closed dossier drops out of the
rotation ledger from its closing session forward — it does not distort `B.size` retroactively.
