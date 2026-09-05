# Privacy: what these skills write about real people

This package is not a text generator with a tabletop theme. Four of its nine skills write
**material about the actual humans at your table** — how they play, what they are afraid of,
what they said out of character, and, if you record, what their voice did for four hours. That
material is durable, greppable and shared with whatever model you point at the repo.

This file states what the package promises, what it refuses, and what it leaves to you. It is
part of the contract, not a disclaimer: every rule below is enforced by a slot, a gate or a check.

---

## The material at issue

| Written by | Artifact | About |
|---|---|---|
| `ttrpg-table-dossier` | player dossier (`type: dossier`) | one real person: playstyle, harvested hooks, tracked values, attendance |
| `ttrpg-session-audio` | transcript, speaker map, off-game note | everything said in the room, in-character and not |
| `ttrpg-session-prep` | GM notes on a scene aimed at a player | a real nerve, when `B.distance` is `close` or `self-insert` |
| `ttrpg-session-log` | session log | who was there, what they did, what they were given |

## The rules the package enforces

**Consent is two gates, not one.** `B.consent_recording` authorises capture. `B.consent_offgame`
authorises *curation of out-of-character talk into a durable, themed, timecoded note*. Agreeing to
be recorded is not agreeing to be indexed, so neither gate is ever inferred from the other, from
the existence of an audio file, or from a folder that happens to exist. Empty or `no` on the first
one stops the pipeline; on the second, the transcript is produced and the off-game note simply is
not written.

**Consent is not a default, so it cannot be overridden.** `E.overrides` reaches strong defaults
(P4…P13, minus the non-overridable ones); it never reaches `B.consent_*`, `B.safety`,
`B.retention` or `B.frame`. There is no configuration of this package in which a safety tool is
switched off by silence: a `none` nobody pronounced reads as *unanswered*, and
`scripts/validate_profile.py` fails the profile that tries it (`CONSENT-STATE`).

**Distance decides what may be aimed at a person.** `B.distance` has three values and every
hook-using skill branches on them. At `self-insert`, material aimed at a character is aimed at a
human under their own name: no reveal about a player the player did not author, a written
off-ramp for any scene built on a hook, and a safety refresh before the session rather than a
memory of session zero. Empty means *ask*, never *assume fictional*.

**Retention is declared, not assumed.** `B.retention` says how long GM-facing material about real
people is kept and who can trigger a deletion. With the slot empty, a skill writing such material
must say out loud that it is keeping it indefinitely and offer to set the rule. **Anyone described
may have any entry removed on request, without discussion** — which is why off-game entries are
short pointers with timecodes and never reproductions: a pointer can be deleted, a quotation has
already been copied.

**Reach is a consent question, not a layout one.** `C.player_access` says what players may read
and `C.gm_private` says where GM-only material lives; `C.capture_paths` only supplies paths that
obey them. When they disagree, the access rule wins and the skill stops and asks — and a profile
that opens the repo to players without declaring a GM-private home fails validation (`CROSS-SLOT`).

**Every run says what it did (P14).** A skill closes its reply with which consent gates it
checked, which inputs were missing, which commands it ran and what they actually returned. It is
how "the off-game note was not written because `B.consent_offgame` says no" becomes visible
instead of being a silence you have to notice.

**Nothing leaves the repo.** No skill uploads, publishes, syncs or posts. Everything is a file in
a folder you control; `C.portability` records how that folder reaches your other machines. Raw
audio lives in a version-control-ignored folder by construction.

## What the package does *not* protect you from

- **The model you point at it.** These are instructions for an agent, and the agent runs on
  someone's infrastructure. A dossier read by a hosted model has been sent to that provider.
  Choose the model for the material: the off-game note and the dossiers are the sensitive ones.
- **Your git history.** Deleting an entry on request removes it from the working tree, not from
  the commits before it. If you version the campaign, say so at session zero, and prefer keeping
  the sensitive notes out of the repo over rewriting history later.
- **Cross-table inference.** A hook harvested for one campaign is still a fact about a person when
  the campaign ends. `B.retention` is where the table decides what happens then.
- **Remote play.** `ttrpg-session-audio` assumes one room and one microphone. Played over a call,
  consent includes the platform that records, and that platform's retention is not this package's.

## For the humans at the table, in one paragraph

The GM's assistant keeps notes about how you play and what you told the table you cared about, so
that scenes can be aimed at things you chose. You can ask what is written about you, and you can
have any of it deleted without giving a reason. If the table is recorded, that is a separate,
explicit yes; turning the out-of-character talk into a searchable note is a third, narrower one.
The safety tools are not a formality: they are the only part of this system with no override.
