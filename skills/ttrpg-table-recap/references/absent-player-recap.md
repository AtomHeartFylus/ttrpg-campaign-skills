# Absent-player catch-up — Phase 5 detail

> **Only needed for Phase 5.** This file covers the full structure and delivery rules of the
> W23 absent-player catch-up note. The entrypoint (SKILL.md) holds the gate check and the trigger
> condition; read this file when the gate clears and you are about to write the note.

## What the note covers

Same fiction-only material as the main recap — the session log, the previous recaps — and the
same P12 constraint, unless `E.overrides` declares `P12 — off`. The audience is different: this
note tells the absent player what their character (and the world) experienced while they were
away, so they can return without an awkward retelling at the table.

**Reading a dossier for this note is narrower than for the main recap.** Take only the
`D.identity` mapping (what the text calls the character) and the fact `B.absence`'s convention
needs (e.g. "held in place at the shrine"). Everything else a dossier carries — Playstyle, Hooks,
Diary — is GM-facing by construction; the content-class gate below governs it, and the default is
**excluded**, not "trimmed for tone".

| Section | Content |
|---|---|
| Where things stand | Where the party is now and how they got there — the starting point for the returning player |
| What happened | The session's central turns, in fiction, at the scale they had in the log |
| Your character's status | The absent character's fate per the `B.absence` convention (waited at camp, held in place, chorus), stated plainly |
| Threads that moved | Arc or relationship development touching the absent character's connections, **drawn only from the log and previous recaps** — never a hook, a playstyle note, or an off-game fact surfaced to explain why it moved |

Length: enough to ground the returning player without burying them. No ceiling from `D.recap`
applies — this note is not read aloud to the table. Apply the same form `D.recap` declares
(prose stays prose, verse stays verse), but do not impose the reading-time ceiling on it.

## Content-class gate — read before writing a line

`C.player_access` and `C.gm_private` are read here as a **content-class policy**, not only a
save-location choice (that is the separate, unchanged decision in "Where to save" below). Four
classes are GM-private by construction and **excluded from this note by default**, wherever the
note ends up saved:

| Class | Normally lives at | Included only if |
|---|---|---|
| Dossier **Playstyle** notes | `C.gm_private` | `C.player_access` names playstyle notes explicitly |
| Dossier **Hooks** | `C.gm_private` | `C.player_access` names hooks explicitly |
| **Off-game note** entries | the off-game path under `C.gm_private` (only exists if `B.consent_offgame` is `yes`) | `B.consent_offgame` is `yes` for everyone quoted **and** `C.player_access` names the off-game note explicitly |
| Raw **transcript** facts | the transcript folder in `C.capture_paths` | `C.player_access` names transcripts explicitly |

`C.player_access`'s ordinary values ("player-facing reference, recaps, logs") do **not** by
themselves reach any of the four rows above — a table that lets players read recaps and logs has
said nothing about whether they may also read a dossier's Hooks section. Silence on a class means
it stays out, exactly like an unpronounced consent slot reads as *unanswered*, never as
permission (`B.consent_offgame`, `B.consent_recording` — never inferred from each other or from
the existence of a file). This is a **read**, never an inference: do not merge
`B.consent_offgame` into `C.player_access` or the reverse, and **no `E.overrides` entry reaches
this gate** — consent and privacy slots are not defaults and are never overridable (SKILL.md's
`E.overrides` branch lists what is; this is not on it).

If the session's central turn genuinely depends on GM-private material (a hook that fired, an
off-game ruling that changed something), tell the returning player what changed **in fiction**
without exposing the private fact behind it — the same discipline `ttrpg-session-prep` and
`ttrpg-table-dossier` already apply to hooks: the player makes the connection; this note does not
spell out the mechanism.

## Where to save

Read `C.player_access` before saving — a **location** decision, separate from the content-class
gate above (a correctly filtered note may still belong in chat only):

- **If players may read the repo:** save beside the session log in a file the naming convention
  (`C.naming`) supports, linked from the session log. Name it clearly (e.g.
  `Sessions/Session 7 — Catch-up — Sorrel.md`).
- **If players read nothing (the repo is GM-only):** deliver in chat only, and note in the run
  report that it cannot be saved to a shared location from here — the GM shares it manually.

In either case, the `type:` frontmatter key for this artifact is **`session-catchup`**, a distinct
package key from the main `session-recap`. The catch-up is a different, privacy-gated artifact;
sharing the recap key would make a consumer that locates artifacts by `type:` mistake it for the
opening recap.

## P12 applies here too

No mechanics, no player names, no table talk, no announcement of what comes next. The absent
character's player is the audience; the character is in the fiction.
