#!/usr/bin/env python3
"""The fixture campaign is dirty ON PURPOSE. This asserts it still is.

    python3 tests/check_fixture.py

`tests/fixture-campaign/` carries deliberately seeded defects, and `tests/evals/
continuity-audit.md` is their answer key. A tidy-minded editor - human or agent - who "fixes"
the hub is not improving the repo: they are deleting the only thing the continuity-audit eval
measures, and the eval then passes for the wrong reason, silently, forever.

So each seeded defect gets a predicate here. The script also asserts the answer key lists as
many defects as this file knows about, which is the mechanical half of the rule "a new seeded
defect goes into the answer key in the same commit".

It does NOT judge the fixture's quality, and it never edits anything. Stdlib only.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FIX = os.path.join(ROOT, "tests", "fixture-campaign")
KEY = os.path.join(ROOT, "tests", "evals", "continuity-audit.md")


def read(*parts):
    p = os.path.join(FIX, *parts)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def hub():
    return read("Hub.md") or ""


def threads():
    return read("Threads.md") or ""


def prep7():
    return read("Sessions", "Session 7 \u2014 The Drowned Toll.md") or ""


def log7():
    return read("Sessions", "Session 7 \u2014 Log.md") or ""


def log6():
    return read("Sessions", "Session 6 \u2014 Log.md") or ""


def dossier(name):
    return read("Dossiers", name) or ""


# Each entry mirrors one row of the answer key, by number. The predicate returns True while the
# defect is still there - which is the state the evals need.
DEFECTS = [
    (1, "stale hub: it still says Session 6 while a Session 7 log exists",
     lambda: bool(re.search(r"Last session played:\s*\*\*Session 6\*\*", hub()))
     and os.path.isfile(os.path.join(FIX, "Sessions", "Session 7 \u2014 Log.md"))),

    (2, "desynced duplicates: hub roster values disagree with the dossiers (P10)",
     lambda: "| Tobit, the debt-scribe | Bruno | 5 | 4 |" in hub()
     and "marks: 6" in dossier("Bruno \u2014 Tobit.md")
     and "wick: 3" in dossier("Bruno \u2014 Tobit.md")),

    (3, "the static roster table exists at all - forbidden by P10 whatever it says",
     lambda: "## Roster" in hub() and "| Character | Player | Marks | Wick |" in hub()),

    (4, "broken link: the hub points at an entity note that does not exist",
     lambda: "[[Eel-Market Buyer]]" in hub()
     and not os.path.isfile(os.path.join(FIX, "Entities", "Eel-Market Buyer.md"))),

    (5, "thread ledger not updated after Session 7",
     lambda: bool(re.search(r"\|\s*The false bell\s*\|\s*open\s*\|", threads()))
     and "the false bell* \u2192 paid" in log7()
     and "debt-ledger" not in threads()),

    (6, "the hub retypes thread statuses, and already disagrees with the ledger",
     lambda: "## Open threads" in hub()
     and "The eel-catcher's promise \u2014 paid (Session 6)." in hub()
     and "Session 7 \u2014 Log" in threads()),

    (7, "a trigger duplicated between the prep's global callout and a scene box (P2)",
     lambda: len(re.findall(r"[Ll]ying to Ulde[^\n]*costs 1 Wick", prep7())) >= 2),

    (8, "dangling seeds: the promised lantern, quiet since Session 3, and the unstaged omen",
     lambda: bool(re.search(r"\|\s*The promised lantern\s*\|\s*open\s*\|\s*Session 3\s*\|"
                            r"\s*Session 3\s*\|", threads()))
     and "heron-omen" in log6()),
]


def main():
    failures = []
    print("fixture defect check - %s" % FIX)
    for num, description, predicate in DEFECTS:
        try:
            ok = predicate()
        except Exception as exc:                     # a moved file must read as a failure
            ok = False
            description += " [predicate raised %s]" % exc.__class__.__name__
        print("  %s  %d. %s" % ("ok  " if ok else "GONE", num, description))
        if not ok:
            failures.append(num)

    key_text = ""
    if os.path.isfile(KEY):
        with open(KEY, encoding="utf-8") as fh:
            key_text = fh.read()
    rows = set(int(n) for n in re.findall(r"^\|\s*(\d+)\s*\|", key_text, re.M))
    known = {n for n, _d, _p in DEFECTS}
    print("")
    if rows != known:
        print("  answer key rows %s != defects tracked here %s"
              % (sorted(rows), sorted(known)))
        print("  a seeded defect belongs in BOTH tests/evals/continuity-audit.md and this file")
        failures.append("answer-key")

    if failures:
        print("\n%d problem(s). A 'GONE' line means the fixture was cleaned: restore the defect "
              "(git checkout) rather than adjusting the check - a clean fixture tests nothing."
              % len(failures))
        return 1
    print("all %d seeded defects still seeded, and the answer key agrees" % len(DEFECTS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
