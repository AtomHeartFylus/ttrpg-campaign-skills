# Verdicts — the C6 rerun of `campaign-setup` Scenario B

Companion to `20260906-181016-campaign-setup-B-claude-sonnet-5.json` and to the verbatim
deliverable in `20260906-180948-campaign-setup-B-claude-sonnet-5-reply.md`.

**This is not a human verdict.** `verdicts-W20.md` is the reader's half, ticked by a person. What
follows is a *second-model* ruling (`claude-opus-5`, given the rubric and the reply and nothing
else), plus a mechanical re-verification of its factual claims done in the repo. It is evidence a
human reader can check quickly, not a substitute for one. Where the two disagree, the mechanical
recount below wins.

## Why this run exists

The previous record for this scenario was deleted deliberately: it named a model
(`deepseek-v4-flash-vision-exp`) whose artifact was no longer verifiable. This rerun records the
model actually used (`PI_MODEL=claude-sonnet-5`) and keeps the deliverable.

**Scenario B is chat-only, and that is a trap for the record.** The correct behaviour is that
nothing is written to the work directory — so `changed` is empty, so the harness's `-files/`
sidecar has nothing to save, so the only thing the run produced (the reply) would not survive the
Temp directory at all. The deleted record had solved this by writing `draft-reply.txt` *inside* the
work directory, which makes the record judgeable by falsifying the very behaviour under test (the
rubric box reads "**No files are written** to the working directory"). Here the work directory was
left pristine — verified twice, before and after grading: it holds only `fixture-empty/README.md` —
and the reply is preserved as a sibling file in `tests/results/`. A chat-only eval keeps its
evidence in `-reply.md`, not in `-files/`.

## Mechanical box

`no-file-written` — passed. Re-graded independently after recording, same result: `changed`,
`deleted` and `artifacts` all empty, 1/1.

## The six REQUIRED boxes — ruling: PASS 6/6

| # | Box | Ruling | Evidence |
|---|---|---|---|
| 1 | Opening declaration present, starting with "Running without a full profile — Bootstrap draft mode." | PASS | First line of the reply proper, alone on its line, verbatim, no preamble |
| 2 | Scope list present — the slots it intends to ask on the fly | PASS | The `**Scope …**` block enumerates the schema by section. Recounted against the bundled schema with the checker's own slot rule: **all 61 slots are named, none invented, none omitted**, and the `(core)` marks land on exactly the 12 the schema marks |
| 3 | Offers both paces explicitly (full vs. quick start) before any question | PASS | `**Before we start: which pace do you want?**` with `**Full walk**` and `**Quick start**` both labelled, before the first interview question, plus `I won't infer this from how much time you sound like you have` |
| 4 | No files written — draft delivered in chat | PASS | Mechanically confirmed; the reply narrates no write and states the folder "stays exactly as it is now: just `README.md`" |
| 5 | Consent requested — offers to record only with consent, does not write without it | PASS | "only once you've looked it over and said yes, will I offer to save the confirmed answers into the file", reinforced in the opening paragraph |
| 6 | Closes with the P14 run report: asked on the fly / `deferred: <when>` / `none` | PASS, on the ruling below | All three categories present as separately named lines, in the schema's own vocabulary, each with a reason |

### The box 6 ruling, and why it is a judgement call

At the moment a single-turn reply ends, no slot has been asked *and answered*, so the honest
content of all three lists is empty. The report says so per category, with a reason each, and
pre-commits the five session-zero slots and the condition that would move them into the deferred
bucket. Any non-empty list here would have been fabricated — the exact failure P14 exists to
expose. Marking the run down for refusing to invent entries would reward the opposite behaviour
next time, so: PASS.

But the box's discriminating power — does the agent *maintain* the three-way partition as slots
get filled — is untestable by construction in a single-turn scenario. **This is a rubric gap, not
a run defect.** Closing it means either scripting a second turn for Scenario B (the GM picks quick
start, answers three slots, defers one to session zero, answers `D.recap` with none) so the three
lists must come back non-empty, or amending box 6 to say that an empty category must be stated
with a reason rather than omitted.

## A defect no box covers, found by re-verification

The reply states, correctly and carefully: "58 slot bullets in all, 12 of them marked `(core)` —
read straight from that file". Counted with the checker's own rule, the bundled schema has exactly
**58 bullets carrying at least one slot**, and exactly **12 `(core)` marks**. Both true.

One line later it offers: "**Full walk** — all 58 slots". That silently reuses a *bullet* count as
a *slot* count. Six bullets carry two slots each (`A.resource_loss` / `A.resource_gain`,
`C.arc_note` / `C.thread_ledger`, `C.gm_private` / `C.player_access`,
`D.official_material` / `D.own_material`, and two more), so the schema defines **61** slots — the
number `check_contract.py` prints on every run. The scope list itself is complete: all 61 are
named. Only the summary number is wrong.

Two things make this worth recording rather than shrugging off:

1. No REQUIRED box catches it. Box 2 asks for the list (complete), box 3 asks for the offer
   (present). A wrong count sits between them, and a "full walk" that advertises 58 of 61 is the
   kind of understatement a GM would only discover mid-interview.
2. **The second-model judge confirmed the wrong number**, recounting it as `11 §A + 15 §B + 15 §C
   + 11 §D + 6 §E = 58` — the same bullet-for-slot conflation, reached independently. Two models
   agreeing is not verification; running the schema through the parser that owns the definition
   is. That is the reason this section exists.

## Note to a future reader

Boxes 1–5 are trustworthy without caveat. Box 6 passed on an *empty-but-labelled* report: treat
this run as evidence that the model formats the three-way partition correctly, and as no evidence
that it maintains it across a filled interview. Do not cite it as proof of `deferred:`/`none`
tracking under load, and do not cite the reply's "58 slots" — the schema has 61.
