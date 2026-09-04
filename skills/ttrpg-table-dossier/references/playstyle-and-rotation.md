# Playstyle notes, spotlight rotation and attendance

Read this while writing the GM-facing half of a dossier or running the rotation check.
`SKILL.md` owns the profile slots, the distance gate and the dossier skeleton; this file owns the
three sections that carry the most craft.

> **The rotation formula, its tolerance and the ledger are defined HERE and nowhere else in the
> package.** `ttrpg-campaign-arc` commits who is protagonist next and cites this check;
> `ttrpg-session-log` records who carried a moment and states no number. If you find a second
> threshold anywhere, it is a bug \u2014 this one wins.

---

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

**Where it lives** depends on `C.player_access`. If players may read the repo, playstyle notes go
in the `C.gm_private` location — a private folder, a separate repo — and the dossier links to them.
Never soften the notes to make them safe to read; move them instead. Under `close` /
`self-insert` these are craft notes about a person under their own name: relocation is not
optional, and `C.gm_private` empty while players have access → stop and ask.

### Spotlight rotation — **this skill owns the formula, the tolerance and the ledger** (P7)
This is the **single** definition in the package. `ttrpg-campaign-arc` commits *who* is protagonist
next and cites this check; `ttrpg-session-log` records who carried a moment and states no number.
Neither restates the arithmetic, and neither keeps a second tally — two tallies from two sources
drift, and nobody updates the second one.

- **One derivation: the dossier diaries.** Each dossier's Diary says which sessions that player
  carried; count from there and nowhere else. **No spotlight table** anywhere, and no parallel
  count from the logs — the logs feed the diaries, the diaries feed this (P10).
- **The formula:** the rotation period is **`B.size / B.protagonists` sessions** — the number of
  sessions after which everyone has carried one. Both are profile slots; **no constant may be
  substituted for either**, and a table that makes everyone a protagonist every session says so in
  `E.overrides` (`P7 — off`) and this check does not run.
- **One tolerance: 1.5×.** Flag a player who has been chorus for more than **1.5 × the rotation
  period** consecutive sessions. That single number is the answer to *has anyone been chorus too
  long?* — below it is inside tolerance, above it is a finding. Nothing else in the package may
  state a competing threshold.
- **Either slot empty → ask for it once and write it back.** Do not run the check on a guessed
  table size, and do not fall back to a hardcoded protagonist count.
- **Qualitative alarms**, which fire before the arithmetic does and do not wait for the tolerance:
  their last diary entries are all reactions to other people's scenes; they have no quoted line in
  the last two logs; they stopped proposing; they are the one who fills silences with jokes rather
  than choices.
- **The fix is a named commitment**, not good intentions: hand `ttrpg-campaign-arc` the name, and
  it schedules which upcoming chapter or front that player carries and on which hook. The lesson of
  the player who was chorus four sessions running, stopped proposing anything, and had to be
  re-recruited to the campaign after having never once complained.
- **`D.shape` = `one-shot`:** the rotation does not exist. Run the within-session check instead —
  every player gets one scene whose outcome depends on them.

### Attendance convention (`B.absence`)
Apply what `B.absence` declares: one in-fiction explanation for absent players, agreed once and used
without negotiation, plus the rule on whether absentees advance. Deciding either in the moment turns
attendance into a negotiation and absence into a grievance. If the slot is empty, ask once and
write it back — the requirements a good convention must meet are in
[session-zero.md](session-zero.md). `D.shape` = `one-shot`: skip it.


---

## Phase 3bis — Updating dossiers after play

**`ttrpg-session-log` owns this step.** It is the authority on what happened (P11) and its state
phase already specifies which properties move, that only players present advance (per `B.absence`),
and that new hooks and playstyle changes get written. Do not re-interview the GM, do not restate
that procedure: take the finished log as input. What this skill adds afterwards:

- **Register of the diary entry:** GM-facing and concrete — the choice they made, what it cost
  them, what they now carry. Not a summary of the session (the log is that), not praise.
- **Hook lifecycle:** mark which hook fired and how it landed; keep unfired ones visibly open; an
  obligation the character took on is a new hook, recorded as one.
- **Playstyle discipline:** revise **only when the table surprised you**, dating the move to its
  session. A section rewritten every week stops recording anything.
- **Spotlight ledger:** no separate bookkeeping — the diary entry **is** the ledger. Run the
  rotation check at `E.audit_cadence`, or every few sessions, not every week.

