#!/usr/bin/env python3
r"""Validate a campaign's overlay skill(s) - the third artifact in the two-layer contract.

    python3 scripts/validate_overlay.py path/to/<campaign>-prep/SKILL.md
    python3 scripts/validate_overlay.py ~/my-campaign        # finds every overlay under it
    python3 scripts/validate_overlay.py --list

An overlay is the escape hatch of the whole design: what is neither a profile slot nor
generalisable. Nothing checked it until now, so the two failure modes it invites were invisible -
an overlay that quietly **restates the base procedure** (and drifts from it), and one that
**re-states profile facts** (and drifts from those). Both are silent at write time and expensive
three sessions later.

What this deliberately does NOT check: system names. An overlay is exactly where the name of your
game, your setting and your characters belong - `NO-SYSTEM-NAMES` is a rule for the *package*,
never for a campaign's own layer.

Stdlib only. The slot ids and principle tags are read from this repo (or `--schema` /
`--principles`), so an overlay is validated against the same two contracts a skill is.
"""
import argparse
import json
import os
import re
import sys
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_contract import Report, _fmt, utf8_stdout  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DEFAULT_SCHEMA = os.path.join(ROOT, "templates", "campaign-profile.md")
DEFAULT_PRINCIPLES = os.path.join(ROOT, "docs", "PRINCIPLES.md")

Rule = namedtuple("Rule", "code level fails_when")

RULES = [
    Rule("OVERLAY-FRONTMATTER", "error",
         "unusable frontmatter: no name/description, name is not hyphen-case or does not match "
         "the folder, no 'Use when', an unknown key, or an unfinished [TODO:"),
    Rule("OVERLAY-DELEGATES", "error",
         "the overlay never names the base skill it sits on - a reader (and a router) cannot "
         "tell which procedure it is adding to"),
    Rule("OVERLAY-RESTATES", "warn",
         "the overlay reproduces the base skill's phase structure instead of adding to it - "
         "the copy is what drifts when the base skill changes"),
    Rule("OVERLAY-SLOT", "error",
         "it cites a slot id the schema does not define, or a numeric section (schema 1)"),
    Rule("OVERLAY-PRINCIPLE", "error",
         "it cites a Pn that does not exist, or switches off one of the package's "
         "non-overridable principles (the 'Requirements' set named at the top of "
         "docs/PRINCIPLES.md) - `E.overrides` in the profile is the only place that decision "
         "lives"),
    Rule("OVERLAY-LINK", "error",
         "a link leaves the overlay folder or points at nothing - an overlay is installed "
         "alone, exactly like a base skill"),
    Rule("OVERLAY-SIZE", "warn",
         "the overlay is past a page - the base skill is probably missing a slot; fix the base "
         "skill instead of growing the exception"),
    Rule("OVERLAY-PROFILE-FACT", "warn",
         "it looks like it is restating a profile fact (a path, a cadence, a guide, a "
         "convention) that belongs in `campaign-profile.md`, where nine skills already read it"),
]
RULE_CODES = [r.code for r in RULES]

SIZE_LIMIT = 120                       # "a page", generously
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "compatibility", "metadata"}
# The non-overridable set (P1, P2, P3, P10, P11, P14, P15 as of this writing) is NOT hardcoded
# here - see load_not_overridable() below, which parses it from docs/PRINCIPLES.md's own
# "Requirements" line so the two can never drift apart silently.
REQUIREMENTS_LINE = re.compile(r"\*\*Requirements\b.*?\*\*", re.S)
SLOT_ID = re.compile(r"(?<![A-Za-z0-9.])([A-E]\.[a-z_]{2,})")
LEGACY = re.compile("\u00a7\\s*\\d")
PN = re.compile(r"(?<![A-Za-z0-9])P(\d{1,2})(?![0-9A-Za-z])")
BASE_SKILL = re.compile(r"\bttrpg-[a-z][a-z-]+\b")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PHASE = re.compile(r"^##+\s+Phase\s+\d", re.M)
# Sentences that smell of a profile slot living in the wrong file. Each maps to the slot that
# owns the fact, so the message can say where it belongs instead of just objecting.
PROFILE_FACTS = [
    (re.compile(r"\bevery (week|month)\b|\bweekly\b|\bfortnightly\b", re.I), "B.cadence"),
    (re.compile(r"\bnotes? (?:live|go|belong) in\b|\bfolder\b.*\.md\b", re.I), "C.root"),
    (re.compile(r"\brecurring (guide|anchor) NPC\b", re.I), "D.guide"),
    (re.compile(r"\bsafety (tool|word|card)s?\b", re.I), "B.safety"),
    (re.compile(r"\brecap\b.*\b(minutes|read aloud)\b", re.I), "D.recap"),
    (re.compile(r"\bwikilink|\[\[.*\]\].*syntax\b", re.I), "C.links"),
]


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def load_contracts(schema_path, principles_path):
    slots = set(re.findall(r"`([A-E]\.[a-z_]+)`", _read(schema_path)))
    principles = set(re.findall(r"^###\s+(P\d{1,2})\b", _read(principles_path), re.M))
    return slots, principles


def load_not_overridable(principles_path):
    """Parse the non-overridable principle set from docs/PRINCIPLES.md's own "Requirements —
    P1, P2, ..." line, instead of hardcoding it here where it can silently drift from the real
    document (this is exactly the bug that once let this file miss P14 and P15). Never falls
    back to a hardcoded default: a document this cannot parse is a validator that no longer
    knows what it is enforcing, and must fail loudly instead of guessing."""
    text = _read(principles_path)
    m = REQUIREMENTS_LINE.search(text)
    if not m:
        sys.exit("fatal: could not find a 'Requirements' line in %s - the non-overridable "
                  "principle set cannot be determined, refusing to validate with a guessed or "
                  "stale list" % principles_path)
    ids = tuple(re.findall(r"P\d{1,2}", m.group(0)))
    if not ids:
        sys.exit("fatal: the 'Requirements' line in %s names no Pn principles - refusing to "
                  "validate with an empty non-overridable set" % principles_path)
    return ids


def find_overlays(path):
    if os.path.isfile(path):
        return [path]
    found = []
    for base, dirs, names in os.walk(path):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for n in sorted(names):
            if n == "SKILL.md":
                found.append(os.path.join(base, n))
    if not found:
        sys.exit("fatal: no SKILL.md under %s" % path)
    return found


def validate_one(path, slots, principles, rep, base_skills=(), not_overridable=()):
    src = _read(path)
    folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
    try:
        where = os.path.relpath(path)
    except ValueError:
        where = os.path.abspath(path)
    where = where.replace("\\", "/")
    lines = src.splitlines()

    m = re.match(r"^---\r?\n(.*?)\r?\n---", src, re.S)
    if not m:
        rep.err("OVERLAY-FRONTMATTER", where, "missing or unterminated YAML frontmatter")
        fm, body = "", src
    else:
        fm, body = m.group(1), src[m.end():]
        keys = set(re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", fm, re.M))
        unexpected = sorted(keys - ALLOWED_KEYS)
        if unexpected:
            rep.err("OVERLAY-FRONTMATTER", where,
                    "unexpected frontmatter key(s): %s - allowed: %s"
                    % (", ".join(unexpected), ", ".join(sorted(ALLOWED_KEYS))))
        nm = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
        name = nm.group(1).strip("\"'") if nm else None
        if not name:
            rep.err("OVERLAY-FRONTMATTER", where, "frontmatter has no 'name'")
        else:
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
                rep.err("OVERLAY-FRONTMATTER", where,
                        "name '%s' is not hyphen-case - the router resolves it literally" % name)
            if folder not in ("", ".") and name != folder:
                rep.err("OVERLAY-FRONTMATTER", where,
                        "frontmatter name '%s' != folder '%s'" % (name, folder))
        ds = re.search(r"^description:\s*(.*?)(?=\n[A-Za-z_][A-Za-z0-9_-]*:|\Z)", fm, re.M | re.S)
        desc = " ".join(ds.group(1).split()).strip("\"'") if ds else ""
        if not desc:
            rep.err("OVERLAY-FRONTMATTER", where, "frontmatter has no 'description'")
        else:
            if "Use when" not in desc:
                rep.err("OVERLAY-FRONTMATTER", where,
                        "description has no explicit 'Use when ...' - the router sees nothing "
                        "else, and an overlay competes with the base skill it sits on")
            if len(desc) > 1024:
                rep.err("OVERLAY-FRONTMATTER", where,
                        "description is %d chars, over the 1024 budget" % len(desc))
        if "[TODO:" in fm:
            rep.err("OVERLAY-FRONTMATTER", where, "frontmatter contains an unfinished [TODO: ...]")
        if "<" in (desc or "") and ">" in (desc or ""):
            rep.err("OVERLAY-FRONTMATTER", where,
                    "description still carries a <placeholder> from templates/overlay-SKILL.md")

    named = {s for s in BASE_SKILL.findall(src)}
    if not named:
        rep.err("OVERLAY-DELEGATES", where,
                "names no base skill - an overlay opens by delegating ('Run ttrpg-<skill> "
                "first'), because the procedure is not here")
    elif base_skills:
        unknown = sorted(s for s in named if s not in base_skills)
        if unknown and not (named & set(base_skills)):
            rep.err("OVERLAY-DELEGATES", where,
                    "names %s, which is not a skill in this package - check the spelling of the "
                    "base skill it delegates to" % ", ".join(unknown))

    phases = PHASE.findall(body)
    if len(phases) >= 3:
        rep.warn("OVERLAY-RESTATES", where,
                 "carries %d 'Phase N' headings - that is the base skill's procedure copied "
                 "into a place that will not be updated with it; keep only the delta"
                 % len(phases))

    body_lines = len([ln for ln in lines if ln.strip()])
    if body_lines > SIZE_LIMIT:
        rep.warn("OVERLAY-SIZE", where,
                 "%d non-blank lines, past the one-page rule - an overlay this size is a "
                 "missing profile slot wearing a disguise" % body_lines)

    heading = ""
    for i, line in enumerate(lines, 1):
        if line.startswith("#"):
            heading = line.lower()
        for sid in SLOT_ID.findall(line):
            if sid not in slots:
                rep.err("OVERLAY-SLOT", "%s:%d" % (where, i),
                        "`%s` is not a slot in the schema - a skill will never read it" % sid)
        if LEGACY.search(line):
            rep.err("OVERLAY-SLOT", "%s:%d" % (where, i),
                    "numeric profile citation %r - schema 2 slots are named (`B.distance`)"
                    % LEGACY.search(line).group(0))
        for pn in PN.findall(line):
            if "P" + pn not in principles:
                rep.err("OVERLAY-PRINCIPLE", "%s:%d" % (where, i),
                        "P%s does not resolve to any principle" % pn)
        low = line.lower()
        if re.search(r"\b(off|ignore|disable|drop)\b", low):
            for pn in PN.findall(line):
                if "P" + pn in not_overridable:
                    rep.err("OVERLAY-PRINCIPLE", "%s:%d" % (where, i),
                            "P%s is not overridable, and an overlay is not where an override "
                            "lives anyway - `E.overrides` in the profile is" % pn)
        # A section that exists to send facts BACK to the profile (the template's "What belongs
        # in the profile instead") names them on purpose: warning there teaches the opposite.
        if "profile" in heading or "campaign-profile.md" in line:
            continue
        for pattern, slot in PROFILE_FACTS:
            if pattern.search(line):
                rep.warn("OVERLAY-PROFILE-FACT", "%s:%d" % (where, i),
                         "reads like a profile fact; `%s` already holds it, and nine skills "
                         "read it there" % slot)
                break

    sdir = os.path.dirname(os.path.abspath(path))
    for i, line in enumerate(lines, 1):
        for raw in LINK.findall(line):
            t = raw.split("#")[0].strip()
            if not t or re.match(r"^[a-z][a-z0-9+.-]*:", t):
                continue
            if t.startswith("/") or t.startswith("..") or "/../" in t:
                rep.err("OVERLAY-LINK", "%s:%d" % (where, i),
                        "link leaves the overlay folder: %s - an overlay is installed alone" % t)
                continue
            if not os.path.exists(os.path.join(sdir, t)):
                rep.err("OVERLAY-LINK", "%s:%d" % (where, i),
                        "link points at %s, which does not exist in the overlay folder" % t)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="validate_overlay.py",
        description="Validate a campaign overlay skill against the package's two contracts.")
    ap.add_argument("target", nargs="?", help="an overlay SKILL.md, or a directory to search")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA)
    ap.add_argument("--principles", default=DEFAULT_PRINCIPLES)
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--only", action="append", metavar="CODE")
    ap.add_argument("--list", action="store_true", help="list the rules and exit")
    args = ap.parse_args(argv)
    utf8_stdout()

    if args.list:
        width = max(len(r.code) for r in RULES)
        for r in RULES:
            print("%-*s  %-5s  %s" % (width, r.code, r.level, r.fails_when))
        return 0
    if not args.target:
        ap.error("give an overlay path (or a directory), or --list")

    only = None
    if args.only:
        only = [c.strip().upper() for item in args.only for c in item.split(",") if c.strip()]
        unknown = sorted(set(only) - set(RULE_CODES))
        if unknown:
            ap.error("unknown rule(s): %s (see --list)" % ", ".join(unknown))

    slots, principles = load_contracts(args.schema, args.principles)
    not_overridable = load_not_overridable(args.principles)
    skills_dir = os.path.join(ROOT, "skills")
    base_skills = tuple(sorted(d for d in os.listdir(skills_dir)
                               if os.path.isdir(os.path.join(skills_dir, d)))) \
        if os.path.isdir(skills_dir) else ()

    rep = Report(only)
    overlays = find_overlays(args.target)
    for path in overlays:
        validate_one(path, slots, principles, rep, base_skills, not_overridable)
    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))

    if args.format == "json":
        print(json.dumps({
            "overlays": [os.path.abspath(p) for p in overlays],
            "findings": [f._asdict() for f in
                         sorted(rep.findings, key=lambda f: (f.level, f.check, f.where))],
            "counts": {"errors": len(rep.errors), "warnings": len(rep.warnings)},
            "ok": not failed,
        }, indent=2, sort_keys=False))
        return 1 if failed else 0

    print("overlay check - %d overlay(s)" % len(overlays))
    print("")
    for line in sorted(_fmt(f) for f in rep.errors):
        print(line)
    if rep.errors and rep.warnings:
        print("")
    for line in sorted(_fmt(f) for f in rep.warnings):
        print(line)
    print("\n%d error(s), %d warning(s)." % (len(rep.errors), len(rep.warnings)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
