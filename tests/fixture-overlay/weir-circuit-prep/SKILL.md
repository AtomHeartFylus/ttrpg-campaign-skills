---
name: weir-circuit-prep
description: "Campaign overlay for The Weir Circuit on top of ttrpg-session-prep. Use when preparing a session of The Weir Circuit. Adds only the campaign-specific constraints: the ballad register of read-aloud text, this table's four known moves, and the casting test for anything that comes out of the fen. The procedure lives in ttrpg-session-prep; this note does not restate it."
license: MIT
metadata:
  author: The Weir Circuit (invented, for tests)
  version: "1.0"
---

# The Weir Circuit — prep overlay

**Run `ttrpg-session-prep` first.** It owns the procedure, the structure and the checks. This
note adds only what is specific to The Weir Circuit and cannot be expressed as a slot in
`campaign-profile.md`.

> Fixture for `tests/checker/test_validate_overlay.py`, and the package's only worked example of
> an overlay. The campaign is invented; so is its system. Shape, not content.

## House voice of read-aloud text

- Ballad register: two beats to a line, no simile that a fen-dweller could not have made.
- The water is never described as *cold*. It is described by what it takes.
- No colour word for the bell. It is heard, or it is not there.

## This table's four known moves (feeds the red team, P9)

- They pay a toll rather than argue it, then resent it two scenes later.
- Bruno negotiates past the point of safety; the standing question is *who is holding the
  ledger he cannot see*.
- Someone dives before the rope plan exists.
- They name a body before it is identified, and the name sticks whether or not it is right.

## Casting test for anything that comes out of the fen

Before a new figure gets dialogue, it answers: *what did the water take from it*, *what does it
want back*, and *what would it accept instead*. A figure that cannot answer stays a fixture —
weather, not a character.

## What belongs in the profile instead

Paths, cadence, the guide, the safety word, the recap form, link syntax: all of that lives in
`campaign-profile.md`, where every skill already reads it. If a rule here starts describing how
the repo is arranged, it is in the wrong file.
