# Audio fixture

`ttrpg-session-audio` is the one skill whose Phase 2 needs a real recording. Everything **around**
that phase — the two consent gates, the storage contract, the speaker map, the off-game curation,
the verify step — is judgement, not transcription, and is testable from a transcript alone.

So this folder holds **synthetic machine output**: what a diarizing tool would have emitted for one
evening of the invented campaign in `../fixture-campaign/`. The eval hands it to the agent as if
Phase 2 had just run.

- `Session 8 - 2026-09-12.diarized.txt` — the tool's diarized, timecoded output. Deliberately
  contains: anonymous positional labels; **one person split across two labels** (`SPEAKER_01` and
  `SPEAKER_04`); **one unresolvable overlap** (`SPEAKER_03`); mangled proper names, which is what
  makes a transcript a memory aid and not minutes (P11); a stretch of off-game talk carrying **one
  hook born off game** and **one mildly tasteless joke** (present so the eval can check that it is
  indexed by timecode and never quoted).

Nothing here is real: no real table, no real recording, no consent to model. The file is text and
small on purpose — the skill's own storage contract keeps real audio out of version control, and
this fixture is not audio.

**Known limit:** Phase 2 end to end (running an actual diarizing tool on real audio) has no eval.
That needs a consented recording, which is exactly the kind of asset this package refuses to invent.
