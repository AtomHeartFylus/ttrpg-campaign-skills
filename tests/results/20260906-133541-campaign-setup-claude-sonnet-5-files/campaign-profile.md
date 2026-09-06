---
type: campaign-profile
schema: 2
---

# Campaign Profile — Driftwood (working title)

## §A — Game

- **`A.ruleset`** — a homebrew d6 thing we call Driftwood, advancement by deeds.
- **`A.adjudicated`** — none (asked; no preference given).
- **`A.fiction`** — none (asked; no preference given).
- **`A.houserules`** — none (asked; no preference given).
- **`A.resource`** — Grit.
- **`A.resource_shape`** — per-character (the GM's own words: "everyone has 4").
- **`A.resource_scale`** — 4, per character.
- **`A.resource_loss`** — backing down. **`A.resource_gain`** — around a fire.
- **`A.resource_asymmetry`** — none (asked; no preference given).
- **`A.resource_zero`** — none (asked; no preference given).
- **`A.resource_handling`** *(setup-only)* — none (asked; no preference given).

## §B — Table

- **`B.size`** — 5.
- **`B.protagonists`** — **unanswered.** Asked directly; the GM's blanket "no preference" covered
  it, and this slot has no declared `default:` to fall back on. Left empty on purpose rather than
  guessed — see the run report: the rotation check (`ttrpg-table-dossier`, P7) has no period to
  compute until this is answered.
- **`B.cadence`** — monthly.
- **`B.horizon`** — ~10 sessions.
- **`B.length`** — 3 hours, soft stop.
- **`B.absence`** — `deferred: session zero`.
- **`B.distance`** — `deferred: session zero`.
- **`B.safety`** — `deferred: session zero`.
- **`B.consent_recording`** — no.
- **`B.consent_offgame`** — no.
- **`B.frame`** — none (asked; no preference given).
- **`B.retention`** — none (asked; no preference given).
- **`B.hooks_count`** — `default: 2–3` (used; the GM said no preference, so this is the schema's
  own declared default, stated here as such — not this skill's invention).
- **`B.hooks_staging`** — none (asked; no preference given).
- **`B.language`** — English (nothing in the repo to infer from yet; this whole interview ran in
  English, so that is what is recorded — say so and offer to change it).

## §C — Repository and artifacts

- **`C.root`** — this folder. Map: `Sessions/` (preps and logs), `Dossiers/` (one per player),
  `Entities/` (NPCs, places, factions), `Hub.md` (state hub), `Threads.md` (thread ledger).
- **`C.granularity`** — one note per entity, small and linked (the package's own standard
  convention, adopted because the GM said "whatever is standard" — proposed, not invented from
  nothing).
- **`C.links`** — `[[wikilinks]]`, no escaping (adopted as the standard convention, same basis).
- **`C.frontmatter`** — plain `tags:` lists; no generated views or queries (adopted as standard).
- **`C.blocks`** — callouts `> [!type]`, checkboxes `- [ ]`, quotes as blockquotes (adopted as
  standard).
- **`C.state_locations`** — Grit and advancement per character: that player's dossier. Thread
  status: `Threads.md`. Entity disposition: the entity's own note.
- **`C.hub`** — `Hub.md`. **`C.arc_note`** — none yet. **`C.thread_ledger`** — `Threads.md`.
- **`C.verify`** — `none — invariant unverifiable`. Proposed and not installed: this skill bundles
  `references/check_links.py` and offered to copy it to `scripts/check_links.py` and register
  `python scripts/check_links.py .` as this slot's command — the GM's script gave no explicit yes
  to that specific offer, so nothing was copied and nothing was written as a side effect of "do
  whatever is standard." Ask again once the GM has seen the offer directly.
- **`C.naming`** — none (asked; no preference given).
- **`C.portability`** *(setup-only)* — not confirmed this session: recommend a versioned folder
  (git) reaching every machine the GM plays from; ask before relying on `C.portability`'s guarantee.
- **`C.inline_exception`** — `default:` prep inlines everything except stat blocks (used; no
  preference given, so the schema's own declared default is stated here as such).
- **`C.gm_private`** — *(to decide alongside `C.player_access` at session zero — required only if
  players end up able to read the repo, which is not yet known)*.
- **`C.player_access`** — `deferred: session zero`.
- **`C.capture_paths`** — n/a (no recording consent).

## §D — Campaign shape and content

- **`D.shape`** — series.
- **`D.backbone`** — fully homebrew. **`D.unit`** — none (asked; no preference given).
- **`D.official_material`** / **`D.own_material`** *(setup-only)* — all own material, per `C.root`.
- **`D.deviation_policy`** — n/a (no source).
- **`D.endgame`** — none (asked; no preference given) — flagged in the run report: `ttrpg-campaign-arc`
  has no ending to seed toward until this is answered.
- **`D.canon_source`** — none (asked; no preference given).
- **`D.guide`** — none (asked; no preference given).
- **`D.tone`** — salt-western register; jokes admitted as breaks. **Recurring thematic pressure: not
  yet stated** — this half of the slot needs one more question the script did not cover; asked, left
  open rather than invented, and named in the run report.
- **`D.recap`** — none — asked directly, answered "no recap, we just start." This is a deliberate,
  durable **`none`**, not an unanswered slot: no opening recap is produced for this campaign.
- **`D.identity`** — none (asked; no preference given).

## §E — Declared overrides and working agreements

- **`E.overrides`** — none. Walked through all eight strong defaults (P4, P5, P6, P7, P8, P9, P12,
  P13) individually; the GM asked to switch none of them off. All defaults in force.
- **`E.deliverable`** — none (asked; no preference given — flagged in the run report: skills should
  ask per run, or default to a chat draft, rather than assume "saved and committed").
- **`E.review`** — none (asked; no preference given).
- **`E.never_without_asking`** — none (asked; no preference given).
- **`E.retroactivity`** — none (asked; no preference given).
- **`E.audit_cadence`** — `default:` every 3–5 sessions (used; no preference given, so the schema's
  own declared default is stated here as such).
