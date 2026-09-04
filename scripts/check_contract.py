#!/usr/bin/env python3
r"""Mechanical contract checker for ttrpg-campaign-skills.

Run from the repo root:  python3 scripts/check_contract.py [repo-root]
Exit code 1 if any ERROR. WARNings never fail the build.

Sixteen checks:

  1  SLOT-RESOLVES     every slot id cited under skills/ (a section letter A-E, a dot,
                       a lowercase slot name) is defined in templates/campaign-profile.md.
  2  NO-LEGACY-SLOTS   no numeric profile citation (a section sigil followed by a digit)
                       survives anywhere under skills/. Schema 2 names its sections.
  3  BUNDLE-IDENTICAL  skills/ttrpg-campaign-setup/references/campaign-profile.md is
                       byte-identical to templates/campaign-profile.md. It is a bundled
                       copy, not a fork: the interview is driven from it.
  4  DEAD-SLOT         every slot defined in the template is read by at least one CONSUMER
                       skill. Citations by ttrpg-campaign-setup do not count: it collects
                       every slot by construction, so counting it would make every dead
                       slot look alive. A slot nothing consumes is a question asked for
                       nobody.
  5  PRINCIPLE-RESOLVES  every Pn cited under skills/ is defined in docs/PRINCIPLES.md;
                       a principle nobody cites is a WARNing, not a failure.
  6  PRINCIPLE-RANGE   the range advertised in a skill preamble ("P1...Pn") equals the
                       highest principle actually defined, and covers every Pn the body
                       cites. P13 resolving fine is exactly why check 5 misses this.
  7  LINK-ESCAPES      no relative link inside a skill folder points outside it
                       (../, docs/, templates/, absolute): install copies the folder alone.
  8  LINK-BROKEN       every inward link resolves to a file that exists once installed.
                       Files the installer materialises are whitelisted; backtick-quoted
                       references/foo.md mentions in prose are checked too.
  9  FRONTMATTER       valid YAML frontmatter with name + description; folder name equals
                       `name`; description carries an explicit "Use when" and at least one
                       sibling-skill boundary; description within DESC_MAX; no U+FFFD.
 10  SECTION-OWNERSHIP no two skills define the same domain section heading (structural
                       boilerplate whitelisted).
 11  NO-SYSTEM-NAMES   no shipped file names one of the game systems or note-taking tools
                       on the blocklist below. A blocklist can never be complete, so this
                       is a floor under the manual agnosticism self-test of AUTHORING §1,
                       not a replacement for it: it catches the names that actually leaked.
                       There is no per-file exception list on purpose - a system name
                       belongs in `A.ruleset`, which the campaign fills, or in an overlay.
 12  MECHANICS-LEAK    no shipped file uses a proprietary subsystem vocabulary (DC, HP,
                       AC, saving throw, d20, encounter table, combat rounds). WARN, not
                       ERROR: a neutral phrasing always exists ("a difficulty value", "the
                       opposition is depleted") but only prose review can pick it. The list
                       is deliberately partial - "XP" stays legal, since a skill may name
                       the measure `A.ruleset` uses when it enumerates alternatives.
 13  ENCODING          no markdown in the repo carries encoding damage: U+FFFD, or a
                       literal \uXXXX escape that renders as six characters. Check 9 caught
                       this only in frontmatter, and only in SKILL.md.
 14  OVERRIDE-MAPPED   every skill carries an `E.overrides` branch in Phase 0 - or, for
                       ttrpg-campaign-setup alone, in the interview phase, since it fills
                       the slot instead of obeying it - and not just a
                       mention of the slot. `E.overrides` is the package's central promise
                       ("declare P5 - off and no skill argues") and eight of nine skills
                       once cited the slot while mapping nothing, which is invisible to a
                       checker that only resolves ids.
 15  ARTIFACT-CONTRACT a skeleton that shows a frontmatter placeholder also declares the
                       package's fixed `type:` key (the cross-skill contract that lets one
                       skill find another's artifact whatever the file is named, exactly as
                       `type: campaign-profile` finds a renamed profile), and no two skills
                       claim the same type value.
 16  PHASE0-PROTOCOL   every consumer skill's Phase 0 carries, before Phase 1, the
                       find-the-profile search protocol and a `D.shape` branch or gate;
                       ttrpg-campaign-setup instead carries its own 'Search before you
                       conclude' protocol. Nine hand-written Phase 0s drift apart unless
                       their shared spine is mechanical.
"""
import io
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                  errors="replace", line_buffering=True)

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
PROFILE = os.path.join(ROOT, "templates", "campaign-profile.md")
PRINC = os.path.join(ROOT, "docs", "PRINCIPLES.md")
SKILLS = os.path.join(ROOT, "skills")
SETUP_SKILL = "ttrpg-campaign-setup"
BUNDLED_PROFILE = os.path.join(SKILLS, SETUP_SKILL, "references", "campaign-profile.md")

SECTION = "\u00a7"          # the slot sigil
DESC_MAX = 1024             # agent-skill description budget
NAME_MAX = 64               # agent-skill name budget

# Historically the installer materialised this file, so a link to it was valid even when the
# checkout lacked it. It is checked-in content now (see BUNDLE-IDENTICAL below), and this
# whitelist only keeps LINK-BROKEN from reporting a second time what that check already owns.
INSTALL_MATERIALISED = {"references/PRINCIPLES.md"}

# Headings every skill legitimately shares: they structure the skill itself, they are
# not claims on a campaign artifact. Only collisions OUTSIDE this set are ownership bugs.
BOILERPLATE = {
    "what not to do",
    "read the campaign profile",
    "read before writing",
    "read before auditing",
    "required elements",
    "verify and hand off",
    "at a glance",
    "when to run",
    "the report",
    "what this skill produces",
    "what the answers imply",
}

errors, warns = [], []


def err(check, where, msg):
    errors.append("ERROR [%s] %s: %s" % (check, where, msg))


def warn(check, where, msg):
    warns.append("WARN  [%s] %s: %s" % (check, where, msg))


def read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


# ---------- load the two contracts ---------------------------------------
for required in (PROFILE, PRINC):
    if not os.path.isfile(required):
        sys.exit("fatal: missing %s" % rel(required))

profile_src = read(PROFILE)

# A slot is DEFINED by a bullet of the form:  - **`A.resource`** - ...
# (also handles two slots declared on one bullet: `A.resource_loss` / `A.resource_gain`)
SLOT = re.compile(r"`([A-E]\.[a-z_]+)`")
defined_slots = set()
# A slot annotated *(setup-only)* is recorded for the humans and for the setup interview;
# no skill is expected to branch on it, so it is exempt from DEAD-SLOT. The exemption is
# parsed from the schema, never hardcoded, and its count is reported so it stays visible.
setup_only_slots = set()
for line in profile_src.splitlines():
    if re.match(r"^\s*-\s+\*\*", line):
        found = SLOT.findall(line)
        defined_slots.update(found)
        if "*(setup-only)*" in line:
            setup_only_slots.update(found)
if not defined_slots:
    err("SLOT-RESOLVES", rel(PROFILE),
        "no slot definitions found (expected bullets like - **`A.resource`**)")

principles = set(re.findall(r"^###\s+(P\d{1,2})\b", read(PRINC), re.M))
if not principles:
    err("PRINCIPLE-RESOLVES", rel(PRINC), "no '### Pn' principle headings found")
highest_principle = max((int(p[1:]) for p in principles), default=0)

skill_dirs = sorted(d for d in os.listdir(SKILLS)
                    if os.path.isdir(os.path.join(SKILLS, d))) if os.path.isdir(SKILLS) else []

# every markdown file under skills/, minus the bundled schema copy: that file DEFINES
# slots, it does not cite them, and counting it would make every dead slot look alive.
skill_md = []
for base, _dirs, names in os.walk(SKILLS):
    for n in sorted(names):
        if n.endswith(".md"):
            skill_md.append(os.path.join(base, n))
skill_md.sort()
cite_md = [p for p in skill_md if os.path.normcase(p) != os.path.normcase(BUNDLED_PROFILE)]

# ---------- 1 + 2 + 4 + 5: citations -------------------------------------
CITE = re.compile(r"(?<![A-Za-z0-9.])([A-E]\.[a-z_]{2,})")
LEGACY = re.compile(SECTION + r"\s*\d")
cited_slots = defaultdict(list)      # slot -> [skill dirs]

for f in cite_md:
    skill = rel(f).split("/")[1] if rel(f).startswith("skills/") else "?"
    for i, line in enumerate(read(f).splitlines(), 1):
        for m in CITE.finditer(line):
            slot = m.group(1)
            if slot in defined_slots:
                cited_slots[slot].append(skill)
            else:
                err("SLOT-RESOLVES", "%s:%d" % (rel(f), i),
                    "`%s` is not a slot defined in templates/campaign-profile.md" % slot)
        if LEGACY.search(line):
            err("NO-LEGACY-SLOTS", "%s:%d" % (rel(f), i),
                "legacy numeric profile citation %r - schema 2 sections are named "
                "(A-E) and slots are cited as `B.distance`"
                % LEGACY.search(line).group(0))
        for m in re.finditer(r"(?<![A-Za-z0-9])P(\d{1,2})(?![0-9A-Za-z])", line):
            if "P" + m.group(1) not in principles:
                err("PRINCIPLE-RESOLVES", "%s:%d" % (rel(f), i),
                    "P%s does not resolve to any principle in docs/PRINCIPLES.md"
                    % m.group(1))

for slot in sorted(defined_slots - setup_only_slots):
    consumers = {s for s in cited_slots.get(slot, ()) if s != SETUP_SKILL}
    if not consumers:
        only_setup = bool(cited_slots.get(slot))
        err("DEAD-SLOT", rel(PROFILE),
            "`%s` is defined in the schema but read by no consumer skill%s - the "
            "interview collects it and nothing ever uses it"
            % (slot, " (only %s cites it, and it collects every slot by "
                     "construction)" % SETUP_SKILL if only_setup else ""))

# Count citations from the skills themselves only: the bundled PRINCIPLES copies define every
# tag, so counting them would make every principle look cited and this warning unreachable.
cited_principles = set()
for f in cite_md:
    if os.path.basename(f) == "PRINCIPLES.md":
        continue
    cited_principles.update("P" + m for m in
                            re.findall(r"(?<![A-Za-z0-9])P(\d{1,2})(?![0-9A-Za-z])", read(f)))
for p in sorted(principles, key=lambda t: int(t[1:])):
    if p not in cited_principles:
        warn("PRINCIPLE-RESOLVES", rel(PRINC), "%s is defined but cited by no skill" % p)

# ---------- 3: the bundled schema is a copy, not a fork ------------------
if not os.path.isfile(BUNDLED_PROFILE):
    err("BUNDLE-IDENTICAL", rel(BUNDLED_PROFILE),
        "missing - %s drives its interview from this bundled copy" % SETUP_SKILL)
else:
    with open(PROFILE, "rb") as a, open(BUNDLED_PROFILE, "rb") as b:
        src, dst = a.read(), b.read()
    if src != dst:
        err("BUNDLE-IDENTICAL", rel(BUNDLED_PROFILE),
            "has drifted from templates/campaign-profile.md (%d vs %d bytes) - it is a "
            "bundled copy, not a fork; re-copy the template" % (len(dst), len(src)))

# Same rule for the principles bundled into every skill: they are CHECKED-IN content, not
# install-time output, so a clone is a valid package and an agent pointed at the repo can
# resolve the tags it is told to cite.
with open(PRINC, "rb") as f:
    princ_src = f.read()
for d in skill_dirs:
    bundled = os.path.join(SKILLS, d, "references", "PRINCIPLES.md")
    if not os.path.isfile(bundled):
        err("BUNDLE-IDENTICAL", "skills/%s/references/PRINCIPLES.md" % d,
            "missing - every skill preamble links it, and installation copies the folder "
            "alone; it must exist in the repo, not be generated by the installer")
    elif open(bundled, "rb").read() != princ_src:
        err("BUNDLE-IDENTICAL", "skills/%s/references/PRINCIPLES.md" % d,
            "has drifted from docs/PRINCIPLES.md - it is a bundled copy, not a fork")

# ---------- 6: advertised principle range vs cited ----------------------
ADV = re.compile(r"`?P1`?\s*(?:\u2026|\.{2,3})\s*`?P(\d{1,2})`?")
for d in skill_dirs:
    p = os.path.join(SKILLS, d, "SKILL.md")
    if not os.path.isfile(p):
        continue
    src = read(p)
    cited = {int(x) for x in
             re.findall(r"(?<![A-Za-z0-9])P(\d{1,2})(?![0-9A-Za-z])", src)}
    m = ADV.search(src)
    if not m:
        warn("PRINCIPLE-RANGE", rel(p), "preamble advertises no principle range")
        continue
    top = int(m.group(1))
    if top != highest_principle:
        err("PRINCIPLE-RANGE", rel(p),
            "preamble advertises P1...P%d but docs/PRINCIPLES.md defines up to P%d"
            % (top, highest_principle))
    over = sorted(n for n in cited if n > top)
    if over:
        err("PRINCIPLE-RANGE", rel(p),
            "cites %s but its preamble advertises only up to P%d"
            % (", ".join("P%d" % n for n in over), top))

# ---------- 7 + 8: links, once the folder is installed alone ------------
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BACKTICK_REF = re.compile(r"`(references/[A-Za-z0-9._/-]+\.[a-z]+)`")
OUTSIDE_HINT = ("docs/", "templates/", "scripts/", "assets/")

for d in skill_dirs:
    sdir = os.path.join(SKILLS, d)
    for base, _dirs, names in os.walk(sdir):
        for n in sorted(names):
            if not n.endswith(".md"):
                continue
            p = os.path.join(base, n)
            for i, line in enumerate(read(p).splitlines(), 1):
                # markdown links resolve against the containing file; a backtick-quoted
                # references/foo.md in prose names a path from the skill folder root.
                targets = [(m.group(1), "link", base) for m in LINK.finditer(line)]
                targets += [(m.group(1), "backtick reference", sdir)
                            for m in BACKTICK_REF.finditer(line)]
                for raw, kind, anchor in targets:
                    t = raw.split("#")[0].strip()
                    if not t or re.match(r"^[a-z][a-z0-9+.-]*:", t):
                        continue                            # anchor or external URL
                    if t.startswith("/") or t.startswith("..") or "/../" in t:
                        err("LINK-ESCAPES", "%s:%d" % (rel(p), i),
                            "%s leaves the skill folder: %s - installation copies the "
                            "folder alone, so this is dead on the installed copy"
                            % (kind, t))
                        continue
                    inside_rel = os.path.relpath(
                        os.path.normpath(os.path.join(anchor, t)), sdir).replace("\\", "/")
                    if inside_rel.startswith(".."):
                        err("LINK-ESCAPES", "%s:%d" % (rel(p), i),
                            "%s leaves the skill folder: %s" % (kind, t))
                        continue
                    if inside_rel in INSTALL_MATERIALISED:
                        continue                            # created by install.sh
                    if not os.path.exists(os.path.join(sdir, inside_rel)):
                        hint = ""
                        if t.startswith(OUTSIDE_HINT):
                            hint = (" - that path exists in the repo but not inside the "
                                    "installed skill folder; bundle the file or drop the link")
                        err("LINK-BROKEN", "%s:%d" % (rel(p), i),
                            "%s points at %s, which does not exist in the skill folder%s"
                            % (kind, t, hint))

# ---------- 9: frontmatter ----------------------------------------------
known_skills = set(skill_dirs)
for d in skill_dirs:
    p = os.path.join(SKILLS, d, "SKILL.md")
    if not os.path.isfile(p):
        err("FRONTMATTER", "skills/" + d, "no SKILL.md")
        continue
    txt = read(p)
    if "\ufffd" in txt:
        err("FRONTMATTER", rel(p), "contains U+FFFD replacement character (encoding damage)")
    m = re.match(r"^---\r?\n(.*?)\r?\n---\s*$", txt, re.S | re.M)
    if not m:
        err("FRONTMATTER", rel(p), "missing or unterminated YAML frontmatter")
        continue
    fm = m.group(1)
    if re.search(r"^\t", fm, re.M):
        err("FRONTMATTER", rel(p), "frontmatter contains a tab (invalid YAML indentation)")
    # The published skill format accepts only these top-level keys; anything else is
    # dropped or rejected by the loader, so a typo here silently loses a field.
    keys = set(re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", fm, re.M))
    unexpected = sorted(keys - {"name", "description", "license", "allowed-tools",
                                "compatibility", "metadata"})
    if unexpected:
        err("FRONTMATTER", rel(p),
            "unexpected frontmatter key(s): %s - allowed: name, description, license, "
            "allowed-tools, compatibility, metadata" % ", ".join(unexpected))
    nm = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
    if not nm:
        err("FRONTMATTER", rel(p), "frontmatter has no 'name'")
    else:
        name = nm.group(1).strip("\"'")
        if name != d:
            err("FRONTMATTER", rel(p),
                "frontmatter name '%s' != folder '%s' (the router resolves by folder)"
                % (name, d))
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            err("FRONTMATTER", rel(p),
                "name '%s' is not hyphen-case (lowercase, digits, single hyphens, no "
                "leading/trailing hyphen)" % name)
        if len(name) > NAME_MAX:
            err("FRONTMATTER", rel(p),
                "name is %d chars, over the %d budget" % (len(name), NAME_MAX))
    ds = re.search(r"^description:\s*(.*?)(?=\n[A-Za-z_][A-Za-z0-9_-]*:|\Z)",
                   fm, re.M | re.S)
    if not ds:
        err("FRONTMATTER", rel(p), "frontmatter has no 'description'")
        continue
    desc = " ".join(ds.group(1).split()).strip("\"'")
    if not desc:
        err("FRONTMATTER", rel(p), "'description' is empty")
        continue
    if len(desc) > DESC_MAX:
        err("FRONTMATTER", rel(p),
            "description is %d chars, over the %d budget" % (len(desc), DESC_MAX))
    if "<" in desc or ">" in desc:
        err("FRONTMATTER", rel(p),
            "description contains an angle bracket - the skill format forbids < and >")
    if "Use when" not in desc:
        err("FRONTMATTER", rel(p),
            "description has no explicit 'Use when ...' trigger - the router sees "
            "nothing else")
    # Unfinished scaffolding: a [TODO: ...] left in the frontmatter or in the body
    # outside a fenced block. Inside a fence it is example text, not a hole.
    if "[TODO:" in fm:
        err("FRONTMATTER", rel(p), "frontmatter contains an unfinished [TODO: ...]")
    fence = None
    for i, line in enumerate(txt[m.end():].splitlines(), 1):
        f = re.match(r"^[ \t]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$", line)
        if f:
            if fence is None:
                fence = f.group(1)[0]
            elif f.group(1)[0] == fence and not f.group(2).strip():
                fence = None
            continue
        if fence is None and re.fullmatch(r"[ ]{0,3}\[TODO:[^\n]*\][ \t]*", line):
            err("FRONTMATTER", rel(p),
                "body contains an unfinished [TODO: ...] placeholder")
    siblings = {s for s in re.findall(r"\bttrpg-[a-z][a-z-]+\b", desc)
                if s != d and s != "ttrpg-campaign-skills"}
    unknown = sorted(s for s in siblings if s not in known_skills)
    if unknown:
        err("FRONTMATTER", rel(p),
            "description names skills that do not exist: %s" % ", ".join(unknown))
    if not (siblings - set(unknown)):
        err("FRONTMATTER", rel(p),
            "description declares no sibling-skill boundary ('Does not ..., see "
            "ttrpg-<skill>') - adjacent skills collide in the router without it")

# ---------- 10: one domain section, one owner ---------------------------
TAGS = re.compile(r"\s*\((?:(?:P\d{1,2}|[A-E]\.[a-z_]+|" + SECTION +
                  r"?[A-E])[,;\s]*)+\)\s*$")
heads = defaultdict(list)
for d in skill_dirs:
    p = os.path.join(SKILLS, d, "SKILL.md")
    if not os.path.isfile(p):
        continue
    fenced = False
    for i, line in enumerate(read(p).splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = re.match(r"^#{2,4}\s+(.+?)\s*$", line)
        if not m:
            continue
        key = TAGS.sub("", m.group(1)).strip().lower()
        key = re.sub(r"^phase\s+\S+\s*[-\u2014]\s*", "", key)
        key = re.sub(r"^\d+(\.\d+)*\s+", "", key)
        if len(key) > 8:
            heads[key].append((d, "%s:%d" % (rel(p), i)))
for key, locs in sorted(heads.items()):
    if key in BOILERPLATE:
        continue
    owners = sorted({d for d, _ in locs})
    if len(owners) > 1:
        err("SECTION-OWNERSHIP", "skills/",
            'section "%s" is defined by %d skills (%s) - two skills claim the same '
            "artifact" % (key, len(owners), ", ".join(loc for _, loc in locs)))

# ---------- 11 + 12 + 13: agnosticism and encoding, mechanically --------
# "Shipped" = what a clone hands to an agent: every skill folder, the schema they read,
# and the principles bundled into all nine. AGENTS.md, README.md and docs/AUTHORING.md
# are meta - AUTHORING has to be able to quote a bad example in order to forbid it.
SHIPPED = list(skill_md)
for base, _dirs, names in os.walk(os.path.join(ROOT, "templates")):
    SHIPPED += [os.path.join(base, n) for n in sorted(names) if n.endswith(".md")]
SHIPPED.append(PRINC)
# The nine bundled copies are byte-identical to docs/PRINCIPLES.md: scan the content once, so
# one defect is one message instead of ten, and the reported count means what it says.
seen, deduped = set(), []
for p in SHIPPED:
    key = os.path.basename(p) if os.path.basename(p) == "PRINCIPLES.md" else os.path.normcase(p)
    if key in seen:
        continue
    seen.add(key)
    deduped.append(p)
SHIPPED = deduped

# One name here is one game system. A base skill that needs to say which system it is
# running is a base skill that stopped being one.
SYSTEM_NAMES = re.compile(
    r"(?<![A-Za-z0-9])("
    r"d\s?&\s?d|dungeons?\s*(?:&|and)\s*dragons|"
    r"pathfinder|dungeon world|call of cthulhu|cthulhu|"
    r"pbta|powered by the apocalypse|blades in the dark|forged in the dark|"
    r"gurps|savage worlds|shadowrun|warhammer|numenera|mothership|delta green|"
    r"vampire: the masquerade|fate core|ars magica|m[o\u00f6]rk borg|apocalypse world|"
    r"ironsworn|runequest|shadowdark|cypher system|fabula ultima|traveller rpg|"
    r"5e|3\.5e|4e|2e|5th edition|osr|"
    # note-taking and play tools: the README promises no skill names an editor, and
    # everything tool-shaped is a slot (`C.links`, `C.frontmatter`, `C.blocks`, `C.verify`)
    r"obsidian|logseq|notion|foundry vtt|roll20|owlbear|fantasy grounds"
    r")(?![A-Za-z0-9])", re.I)

# Vocabulary that presupposes one family of systems. Acronyms are matched case-sensitively
# (a lowercase "ac" is a word), phrases are not.
MECH_ACRONYMS = re.compile(r"(?<![A-Za-z0-9])(DCs?|HP|AC|THAC0|d20)(?![A-Za-z0-9])")
MECH_PHRASES = re.compile(
    r"(?<![A-Za-z0-9])(hit points?|armou?r class|difficulty class|saving throws?|"
    r"advantage/disadvantage|encounter tables?|spell slots?|long rest|"
    r"combat rounds?|rounds? of combat)(?![A-Za-z0-9])", re.I)

BAD_ESCAPE = re.compile(r"\\u[0-9a-fA-F]{4}")

for f in SHIPPED:
    for i, line in enumerate(read(f).splitlines(), 1):
        m = SYSTEM_NAMES.search(line)
        if m:
            err("NO-SYSTEM-NAMES", "%s:%d" % (rel(f), i),
                "names a game system (%r) - a base skill never does; the system is "
                "`A.ruleset`, which the campaign fills, and anything irreducibly "
                "system-shaped goes in an overlay" % m.group(0))
        for mm in (MECH_ACRONYMS.search(line), MECH_PHRASES.search(line)):
            if mm:
                warn("MECHANICS-LEAK", "%s:%d" % (rel(f), i),
                     "uses the vocabulary of one system family (%r) - say it neutrally "
                     "(a difficulty value, a cost, the opposition is depleted) or read "
                     "the term from `A.ruleset`" % mm.group(0))
# ENCODING is not limited to shipped files: no markdown in this repo has a reason to carry
# U+FFFD or a literal escape, AGENTS.md included - it is the first file an agent reads.
all_md, seen_md = [], set()
for base, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d != ".git"]
    for n in sorted(names):
        p = os.path.join(base, n)
        if n.endswith(".md") and os.path.normcase(p) not in seen_md:
            seen_md.add(os.path.normcase(p))
            all_md.append(p)
for f in all_md:
    for i, line in enumerate(read(f).splitlines(), 1):
        if "\ufffd" in line:
            err("ENCODING", "%s:%d" % (rel(f), i),
                "contains U+FFFD replacement character (encoding damage)")
        e = BAD_ESCAPE.search(line)
        if e:
            err("ENCODING", "%s:%d" % (rel(f), i),
                "contains the literal escape %r - it renders as six characters, not as "
                "the intended glyph; write the character itself" % e.group(0))

# ---------- 14: the override mechanism is mapped, not mentioned ---------
# Citing `E.overrides` in a Phase 0 table row is not implementing it. The branch is what
# tells a reader WHICH of that skill's requirements each override switches off.
BRANCH = re.compile(r"\*\*`E\.overrides`\s+branch\s+\u2014\s+mandatory\.\*\*")
for d in skill_dirs:
    p = os.path.join(SKILLS, d, "SKILL.md")
    if not os.path.isfile(p):
        continue
    src = read(p)
    if not BRANCH.search(src):
        err("OVERRIDE-MAPPED", rel(p),
            "has no '**`E.overrides` branch \u2014 mandatory.**' block - the slot must be mapped "
            "to what stops being required in THIS skill, not merely listed in Phase 0")
    elif d == SETUP_SKILL:
        # The interviewer FILLS the slot instead of obeying it, so its branch belongs to the
        # interview phase, not to Phase 0. Stated here rather than silently tolerated.
        pass
    elif "E.overrides" not in src.split("## Phase 1")[0]:
        err("OVERRIDE-MAPPED", rel(p),
            "maps `E.overrides` outside Phase 0 - it is read before anything is produced")

# ---------- 15: the artifact type contract -------------------------------
# A Phase 2 skeleton showing a frontmatter placeholder must also declare the fixed `type:` key,
# and one type value has one owner - two skills claiming the same type is the SECTION-OWNERSHIP
# bug at the artifact level.
artifact_types = defaultdict(list)
for d in skill_dirs:
    p = os.path.join(SKILLS, d, "SKILL.md")
    if not os.path.isfile(p):
        continue
    fence = None
    needs, found = [], []
    for i, line in enumerate(read(p).splitlines(), 1):
        f = re.match(r"^[ \t]*(`{3,}|~{3,})", line)
        if f:
            fence = None if fence else f.group(1)[0]
            continue
        if fence is None:
            continue
        if "frontmatter per C.frontmatter" in line:
            needs.append(i)
        m = re.match(r"^type:\s*([a-z][a-z-]*)", line)
        if m:
            found.append((i, m.group(1)))
    if needs and not found:
        err("ARTIFACT-CONTRACT", "%s:%d" % (rel(p), needs[0]),
            "skeleton shows a frontmatter placeholder but declares no fixed `type:` key - "
            "without it no other skill can find this artifact once the campaign names it")
    for i, val in found:
        artifact_types[val].append((d, "%s:%d" % (rel(p), i)))
for val, locs in sorted(artifact_types.items()):
    owners = sorted({d for d, _ in locs})
    if len(owners) > 1:
        err("ARTIFACT-CONTRACT", "skills/",
            "`type: %s` is claimed by %d skills (%s) - one artifact type, one owner"
            % (val, len(owners), ", ".join(loc for _, loc in locs)))
    if val == "campaign-profile":
        err("ARTIFACT-CONTRACT", locs[0][1],
            "`type: campaign-profile` belongs to the schema, not to a skill's skeleton")

# ---------- 16: the Phase 0 protocol is present and ordered ---------------
# The shared spine of every consumer Phase 0: find the profile before declaring it missing,
# and branch on D.shape - both before anything is produced. OVERRIDE-MAPPED owns the third step.
FINDIT = "Find it before declaring it missing"
DSHAPE_BRANCH = re.compile(r"\*\*`D\.shape`\s+(branch|gate)")
for d in skill_dirs:
    p = os.path.join(SKILLS, d, "SKILL.md")
    if not os.path.isfile(p):
        continue
    src = read(p)
    if d == SETUP_SKILL:
        if "Search before you conclude" not in src:
            err("PHASE0-PROTOCOL", rel(p),
                "the finder skill must keep its 'Search before you conclude' protocol - it is "
                "what every other skill's find-it rule delegates to")
        continue
    cut = src.find("\n## Phase 1")
    head = src[:cut] if cut != -1 else src
    if FINDIT not in head:
        err("PHASE0-PROTOCOL", rel(p),
            "Phase 0 lacks the find-the-profile protocol ('%s') before Phase 1 - a profile "
            "that exists but is not found re-interviews a GM who already answered" % FINDIT)
    if not DSHAPE_BRANCH.search(head):
        err("PHASE0-PROTOCOL", rel(p),
            "no `D.shape` branch or gate before Phase 1 - a skill that cannot serve a shape "
            "must say so before it produces anything")

# ---------- report -------------------------------------------------------
print("contract check - %s" % ROOT)
print("  %d slots defined (%d setup-only, exempt from DEAD-SLOT), %d cited | "
      "%d principles defined, %d cited | %d skills, %d markdown files | "
      "%d shipped files scanned for system leaks"
      % (len(defined_slots), len(setup_only_slots), len(cited_slots), len(principles),
         len(cited_principles & principles), len(skill_dirs), len(skill_md),
         len(SHIPPED)))
print("")
for line in sorted(errors):
    print(line)
if errors and warns:
    print("")
for line in sorted(warns):
    print(line)
print("\n%d error(s), %d warning(s)." % (len(errors), len(warns)))
sys.exit(1 if errors else 0)
