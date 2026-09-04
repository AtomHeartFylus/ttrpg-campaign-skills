# TTRPG Campaign Skills

A package of **agent skills for running a tabletop RPG campaign** — prep, play, record, recap,
continuity — that is **agnostic of the game system**.

These skills are not theory. They are distilled from a real, long-running weekly campaign
(9 players, a 10-module published adventure heavily reworked as homebrew, a full session
cycle documented in an Obsidian vault), and every rule in them exists because something
broke at the table without it.

---

## The problem this solves

Skills written for one campaign are excellent and unshareable ("remember the Harbourmaster's beat",
"spend a notch of Salt"). Skills written generically are shareable and useless ("give NPCs
motivations"). This package resolves the tension with **two layers**:

| Layer | Lives in | Contains | Written once per |
|---|---|---|---|
| **Base skill** | this repo, `skills/` | the *procedure* and the *tests* — never a system name | ever |
| **Campaign profile** | your campaign repo, `campaign-profile.md` | the *facts* of your table: system, dramatic resource, tone, canon text, recurring guide, conventions | campaign |
| **Overlay skill** (optional) | your campaign repo | only what cannot be expressed as a profile slot | campaign |

A base skill reads the profile in its first phase and speaks in **slot names**
("the dramatic resource", "the recurring guide"), never in the vocabulary of one game.
When a slot is empty, the skill **degrades gracefully** — it drops the corresponding section
instead of inventing one.

See [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md) for the design invariants every skill is built on,
and [`docs/AUTHORING.md`](docs/AUTHORING.md) if you want to write or modify a skill.

---

## The skills

| Skill | Use it when | Maturity |
|---|---|---|
| `ttrpg-campaign-setup` | starting a campaign repo/vault, or filling the campaign profile | v1 |
| `ttrpg-table-dossier` | session zero, player dossiers, safety tools, spotlight budget, attendance rules | v1 |
| `ttrpg-session-prep` | writing the prep document you will actually hold during play | v1 |
| `ttrpg-session-log` | recording what really happened after a session | v1 |
| `ttrpg-table-recap` | writing the in-fiction recap read aloud to open the next session | v1 |
| `ttrpg-session-audio` | turning a recorded session into transcript, log material and off-game notes | v1 |
| `ttrpg-entity-note` | creating an NPC, place, faction, item or creature note | v1 |
| `ttrpg-campaign-arc` | planning a season/arc, tracking open threads and spotlight rotation | v1 |
| `ttrpg-continuity-audit` | checking campaign state for drift, dangling threads, broken links | v1 |

The skills form a closed cycle:

```
   setup ──► table-dossier ──► session-prep ──► [PLAY] ──► session-audio ──► session-log
                                    ▲                                            │
                                    └──────── table-recap ◄──────────────────────┘
              campaign-arc and continuity-audit run across the whole loop
```

---

## Install

Skills are plain folders with a `SKILL.md`. Everything a skill needs to stand alone is **checked
into the repo**, not generated at install time — each skill carries its own copy of the principles,
and `ttrpg-campaign-setup` carries the profile schema it interviews you from. A clone is already a
valid package; the installer only **copies** folders:

```sh
# Windows (PowerShell, from the repo root)
./install.ps1 -Target "$HOME/.agents/skills"
# if the host policy is Restricted:
#   powershell -ExecutionPolicy Bypass -File ./install.ps1 -Target "$HOME/.agents/skills"

# macOS / Linux
./install.sh ~/.agents/skills          # or: sh install.sh ~/.agents/skills
```

Keeping the repo as the **canonical copy** and re-running the installer after a change means a fix
travels to every machine and every harness you use. **Edit the repo, never the installed copy:**
installing replaces each target folder wholesale, so local edits to an installed skill — and any
stray file you left there — are silently lost on the next install. That is intended (the source is
canonical), but it surprises people once.

---

## Adopting them for your campaign

1. Run `ttrpg-campaign-setup` — it creates (or audits) the repo skeleton and walks you
   through `campaign-profile.md`.
2. Fill the profile honestly. Empty slots are legitimate: they switch sections off.
3. Run `ttrpg-table-dossier` for session zero: the safety conversation, one dossier per player and
   the harvested hooks. `ttrpg-session-prep` reads those dossiers as a required input, and
   `B.distance` is decided at that table, not in the interview — skipping this step is what makes a
   first prep aim at nerves nobody agreed to expose.
4. Play a session with `ttrpg-session-prep`, then close the loop with `ttrpg-session-log`
   (and `ttrpg-table-recap` to open the next one).
5. Only when a rule is *specific to your campaign and cannot be a profile slot*, write an
   overlay skill (see `templates/overlay-SKILL.md`). Overlays should be short; if an overlay
   grows past a page, the base skill is probably missing a slot.

The installer copies `skills/` only: `docs/`, `templates/` and `tests/` stay in the clone, which is
where you read the principles, start an overlay from, and run the evals.

---

## Worked examples and evals

Each artifact-producing skill bundles a complete **worked example** of its output
(`references/example-*.md`): one invented campaign ("The Weir Circuit", system "Lantern &
Ledger") runs through prep, log, recap and an entity note, annotated with why each block is the
way it is. They are shapes to calibrate on, never content to reuse — every name and number in them
is fictional on purpose.

`tests/` holds the **behavioral eval harness**: `fixture-campaign/` is that same invented campaign
as a repo with deliberately seeded defects, and `evals/` holds one scenario + pass/fail rubric per
covered skill. `scripts/check_contract.py` proves the skills are well-formed; the evals are how you
check they *work* — after a behavioural change, or before trusting a new model with your campaign.
Protocol in [`tests/README.md`](tests/README.md).

---

## What this package assumes, and what it leaves alone

**The substrate.** These skills assume your campaign memory is a tree of **markdown notes in a
versioned folder** that an agent can read and write. They do **not** assume which tool displays
them: no skill names an editor, and everything tool-shaped is a profile slot instead — link syntax
and its escaping (`C.links`), which values are properties (`C.frontmatter`), forbidden characters in
filenames (`C.naming`), the verification command and its invariant (`C.verify`). A skill can do
nothing with the name of an app; it can do everything with those four answers. If your campaign
lives in a hosted wiki or a shared document instead of in files, this package has no ground to
stand on — that is a boundary, not an oversight.

**One thing tool-shaped is only half a slot.** The skeletons show callouts, checkboxes and quotes in
one dialect. `C.blocks` says how your note system writes them, and a skill keeps the *roles* while
rendering them your way — plain headings and blockquotes are a complete answer.

**One GM, and a table in a room.** Every skill addresses a single person who prepares, runs and
records; there is no slot for who leads, so a GM-less or rotating-GM game gets no support here.
`ttrpg-session-audio` additionally assumes a shared room with one microphone: played remotely, three
things change that no slot covers — consent now includes the platform that records, per-user tracks
make diarization pointless, and invoking a safety tool over a call is a different act. Both are
boundaries of an extraction from one table, not principles.

**Deliberate non-goals.** No encounter design or difficulty balancing, no rules lookup or reference
retrieval, no character sheets or level-up assistance, no virtual-tabletop or map integration.
Those are where system-agnosticism genuinely breaks — you cannot balance an encounter without
knowing the system — and they are already served by real tools. This package works on *text that
persists and gets forgotten*, not on the mathematics of a ruleset.

**Known gaps, honestly.** The package is an extraction from one long campaign, so its holes are
that table's comforts: there is no item/economy ledger (a promised magic item that never arrives is
the same defect `ttrpg-continuity-audit` hunts in narrative threads, and it has nothing to check
against), no scheduling and attendance logistics (the most common cause of campaign death), nothing
player-facing except the recap, and nothing that lands a finale or archives a finished campaign.
These wait for a second campaign to earn them rather than being invented here.

---

## Design bias, stated up front

These skills assume a table where:

- **the fiction outranks the system** — mechanics serve scenes, not the other way round;
- **a scene without a dramatic question is decorative** — including combat;
- **what is not written down is lost** — the log, not memory, is the source of truth;
- **prep is a play aid, not a document** — it is read under pressure, mid-session, with
  people talking.

If your table is a tactical dungeon crawl and you like it that way, several invariants here
(non-combat exit conditions, moral compass, white space for roleplay) will fight you. Switch them
off explicitly in the profile's `E.overrides`, where a skill will read the decision and comply
without arguing — rather than fighting the skills note by note.

## License

MIT — see [LICENSE](LICENSE). Written by Filippo Milanoli Turlotte; the skills carry the package as
their `metadata.author`, because they are meant to be forked and filled by whoever runs the table.
