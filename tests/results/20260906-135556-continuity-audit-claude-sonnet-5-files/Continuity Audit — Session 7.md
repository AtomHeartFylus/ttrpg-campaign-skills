# Continuity audit — sessions 1–7 (window: whole history, no prior arc pass or audit exists)

## Invariants
| Check | Result | Evidence |
|---|---|---|
| Link integrity | **fail: 4 broken** (3 distinct targets) | `python scripts/check_links.py .` → `12 file(s), 24 link(s), 4 broken, 0 case-only mismatch(es)` — `Hub.md:25 -> Eel-Market Buyer`, `Sessions/Session 6 — Log.md:4 -> Session 6 — The Long Reach`, `Sessions/Session 7 — The Drowned Toll.md:16` and `:74 -> Bell-Wight — stats`. `C.verify` declares no command yet, so this was run by hand from the package's bundled checker, not claimed as the profile's own invariant. |
| Single source of truth | 2 duplicates (roster values; thread status) | see F1, F2 below |
| Hub vs last log | stale — Session 6 vs Session 7 played | see F3 |

## Findings
- **F1 — blocking** · `Hub.md` "Last session played: **Session 6**" · [[Session 7 — Log]] exists and is the campaign's actual last night played · **recommendation:** update the hub's line by hand to Session 7; nothing else in the hub's "Where things stand" needs to change beyond that and the location (far bank, per the log's exit state).
- **F2 — blocking** · `Hub.md`'s Roster table (lines ~9–14) vs `Dossiers/*` · hub says Maren 5 marks/3 Wick, Tobit 5/4, Iole 5/3, Sorrel 5/4; the dossiers (the owning notes) say Maren 6/4, Tobit 6/3, Iole 6/3, Sorrel 5/4 (unchanged, absent Session 7) · **recommendation:** the dossiers are the source of truth (P10) — propose updating the hub's copies to match, in the direction dossier → hub, never the reverse. The table's continued existence is itself the deeper problem (see F3).
- **F3 — blocking (structural)** · `Hub.md`'s "Roster" table exists at all · a static per-character marks/Wick table in the hub is a second, typed copy of a value `C.state_locations` already assigns to one home (the dossiers) · **recommendation:** remove the table and replace it with a line pointing at `Dossiers/`, or a generated view if this vault's tooling supports one — never a second hand-maintained table, whatever its values say.
- **F4 — drift** · `Hub.md` "Open threads" bullets vs `Threads.md` · the hub retypes thread status as its own bullet list, and it already disagrees with the ledger: hub says "The eel-catcher's promise — paid (**Session 6**)", `Threads.md` says paid via **[[Session 7 — Log]]** · **recommendation:** the ledger (`C.thread_ledger`) is the one home for status (P10); replace the hub's bullet list with a link to `Threads.md` and correct the discrepancy there, not in two places.
- **F5 — drift** · `Threads.md` "The false bell" row says **open** · [[Session 7 — Log]] records it cut loose and the body identified — the objective the false-bell thread existed to resolve · **recommendation:** update the row to *paid*, citing Session 7.
- **F6 — drift** · `Threads.md` has no row for **the fen's debt-ledgers** · [[Session 7 — Log]]'s own Pending list says this thread opened this session, and the prep's GM-only note (Scene 3) is where it was seeded in play · **recommendation:** add the row (seeded Session 7, status open) rather than let a session-log pending item stand in as the only record.
- **F7 — cosmetic/hygiene (P2)** · `Sessions/Session 7 — The Drowned Toll.md` · "Lying to Ulde inside the gate costs 1 Wick" appears **both** in the top `[!warning]` global box and again inside Scene 1's `[!todo]` box ("Wick: lying to Ulde inside the gate costs 1 Wick — say it before the first lie.") · **recommendation:** keep the value in the scene box only; the global box should state the principle without repeating the number, as `references/scene-anatomy.md` itself specifies.
- **F9 — drift (P8/check C)** · [[Session 6 — Log]] "Missed opportunities": **the heron-omen** was never staged, marked recoverable there ("any dawn scene") — [[Session 7 — Log]] had a dawn-adjacent opening (the ferry) and still did not stage it. Two sessions quiet now, and it lives only inside a log's prose, never in `Threads.md` — a seed visible in a log but absent from the tracker (check C) · **recommendation:** either add it to `Threads.md` as its own row so it stops depending on someone re-reading Session 6, or hand `ttrpg-campaign-arc` an explicit revive-or-declare-lost call on it now, same as the lantern.
- **F8 — hygiene** · recurring name **"the eel-catcher"** appears in both [[Session 6 — Log]] and [[Session 7 — Log]] (a promise made to them, kept on their behalf) with no entity note ever created · **recommendation:** hand this name to `ttrpg-entity-note`; not created here (one owner per artifact).

## Checks not run
- None dropped by an override — `E.overrides` declares none switched off; checks A–H all ran.
- Check D's deviation-drift sub-check did not apply: `D.backbone` is fully homebrew with `D.deviation_policy: n/a` — there is no source material to diverge from, so its silence is not a finding.
- Check H (retention): `B.retention` states a rule ("GM notes about players kept for the season, then deleted"), so the check is live, but every dossier's Playstyle/Hooks entry in this window is written as undated prose — there is no per-entry date to compare against the rule. **Nothing overdue is reported because nothing here can be dated, not because nothing is overdue.** Proposed: future Playstyle/Hooks entries should carry the session they were observed in, the way the rotation diary already does, so this check has something to measure next time.

## Threads to decide → ttrpg-campaign-arc
| Thread | Last seen | Recommendation | Why |
|---|---|---|---|
| The promised lantern | Session 3 (per `Threads.md`; the log itself is outside this repo's window) | revive or declare lost | 4 sessions of silence (4, 5, 6, 7) with no appearance — past due for a decision, and this skill hands the decision, it does not make it |
| The false bell | resolved in play (Session 7) | mark paid | see F5 — a ledger correction, not a live decision, but the arc pass is where the ledger gets touched |
| The fen's debt-ledgers | opened Session 7 | schedule | new thread this window; needs a home in the next arc pass |
| The heron-omen | Session 6 (missed opportunity, never staged) | revive or declare lost | quiet 2 sessions running and only recorded in a log's prose, not the ledger (F9) |

## Proposed changes — NOTHING APPLIED
| # | File | Change | Reason | Read aloud? | Risk |
|---|---|---|---|---|---|
| 1 | `Hub.md` | "Last session played" → Session 7; location → far bank | F1 | no | low |
| 2 | `Hub.md` | delete the Roster table; replace with a pointer to `Dossiers/` | F2, F3 | no | low — no value is lost, only the second copy |
| 3 | `Hub.md` | delete the "Open threads" bullet list; replace with a pointer to `Threads.md` | F4 | no | low |
| 4 | `Threads.md` | "The false bell" → paid, cite Session 7 | F5 | no | low |
| 5 | `Threads.md` | add row: the fen's debt-ledgers — open, seeded Session 7 | F6 | no | low |
| 6 | `Sessions/Session 7 — The Drowned Toll.md` | remove the Wick-cost number from the top `[!warning]` box, keep it in Scene 1's box only | F7 | no | low — this note is already played; edits here are historical hygiene, ask before touching a note `E.never_without_asking` covers if that includes played preps |
| 7 | (hand-off, no file edit here) | give "the eel-catcher" to `ttrpg-entity-note` | F8 | — | — |

Then: apply only the approved rows, and re-run `python scripts/check_links.py .` afterwards,
reporting its output. Rows 1–5 are pure bookkeeping; row 6 touches an already-played prep note and
is flagged for explicit approval given `E.never_without_asking`.
