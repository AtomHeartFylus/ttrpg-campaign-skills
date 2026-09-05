#!/usr/bin/env python3
r"""Validate a campaign's own `campaign-profile.md` against the schema it was cut from.

    python3 scripts/validate_profile.py /path/to/campaign-profile.md
    python3 scripts/validate_profile.py ~/campaign --strict --format json
    python3 scripts/validate_profile.py --list        # the rules, and what each fails on

`check_contract.py` validates the package. This validates **the other half of the contract**:
the file a table fills in. Everything it checks was, until now, a sentence in the schema that
only a careful reader enforced - and a profile is read by nine skills that will each believe it.

What it will never do: guess a value, or rewrite the file. A profile with unanswered slots is
legitimate (that is the four-state rule); it is *reported*, so nobody discovers mid-session that
the slot the recap needed was never asked.

Stdlib only. The schema is read from this repo (or from `--schema`), so the rules follow the
schema instead of being transcribed into this file: an enum declared in a slot line is picked up
here the day it is added.
"""
import argparse
import json
import os
import re
import sys
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_contract import Report, _fmt, utf8_stdout  # noqa: E402  (one reporting shape)

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DEFAULT_SCHEMA = os.path.join(ROOT, "templates", "campaign-profile.md")

Rule = namedtuple("Rule", "code level fails_when")

RULES = [
    Rule("PROFILE-FRONTMATTER", "error",
         "the file is not a campaign profile: no `type: campaign-profile`, or a schema "
         "version this validator does not know"),
    Rule("SLOT-MISSING", "error",
         "a slot the schema defines has no line at all (core slot = error, other = warning) - "
         "a skill that cannot find a slot cannot tell 'never asked' from 'deleted'"),
    Rule("CORE-UNANSWERED", "error",
         "a `(core)` slot is still an untouched placeholder - the cycle cannot start on it"),
    Rule("DEFERRED-FORM", "error",
         "`deferred:` carries no `<when>` - a deferral nobody can close is an empty slot with "
         "a nicer name"),
    Rule("SLOT-ENUM", "error",
         "a slot whose schema line declares alternatives holds none of them"),
    Rule("CONSENT-STATE", "error",
         "a consent or safety slot says `none` - silence never switches a safety tool off; "
         "write what the table actually said"),
    Rule("CROSS-SLOT", "error",
         "two slots contradict each other (capture paths without recording consent, player "
         "access without a GM-private location, protagonists above table size, a resource "
         "family under a resource that is `none`)"),
    Rule("OVERRIDE-SCOPE", "error",
         "`E.overrides` switches off a principle that is not overridable (P1, P2, P3, P10, "
         "P11), or names a principle without saying off/replaced"),
    Rule("UNKNOWN-SLOT", "warn",
         "the profile defines a slot id the schema does not - no skill will ever read it"),
    Rule("PROFILE-ENCODING", "error",
         "the profile carries U+FFFD or a literal \\uXXXX escape"),
    Rule("UNANSWERED", "warn",
         "a non-core slot is still an untouched placeholder - legitimate, and reported so it "
         "is a decision rather than a surprise"),
]
RULE_CODES = [r.code for r in RULES]

# Consent is not a default and no override reaches it: `none` here is unanswered, never a
# decision. The list is the schema's own, kept here because it is a *rule*, not a value.
CONSENT_SLOTS = ("B.safety", "B.consent_recording", "B.consent_offgame", "B.retention", "B.frame")
NOT_OVERRIDABLE = ("P1", "P2", "P3", "P10", "P11")
KNOWN_SCHEMAS = ("2",)

SLOT_TOKEN = re.compile(r"`([A-E]\.[a-z_]+)`")
# A slot is DEFINED by a bold span that contains nothing but slot ids: **`B.size`**, or
# **`A.resource_loss` / `A.resource_gain`** for two sharing one answer. A slot id merely
# MENTIONED inside another slot's value ("With `B.size` this fixes the rotation period",
# "**Required whenever `C.player_access` ...**") is prose, not a second definition - reading
# it as one silently reassigned three core slots to the wrong bullet.
BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
DEFINITION = re.compile(r"^(?:`[A-E]\.[a-z_]+`)(?:\s*[/,]\s*`[A-E]\.[a-z_]+`)*$")
BULLET = re.compile(r"^\s*-\s+\*\*")
DEFERRED = re.compile(r"^deferred\s*:?\s*(.*)$", re.I)
EMPTY_ANSWER = re.compile(r"^(none|n/?a)\b", re.I)
PLACEHOLDER_ANGLE = re.compile(r"<[^>]{3,}>")
BAD_ESCAPE = re.compile(r"\\u[0-9a-fA-F]{4}")
LEADING_INT = re.compile(r"^\D{0,12}?(\d+)")


# ---------- parsing -------------------------------------------------------

Slot = namedtuple("Slot", "id value line core setup_only")


def parse_slots(text):
    """{slot id: Slot}. A bullet may declare several slots; each takes the text that follows
    it, up to the next slot on the same bullet. A segment that is only punctuation (the
    schema's `A.resource_loss` / `A.resource_gain` bullet) shares the next slot's value."""
    slots = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if not BULLET.match(lines[i]):
            i += 1
            continue
        start = i
        block = [lines[i]]
        i += 1
        # continuation lines: indented, or plain prose belonging to the same bullet
        while i < len(lines) and lines[i].strip() and not BULLET.match(lines[i]) \
                and not lines[i].startswith(("#", ">", "-", "|")):
            block.append(lines[i])
            i += 1
        blob = "\n".join(block)
        marks = [(m, SLOT_TOKEN.findall(m.group(1)))
                 for m in BOLD.finditer(blob) if DEFINITION.match(m.group(1).strip())]
        if not marks:
            continue
        pending = []
        for n, (m, ids) in enumerate(marks):
            end = marks[n + 1][0].start() if n + 1 < len(marks) else len(blob)
            raw = blob[m.end():end]
            core = "*(core)*" in raw
            setup_only = "*(setup-only)*" in raw
            raw = raw.replace("*(core)*", "").replace("*(setup-only)*", "")
            raw = re.sub(r"^[\s*/,;:\u2014\u2013-]+", "", raw)
            value = " ".join(raw.split()).strip()
            if not value:
                pending.extend((sid, start + 1, core, setup_only) for sid in ids)
                continue
            for sid, ln, c, so in pending:
                slots[sid] = Slot(sid, value, ln, c, so)
            pending = []
            for sid in ids:
                slots[sid] = Slot(sid, value, start + 1, core, setup_only)
        for sid, ln, c, so in pending:
            slots[sid] = Slot(sid, "", ln, c, so)
    return slots


def parse_enums(schema_slots):
    """Alternatives a schema line declares, e.g. **`one-shot` | `series` | `open sandbox`**.
    Read from the schema so a new enum needs no edit here."""
    enums = {}
    for sid, slot in schema_slots.items():
        head = slot.value[:160]
        m = re.match(r"\**\s*((?:`[^`]+`\s*\|\s*)+`[^`]+`)\**", head)
        if m:
            enums[sid] = [o.strip(" `") for o in m.group(1).split("|")]
    return enums


def state_of(slot, schema_slot):
    """placeholder | deferred | none | value - the four states, as the schema defines them."""
    v = slot.value.strip()
    if not v:
        return "placeholder"
    if schema_slot is not None and _norm(v) == _norm(schema_slot.value):
        return "placeholder"
    if PLACEHOLDER_ANGLE.search(v):
        return "placeholder"
    if DEFERRED.match(v):
        return "deferred"
    if EMPTY_ANSWER.match(v):
        return "none"
    return "value"


def _norm(s):
    return re.sub(r"[\s*_`]+", " ", s).strip().lower()


# ---------- the rules -----------------------------------------------------

def validate(profile_path, schema_path, only=None):
    rep = Report(only)
    schema_text = _read(schema_path)
    text = _read(profile_path)
    schema_slots = parse_slots(schema_text)
    enums = parse_enums(schema_slots)
    slots = parse_slots(text)
    where = os.path.basename(profile_path)

    def at(sid):
        s = slots.get(sid)
        return "%s:%d" % (where, s.line) if s else where

    # -- frontmatter
    fm = re.match(r"^---\r?\n(.*?)\r?\n---", text, re.S)
    if not fm or "type: campaign-profile" not in fm.group(1):
        rep.err("PROFILE-FRONTMATTER", where,
                "no `type: campaign-profile` in the frontmatter - that key is how every skill "
                "finds this file whatever it is named; a renamed profile without it is invisible")
    else:
        m = re.search(r"^schema:\s*(\S+)", fm.group(1), re.M)
        if not m:
            rep.err("PROFILE-FRONTMATTER", where, "frontmatter declares no `schema:` version")
        elif m.group(1) not in KNOWN_SCHEMAS:
            rep.err("PROFILE-FRONTMATTER", where,
                    "schema %s is not one this validator knows (%s) - re-cut the profile from "
                    "templates/campaign-profile.md and migrate per CHANGELOG"
                    % (m.group(1), ", ".join(KNOWN_SCHEMAS)))

    # -- encoding
    for i, line in enumerate(text.splitlines(), 1):
        if "\ufffd" in line:
            rep.err("PROFILE-ENCODING", "%s:%d" % (where, i),
                    "contains U+FFFD replacement character (encoding damage)")
        e = BAD_ESCAPE.search(line)
        if e:
            rep.err("PROFILE-ENCODING", "%s:%d" % (where, i),
                    "contains the literal escape %r - write the character itself" % e.group(0))

    # -- presence, state, enums
    states = {}
    for sid, schema_slot in sorted(schema_slots.items()):
        slot = slots.get(sid)
        if slot is None:
            if schema_slot.core:
                rep.err("SLOT-MISSING", where,
                        "`%s` *(core)* has no line in this profile - a skill cannot tell a "
                        "deleted slot from an unanswered one" % sid)
            else:
                rep.warn("SLOT-MISSING", where,
                         "`%s` has no line in this profile - keep the line and leave it "
                         "unanswered instead of deleting it" % sid)
            continue
        st = state_of(slot, schema_slot)
        states[sid] = st
        if st == "placeholder":
            if schema_slot.core:
                rep.err("CORE-UNANSWERED", at(sid),
                        "`%s` is a core slot and still holds the schema's placeholder - the "
                        "cycle cannot start on it; run ttrpg-campaign-setup" % sid)
            elif not schema_slot.setup_only:
                rep.warn("UNANSWERED", at(sid),
                         "`%s` was never asked - the first skill that needs it will stop and "
                         "ask; that is the design, not a bug" % sid)
        if st == "deferred":
            when = DEFERRED.match(slot.value).group(1).strip(" .-\u2014")
            if not when:
                rep.err("DEFERRED-FORM", at(sid),
                        "`%s` says `deferred` without naming *when* - write "
                        "`deferred: session zero`, so the deferral can be closed" % sid)
        if st == "value" and sid in enums:
            first = _norm(slot.value)
            if not any(first.startswith(_norm(opt)) for opt in enums[sid]):
                rep.err("SLOT-ENUM", at(sid),
                        "`%s` holds %r; the schema declares it as one of: %s - a skill branches "
                        "on this string" % (sid, slot.value[:60], ", ".join(enums[sid])))
        if sid in CONSENT_SLOTS and st == "none":
            rep.err("CONSENT-STATE", at(sid),
                    "`%s` says `none`. Consent and safety are not defaults: a `none` nobody "
                    "pronounced reads as *unanswered*, and silence never switches a safety tool "
                    "off. Write what the table said (`no`, or the agreement itself)" % sid)

    for sid in sorted(set(slots) - set(schema_slots)):
        rep.warn("UNKNOWN-SLOT", at(sid),
                 "`%s` is not a slot in the schema - no skill reads it; put campaign-specific "
                 "rules in an overlay skill instead" % sid)

    _cross_slot(rep, slots, states, at)
    _overrides(rep, slots, states, at)
    return rep, slots, states, schema_slots


def _val(slots, sid):
    return slots[sid].value if sid in slots else ""


def _cross_slot(rep, slots, states, at):
    st = states.get

    # Recording consent gates the capture layout, and the two are written far apart.
    if st("C.capture_paths") == "value" and st("B.consent_recording") != "value":
        rep.err("CROSS-SLOT", at("C.capture_paths"),
                "capture paths are declared while `B.consent_recording` is not answered - a "
                "layout for a pipeline nobody consented to is the pipeline's first step")
    if st("C.capture_paths") == "value" and st("B.consent_recording") == "value" \
            and not re.match(r"^(yes|y\b)", _val(slots, "B.consent_recording").strip(), re.I):
        rep.err("CROSS-SLOT", at("C.capture_paths"),
                "capture paths are declared but `B.consent_recording` does not start with an "
                "explicit `yes` - no skill may start a capture pipeline on this profile")
    if re.search(r"off[- ]game", _val(slots, "C.capture_paths"), re.I) \
            and not re.match(r"^(yes|y\b)", _val(slots, "B.consent_offgame").strip(), re.I):
        rep.err("CROSS-SLOT", at("C.capture_paths"),
                "an off-game note path is declared without an explicit `yes` in "
                "`B.consent_offgame` - agreeing to be recorded is not agreeing to be indexed")

    # If players can read the repo, GM-facing material needs a declared home.
    access = _val(slots, "C.player_access")
    if st("C.player_access") == "value" and not re.search(r"\b(nothing|none)\b", access, re.I) \
            and st("C.gm_private") not in ("value",):
        rep.err("CROSS-SLOT", at("C.gm_private"),
                "`C.player_access` lets players read something while `C.gm_private` is not "
                "answered - a skill must never improvise where GM-only material lives")

    # Rotation arithmetic: P7 is defined by these two numbers and nothing else.
    size, prot = LEADING_INT.match(_val(slots, "B.size")), \
        LEADING_INT.match(_val(slots, "B.protagonists"))
    if size and prot and int(prot.group(1)) > int(size.group(1)):
        rep.err("CROSS-SLOT", at("B.protagonists"),
                "`B.protagonists` (%s) exceeds `B.size` (%s) - the rotation period is not a "
                "number" % (prot.group(1), size.group(1)))

    # A resource that is `none` switches off a whole family; a resource with a value drags it.
    family = ["A.resource_shape", "A.resource_scale", "A.resource_loss", "A.resource_gain",
              "A.resource_asymmetry", "A.resource_zero"]
    if st("A.resource") == "none":
        filled = [s for s in family if st(s) == "value"]
        if filled:
            rep.err("CROSS-SLOT", at("A.resource"),
                    "`A.resource` is `none` but its family still holds values (%s) - prep, log "
                    "and arc read those and will show a resource this table does not play"
                    % ", ".join(filled))
    elif st("A.resource") == "value" and st("A.resource_shape") != "value":
        rep.err("CROSS-SLOT", at("A.resource"),
                "`A.resource` has a value but `A.resource_shape` is unanswered - the log's exit "
                "state has one row per character, one row, or one per faction because of it")

    # A one-shot has no recap to open and no arc above it.
    if re.match(r"^one[- ]shot", _val(slots, "D.shape").strip(), re.I) \
            and st("D.recap") == "value":
        rep.warn("CROSS-SLOT", at("D.recap"),
                 "`D.shape` is a one-shot but `D.recap` declares a recap form - there is no "
                 "previous session to recap; ttrpg-table-recap will stop")


def _overrides(rep, slots, states, at):
    if states.get("E.overrides") != "value":
        return
    value = _val(slots, "E.overrides")
    for pn in re.findall(r"(?<![A-Za-z0-9])P(\d{1,2})(?![0-9A-Za-z])", value):
        tag = "P" + pn
        if tag in NOT_OVERRIDABLE:
            rep.err("OVERRIDE-SCOPE", at("E.overrides"),
                    "%s appears in `E.overrides`, and it is not overridable: it prevents a "
                    "document failing at the table or state silently desynchronising. Only P4, "
                    "P5, P6, P7, P8, P9, P12 and P13 are strong defaults" % tag)
    tags = re.findall(r"(?<![A-Za-z0-9])P\d{1,2}(?![0-9A-Za-z])", value)
    if tags and not re.search(r"\b(off|replaced|disabled)\b", value, re.I):
        rep.err("OVERRIDE-SCOPE", at("E.overrides"),
                "`E.overrides` names %s without saying `off` or `replaced by <x>` - a skill "
                "reads the verb, not the intention (format: `P7 - off: reason`)"
                % ", ".join(sorted(set(tags))))


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def resolve_profile(path):
    """Accept the profile itself, or a campaign root to search - the same courtesy every skill
    extends: find it before declaring it missing."""
    if os.path.isfile(path):
        return path
    if os.path.isdir(path):
        direct = os.path.join(path, "campaign-profile.md")
        if os.path.isfile(direct):
            return direct
        for base, dirs, names in os.walk(path):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for n in sorted(names):
                if n.endswith(".md"):
                    p = os.path.join(base, n)
                    try:
                        head = _read(p)[:400]
                    except OSError:
                        continue
                    if "type: campaign-profile" in head:
                        return p
        sys.exit("fatal: no campaign profile under %s (searched for `type: campaign-profile`)"
                 % path)
    sys.exit("fatal: no such file or directory: %s" % path)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="validate_profile.py",
        description="Validate a campaign profile against the schema it was cut from.")
    ap.add_argument("profile", nargs="?", help="the profile, or a campaign root to search")
    ap.add_argument("--schema", default=DEFAULT_SCHEMA,
                    help="the schema to validate against (default: this repo's template)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--only", action="append", metavar="CODE",
                    help="report only these rules (repeatable, or comma-separated)")
    ap.add_argument("--list", action="store_true", help="list the rules and exit")
    args = ap.parse_args(argv)
    utf8_stdout()

    if args.list:
        width = max(len(r.code) for r in RULES)
        for r in RULES:
            print("%-*s  %-5s  %s" % (width, r.code, r.level, r.fails_when))
        return 0
    if not args.profile:
        ap.error("give a profile path (or a campaign root), or --list")

    only = None
    if args.only:
        only = [c.strip().upper() for item in args.only for c in item.split(",") if c.strip()]
        unknown = sorted(set(only) - set(RULE_CODES))
        if unknown:
            ap.error("unknown rule(s): %s (see --list)" % ", ".join(unknown))

    path = resolve_profile(args.profile)
    rep, slots, states, schema_slots = validate(path, args.schema, only)
    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))

    core = [s for s in schema_slots.values() if s.core]
    answered = sum(1 for s in core if states.get(s.id) in ("value", "deferred", "none"))
    counts = {st: sum(1 for v in states.values() if v == st)
              for st in ("value", "deferred", "none", "placeholder")}
    summary = ("%d/%d slots present | core answered %d/%d | %d value, %d deferred, %d none, "
               "%d never asked" % (len(states), len(schema_slots), answered, len(core),
                                   counts["value"], counts["deferred"], counts["none"],
                                   counts["placeholder"]))

    if args.format == "json":
        print(json.dumps({
            "profile": os.path.abspath(path),
            "schema": os.path.abspath(args.schema),
            "summary": summary,
            "states": states,
            "findings": [f._asdict() for f in
                         sorted(rep.findings, key=lambda f: (f.level, f.check, f.where))],
            "counts": {"errors": len(rep.errors), "warnings": len(rep.warnings)},
            "ok": not failed,
        }, indent=2, sort_keys=False))
        return 1 if failed else 0

    print("profile check - %s" % os.path.abspath(path))
    print("  %s" % summary)
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
