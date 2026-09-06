# Running the interview

Companion to Phase 2 of `SKILL.md`. **This file does not list the slots either.** The slot list is
`references/campaign-profile.md` and nowhere else; what follows is how to *walk* it without losing
a GM's patience or their answers.

---

## The walk

- **One pass, in schema order.** Read the bundled schema, then move down it. Reordering feels
  helpful and is not: the schema is ordered so that later answers depend on earlier ones (what the
  rules adjudicate before what the resource does; how close the players sit to their characters
  before what may be harvested about them).
- **3–5 adjacent slots per message.** One slot per message is an interrogation; a whole section at
  once produces one paragraph that answers two slots and silently drops four.
- **Ask with the schema's own words.** Each slot carries an explanatory line written for this
  purpose. Paraphrasing it is how a slot quietly turns into a different question.
- **Record in the GM's vocabulary.** If they say "grit", the slot says grit, not "dramatic
  resource". Downstream skills speak slot ids; the *values* stay in the table's language.
- **Never fill a slot the GM did not answer.** `none` is a real answer and a load-bearing one; a
  plausible invention is a silent bug that surfaces three sessions later.
- **Close with a diff.** Slot ids in the schema, minus slot ids in your filled profile, equals the
  slots you forgot. Run it literally — this is a set difference, not an impression.

## When the GM answers in paragraphs

Most GMs answer four slots in one enthusiastic paragraph and skip the fifth.

1. Split the paragraph into the slots it actually answered, and quote each answer back beside its
   slot id.
2. Name what it did **not** answer, then ask only those.
3. Do not credit a slot from tone. "It's pretty grim" is a `D.tone` answer; it is not a
   `D.endgame`, a `B.safety` or an `A.fiction` answer, however grim.

An inferred value must be confirmed before it is written. "I read your pitch as X — is that right?"
costs one line and prevents a profile that quietly describes a campaign nobody is running.

## Depth: what to press on, section by section

- **§A (game).** Push past the ruleset name to what the rules *decide* and what is deliberately
  never rolled for — that boundary is what makes prep either sharp or a list of numbers. If a dramatic
  resource exists, this is where GMs under-specify most; see the asymmetry rule below. If none
  exists, say `none` once and stop offering to invent one.
- **§B (table).** The three slots the rest of the package branches on live here (`B.distance`,
  `B.consent_recording`, plus the size/protagonist pair that fixes rotation). Ask for numbers, not
  adjectives: "five players, two carry a session" is usable, "a big group" is not.
- **§C (repository).** Half of it is observation, half is decision. Every answer must be concrete
  enough to act on without a follow-up question: a path, a syntax written literally, a command that
  runs. "We use standard wiki links" is not an answer to a link-syntax slot; the exact bracket form,
  with an alias and an embedded attachment, is.
- **§D (shape and content).** The shape slot is asked *first* in this section and its consequences
  stated out loud (see SKILL.md). Endgame is asked even when the campaign has just started: endings
  are selected by seeds planted early, so an unasked endgame slot is a campaign that cannot plant
  them.
- **§E (agreements and overrides).** GMs rarely volunteer these; offer the shape of an answer. The
  overrides slot in particular: read the strong defaults out and ask which ones this table does not
  want. `none` is common and legitimate — blank is not, because blank reads as "never asked". A GM
  who has never seen the package applied has nothing to judge these against yet, so read out what
  each one costs on and off — one line each, so "none" is a choice and not a shrug:
  - `P4` (NPC intentions) — **on:** any NPC whose will is not obvious gets a stated want, proportional
    to their weight. **off:** NPCs may stay pure obstacles or scenery.
  - `P5` (scene question + non-combat exit) — **on:** every scene states its dramatic question and a
    way out that is not combat. **off:** scenes may run with neither stated — closer to pure
    tactical play.
  - `P6` (white space) — **on:** prep plans 1–2 explicit no-mechanics conversation scenes per
    session. **off:** no dedicated non-mechanical scene is required.
  - `P7` (spotlight rotation) — **on:** `B.protagonists` sets who is in focus each session, rotating
    so nobody stays chorus forever. **off:** e.g. every player is a protagonist every session by
    design — no rotation is tracked.
  - `P8` (content margin) — **on:** prep carries 1–2 optional scenes beyond the main path. **off:**
    the main path only, no margin content required.
  - `P9` (red-team) — **on:** prep predicts 3–5 likely derailing choices, each with a response
    pressure. **off:** no derailment-prediction section required.
  - `P12` (fiction-only player-facing text) — **on:** the recap and other player-facing text stay
    strictly in-fiction — no mechanics, no meta, no fourth wall. **off:** the table wants a
    behind-the-scenes register in what players read.
  - `P13` (admission test) — **on:** a new NPC, place, faction or object answers why-here /
    why-now / what-changes before entering play. **off:** elements may enter without that test —
    faster improv, more consistency risk.

## The asymmetry question

For anything with an economy — a resource, a favour, a reputation, a debt — ask explicitly:

> **Who may hold it, who may give it, and who structurally *cannot* receive it?**

The lesson: a table spent a session's emotional climax donating a resource to recipients who were
mechanically incapable of receiving it, because the rule lived in a second rulebook and nowhere in
the repo. The GM knew the rule and did not think to state it. Nobody asks this without a prompt;
this is the prompt.

Ask the same three questions of the zero state and the recovery triggers: what happens at zero, how
often it can happen, and whether recovery is a rule or a favour.

## Wording for the gating slots

**`B.distance`.** Do not ask it as a taxonomy question, ask it as a fact:

> "Are the characters the players themselves under their own names, people close to them, or
> invented characters? I ask because it changes what I am allowed to write: if the characters are
> the players, a hook I harvest about a character is aimed at a real person, and a GM note about a
> player is a note about someone who is in the room."

Record the answer, and record any qualification the GM adds ("themselves but ten years younger") —
that qualification is what the hook-harvesting skills need.

**`B.consent_recording`.** Ask for a sentence, not a nod:

> "Is the table recorded, and has everyone at it — including anyone who drops in — actually said
> yes? I need the answer as words someone said, not as an inference."

Then write the token first and exactly what you were told after it — `**yes** — <their sentence>`,
or `**no** — <what is missing>`. The token is the same word whatever language the table speaks
(the schema's `B.consent_recording` line says why); the sentence stays in theirs, verbatim, because
it is the half that says *who* agreed and to *what*. If the answer is "I've always recorded and
nobody minded", that is `no` until they are asked. Do not fill the capture-path slots, and say plainly that the
audio pipeline stays off until the slot says yes. There is no version of this where guessing is
the cheap option.

**`B.consent_offgame`.** A separate question, asked of the same people, never inferred from the
first:

> "Separately from recording: may the out-of-character half of the evening become a durable,
> themed, timecoded note about what people said as themselves? Everyone present has to say yes,
> and any of them can have any entry deleted later without giving a reason."

A `yes` to recording is not a `yes` to this. Silence, "probably fine" and last session's answer are
all `no`. Write it in the same form as the slot above — token, then what you were told, verbatim if
it was qualified.

**`D.shape`.** Ask, then state the consequences before moving on — one-shot switches whole skills
off, sandbox reshapes what the arc note holds. A GM who hears this at interview time chooses
deliberately; a GM who discovers it in session three thinks the package is broken.

## Failure modes seen in practice

- The slot list gets summarised into the agent's plan and the walk follows the summary. Every slot
  added to the schema after that summary was written is never asked. This is the exact bug this
  skill was rebuilt to kill.
- A section is skipped because the GM "clearly does not care about it" — and the profile then has
  blanks that read downstream as *never asked*, so every skill stops and asks anyway.
- Answers are recorded in the package's vocabulary instead of the table's, and the GM stops
  recognising their own campaign in the profile.
- The interview produces a beautiful essay in chat and no file. The deliverable is the file.
