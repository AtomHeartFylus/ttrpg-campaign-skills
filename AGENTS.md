# AGENTS.md — ttrpg-campaign-skills

Operational file for whoever works on this repo, human or agent. Read it before editing anything;
update it when a decision here stops being true.

This repo is a **system-agnostic package of agent skills for running a tabletop RPG campaign**. It
is not a knowledge collection of independent notes: the nine skills share one data note
(`templates/campaign-profile.md`) and can contradict each other. That coupling is the whole design,
and it is why this repo has a contract checker where a looser collection would not need one.

## Commands

- Check everything: `python scripts/check_contract.py` (from the repo root; stdlib only, no
  dependencies). Ten checks, exit 0 or 1.
- Install into an agent skills directory: `./install.sh ~/.agents/skills` (or
  `sh install.sh <target>`); PowerShell: `./install.ps1 -Target "$HOME/.agents/skills"`, with
  `powershell -ExecutionPolicy Bypass -File ./install.ps1 ...` if the host policy is `Restricted`.
- Install smoke test: install into a throwaway directory and confirm nine folders, each with its
  own `references/PRINCIPLES.md`.

## Testing

- `scripts/check_contract.py` must exit 0 before every commit. **Never weaken a check to get
  green** — a check that fires is either a real defect or a missing declaration in the schema.
- The checker also covers what an external skill validator would (frontmatter keys, hyphen-case
  name, description budget, `[TODO:` leftovers), so validation needs nothing outside this repo.
- When a check needs an exception, express it in the schema and make the exception *visible*: the
  `(setup-only)` marker on a slot is the worked example — it is parsed from the profile, never
  hardcoded, and its count is printed in the summary line.

## Project structure

- `skills/` — nine skill folders. Entrypoint `SKILL.md`, plus `references/` for depth.
- `templates/` — `campaign-profile.md` (the schema every skill reads) and `overlay-SKILL.md`.
- `docs/` — `PRINCIPLES.md` (P1…P13, cited by tag) and `AUTHORING.md` (how to write a skill here).
- `scripts/` — `check_contract.py`, the only script.

## Active decisions

Decisions already taken. Reopen them deliberately, do not re-litigate them by accident.

- **Two layers.** A base skill never names a game system, setting, mechanic or character; anything
  irreducibly campaign-specific goes in a thin overlay in the campaign's own repo. Everything
  variable is a slot in `campaign-profile.md`.
- **The profile schema is named, not numbered.** Sections are `§A Game`, `§B Table`,
  `§C Repository`, `§D Campaign shape and content`, `§E Overrides`; slots are cited as `B.distance`,
  `D.shape`, `E.overrides`. Numeric `§1..§10` citations are a hard error: renumbering on every added
  slot was the mechanism that produced six slots nobody read.
- **Cross-cutting rules live once**, in `docs/PRINCIPLES.md`, cited by tag and never restated.
  P1/P2/P3/P10/P11 are hard requirements; the rest are strong defaults a campaign may switch off
  through `E.overrides`.
- **Bundled files are checked-in content, not installer output.** Every skill carries its own
  `references/PRINCIPLES.md`, and `ttrpg-campaign-setup` carries a copy of the profile schema.
  Byte-identity is enforced by the checker. Generating them at install time made every committed
  state invalid: a fresh clone had nine dangling links.
- **The setup interview is driven from its bundled copy of the schema**, never from a hand-copied
  slot list. A new slot becomes askable by existing, not by someone remembering to transcribe it.
- **Every slot must have a reader.** A slot no skill branches on is a question asked for nobody.
  The exception is slots explicitly marked `(setup-only)`: recorded for the humans, not for
  branching.
- **Empty slot ≠ default.** An empty slot switches the corresponding section *off*, or makes the
  skill ask; it never authorises a guess. Consent slots are the sharp case: `B.consent_recording`
  and `B.consent_offgame` are separate gates, and neither is ever inferred from the other or from
  the existence of a file.
- **Entrypoint vs `references/`.** The entrypoint keeps what is needed *every* time; `references/`
  gets what is needed *one way only*. Entrypoints stay near 210 lines, and a link inside a skill
  folder must resolve inside that folder — installation copies the folder alone.
- **The package is an extraction from real play.** Nothing enters because it sounds useful: encounter
  balancing, rules lookup, character sheets and VTT integration are deliberate non-goals, and the
  known gaps (item/economy ledger, scheduling, player-facing handouts, endgame and archival) wait
  for a second campaign to earn them.

## Authoring

`docs/AUTHORING.md` is the contract for writing a skill here: description shape, slot citation,
principle citation, the `E.overrides` and `D.shape` branches, and the change procedure. Follow it
before inventing a new convention, and add the convention there if it survives review.
