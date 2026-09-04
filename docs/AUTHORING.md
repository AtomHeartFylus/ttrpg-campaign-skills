# Authoring rules for skills in this package

Read this before writing or modifying any `skills/*/SKILL.md`. Consistency between skills is
what makes the package usable; the router picks between them on descriptions alone.

---

## 1. The agnosticism contract

A base skill **must not name a game system, setting, mechanic or character**. It names
**profile slots** (see `templates/campaign-profile.md`):

| Never write | Write |
|---|---|
| "Hope triggers" | "triggers for the dramatic resource (profile §2)" |
| "the Galileo beat" | "the recurring guide's prepared beat (profile §5), if the profile declares one" |
| "the Dante tercet" | "the canon quote (profile §4), with its declared delivery mode" |
| "Sessioni/Sessione N - Diario.md" | "the session log note, at the path the profile declares (§9)" |

**Graceful degradation is mandatory.** For every profile-dependent section, state what happens
when the slot is empty: usually *drop the section*, sometimes *ask the user once*. Never invent.

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
<Which slots this skill needs; what to do for each missing slot.>

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

## 3. Descriptions and routing

The `description` is the only thing the router sees. It must contain:
1. the **artifact** produced, 2. an explicit **"Use when …"** trigger phrased the way a user
would ask, 3. the **negative boundary** naming the sibling skill that owns the adjacent job.

Sibling skills in this package have deliberately adjacent jobs (prep vs. log vs. recap). Without
the negative boundary they collide.

## 4. Principles, not restatements

Cite the principles by tag (`P7 (spotlight rotation)`), do not re-argue them. The full text ships
inside each installed skill as `references/PRINCIPLES.md`; never link to a path outside the skill
folder, because installation copies the folder alone.

**Distinguish requirement from convention.** A rule that prevents a document failing at the table
or state desynchronising is a requirement and may use absolute language. A rule that encodes this
author's taste in play is a *default* — state it as such, and say which profile slot overrides it.
Do not promote a single remembered failure into a universal law.} If you find
yourself writing a new general rule, add it to PRINCIPLES with an ID and reference it — one
lesson, one home.

## 5. Register

- Imperative, dense, no encouragement, no filler. The reader is an agent under a token budget.
- Prefer a **test** over an adjective: "a GM who never read the source can run it from this alone"
  beats "make it clear".
- Show a **skeleton** for anything the skill produces; skeletons are copied, prose is skimmed.
- Every rule that came from a real failure keeps a one-clause trace of it ("the lesson of the
  session where they fled the boss and the script had no answer"). It is what makes the rule stick.
- Length: aim under 250 lines. Over that, split or push detail into a reference file in the skill
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
3. Bump `metadata.version`; note the lesson in the commit message.
4. Re-run the agnosticism self-test (§1) on the touched sections.
