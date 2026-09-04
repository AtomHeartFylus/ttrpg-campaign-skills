# Arc elements in full

Read this while writing or revising the arc note. `SKILL.md` owns the gate, the profile slots
and the mandatory skeleton; this file owns how each section of that skeleton is built.

**It does not own the spotlight.** `ttrpg-table-dossier` owns the rotation formula, the tolerance
and the per-player ledger; the arc note carries only the forward commitment, which stays in
`SKILL.md` because that boundary is the thing most easily violated.

---

### The backbone table (`D.backbone`)
One row per chapter, region or front. Columns carry weight:

- **Sessions (range)**, never an exact number. A chapter that "takes 3 sessions" takes 2 or 5. The
  range is the contract; the row also names **what falls first** if it runs long (P8 at arc scale).
- **What it must deliver** — the *function* of the chapter, not its content: the reveal that must
  land, the relationship that must change, the capability the party must gain, the question that
  must be forced. Content is prep's problem; if a chapter has no function, it is filler and either
  gets one or gets cut.
- **Tone shift** — where the register changes and what it changes *to* (`D.tone`). A campaign that
  stays at one intensity for twenty sessions has no climax, only a plateau.
- **Resource curve** (`A.resource`) — where the dramatic resource must be at its lowest and where
  it can be regained. Pressure that never eases stops being felt. Drop this column if the slot is
  empty.

**Sandbox rows are fronts** (`D.shape` = `open sandbox`, or `D.backbone` declaring no backbone):
a pressure, who drives it, what happens if the party never intervenes, and the visible sign it has
advanced. Same columns otherwise. Never invent a linear plot for a table that chose a sandbox.

### The deviation ledger (`D.canon_source`, `D.deviation_policy`)
**Every deliberate divergence from the source is recorded with its reason.** Not for bookkeeping:
the divergence is what future prep must stay consistent with, and a divergence remembered only in
the GM's head becomes a contradiction three months later, at the table, in front of everyone.

Each entry states what the source says, what this campaign does instead, **why**, and **what it
binds downstream** — the consequences now locked in (an NPC who cannot appear, a secret that no
longer exists, a rule inverted for the whole campaign). Entries are append-only and dated by
session; reversing a deviation is a new entry, not an edit. Drop this section only if
`D.canon_source` and `D.official_material` both declare no source material — a fully homebrew
campaign has no source to deviate from, and an empty ledger is not a finding.

### The open-thread tracker (P11)
Fed by the session logs, not by memory. One row per live promise, with four fields that are all
mandatory:

- **Seeded in** — link to the log where it entered the fiction. If you cannot cite it, the table
  never actually saw it: it is an idea, not a thread.
- **Owner** — which PC or NPC carries it. A thread nobody owns is not going to come back.
- **What would pay it off** — the concrete scene or revelation that closes it. Without this the
  thread cannot be scheduled, only worried about.
- **Status** — *alive* / *paid (link the log)* / *lost*. **"Lost" is a legitimate, deliberate
  status**: declaring a seed dead is planning; letting it rot unlisted is drift.

At every arc pass, decide each *alive* thread: schedule it into a backbone row, or declare it lost.
`ttrpg-continuity-audit` finds and reports dangling threads; **the decision is made here.**


### Pacing over the horizon (`B.cadence`, `B.horizon`)
Cadence × horizon gives the real session budget. Say it out loud in the note, then check the
backbone against it: a backbone that needs 40 sessions on a 20-session horizon is a plan to end the
campaign in the middle, and the cut is decided **now**, not by exhaustion later.

Plan explicitly: where the register shifts (`D.tone`), where the **quiet session** goes (P6 at arc
scale — a whole low-pressure session is legitimate and must be scheduled or it will never happen),
where the resource curve bottoms out (`A.resource`), and which chapters are compressible if
attendance collapses or the horizon shortens.

### The endgame, seeded early
Decide the endgame while there is still time to seed it. Record:

- **The final beats** — the two or three images the campaign is built to arrive at.
- **What must already exist** for them to land: which entity, promise or object must be planted,
  and **in which session** it is planted. Write those seeds into the backbone rows as delivery
  requirements, not as hopes.
- **The conditions that select between endings** — the states of the world the players' choices
  actually control, so the ending is earned rather than chosen by the GM at the last minute.
- **The recurring guide's resolution** (`D.guide`), if the profile declares one.
- **What is deliberately left open** — mark it as a choice, so a later pass does not "fix" it.

A finale improvised in the last session is a finale nobody was allowed to affect.

