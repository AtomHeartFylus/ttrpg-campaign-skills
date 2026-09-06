---
type: campaign-profile
schema: 2
---

# Campaign Profile — The Weir Circuit

> Fixture for behavioral evals (see `tests/README.md`). The campaign, its system and every value
> are invented; the repo around this profile contains **deliberately seeded defects** listed in
> `tests/evals/`. Do not fix it in place — evals run on a copy.

## §A — Game

- **`A.ruleset`** — Lantern & Ledger, house edition: pools of d6 against a threshold; advancement
  in *marks* (a mark per session objective met; three marks buy a new craft).
- **`A.adjudicated`** — violence, hazards of the fen, working underwater.
- **`A.fiction`** — persuasion between people is never rolled; it is played.
- **`A.houserules`** — none that change preparation.
- **`A.resource`** — Wick.
- **`A.resource_shape`** — per-character.
- **`A.resource_scale`** — 5 Wick per character at the start of a season.
- **`A.resource_loss`** — a lie told where the fen can hear. **`A.resource_gain`** — a promise
  kept aloud at personal cost.
- **`A.resource_asymmetry`** — only the living hold Wick; the drowned can spend a character's
  Wick against them but may never be given any.
- **`A.resource_zero`** — the character's shadow starts answering for them; the player loses the
  right to stay silent.
- **`A.resource_handling`** *(setup-only)* — a candle-stub per character, physically shortened.

## §B — Table

- **`B.size`** — 5 (Ada, Bruno, Cleo, Dara, Enzo). *(written back at onboarding, W17b — rotation
  period becomes 5 / `B.protagonists` (2) = 2.5 sessions; ask the table which way to round.)*
- **`B.protagonists`** — 2 per session → rotation period 2.
- **`B.cadence`** — weekly. **`B.horizon`** — one season, ~14 sessions.
- **`B.length`** — four hours, hard stop.
- **`B.absence`** — the absent wait at the last safe camp and do not advance.
- **`B.distance`** — fictional.
- **`B.safety`** — pause-word "weir"; anyone may invoke; scene rewinds without discussion;
  refreshed at each chapter start.
- **`B.consent_recording`** — no. **`B.consent_offgame`** — no.
- **`B.frame`** — folk-ballad register, no real or public figures admitted.
- **`B.retention`** — GM notes about players kept for the season, then deleted.
- **`B.hooks_count`** — 2 per player. **`B.hooks_staging`** — parallels.
- **`B.language`** — English.

## §C — Repository and artifacts

- **`C.root`** — this folder. Map: `Sessions/` (preps and logs), `Dossiers/` (one per player),
  `Entities/` (NPCs, places, factions), `Hub.md` (state hub), `Threads.md` (thread ledger).
- **`C.granularity`** — one note per entity, small and linked.
- **`C.links`** — `[[wikilinks]]`, no escaping.
- **`C.frontmatter`** — plain `tags:` lists; no generated views or queries.
- **`C.blocks`** — callouts `> [!type]`, checkboxes `- [ ]`, quotes as blockquotes.
- **`C.state_locations`** — marks and Wick per character: that player's dossier. Thread status:
  `Threads.md`. Entity disposition: the entity's note.
- **`C.hub`** — `Hub.md`. **`C.arc_note`** — none yet. **`C.thread_ledger`** — `Threads.md`.
- **`C.verify`** — none declared yet.
- **`C.naming`** — plain names with spaces and em-dashes; no slashes or colons.
- **`C.portability`** *(setup-only)* — single machine, versioned folder.
- **`C.inline_exception`** — default: prep inlines everything except stat blocks.
- **`C.gm_private`** — not needed. **`C.player_access`** — players read nothing.
- **`C.capture_paths`** — n/a (no recording consent).

## §D — Campaign shape and content

- **`D.shape`** — series.
- **`D.backbone`** — fully homebrew. **`D.unit`** — one chapter beat per session.
- **`D.official_material`** / **`D.own_material`** *(setup-only)* — all own material, per `C.root`.
- **`D.deviation_policy`** — n/a (no source).
- **`D.endgame`** — the fen floods, or the debt-ledgers burn: seeded from chapter two onward.
- **`D.canon_source`** — the Weir Ballads; rewritten in-world; read aloud by the GM; no recordings.
- **`D.guide`** — Brenna the Ferrywoman; arc: what she ferries at night; voice: answers a
  question with a toll; owes one prepared beat per session.
- **`D.tone`** — fen-gothic; wry breaks admitted; recurring pressure: what a fair price is.
- **`D.recap`** — in-fiction prose, read by the GM, ceiling three minutes.
- **`D.identity`** — role-epithets; per-character values in the dossiers.

## §E — Declared overrides and working agreements

- **`E.overrides`** — none. All defaults in force.
- **`E.deliverable`** — saved notes in the repo, committed.
- **`E.review`** — blunt.
- **`E.never_without_asking`** — renaming or moving any existing note.
- **`E.retroactivity`** — past notes may be corrected; corrections recorded in the note itself
  under a "Corrections" line.
- **`E.audit_cadence`** — every 3 sessions.
