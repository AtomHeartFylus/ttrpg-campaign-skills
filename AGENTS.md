# AGENTS.md — ttrpg-campaign-skills

Operational file for whoever works on this repo, human or agent. Read it before editing anything;
update it when a decision here stops being true.

This repo is a **system-agnostic package of agent skills for running a tabletop RPG campaign**. It
is not a knowledge collection of independent notes: the nine skills share one data note
(`templates/campaign-profile.md`) and can contradict each other. That coupling is the whole design,
and it is why this repo has a contract checker where a looser collection would not need one.

## Commands

- Check everything: `python scripts/check_contract.py` (from the repo root; stdlib only, no
  dependencies). Fourteen checks, exit 0 or 1.
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
- It puts a **floor** under the two-layer rule: `NO-SYSTEM-NAMES` (error) fails on a blocklisted
  game system or note-taking tool in anything shipped, `MECHANICS-LEAK` (warn) flags the vocabulary
  of one system family, `ENCODING` (error) catches U+FFFD and literal `\uXXXX` escapes in every
  markdown file, `OVERRIDE-MAPPED` (error) fails a skill that mentions `E.overrides` without
  mapping it. A blocklist is never complete, so the manual agnosticism self-test of
  `docs/AUTHORING.md` §1 is still required — these checks catch the names that actually leaked: a
  whole transliterated campaign once survived the ritual inside a base skill.
- `NO-SYSTEM-NAMES` has **no per-file exception list on purpose**. A system name belongs in
  `A.ruleset`, which the campaign fills, or in an overlay outside this repo. The worked example in
  the schema is an invented campaign for the same reason: a realistic one gets copied, not read.
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
- **Empty slot ≠ default, unless the schema declares one.** An empty slot switches the corresponding
  section *off*, or makes the skill ask; it never authorises a guess. The one exception is visible
  and lives in the schema: a slot may carry an explicit **`default:`**, which a skill may use only
  by citing it and only while saying in its output that it did (`B.hooks_count`, `D.recap`'s
  ceiling, `E.audit_cadence`, `C.inline_exception`). A number stated on a skill's own authority is a
  hardcoded constant with a friendlier name — `docs/PRINCIPLES.md` included, which is why P7 names
  `B.protagonists` instead of a count.
- **A slot has four states, not two:** an untouched placeholder (never asked → stop and ask),
  `deferred: <when>` (the answer belongs to a conversation still to come → reads as empty),
  `none` (asked and answered empty → that section is off durably), or a value. Session zero owns
  five of them, so the interview writes `deferred: session zero` and never `none` for
  `B.distance`, `B.safety`, `D.tone`, `C.player_access`, `B.absence`.
- **`E.overrides` is mapped, not mentioned.** Every skill carries an `E.overrides` branch: a table
  of the overridable defaults *that skill* enforces against what stops being required when each is
  off. Citing the slot without mapping it was the state that let eight skills advertise the
  mechanism and implement nothing; enforcing a switched-off default is as wrong as inventing a slot
  value, and the *Verify* and *What NOT to do* lists are where it creeps back as an absolute.
  Consent slots (`B.consent_*`, `B.safety`, `B.retention`, `B.frame`) are not defaults and no
  override reaches them.
- **One owner per artifact, written down.** Thread *status* lives only in `C.thread_ledger` and the
  hub views it; the per-session speaker map lives in its own note beside the transcript pair, never
  inside the session log; the shared-party-clock value lives on the party note that
  `ttrpg-campaign-setup` creates when `A.resource_shape` calls for it; the dossier Diary carries one
  entry per session *attended*, marked carried or chorus, because that mark is the only input the
  rotation check has. Each of these was a place where two skills wrote the same thing. Consent slots are the sharp case: `B.consent_recording`
  and `B.consent_offgame` are separate gates, and neither is ever inferred from the other or from
  the existence of a file.
- **Entrypoint vs `references/`.** The entrypoint keeps what is needed *every* time; `references/`
  gets what is needed *one way only*. Entrypoints stay in the 200–250 line band (the `E.overrides`
  and `D.shape` branches are Phase 0 material and cannot move to `references/`), and a link inside
  a skill folder must resolve inside that folder — installation copies the folder alone.
- **The package is an extraction from real play.** Nothing enters because it sounds useful: encounter
  balancing, rules lookup, character sheets and VTT integration are deliberate non-goals, and the
  known gaps (item/economy ledger, scheduling, player-facing handouts, endgame and archival) wait
  for a second campaign to earn them.

## Authoring

`docs/AUTHORING.md` is the contract for writing a skill here: description shape, slot citation,
principle citation, the `E.overrides` and `D.shape` branches, and the change procedure. Follow it
before inventing a new convention, and add the convention there if it survives review.
