---
name: ttrpg-session-audio
description: "Turn a recorded session into usable material: a versioned transcript pair, a per-session speaker map, and a curated off-game note. Use when asked to transcribe, diarize or process a session recording, to set up the recording/transcript conventions of a campaign repo, or to salvage the out-of-character half of an evening. Covers the storage contract (large audio out of version control, text transcripts in), any diarizing speech-to-text tool, the readable + timecoded file pair, rebuilding anonymous speaker labels per session, and curating off-game talk by theme with timecodes. Does not write the record of what happened (see ttrpg-session-log) or the in-fiction opening recap (see ttrpg-table-recap)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Session audio

Turns the raw recording of an evening into three things worth keeping: a **transcript pair**, a
**speaker map** for that session, and a **curated off-game note**. It runs between play and the
session log.

> **P11 — the log is the authority.** A transcript is a memory aid, **never minutes**. Proper
> names and campaign terms come out mangled; speaker turns are unreliable wherever voices overlap.
> On divergence: re-listen at the timecode, and the log wins.

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Read the campaign profile

| Slot | Used for | If empty |
|---|---|---|
| §7 Table conventions | language of play → the language the transcription runs in | ask once |
| §8 Player-facing outputs | what players may read of the repo — transcripts and off-game notes are the most sensitive files in it | treat both as GM-only |
| §9 Repo conventions | where audio, transcripts and the off-game note live; naming; what is ignored by version control; verification command | propose the layout in Phase 1 and ask before creating folders |
| §10 Working agreements | whether external/cloud tools may be used; whether files may be created without asking | ask before uploading anything and before creating folders |

**Consent is a precondition, not a step.** Everyone at the table knows the evening is recorded, and
knows where the files end up. If the repo is public or shared, transcripts and off-game notes are
the files that leak private conversation — confirm their visibility against §8/§10 **before** the
first commit, not after.

## Phase 1 — The storage contract

Two classes of file with opposite handling. Get this wrong once and the repository is permanently
heavy.

| Artifact | Size | Version control | Why |
|---|---|---|---|
| Raw audio of the evening | hundreds of MB | **excluded** (ignore rule) | binary, undiffable, not part of the repo's history |
| Readable transcript (plain text) | tens of KB | **committed** | text, diffs cleanly, is the searchable memory |
| Timecoded transcript (subtitle format) | tens of KB | **committed** | the index back into the audio |
| Intermediate machine output (word-level JSON and similar) | MB | **excluded** | a build artifact of the tool, regenerable |

Conventions to record in profile §9 once, then follow forever:

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
  — is fine, provided §10 permits sending the table's audio to a third party.
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

## Phase 5 — Curate the off-game half

**Roughly half of an evening is out-of-character talk** — tangents, arguments, jokes, life news,
digressions that have nothing to do with the fiction. It is not waste and it does not get thrown
away, but it is also not a second transcript.

Produce one note per session, at the path §9 declares, structured **by theme** with **timecodes
pointing back into the timecoded transcript**:

```markdown
---
<frontmatter per §9: session tag, off-game tag>
---

# Session N — Off-game

> [!info] Curation by theme of the out-of-character talk. Timecodes index the transcript;
> this is not a transcript.

## <Theme — a phrase, not a category>
- `00:41:12` <one or two lines: what was said and why it matters>
- `01:03:55` <…>

## Hooks born off game
- `01:22:07` <the idea, and where it could enter the fiction>

## Table mood
- <what the evening felt like; what the group was chewing on; who was tired, who was on>

## Indexed, not quoted
- `02:14:30` crude/personal exchange — indexed only
```

Rules:

- **Two jobs, both worth the effort.** (a) Record the **mood of the table** — the material that
  later explains why a scene landed or died. (b) Preserve **hooks born off game**: a genuine share
  of campaign material is invented sideways, in a digression, and is lost by morning otherwise.
- **Curate, do not transcribe.** A theme with two timecodes beats ten verbatim lines. If a section
  is growing into a rewrite of the transcript, cut it back to its index entries.
- **Crude, offensive or private material is indexed by timecode and not quoted.** The full record
  already exists in the transcript; the curated note does not need to reproduce it, and a quoted
  line in a curated note is the one that gets read out of context.
- Anything said off game that concerns a person at the table and not the campaign gets an index
  entry at most — or nothing, on request. Honour a "don't write that down" immediately and without
  argument.
- The hooks section is the one that feeds forward: when a hook is used, the next prep's global
  threads or a hook entry in the player's dossier owns it from then on (P10) — the off-game note
  keeps only its birth timecode.

## Phase 6 — Verify and commit

- The transcript pair exists, both files share the base name of the audio, and the timecoded one
  actually opens at the right positions (spot-check two timecodes).
- The ignore rules hold: run the repo's status check and confirm **no audio and no intermediate
  machine output are staged**. Check the size of what you are about to commit.
- The speaker map is in this session's log, with unresolved labels marked as unresolved.
- The off-game note is a curation, not a transcript, and contains no quoted crude/private material.
- Visibility confirmed against §8/§10 before the first commit of transcripts or off-game notes.
- Links follow §9 syntax; run the profile's verification command — invariant as declared
  (typically **0 broken links**).

## What NOT to do

- Do not commit the audio, or any multi-megabyte intermediate output of the transcription tool.
- Do not name a specific tool or environment as a requirement in campaign notes — record the
  output contract (readable + timecoded, diarized) and the invocation, nothing more.
- Do not upload the table's audio to a third-party service without checking §10.
- Do not reuse last session's speaker map, and do not put a speaker map anywhere but that
  session's log.
- Do not guess an unresolved speaker.
- Do not treat the transcript as minutes, quote it into the log, or copy names out of it.
- Do not turn the off-game note into a second transcript, and do not quote crude, offensive or
  private material in it — index it by timecode.
- Do not discard the off-game half. It is where the table's mood and a share of its hooks live.
