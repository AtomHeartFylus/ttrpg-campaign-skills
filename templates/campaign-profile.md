---
type: campaign-profile
schema: 1
---

# Campaign Profile — <Campaign name>

> This note is the **contract between your campaign and the base skills**. Every skill in
> `ttrpg-campaign-skills` reads it before doing anything, and speaks in the slot names below
> instead of the vocabulary of one game.
>
> **Empty slots are legitimate**: they switch the corresponding sections of a skill *off*.
> Never let a skill invent a slot it cannot find here — it must ask, or drop the section.
> Keep this note short. It is a data sheet, not a setting bible: link out to the long notes.

---

## 1. System

- **Ruleset:** <e.g. D&D 5e + a supplement / Call of Cthulhu 7e / a PbtA hack / diceless>
- **What the rules adjudicate:** <combat, resource attrition, social conflict…>
- **What is left to fiction:** <what you deliberately never roll for>
- **House rules that change GM prep:** <only the ones that change how a session is written>

## 2. Dramatic resource (optional, repeatable)

The mechanic that carries the emotional weight of the campaign. Many campaigns have none —
leave empty and the resource sections disappear from prep and log.

- **Name:** <e.g. Hope / Sanity / Stress / Doom clock / none>
- **Shape:** <per-character value | shared party clock | both> — decides whether the log's exit state
  has one row per character or a single row
- **Scale and starting value:** <e.g. 33 points; 1d4 "spark", 1d6 "glimmer">
- **How it is lost:** <the named triggers>
- **How it is regained:** <the named triggers>
- **Who can hold or receive it:** <asymmetries matter — note them here, they are easy to lose>
- **At zero:** <consequence>
- **Physical handling at the table:** <tokens, tracker, sheet — the gesture is part of the mechanic>

## 3. Tone

- **Dominant register:** <e.g. grim, oppressive>
- **Admitted breaks:** <e.g. flashes of grotesque comedy — and how they must not break atmosphere>
- **The question every scene should raise:** <the campaign's recurring thematic pressure>
- **Hard lines / lines & veils:** <link to the table dossier>

## 4. Canon source (optional)

A text, module or corpus the campaign leans on and quotes.

- **Source text:** <link to the in-repo note or edition>
- **Status:** <verbatim canon / rewritten homebrew / the source does not exist in-world>
- **How it is delivered at the table:** <recorded actor readings / GM reading aloud / paraphrase>
- **Where the recordings live:** <path convention, if any>

## 5. Recurring guide / anchor NPC (optional)

- **Who:** <name and link>
- **Arc:** <what they want across the campaign>
- **Voice in one line:** <the register, so it stays consistent>
- **Per-session obligation:** <e.g. one prepared beat per session, or none>

## 6. Campaign structure

- **Backbone:** <published modules / chapters / fully homebrew / sandbox>
- **Unit of play:** <what a "session" covers>
- **Where the official material lives:** <folder>
- **Where your reworked material lives:** <folder>
- **Relationship between the two:** <how much you deviate, and how deviations are recorded>

## 7. Table conventions

- **Cadence and expected campaign horizon:** <weekly / monthly; ~one year>
- **Table size:** <how many players; the number drives spotlight rotation (P7)>
- **Protagonists per session:** <how many players carry a session, default 2-3; with the table size
  this fixes the rotation period, so nobody stays chorus for longer than it>
- **Hooks harvested per player:** <how many exposed nerves to collect at session zero, default 2-3>
- **How hooks are staged:** <parallels that the player connects on their own | literal appearances
  of the named subject | both, and when each>
- **Absent players:** <the fixed in-fiction convention; do they level?>
- **Safety tools:** <which, and when they are refreshed>
- **Session length and hard stop:** <drives content margin, P8>
- **Language of play and of read-aloud text:** <e.g. Italian at the table, English in the repo>
- **Recording:** <is the table recorded? who has consented? consent is a precondition, not an
  assumption — a skill may not start a capture pipeline without an explicit yes here>
- **Transcript visibility:** <GM-only / shared with players — off-game notes especially>

## 8. Player-facing outputs

- **Opening recap:** <form: in-fiction prose / verse / none; who reads it>
- **Reading-time ceiling:** <how long the recap may run when read aloud, e.g. 3-5 minutes, or a
  form-native unit like a strophe count — this is a table fact, not a literary one>
- **In-fiction identity of the characters:** <the name the recap calls each protagonist — real
  name, role, epithet? The per-character value lives as a property in the player dossier; this
  slot only declares the *rule*>
- **Player-facing reference:** <cheat sheet note, if any>
- **What players may read of the repo:** <so prep can hold secrets safely>
- **Where GM-only material lives:** <required whenever players can read the repo: a private folder,
  a separate repo, an ignored path. A skill must never improvise this location>

## 9. Repository conventions

- **Vault / repo root and folder map:** <table of folder → content>
- **Note granularity:** <e.g. one note per entity, small and linked>
- **Link syntax:** <e.g. Obsidian wikilinks `[[Folder/Note|alias]]`, slash separators, escaped pipes in tables>
- **Frontmatter conventions:** <tag families; which values are properties and therefore the single
  source of truth (P10)>
- **State single-source-of-truth locations:** <which note holds which tracked value>
- **Verification command:** <e.g. `python scripts/link_check.py .` — invariant: 0 broken links>
- **Naming rules:** <file naming, forbidden characters>
- **Portability:** <how this repo reaches the other machines you work from (git remote, sync folder)
  and where the canonical copies of skills/overlays live inside it. All persistent campaign memory
  lives in files here — never in account-bound memory or one chat's context>
- **Declared exception to link-don't-copy:** <which documents may inline source material and which
  must stay linked — by default, prep documents inline everything except stat blocks (P1)>
- **Session capture paths (only if §7 declares recording):**
  - raw audio folder — large, **ignored by version control**
  - transcript folder — text, **versioned** (readable transcript + timecoded subtitle file)
  - off-game curation note path
  - naming rule tying audio, transcript and session number together

## 10. Working agreements with the assistant

Standing preferences that are not campaign facts but change how the work is done.

- **Default deliverable:** <a saved note in the repo, vs. a draft in chat>
- **Review posture:** <how blunt; whether unsolicited improvement is wanted>
- **What to never do without asking:** <e.g. rename or reorganise existing notes>
- **Retroactivity:** <may past material be corrected for consistency?>

---

## Filled example (excerpt)

> **Dramatic resource — Hope.** 33 points per character. Lost by accepting a sin (cost 2),
> by dying, by circle-specific hazards. Regained through acts of mercy, familiar spirits,
> inspiration, surviving your own circle. **Asymmetry:** the damned cannot receive it; noble
> spirits can, at half the donated amount. At zero: a despair roll, three per campaign, failure
> is permanent loss. At the table it lives in physical tokens handed across the table.

> **Recurring guide — Galileo.** Wants to see the stars again; a Limbo soul who does not know
> whether he can cross the final threshold. Learned but never doctrinal; explains by observation
> and measure. One prepared beat per session.
