---
eval: campaign-setup-B
model: claude-sonnet-5
when: 20260906-180948
---

Running without a full profile — Bootstrap draft mode.

**Phase 0 — search.** I looked for an existing profile first: `find . -name campaign-profile.md`
and a grep for `type: campaign-profile` across the folder, in case it was renamed. Both came back
empty — the only file here is `README.md`, and it isn't one. So there's no profile to adopt, and
`E.deliverable` is set to *draft in chat* here, which means: I run the Bootstrap interview
conversationally, and what you get at the end is the filled profile **as this conversation's
reply**, not a file on disk. Nothing gets written to this folder unless you explicitly ask me to,
and even then only the parts you've confirmed.

**Scope — what I'll ask you, on the fly, since nothing here answers any of it for me:**

- **§A Game** — `A.ruleset` *(core)*, `A.adjudicated`, `A.fiction`, `A.houserules`, `A.resource`
  *(core)* and its family (`A.resource_shape`, `A.resource_scale`, `A.resource_loss` /
  `A.resource_gain`, `A.resource_asymmetry`, `A.resource_zero`, `A.resource_handling`).
- **§B Table** — `B.size` *(core)*, `B.protagonists` *(core)*, `B.cadence`, `B.horizon`,
  `B.length`, `B.absence`, `B.distance` *(core)*, `B.safety` *(core)*, `B.consent_recording`,
  `B.consent_offgame`, `B.frame`, `B.retention`, `B.hooks_count`, `B.hooks_staging`,
  `B.language`.
- **§C Repository** — `C.root` *(core)*, `C.granularity`, `C.links` *(core)*, `C.frontmatter`,
  `C.blocks`, `C.state_locations`, `C.hub`, `C.arc_note` / `C.thread_ledger`, `C.verify`,
  `C.naming`, `C.portability`, `C.inline_exception`, `C.gm_private`, `C.player_access`,
  `C.capture_paths`.
- **§D Shape and content** — `D.shape` *(core)*, `D.backbone`, `D.unit`, `D.official_material` /
  `D.own_material`, `D.deviation_policy`, `D.endgame`, `D.canon_source`, `D.guide`, `D.tone`
  *(core)*, `D.recap` *(core)*, `D.identity`.
- **§E Overrides and agreements** — `E.overrides` *(core)*, `E.deliverable` (already set: draft in
  chat), `E.review`, `E.never_without_asking`, `E.retroactivity`, `E.audit_cadence`.

That's every slot in the bundled schema (`references/campaign-profile.md`) — 58 slot bullets in
all, 12 of them marked `(core)` — read straight from that file, not a number I'm carrying around
in my head.

**Before we start: which pace do you want?**

- **Full walk** — all 58 slots, in schema order, §A through §E. Nothing skipped, nothing
  batched away for "looking optional."
- **Quick start** — only the 12 `(core)` slots plus their direct dependents (a value on
  `A.resource` pulls in its whole resource family; a value on `D.recap` pulls in its reading-time
  ceiling). Everything else is left as an untouched placeholder — not `none`, just genuinely
  unasked — until the first skill that needs one stops and asks it back to you. Five of those
  slots (`B.distance`, `B.safety`, `D.tone`, `C.player_access`, `B.absence`) get written
  `deferred: session zero` rather than skipped outright if you'd rather settle them at the table
  than guess now.

I won't infer this from how much time you sound like you have — tell me which one, and we'll go
section by section, 3–5 slots per message, in the schema's own order and wording.

One more thing up front, since we're in draft mode: at the end of this, I will not write
`campaign-profile.md` — or anything else — into this folder on my own. I'll show you the filled
draft here in chat, and only once you've looked it over and said yes, will I offer to save the
confirmed answers into the file. Until you say that yes, the folder stays exactly as it is now:
just `README.md`.

---

**Run report**
- Defaults used: none — no slot has been answered yet, so no `default:` value (`B.hooks_count`,
  `C.inline_exception`, `D.recap`'s ceiling, `E.audit_cadence`) has come into play.
- Overrides honoured: none yet — `E.overrides` hasn't been asked; nothing has been switched off.
- Inputs unavailable: no existing profile, README, pitch or chat log to mine answers from — the
  folder holds only the fixture `README.md`; every slot above will be asked on the fly rather than
  inferred.
- Asked on the fly so far: none — this is the opening message; the interview itself starts once
  you pick a pace.
- Deferred (`deferred: <when>`): none written yet — the five session-zero slots
  (`B.distance`, `B.safety`, `D.tone`, `C.player_access`, `B.absence`) will get
  `deferred: session zero` only if and when you tell me the table hasn't settled them.
- Empty (`none`): none written yet — nothing has been asked and answered empty.
- Language: no repo content to infer a language from yet; I'm writing in the language you opened
  the conversation in and will say so again, and ask, if that ever needs confirming.
- Commands run: `find . -name campaign-profile.md` → no output (no match); grep for
  `type: campaign-profile` across the folder → no output (no match). No file was created, moved,
  or modified.
