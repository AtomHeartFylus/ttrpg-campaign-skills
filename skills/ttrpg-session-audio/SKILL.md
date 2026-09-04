---
name: ttrpg-session-audio
description: "Turn a recorded session into usable material: a versioned transcript pair, a per-session speaker map, and — only when separately consented to — a curated off-game note. Use when asked to transcribe, diarize or process a session recording, to set up the recording and transcript conventions of a campaign repo, or to salvage the out-of-character half of an evening. Covers the two independent consent gates that must pass before anything runs, the storage contract (large audio out of version control, text transcripts in), any diarizing speech-to-text tool, the readable + timecoded file pair, rebuilding anonymous speaker labels session by session, and curating off-game talk by theme with timecodes. Does not write the record of what happened (see ttrpg-session-log) or the in-fiction opening recap (see ttrpg-table-recap)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.1"
---

# Session audio

Turns the raw recording of an evening into things worth keeping: a **transcript pair**, a
**speaker map** for that session, and — behind its own consent gate — a **curated off-game note**.
It runs between play and the session log.

> **P11 — the log is the authority.** A transcript is a memory aid, **never minutes**. Proper
> names and campaign terms come out mangled; speaker turns are unreliable wherever voices overlap.
> On divergence: re-listen at the timecode, and the log wins.

---

> Principles are cited below by tag (`P1`…`P13`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

**Find it before declaring it missing.** Search the repo/vault root for a file named
`campaign-profile.md` (`rg --files -g campaign-profile.md`, or the equivalent) before concluding
there is none. A profile that exists but was not found re-interviews a GM who already answered.
Only if the search comes back empty, run `ttrpg-campaign-setup` first — do not guess conventions.

| Slot | Used for | If empty |
|---|---|---|
| `B.consent_recording` | **gate 1** — is the table recorded, and who has explicitly agreed | **stop and ask**; never proceed on an assumption |
| `B.consent_offgame` | **gate 2** — may the out-of-character talk become a durable curated note | **no off-game note.** Everything else runs normally |
| `C.capture_paths` | where audio, transcripts and the off-game note live, and their naming — **read this, do not derive a layout** | propose the contract in Phase 1, ask, then write the accepted answer back into `C.capture_paths` |
| `C.player_access`, `C.gm_private` | what players may read of the repo; **where the off-game note is allowed to live** | treat transcripts and the off-game note as GM-only |
| `B.retention` | how long transcripts and off-game entries are kept, and who can trigger a deletion | say plainly that this material is being kept indefinitely, and offer to set the rule — do not quietly assume forever |
| `B.language` | the language the transcription runs in | ask once |
| `C.naming`, `C.links`, `C.frontmatter`, `C.verify` | file naming, link syntax, what version control ignores, verification command | follow the repo's existing convention; skip link verification |
| `E.never_without_asking`, `E.overrides` | whether external/cloud tools may be used; whether files may be created without asking | ask before uploading anything and before creating folders |
| `D.shape` | one-shot / series / open sandbox — see the branch below | proceed; this skill is the least shape-sensitive in the package |

### The consent gates — two slots, read first, never merged

These are the only slots in this package that can stop a skill dead. They are read **before**
Phase 1, not as a checklist item afterwards, and **neither one implies the other**.

**Gate 1 — `B.consent_recording`, for the whole skill:**

- **`yes`, with the agreeing parties named** → proceed.
- **`no`** → **stop.** Do not transcribe, do not create folders, do not index a file that already
  exists. Report that the profile declares this table is not recorded, and end.
- **empty, ambiguous, or a `yes` that names nobody** → **stop and ask** the GM to confirm that
  everyone at the table has agreed and where the files may live; write the answer into
  `B.consent_recording` before running anything.
- **The existence of an audio file is not consent and never becomes consent.** A recording proves
  a recording was made — nothing about who agreed to it. Handed a file with the slot empty, ask.
- **Re-check when the roster changes.** A player who joined after the agreement has not given one.

**Gate 2 — `B.consent_offgame`, for Phase 5 only.** Agreeing to be recorded is **not** agreeing to
a durable, themed, timecoded index of your out-of-character talk: the first is a file nobody reads,
the second is a document about named people that outlives the evening.

- **explicit `yes`, per person present** → Phase 5 runs.
- **`no`, empty, ambiguous, or a `yes` that does not cover everyone at the table that night** →
  **skip Phase 5 entirely.** Produce the transcript pair and the speaker map as normal and say that
  the off-game note was not produced, and why. This is not a degraded run; it is the default.
- **Never infer gate 2 from gate 1, from an existing recording, or from a previous session's
  answer.** They are different questions asked of the same people.

**`D.shape` branch — mandatory.** `series` → as written; the speaker map is rebuilt per session and
never carried forward. `one-shot` → identical, with one file and one map; there is no next session
to feed, so a hook born off game goes into that single log or is declared unused. `open sandbox` →
identical. Empty → proceed; nothing in this skill depends on the answer.

## Phase 1 — The storage contract

Two classes of file with opposite handling. Get this wrong once and the repository is permanently
heavy.

| Artifact | Size | Version control | Why |
|---|---|---|---|
| Raw audio of the evening | hundreds of MB | **excluded** (ignore rule) | binary, undiffable, not part of the repo's history |
| Readable transcript (plain text) | tens of KB | **committed** | text, diffs cleanly, is the searchable memory |
| Timecoded transcript (subtitle format) | tens of KB | **committed** | the index back into the audio |
| Intermediate machine output (word-level JSON and similar) | MB | **excluded** | a build artifact of the tool, regenerable |

**`C.capture_paths` declares the folders and the naming rule. Read them and follow them.** Do not
re-derive a layout that the profile already fixes. If the slot is empty, propose the conventions
below, ask before creating anything, and write the accepted answer back into `C.capture_paths` so
the next session does not re-decide it:

- Audio lives in its own folder, named `Session N - YYYY-MM-DD.<ext>`, and is matched by an ignore
  rule. Keep the originals **outside** the repo as well — losing them costs the timecodes.
- Both transcript files carry **the same base name as the audio file**, in a sibling transcript
  folder. Same name = the pair is self-evident a year later.
- Session recordings of play are a different asset class from any audio used *during* play
  (readings, music, ambience) — different folder, different ignore policy. Do not mix them.

## Phase 2 — Transcribe with a diarizing tool

Any speech-to-text tool that produces **speaker-diarized output with timecodes** satisfies this
skill. The requirement is the output shape, never a particular product.

- Produce **two files**: a readable transcript with speaker labels, and a **timecoded** one in a
  subtitle format. The timecodes are the whole point — every later reference is a timecode.
- Run the tool **outside the campaign repo**. A transcription stack pulls heavy dependencies; the
  repo holds a campaign, not an environment. Record the invocation in a note, not the environment
  itself.
- *Example of a local pipeline (not a requirement):* an open-source speech-to-text model of the
  Whisper family plus a speaker-diarization stage, run on a local GPU from a separate project
  directory, with a small script that emits both files. Any equivalent — including a hosted service
  — is fine, provided `E.never_without_asking` and `E.overrides` permit sending the table's audio to
  a third party, and `B.consent_recording` covers that third party too.
- Do not hand-correct the transcript. It is machine output and is allowed to be wrong (P11); its
  corrections live in the log, not in the file.

## Phase 3 — Rebuild the speaker map, per session

Diarization labels are **anonymous and positional** (`SPEAKER_00`, `SPEAKER_01`, …). They carry
**no continuity between files**: the same person is a different number next session, and one person
may be split across two labels.

Therefore:

- Rebuild the map **every session**, by sampling a few timecodes per label until each is
  identified.
- Record it **in that session's log** and nowhere else — it is a fact about that file, not about
  the campaign (P10). A global "speaker table" in an index is guaranteed to be wrong.
- Mark labels you could not resolve as unresolved. Do not guess a speaker to make the map look
  complete.

```markdown
## Speaker map (Session N transcript)
| Label | Person | Notes |
|---|---|---|
| SPEAKER_00 | <GM> | |
| SPEAKER_01 | <player> | merges with SPEAKER_04 after ~1:12:00 |
| SPEAKER_03 | unresolved | two voices overlapping |
```

## Phase 4 — Use it as a memory aid

- Search the transcript for the beat you half-remember, take its **timecode**, re-listen there.
- Feed the result into `ttrpg-session-log` as testimony to confirm — never paste transcript text
  into the log, and never let the transcript overrule what the GM reports (P11).
- Expect proper names, invented terms and system vocabulary to be corrupted. Never copy a name out
  of a transcript into a note: read it back from the entity note that owns it.
- Do not build a second narrative summary of the session out of the transcript. The log is the
  narrative; the transcript is an index into audio.


## Phase 5 — Curate the off-game half — only behind gate 2

**`B.consent_offgame` governs this entire phase.** Empty, `no`, or not covering everyone present
→ **skip it and say so.** Nothing else in this skill changes; this is the default, not a degraded
run. On an explicit yes, follow
[references/off-game-note.md](references/off-game-note.md), which owns the shape and the rules.

The load-bearing summary, so it is not mistaken for surveillance:

- **Exactly two things are worth keeping** — the **mood of the table** (what later explains why a
  scene landed or died) and **hooks born off game**. An entry serving neither is not written.
- **Where it lives is read from `C.player_access` / `C.gm_private`, never improvised.** If players
  can read the repo, it goes to the GM-private location or is agreed openly with the table; if
  `C.gm_private` is empty while players have access, stop and ask.
- **Curate, do not transcribe:** themes with timecodes into the timecoded transcript, not quotes.
- **Crude, offensive or personal material is indexed by timecode and never quoted.**
- **Any participant may have any entry removed, without discussion or a reason** — which is exactly
  why entries are short pointers rather than reproductions: a pointer deletes cleanly. State the
  rule in the note's own header.

## Phase 6 — Verify and commit

- The transcript pair exists, both files share the base name of the audio, and the timecoded one
  actually opens at the right positions (spot-check two timecodes).
- `B.consent_recording` was read and passed **before** anything ran; `B.consent_offgame` was read
  independently, and Phase 5 ran only on an explicit yes. Both answers live in the profile rather
  than in this conversation.
- The ignore rules hold: run the repo's status check and confirm **no audio and no intermediate
  machine output are staged**. Check the size of what you are about to commit.
- The speaker map is in this session's log, with unresolved labels marked as unresolved.
- If it exists: the off-game note is a curation, not a transcript; it contains no quoted crude or
  personal material; it sits where `C.player_access` / `C.gm_private` permit; and it carries the
  removal rule in its own header.
- Links follow `C.links` syntax; run the `C.verify` command — invariant as declared (typically
  **0 broken links**).

## What NOT to do

- Do not start, continue or resume a capture pipeline while `B.consent_recording` is empty, `no`
  or ambiguous — and never infer consent from the existence of an audio file.
- Do not write an off-game note on the strength of `B.consent_recording`, a previous session's
  answer, or the fact that a recording exists. Gate 2 is asked separately, of everyone present.
- Do not re-derive a folder layout that `C.capture_paths` already declares, or improvise where a
  GM-private note lives.
- Do not commit the audio, or any multi-megabyte intermediate output of the transcription tool.
- Do not name a specific tool or environment as a requirement in campaign notes — record the
  output contract (readable + timecoded, diarized) and the invocation, nothing more.
- Do not upload the table's audio to a third-party service without checking the profile's working
  agreements and confirming the consent slots cover that service.
- Do not reuse last session's speaker map, and do not put a speaker map anywhere but that
  session's log.
- Do not guess an unresolved speaker.
- Do not treat the transcript as minutes, quote it into the log, or copy names out of it.
- Do not turn the off-game note into a second transcript, and do not quote crude, offensive or
  personal material in it — index it by timecode.
- Do not argue with, defer or negotiate a removal request. Delete the entry.
- Do not write an off-game entry that serves neither the table's mood nor a hook.
