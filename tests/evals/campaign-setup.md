# Eval — ttrpg-campaign-setup

Two scenarios: the standard bootstrap on an empty folder (Scenario A) and the conversational "draft
in chat" bootstrap sub-mode (Scenario B) added by W21b.

---

### Scenario A — bootstrap on empty folder

The only eval that runs on an **empty folder**, not on the fixture. It needs a scripted GM: the
grader answers the interview from the script below, and refuses to elaborate beyond it.

Setup: an empty temp folder as working directory.

Prompt (verbatim):

> I'm starting a new campaign and want this folder set up properly. Interview me.

GM script — answer only what is asked, with only this:

- System: "a homebrew d6 thing we call Driftwood, advancement by deeds"
- Resource: "Grit — you lose it when you back down, get it back around a fire. Everyone has 4."
- Table: 5 players, monthly, ~10 sessions, 3 hours with a soft stop
- Shape: series, fully homebrew
- Tone: "salt-western, jokes allowed"
- Recap: "no recap, we just start"
- For anything about safety tools, distance, absences or player access: **"we'll settle that at
  session zero"**
- For anything else: "no preference — whatever is standard"

### Rubric

REQUIRED — every box, or the eval fails:

- [ ] Searches for an existing profile before interviewing (empty folder → proceeds to create).
- [ ] Walks the **bundled schema** and produces a `campaign-profile.md` with `type:
      campaign-profile`, sections A–E, slots cited by name.
- [ ] Before asking anything, offers both paces explicitly — full walk vs. quick start — with the
      real slot/`(core)` counts read from the bundled schema (not a number written into the
      skill), and lets the GM choose rather than inferring it from tone. This scenario's GM never
      asks for either, so the offer must come from the agent unprompted.
- [ ] Session-zero answers are recorded as **`deferred: session zero`** (`B.distance`, `B.safety`,
      `B.absence` at minimum) — never guessed, never written as `none`, never left as raw
      placeholders after being asked.
- [ ] Closing report says, for each slot written `deferred: session zero`, what stalls if session
      zero is skipped — sourced from `session-prep`/`table-dossier`/`table-recap`'s own Phase 0
      tables (e.g. prep will ask once before aiming a scene at a hook, or before running a heavy
      scene), not invented wording.
- [ ] "No preference" answers: the slot is either filled with the declared `default:` where the
      schema carries one (said out loud), or left honestly empty — **no invented values** (no
      made-up naming rules, no invented verify command, no fabricated overrides).
- [ ] `D.recap` records **none** (asked and answered) — which is different from empty.
- [ ] The repo skeleton matches what the answers imply (folders for sessions/dossiers/entities or
      equivalent, per its own `C.root` map) — and nothing more.
- [ ] Consent slots (`B.consent_recording`, `B.consent_offgame`) are not silently defaulted to
      anything; unasked-and-unanswered reads as unanswered.
- [ ] `C.verify` (Phase 3.4): the agent **proposes** copying the bundled `check_links.py` into
      `scripts/` and registering it as the command — it does not create the file or write the
      command as a side effect of "whatever is standard". If the GM's answer does not amount to an
      explicit yes to adding that script, `C.verify` reads `none — invariant unverifiable`, not an
      invented or silently-installed command.
- [ ] The GM's own words survive into the slots ("Grit", "backing down", "around a fire") instead
      of being normalised into generic phrasing.
- [ ] **Closes with the run report** (P14): declared defaults used and where declared, overrides
      honoured, inputs unavailable, language chosen, commands run with their real output — in the
      reply, never inside the artifact.

SHOULD — quality signals, note misses:

- [ ] Ends by saying which skills are now unblocked and that session zero (`ttrpg-table-dossier`)
      is the declared next step for the deferred slots.
- [ ] Interview is paced (grouped questions, not 61 at once).

---

## Scenario B — bootstrap draft in chat (W21b)

Setup: an empty temp folder as working directory. `E.deliverable` is set to `draft in chat`.

Prompt (verbatim):

> I'm starting a new campaign called "The Weir Circuit" but I don't want to write any files yet. Let's do the interview.

### Rubric

REQUIRED — every box, or the eval fails:

- [ ] **Opening declaration is present** — starts with "Running without a full profile — Bootstrap draft mode." (W21b)
- [ ] **Scope list is present** — lists the slots it intends to ask on the fly so the GM sees them up front. (W21b)
- [ ] Offers both paces explicitly (full vs. quick start) before diving into questions.
- [ ] **No files are written** to the working directory — the draft profile is delivered as a chat reply only. (W21b)
- [ ] **Consent is requested** — explicitly offers to record the confirmed answers into the profile only with consent, and does not write without it. (W21b)
- [ ] **Closes with the run report (P14)**: includes which slots were asked on the fly, which are `deferred: <when>`, and which are empty (`none`). (W21b)

---

## Machine-checked boxes

`tests/run_eval.py` prepares the work copy and ticks the boxes below; everything in the rubrics
above still needs a reader. Scenario B is chat-only in the fixture (no file is written), so its
mechanical checks are limited to absence-of-repo-writes.

<!-- eval-spec
{
  "skill": "ttrpg-campaign-setup",
  "fixture": "fixture-empty",
  "scenarios": {
    "A": {
      "prompt_index": 0,
      "setup": [],
      "artifact": {
        "type": "campaign-profile"
      },
      "mechanical": [
        {
          "id": "profile-created",
          "kind": "file-exists",
          "glob": "**/campaign-profile.md",
          "cite": "Phase 2"
        },
        {
          "id": "type-key",
          "kind": "frontmatter",
          "key": "type",
          "equals": "campaign-profile",
          "cite": "Phase 2",
          "why": "how every other skill finds this file, whatever it is named"
        },
        {
          "id": "session-zero-deferrals",
          "kind": "regex",
          "pattern": "(?i)deferred:\\s*session zero",
          "min": 3,
          "cite": "four-state rule",
          "why": "B.distance, B.safety, B.absence at minimum - never none, never a guess"
        },
        {
          "id": "recap-answered-none",
          "kind": "regex",
          "pattern": "`D\\.recap`\\*\\*[^\\n]*\\bnone\\b",
          "min": 1,
          "i": true,
          "cite": "D.recap",
          "why": "asked and answered empty is not the same as never asked"
        },
        {
          "id": "no-todo-placeholders",
          "kind": "regex",
          "pattern": "\\[TODO:",
          "min": 0,
          "max": 0,
          "cite": "Phase 2"
        }
      ]
    },
    "B": {
      "prompt_index": 1,
      "setup": [],
      "artifact": {
        "type": "campaign-profile"
      },
      "mechanical": [
        {
          "id": "no-file-written",
          "kind": "file-exists",
          "glob": "**/campaign-profile.md",
          "min": 0,
          "max": 0,
          "cite": "W21b",
          "why": "draft in chat sub-mode must not write files to the repo"
        }
      ]
    }
  }
}
-->
