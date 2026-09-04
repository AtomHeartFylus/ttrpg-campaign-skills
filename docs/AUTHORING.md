# Authoring rules for skills in this package

Read this before writing or modifying any `skills/*/SKILL.md`. Consistency between skills is
what makes the package usable; the router picks between them on descriptions alone.

---

## 1. The agnosticism contract

A base skill **must not name a game system, setting, mechanic or character**. It names
**profile slots** (see `templates/campaign-profile.md`):

| Never write | Write |
|---|---|
| "Salt triggers" | "the dramatic resource's loss and gain triggers (`A.resource_loss` / `A.resource_gain`)" |
| "the Harbourmaster beat" | "the recurring guide's prepared beat (`D.guide`), if the profile declares one" |
| "the tide-table couplet" | "the canon quote (`D.canon_source`), with its declared delivery mode" |
| "Voyages/Voyage 4 - Ledger.md" | "the session log note, at the path the profile declares (`C.root`)" |
| "a difficulty class, a hit point total" | "a difficulty value, a cost, a quantity — in the terms `A.ruleset` uses" |

**Cite slots by named id — schema 2 has no numbers.** Sections are letters `A`…`E`, slots are
`A.resource`, `B.distance`, `C.verify`, `D.shape`, `E.overrides`. A numeric citation (`§2`, `§9`)
is a schema-1 fossil and fails the contract check: numbering renumbered itself the moment three
authors added slots in parallel, which is how five slots were added to the schema and never asked.
Adding a slot must never renumber another one.

**Graceful degradation is mandatory.** For every profile-dependent section, state what happens
when the slot is empty. There are exactly three legitimate answers, and inventing a value is not
one of them:

1. **Drop the section** — the default answer, and always available.
2. **Ask once** — when the artifact cannot exist without the value.
3. **Use the declared default** — only for the few slots that carry an explicit **`default:`** in
   `templates/campaign-profile.md`, only by citing it, and only while *saying in the output that
   the fallback was used* and offering to record the table's real value. A number a skill states on
   its own authority is a hardcoded constant, even when it is a reasonable one.

**Say it in the vocabulary of no system.** `A.ruleset` is the only place a system is named, and a
skill reads it rather than presupposing it: difficulty values, costs, quantities and depletion have
neutral names, and `scripts/check_contract.py` warns on the vocabulary of one family (`DC`, `HP`,
`AC`, saving throws, `d20`, encounter tables, combat rounds) and fails on a system name.

**Self-test before committing a skill:** re-read it substituting a wildly different campaign
(a modern investigative horror one-shot, a diceless political intrigue game). Every sentence that
stops making sense is a leaked assumption — move it to a profile slot, or to an overlay.

## 2. Structure of a SKILL.md

```markdown
---
name: ttrpg-<verb-or-artifact>
description: "<what it produces> Use when <trigger>. Covers <the 3-5 things it decides>.
  Does not <negative boundary>, see <sibling skill>."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# <Title>

<Two or three lines: what artifact this produces and who reads it under what conditions.>

## Phase 0 — Read the campaign profile
<Which slots this skill needs; what to do for each missing slot;
 what `E.overrides` switches off; what this skill does for each value of `D.shape`.>

## Phase 1 — Read before writing
<Ordered list of inputs, each with what to extract from it. Stop and report if an input is stale.>

## Phase 2 — <Produce>
<The mandatory structure of the artifact, as a fenced skeleton.>

## Phase 3 — Required elements
<The non-negotiables, each tied to a principle: "... (P5)".>

## Phase 4 — Verify
<A checklist the agent can actually run, ending in the profile's verification command.>

## What NOT to do
<Failure modes observed in practice, imperative and short.>
```

## 2bis. Two things every Phase 0 must do

**Read `E.overrides` and obey it.** The overrides slot lists the principles this campaign has
deliberately switched off or replaced (see `docs/PRINCIPLES.md`: P1, P2, P3, P10 and P11 are not
overridable; the rest are strong defaults). A skill treats an overridden principle exactly as it
treats an empty slot: **drop the section, or adapt it to the replacement the profile names**, in
silence and without arguing. A skill that enforces a principle the profile has switched off is
broken in the same way as one that invents a slot value.

```markdown
## Phase 0 — Read the campaign profile
Read `E.overrides` first. `P6 — off` → skip the conversation-scene requirement entirely.
`P7 — replaced by <x>` → apply <x> wherever this skill would have rotated the spotlight.
```

**Declare behaviour for every value of `D.shape`.** `one-shot`, `series`, `open sandbox` are not
flavour: a one-shot has no previous log, no arc note, no cross-session rotation and no recap; a
sandbox has fronts where a series has chapters. Every skill states, in Phase 0, what it does for
each of the three — and a skill that cannot serve a value **says so and stops**:

```markdown
`D.shape` = `one-shot` → there is no previous session and no arc to deviate from.
This skill has nothing to operate on: say so and stop. Do not synthesise a history.
`D.shape` = `open sandbox` → read fronts from `C.arc_note`, not a chapter list.
```

Silent degradation is the failure mode here: a skill that quietly produces an empty recap for a
one-shot looks like it worked.

## 3. Descriptions and routing

The `description` is the only thing the router sees. It must contain, **in this order**:
1. the **artifact** produced, 2. an explicit **"Use when …"** trigger phrased the way a user
would ask, 3. the **negative boundary** naming the sibling skill that owns the adjacent job.

Front-load: routers weight the opening tokens and some harnesses truncate, so the artifact and
the trigger come first and stay tight. Do **not** enumerate the skill's contents ("Covers …") in
the description — that is documentation, and it belongs in the body's opening lines, where it
costs routing nothing.

Sibling skills in this package have deliberately adjacent jobs (prep vs. log vs. recap). Without
the negative boundary they collide.

## 4. Principles, not restatements

Cite the principles by tag (`P7 (spotlight rotation)`), do not re-argue them. The full text ships
inside each installed skill as `references/PRINCIPLES.md`; never link to a path outside the skill
folder, because installation copies the folder alone.

**Distinguish requirement from convention.** A rule that prevents a document failing at the table
or state desynchronising is a requirement (P1, P2, P3, P10, P11) and may use absolute language. A
rule that encodes this author's taste in play is a *default* — state it as such, and name
`E.overrides` as the place a campaign switches it off. Do not promote a single remembered failure
into a universal law, and never write "always" about a principle a profile is allowed to disable.

If you find yourself writing a new general rule, add it to PRINCIPLES with an ID and reference it
— one lesson, one home.

## 5. Register

- Imperative, dense, no encouragement, no filler. The reader is an agent under a token budget.
- Prefer a **test** over an adjective: "a GM who never read the source can run it from this alone"
  beats "make it clear".
- Show a **skeleton** for anything the skill produces; skeletons are copied, prose is skimmed.
- Every rule that came from a real failure keeps a one-clause trace of it ("the lesson of the
  session where they fled the boss and the script had no answer"). It is what makes the rule stick.
- Length: the 200–250 line band. Under it a Phase 0 branch is usually missing; over it, split or
  push detail into a reference file in the skill
  folder and link it.

## 6. Overlays

A campaign overlay skill (`templates/overlay-SKILL.md`) may only contain what is **neither a
profile slot nor generalisable**: house aesthetics, this table's recurring behaviour patterns,
literary constraints of a specific form. It must open by delegating to the base skill and must
not restate its procedure. If an overlay grows past a page, the base skill is missing a slot —
fix the base skill instead.

## 7. Changing a skill

1. Change the canonical copy in this repo, never the installed copy.
2. If the change is a general lesson, it goes to PRINCIPLES first, then the skills reference it.
3. If it adds or renames a **profile slot**, change `templates/campaign-profile.md` — the single
   source — and re-copy it to `skills/ttrpg-campaign-setup/references/campaign-profile.md`, which
   is a *bundled copy, not a fork*: that skill drives its interview by walking the file, so a slot
   added to the template reaches the interview the same day. Never hand-copy a slot list into a
   SKILL.md. Then make some skill actually *read* the new slot; a slot nothing consumes is a
   question asked for nobody.
4. Bump `metadata.version`; note the lesson in the commit message.
5. Re-run the agnosticism self-test (§1) on the touched sections. If the change adds or drops a
   requirement that a principle carries, update that skill's `E.overrides` branch in the same
   commit — and check the *Verify* and *What NOT to do* lists, which are where an overridable
   default gets quietly re-imposed as an absolute.
6. If the change touches a **skeleton, a required element or a Phase 0 branch**, update that
   skill's worked example (`references/example-*.md`, §8) in the same commit — an example that
   contradicts its skill is worse than none — and re-check the matching rubric in `tests/evals/`
   (§9), running the eval when the change is behavioural.
7. **Run `python scripts/check_contract.py` from the repo root. It must exit 0. This is a
   mandatory pre-commit step — do not commit red, and do not weaken a check to get green.**
   It is stdlib-only and lives in this repo on purpose: validating a clone must never require a
   tool installed somewhere else on the machine. It absorbs the checks an external skill validator
   would run (frontmatter keys, hyphen-case name, description budget, unfinished `[TODO:`), so
   there is one command, not two.

What the checker enforces mechanically, so you do not have to remember it:

| Check | Fails when |
|---|---|
| `SLOT-RESOLVES` | a skill cites a slot id the template does not define |
| `NO-LEGACY-SLOTS` | a numeric `§n` profile citation survives under `skills/` |
| `BUNDLE-IDENTICAL` | the bundled schema copy has drifted from the template |
| `DEAD-SLOT` | a slot is defined but no consumer skill reads it |
| `PRINCIPLE-RESOLVES` | a cited `Pn` is not defined in `docs/PRINCIPLES.md` (unused principle = warning) |
| `PRINCIPLE-RANGE` | a preamble advertises a range that is not the real ceiling, or the body cites above it |
| `LINK-ESCAPES` | a link points outside the skill folder (`../`, `docs/`, `templates/`) |
| `LINK-BROKEN` | an inward link or a backtick-quoted `references/…` path has no file |
| `FRONTMATTER` | name ≠ folder, no `Use when`, no sibling boundary, over the description budget, encoding damage |
| `SECTION-OWNERSHIP` | two skills define the same domain section heading |
| `NO-SYSTEM-NAMES` | anything shipped names a game system — no exception list: the system is `A.ruleset` |
| `MECHANICS-LEAK` | the vocabulary of one system family appears (`DC`, `HP`, `AC`, saving throw, `d20`, encounter table, combat rounds) — warning |
| `ENCODING` | a shipped markdown file carries U+FFFD or a literal `\uXXXX` escape |
| `OVERRIDE-MAPPED` | a skill mentions `E.overrides` without a branch mapping it to what stops being required |
| `ARTIFACT-CONTRACT` | a skeleton shows a frontmatter placeholder without the fixed `type:` key, or two skills claim the same type value |
| `PHASE0-PROTOCOL` | a consumer skill's Phase 0 lacks the find-the-profile protocol or a `D.shape` branch/gate before Phase 1 |

## 8. Worked examples

A skill that produces an artifact ships one complete example of it in
`references/example-<artifact>.md`, because a model calibrates shape and register from an example
faster than from any number of rules. The rules for writing one:

- **Invented campaign only.** The example campaign, its system, every name and number are made up
  for the example (the current ones share "The Weir Circuit" / "Lantern & Ledger", so prep, log
  and recap show one cycle on one evening). A realistic example gets copied instead of read — the
  same reason the schema's filled excerpt is invented — and it still passes `NO-SYSTEM-NAMES` and
  `MECHANICS-LEAK` like everything shipped.
- **Guard header first.** The file opens with an HTML comment stating it is *a shape, not
  content*, never to be reused literally, followed by the invented profile slots the example
  assumes — so a reader can see which blocks an empty slot would have dropped.
- **Annotated, sparsely.** HTML comments explain *why* a block is the way it is, citing principles
  and slots; a real artifact carries none, and the guard says so.
- **One configuration per example; structural branches get deltas.** A worked example
  instantiates exactly one profile configuration — an example is a de facto default, so a second
  full example covering "the common case" would reintroduce a hardcoded default through the
  strongest teaching channel, and would double the drift surface §7 step 6 has to police. A branch
  that changes the artifact's *structure* (`D.shape`, `A.resource_shape`, `B.distance`, an
  override that removes a section) is covered instead by a 2–5 line `VARIANT —` annotation at the
  branch point: what this block becomes under the other value. Flavour variants need nothing —
  the profile injects the flavour at runtime.
- **Linked from the entrypoint** with the read-once framing, and kept in step with the skill:
  changing a skeleton or a required element without updating the example (§7, step 6) leaves the
  strongest teaching signal contradicting the rules.
- Wikilinks (`[[…]]`) inside example content are invisible to the link checks; markdown links are
  not — do not use them for fictional targets.

## 9. Behavioral evals

`check_contract.py` proves form; `tests/` proves behaviour. `tests/fixture-campaign/` is a full
invented campaign repo with **deliberately seeded defects** (the answer key lives in
`tests/evals/continuity-audit.md`), and `tests/evals/` holds one scenario + rubric per covered
skill. Protocol, coverage and the rules for writing a new eval are in `tests/README.md`.

The two duties this file adds:

- A **behavioural** change to a skill (a phase, a required element, a branch — not wording) is not
  done until its eval passes again, or its rubric is deliberately updated in the same commit.
- A new **seeded defect** in the fixture goes into the answer key in the same commit, or the audit
  eval starts failing for the wrong reason. Never clean the fixture: a clean fixture tests nothing.

Neither is mechanical — the checker cannot grade a prep. That is the point: these are the checks
that need a reader, kept cheap enough to actually run.
