---
name: ttrpg-campaign-setup
description: "Bootstrap a campaign repository and produce its filled campaign-profile.md — the contract the other ttrpg-* skills read — or adopt and audit a repo that already has material. Use when starting a campaign vault, filling or revising the campaign profile, or checking that an existing campaign's conventions are coherent. Does not run session zero or write player dossiers (see ttrpg-table-dossier), write session prep (see ttrpg-session-prep), or chase narrative drift and dangling threads (see ttrpg-continuity-audit)."
license: MIT
metadata:
  author: ttrpg-campaign-skills
  version: "1.0"
---

# Campaign setup

Produces the **filled `campaign-profile.md`** — the contract every other skill in this package
reads first — plus the folder skeleton, the state hub and the conventions the profile declares.
Read by an agent that starts cold on a machine it has never seen before.

> **The deliverable is the profile.** Folders, hubs and scripts are what the profile's answers
> imply. If you finish with a beautiful skeleton and an unfilled profile, you produced nothing.

---

> Principles are cited below by tag (`P1`…`P12`); their full text is in
> [references/PRINCIPLES.md](references/PRINCIPLES.md), bundled into this folder at install time.

## Phase 0 — Pick the mode

| Situation | Mode | What you do |
|---|---|---|
| Empty or near-empty repo | **Bootstrap** | Phases 1–3, in order |
| Repo already holds real material, no profile | **Adoption** | Phase 3bis first, then write the profile to match what is already there |
| Profile exists | **Audit** | Phase 4 only: declared conventions vs. actual state; report drift, change nothing without asking |

Never mix modes silently. Say which one you are in before the first question or the first write.

## Phase 1 — Read before writing

1. **Whatever exists already** — file tree, `README`, any conventions note. Two minutes of `ls`
   and `rg` prevents an interview that asks what the repo already answers.
2. **`templates/campaign-profile.md`** — the slot list is the interview script; do not reorder it.
3. **The GM's own words** for the campaign: an existing pitch, a chat, a hand-written page. Mine
   answers from it *and then confirm them* — an inferred slot value is a guess until the GM says yes.

If the repo is not under version control or has no sync path to the GM's other machines, flag it
now: the portability rule (Phase 3) is unenforceable without it.

## Phase 2 — The interview, slot by slot

Walk the profile **in order**, one slot at a time, in short batches. For each slot: ask, record the
answer in the GM's own vocabulary, move on. Do not fill a slot the GM did not answer.

**Empty is an answer.** Write `none` (or `not decided yet — ask before assuming`) into the slot.
That is a load-bearing distinction:

| Slot content | Meaning for every downstream skill |
|---|---|
| `<placeholder text>` | never asked → **stop and ask** before producing anything that needs it |
| `none` | asked, answered empty → **drop the corresponding section**, silently and permanently |
| a value | use it, in the GM's wording |

| Slot | Ask | If empty |
|---|---|---|
| §1 System | ruleset; what the rules adjudicate; what is deliberately never rolled for; only the house rules that change how a session is *written* | ask once — nearly every skill needs it |
| §2 Dramatic resource | is there a mechanic carrying the emotional weight? scale, loss and regain triggers, **who may hold or receive it**, at zero, physical handling | drop resource sections everywhere. Never invent one |
| §3 Tone | dominant register; admitted breaks and how they must not break atmosphere; the question every scene should raise; hard lines | ask the register at least; leave the rest empty |
| §4 Canon source | is there a text or corpus the campaign quotes? verbatim or reworked; does it exist in-world; delivery mode; where recordings live | no quote blocks anywhere |
| §5 Recurring guide | is there an anchor NPC travelling with the party? arc, voice in one line, per-session obligation | no beat section in prep |
| §6 Structure | published backbone or homebrew; unit of play; where official vs. reworked material lives; how deviations are recorded | treat the campaign as fully homebrew |
| §7 Table conventions | cadence and horizon; table size; absent-player rule; safety tools and refresh; session length; language of play vs. language of the repo | table size and cadence must be asked — they drive P7 and P8. The rest is `ttrpg-table-dossier`'s session zero |
| §8 Player-facing outputs | opening recap form and who reads it; player cheat sheet; **what players may read of the repo** | assume players read nothing, and say so — prep may then hold secrets |
| §9 Repo conventions | folder map; note granularity; link syntax; frontmatter/tag families; which values are properties; verification command | Phase 3 produces these; write back every decision |
| §10 Working agreements | default deliverable (saved note vs. chat draft); how blunt the review; what never to do without asking; is retroactive correction allowed | default to: save notes in the repo, ask before renaming or reorganising anything |

**Asymmetries are the thing GMs forget to state.** For §2 especially, ask explicitly *who cannot
receive or hold the resource* — the lesson of the table that spent a session's emotional climax
donating a resource to recipients structurally unable to receive it, because the rule lived in a
second rulebook and nowhere in the repo.

## Phase 3 — What the answers imply

### 3.1 Folder skeleton
One note per entity, **small and linked**, never monolithic documents. Folder names in the language
the profile declares for the repo (§7). Create only what the answers justify:

```
<repo root>/
  campaign-profile.md        # the contract; §9 declares everything below
  <state hub>.md             # single source of truth for current state (P10)
  <sessions>/                # prep + log, one pair per session, progressively numbered
  <people>/                  # one note per PLAYER — see ttrpg-table-dossier
  <entities>/                # one note per NPC / creature / faction
  <places>/                  # one note per location, at the granularity §6 implies
  <items>/                   # only if §1 makes items significant
  <official>/  <reworked>/   # only if §6 declares a published backbone it deviates from
  <player-facing>/           # only what §8 says players may read
  <recaps>/                  # only if §8 declares an opening recap form
  assets/                    # media; declare in .gitignore what is too large to version
  scripts/                   # the verification command of §9
```

Write the resulting map into §9 as a folder → content table, and say **where each kind of new note
goes**. An agent that cannot answer "where does this note belong?" from the profile will invent a
folder, and the second folder for the same thing is how a vault dies.

### 3.2 The state hub (P10)
Exactly one note is the campaign's current state. It holds **only what does not live as a property
of an entity note**: where the party is, last session played, open threads, unresolved obligations,
what comes next.

- Values tracked per entity (advancement, resources, position, status — whatever §1 makes worth
  tracking) live **only** in that entity's note, as frontmatter properties, and are *read* here
  through a live view or query.
- **Static roster tables are forbidden** in the hub, in indexes and in prep. They desynchronise on
  the first update and then lie confidently.
- If the tooling has no query/view mechanism, the hub links to the entity notes and states the
  values are *there*. A link that forces one click beats a table that is wrong.
- Record in §9 which note is the hub and which note owns which tracked value.
- Single-session play (§6 unit of play = the whole campaign): the hub collapses into the prep note.
  Say so in §9 rather than creating an empty hub.

### 3.3 Frontmatter, tags, links, names
Decide once, write into §9, apply everywhere:

- **Tag families** with the type in the namespace (`<kind>/<subkind>`), declared as a closed list.
  A tag that exists in one note only is a typo until proven otherwise.
- **Properties vs. body:** every tracked value is a property (P10). Prose in the body, state in the
  frontmatter.
- **Link syntax** written literally in §9, including the awkward cases (path separators, aliases,
  escaping inside tables, how attachments are embedded). Ambiguity here produces silent breakage.
- **File naming:** allowed separators and **forbidden characters** — the lesson of the vault where
  an en-dash instead of a hyphen broke every link to a note without a single error message.
- **Search before creating.** Update the existing note; do not create a near-duplicate.
- **Link, don't copy** is the vault-wide rule. The single declared exception is the session prep
  document (P1) — record the exception in §9 so nobody "fixes" it later.

### 3.4 Verification command and invariant
Install a link/reference checker in `scripts/`, and record in §9 the exact command plus its
invariant — typically **0 broken links**, covering embedded attachments as well as notes.

- Run it once at setup, on the current repo, and report the number. A checker whose baseline is
  already red is not an invariant, it is decoration.
- Every skill in this package ends its verify phase with this command; if you cannot install one,
  write `verification: none — invariant unverifiable` into §9 rather than naming a command that
  does not exist.

### 3.5 Portability — all memory lives in files in the repo
**Every persistent fact about this campaign must exist as a file inside the repo.** The profile,
the conventions, the state hub, the dossiers, the working agreements of §10, and the canonical copy
of any campaign-specific skill or overlay (keep it in-repo and *install* from there; fix the
canonical copy first, never the installed one).

Never store campaign memory in an account-bound assistant memory, a harness setting, a local config
or the context of one chat. The same campaign is worked on from **different machines, harnesses and
models** — anything not in the repo does not exist for the next agent.

*Test:* a fresh agent, on another machine, with a different model, given only a clone of this repo
and no conversation history, can prepare the next session. Anything that fails this test is a bug
in the repo, not a limitation of the agent.

## Phase 3bis — Adoption mode (the repo already has material)

The existing repo is **the authority on its own conventions**. Your job is to describe it, not to
improve it.

1. **Inventory before opinions.** File tree with counts per folder; frequency of frontmatter keys
   and of tags; a sample of link forms; file-naming patterns. `rg -o` over the vault (or the
   equivalent) gives all four in a minute — do not read a large vault note by note.
2. **The majority pattern is the convention.** Whatever most notes actually do goes into §9, in the
   repo's own vocabulary, even where you would have chosen otherwise. Minority forms are *gaps*,
   not errors to fix.
3. **Write the profile to match reality.** Slots the material answers (folder map, tag families,
   granularity, link syntax, backbone) get filled by observation and then **confirmed** with the GM.
   Slots only the GM can answer (tone, dramatic resource, table conventions, working agreements)
   are asked, never inferred from vibes.
4. **Report the gaps, do not close them.** One ranked list: inconsistent tag or naming forms with
   counts, duplicate notes for one entity, state duplicated outside its source of truth, broken
   links, folders with no declared purpose. For each, a one-line proposed fix and the cost. Then
   stop.
5. **Never rename, move, merge or reorganise an existing note without asking** — record that rule
   in §10 so every later skill inherits it. Adoption that silently reshapes a working vault is the
   single fastest way to lose a GM's trust and their muscle memory.

## Phase 4 — Verify

- The profile has **no leftover placeholders**: every slot holds a value or an explicit `none`.
- Each `none` was *asked*, not assumed.
- §9 answers, without further conversation: where does a new note of each kind go, what is the link
  syntax, which values are properties, which note is the state hub, what is the verification
  command and its invariant.
- The state hub contains no static roster table; no tracked value appears in two places (P10).
- The verification command runs and meets its declared invariant; report the actual number.
- Portability test passes: nothing needed for the next session lives outside the repo.
- Adoption mode only: the profile describes the repo **as it is**; the gap list was reported and
  nothing was renamed, moved or reorganised.

## What NOT to do

- Do not invent a slot value, and do not "reasonably assume" one. Ask, or write `none`.
- Do not leave a template placeholder in a delivered profile — downstream skills read it as
  "never asked" and stall.
- Do not build folders for material the profile does not declare.
- Do not create a static roster or state table anywhere, however convenient.
- Do not name a verification command you have not run.
- Do not store any campaign fact outside the repo — not in an assistant memory, not in a local
  setting, not in this conversation.
- Do not restructure an existing vault to match this skeleton. Adopt it, report the gaps, ask.
- Do not turn the profile into a setting bible: it is a data sheet that links out.
