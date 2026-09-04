#!/usr/bin/env python3
"""Mechanical contract checker for ttrpg-campaign-skills.

Run from the repo root:  python3 scripts/check_contract.py [repo-root]
Exit code 1 if any ERROR. WARNings never fail the build.

Ten checks:

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

# Files the installer creates inside every skill folder. A link to one of these is
# valid even though the file is absent from the checkout (see install.sh).
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

cited_principles = set()
for f in cite_md:
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
    nm = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
    if not nm:
        err("FRONTMATTER", rel(p), "frontmatter has no 'name'")
    elif nm.group(1).strip("\"'") != d:
        err("FRONTMATTER", rel(p),
            "frontmatter name '%s' != folder '%s' (the router resolves by folder)"
            % (nm.group(1), d))
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
    if "Use when" not in desc:
        err("FRONTMATTER", rel(p),
            "description has no explicit 'Use when ...' trigger - the router sees "
            "nothing else")
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

# ---------- report -------------------------------------------------------
print("contract check - %s" % ROOT)
print("  %d slots defined (%d setup-only, exempt from DEAD-SLOT), %d cited | "
      "%d principles defined, %d cited | %d skills, %d markdown files"
      % (len(defined_slots), len(setup_only_slots), len(cited_slots), len(principles),
         len(cited_principles & principles), len(skill_dirs), len(skill_md)))
print("")
for line in sorted(errors):
    print(line)
if errors and warns:
    print("")
for line in sorted(warns):
    print(line)
print("\n%d error(s), %d warning(s)." % (len(errors), len(warns)))
sys.exit(1 if errors else 0)
