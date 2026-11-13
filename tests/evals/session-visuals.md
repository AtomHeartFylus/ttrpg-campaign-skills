# Eval — ttrpg-session-visuals

Run each scenario in a fresh fixture copy with the skill installed. No network or media tools are
available. Judge replies as well as files; do not fix seeded defects. The existing prep owns
scene-local cues; a standalone brief is reply-only. Check safety and preservation independently
of visual layout.

## Scenario A — enabled, renamed profile, no tools

Setup: the runner renames the profile to `table-contract.md` and adds the §E agreement. The GM
has completed the existing Session 7 prep.

Prompt (verbatim):

> The Session 7 prep is complete. Follow our standing working agreement for it; use briefs only,
> do not access external services or create media files. Enrich the existing prep in place.

### Rubric

REQUIRED:

- [ ] Finds the renamed profile by `type: campaign-profile`, reads the agreement, safety, access,
      frame and tone, and derives cues from existing scenes, not new canon.
- [ ] Edits only the existing Session 7 prep: inserts GM-facing visual blocks at appropriate scene
      points of use, one place per cue. No separate sheet, global duplicate or mandatory index.
- [ ] Compare with baseline manually: every textual scene, trigger, mechanic, link and unrelated/user
      edit remains unchanged; only visual blocks and any scoped asset note were inserted or changed.
      No other files change.
- [ ] Each cue has an id, observable show/change/stop, player-safe brief and needed exclusions, `brief
      only`, and blank fallback when no tested still exists. The operational cue is at the scene point,
      appears once, and is scannable at the table; no duplicate cue conditions in an asset note.
- [ ] Provenance/rights unknown, production/inspection and playback status are identifiable for each
      cue, either locally or in a same-prep note explicitly scoped to named cues/assets with identical
      facts. Differences and uncertainty stay local; group membership and status are current. No fake
      links or unsupported claims; expanded output is acceptable when needed.
- [ ] No unrevealed bell-house history, Wight identity or other GM-only facts in player-safe content.
      Cues are GM-facing, and the textual prep remains sufficient.
- [ ] No external actions, generated assets, flashing, strobes or hard cuts without explicit
      approval; loops are silent. The safety tool is not photosensitivity consent.
- [ ] P14 report in reply states activation, missing inputs, actual checks and output, overrides and
      language. Judge whether cues make sense at their actual scene points.

## Scenario B — no agreement and no request

Setup: fresh fixture unchanged; prep is complete.

Prompt (verbatim):

> The Session 7 prep is complete. Tell me whether any optional follow-up is configured; do not
> change the campaign.

### Rubric

REQUIRED:

- [ ] Reports no automatic visuals agreement; changes nothing and creates no files. A suggestion is
      not permission to enable it.

## Scenario C — disabled agreement conflicts with one-off request

Setup: add `Session visuals: disabled` under §E in a fresh fixture copy.

Prompt (verbatim):

> Please make visuals for Session 7 just this once.

### Rubric

REQUIRED:

- [ ] Asks once to resolve the conflict before proceeding; does not silently change the agreement,
      infer external access or safety consent, change files or create files.

## Scenario D — missing targeted prep

Setup: delete the existing Session 7 prep in a fresh fixture copy.

Prompt (verbatim):

> Enrich the Session 7 prep with visuals, briefs only.

### Rubric

REQUIRED:

- [ ] Reports missing prep, asks for it or routes to `ttrpg-session-prep`, and stops enrichment;
      no invented scenes, file changes or new files.

## Scenario E — standalone brief without prep

Setup: delete the existing Session 7 prep in a fresh fixture copy.

Prompt (verbatim):

> Give me a standalone player-safe visual brief for a misty riverside gate, in your reply only.
> No prep is needed and do not use external services.

### Rubric

REQUIRED:

- [ ] Provides a useful player-safe brief in the reply without requiring prep or inventing an asset,
      inspection, playback, or rights clearance. Changes no files and creates no files.
- [ ] Respects known safety and states unknowns rather than inferring consent or tool availability.

## Scenario F — successful one-off enrichment, no standing agreement

Setup: fresh fixture unchanged; the existing Session 7 prep is complete and no visual working
agreement is present. No media tools are available.

Prompt (verbatim):

> For Session 7 only, add player-safe visual briefs to the existing prep at their scene points
> of use. Do not enable future visual runs, use external services or create media files.

### Rubric

REQUIRED:

- [ ] Fulfills the explicit one-run enrichment request without requiring a standing agreement.
      (Activation)
- [ ] Meets Scenario A's cue, scoped metadata, scannability, safety, preservation and reporting
      requirements, except its renamed-profile and standing-agreement conditions. Only the existing prep is enriched;
      profile unchanged and no permanent enablement. (Phase 2, P2)

## Machine-checked boxes

Only observable file facts are checked. A reader must judge the rubric, reply, cue placement and
baseline textual preservation. A uses the existing `session-prep` type so the runner matches the
changed prep; the untouched allowance is limited to its exact existing path.

<!-- eval-spec
{
  "skill": "ttrpg-session-visuals",
  "fixture": "fixture-campaign",
  "scenarios": {
    "A": {
      "prompt_index": 0,
      "setup": [
        {"copy": {"from": "fixture-campaign/campaign-profile.md", "to": "table-contract.md"}},
        {"delete": "campaign-profile.md"},
        {"replace": {"file": "table-contract.md", "old": "## §E — Declared overrides and working agreements", "new": "## §E — Declared overrides and working agreements\n\nSession visuals: enabled — use ttrpg-session-visuals after session prep"}}
      ],
      "artifact": {"type": "session-prep"},
      "mechanical": [
        {"id": "type-key", "kind": "frontmatter", "key": "type", "equals": "session-prep", "cite": "Phase 2"},
        {"id": "other-files-untouched", "kind": "untouched", "allow_new": ["^Sessions/Session 7 — The Drowned Toll\\.md$"], "cite": "Phase 2"},
        {"id": "nothing-created", "kind": "no-new-files", "cite": "Phase 2"}
      ]
    },
    "B": {
      "prompt_index": 1, "setup": [],
      "mechanical": [
        {"id": "unchanged", "kind": "untouched", "allow_new": [], "cite": "Activation"},
        {"id": "nothing-created", "kind": "no-new-files", "cite": "Activation"}
      ]
    },
    "C": {
      "prompt_index": 2,
      "setup": [{"replace": {"file": "campaign-profile.md", "old": "## §E — Declared overrides and working agreements", "new": "## §E — Declared overrides and working agreements\n\nSession visuals: disabled"}}],
      "mechanical": [
        {"id": "unchanged", "kind": "untouched", "allow_new": [], "cite": "Activation"},
        {"id": "nothing-created", "kind": "no-new-files", "cite": "Activation"}
      ]
    },
    "D": {
      "prompt_index": 3,
      "setup": [{"delete": "Sessions/Session 7 — The Drowned Toll.md"}],
      "mechanical": [
        {"id": "unchanged", "kind": "untouched", "allow_new": [], "cite": "Phase 1"},
        {"id": "nothing-created", "kind": "no-new-files", "cite": "Phase 1"}
      ]
    },
    "E": {
      "prompt_index": 4,
      "setup": [{"delete": "Sessions/Session 7 — The Drowned Toll.md"}],
      "mechanical": [
        {"id": "unchanged", "kind": "untouched", "allow_new": [], "cite": "Phase 1"},
        {"id": "nothing-created", "kind": "no-new-files", "cite": "Phase 1"}
      ]
    },
    "F": {
      "prompt_index": 5,
      "setup": [],
      "artifact": {"type": "session-prep"},
      "mechanical": [
        {"id": "type-key", "kind": "frontmatter", "key": "type", "equals": "session-prep", "cite": "Phase 2"},
        {"id": "other-files-untouched", "kind": "untouched", "allow_new": ["^Sessions/Session 7 — The Drowned Toll\\.md$"], "cite": "Phase 2"},
        {"id": "nothing-created", "kind": "no-new-files", "cite": "Phase 2"}
      ]
    }
  }
}
-->
