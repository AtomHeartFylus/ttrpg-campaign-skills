# TTRPG Campaign Skills

A package of **agent skills for running a tabletop RPG campaign** — prep, play, record, recap,
continuity — that is **agnostic of the game system**.

These skills are not theory. They are distilled from a real, long-running weekly campaign
(9 players, a 10-module published adventure heavily reworked as homebrew, a full session
cycle documented in an Obsidian vault), and every rule in them exists because something
broke at the table without it.

---

## The problem this solves

Skills written for one campaign are excellent and unshareable ("remember the Galileo beat",
"spend Hope tokens"). Skills written generically are shareable and useless ("give NPCs
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

| Skill | Use it when | Status |
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

Skills are plain folders with a `SKILL.md`. Install them with the script, which **copies** each
folder and materialises the files a skill needs to stand alone (the principles, the profile
template). Do not symlink `skills/` — a symlinked folder is missing exactly those materialised
files, and every skill opens with a dead link:

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
3. Play a session with `ttrpg-session-prep`, then close the loop with `ttrpg-session-log`.
4. Only when a rule is *specific to your campaign and cannot be a profile slot*, write an
   overlay skill (see `templates/overlay-SKILL.md`). Overlays should be short; if an overlay
   grows past a page, the base skill is probably missing a slot.

---

## Design bias, stated up front

These skills assume a table where:

- **the fiction outranks the system** — mechanics serve scenes, not the other way round;
- **a scene without a dramatic question is decorative** — including combat;
- **what is not written down is lost** — the log, not memory, is the source of truth;
- **prep is a play aid, not a document** — it is read under pressure, mid-session, with
  people talking.

If your table is a tactical dungeon crawl and you like it that way, several invariants here
(non-combat exit conditions, moral compass, white space for roleplay) will fight you. Drop
them explicitly in the profile rather than silently.

## License

MIT — see [LICENSE](LICENSE).
