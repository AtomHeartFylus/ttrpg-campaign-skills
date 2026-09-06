#!/usr/bin/env python3
r"""Mechanical contract checker for ttrpg-campaign-skills.

    python3 scripts/check_contract.py [repo-root] [--strict] [--only CODE] [--format json]
    python3 scripts/check_contract.py --list        # every check and what it fails on

Exit 1 on any ERROR; WARNings fail only under `--strict` (which is what CI runs).

The checks themselves are registered in CHECKS below, one entry per code, and each one
owns a function in this file. `tests/checker/` keeps a negative fixture per registered
code: a checker with no test of its own does not fail when a regex stops matching - it
silently stops checking.

Stdlib only, on purpose: validating a clone must never require a tool installed
somewhere else on the machine.
"""
import argparse
import io
import json
import os
import re
import sys
from collections import defaultdict, namedtuple

def utf8_stdout():
    """Print em-dashes and section sigils on a console that defaults to something else.
    Called from main(), never at import: wrapping the same buffer twice closes the first
    wrapper when it is collected, and the second print raises on a closed file."""
    if hasattr(sys.stdout, "buffer") and getattr(sys.stdout, "encoding", "").lower() not in (
            "utf-8", "utf8"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8",
                                     errors="replace", line_buffering=True)


SECTION = "\u00a7"          # the slot sigil
DESC_MAX = 1024             # agent-skill description budget
NAME_MAX = 64               # agent-skill name budget
SETUP_SKILL = "ttrpg-campaign-setup"

# Historically the installer materialised this file, so a link to it was valid even when the
# checkout lacked it. It is checked-in content now (see BUNDLE-IDENTICAL), and this whitelist
# only keeps LINK-BROKEN from reporting a second time what that check already owns.
INSTALL_MATERIALISED = {"references/PRINCIPLES.md", "references/check_links.py"}

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
    # P14's report is about the run, not about a campaign artifact: every skill closes with it,
    # and that is the point - a section only one skill owned would make the report optional.
    "close with the run report",
}

Check = namedtuple("Check", "code level fails_when")

CHECKS = [
    Check("SLOT-RESOLVES", "error",
          "a skill cites a slot id templates/campaign-profile.md does not define"),
    Check("NO-LEGACY-SLOTS", "error",
          "a numeric profile citation survives under skills/ - schema 2 names its sections"),
    Check("BUNDLE-IDENTICAL", "error",
          "a bundled copy (the schema in setup, the principles in all nine) has drifted "
          "from its canonical source, or is missing"),
    Check("DEAD-SLOT", "error",
          "a slot is defined but read by no consumer skill - a question asked for nobody"),
    Check("PRINCIPLE-RESOLVES", "error",
          "a cited Pn is not defined in docs/PRINCIPLES.md (an uncited principle warns)"),
    Check("PRINCIPLE-RANGE", "error",
          "a preamble advertises a principle range that is not the real ceiling, or the "
          "body cites above it"),
    Check("LINK-ESCAPES", "error",
          "a link leaves the skill folder - installation copies the folder alone"),
    Check("LINK-BROKEN", "error",
          "an inward link or a backtick-quoted references/... path has no file"),
    Check("FRONTMATTER", "error",
          "invalid frontmatter: unknown key, name != folder, no 'Use when', no sibling "
          "boundary, over the description budget, unfinished [TODO:, encoding damage"),
    Check("SECTION-OWNERSHIP", "error",
          "two skills define the same domain section heading"),
    Check("NO-SYSTEM-NAMES", "error",
          "anything shipped names a game system or a note-taking tool - no exception "
          "list: the system is `A.ruleset`, which the campaign fills"),
    Check("MECHANICS-LEAK", "warn",
          "the vocabulary of one system family appears (DC, HP, AC, saving throw, d20, "
          "encounter table, combat rounds)"),
    Check("ENCODING", "error",
          "a markdown file carries U+FFFD or a literal \\uXXXX escape"),
    Check("OVERRIDE-MAPPED", "error",
          "a skill mentions `E.overrides` without a branch mapping it to what stops "
          "being required in THAT skill"),
    Check("ARTIFACT-CONTRACT", "error",
          "a skeleton shows a frontmatter placeholder without the fixed `type:` key, or "
          "two skills claim the same type value"),
    Check("PHASE0-PROTOCOL", "error",
          "a skill's Phase 0 carries no `<!-- phase0: ... -->` marker, declares an element it "
          "does not implement, or omits one its role requires (find-profile, d-shape, "
          "overrides; the finder skill declares search-protocol instead)"),
    Check("ENTRYPOINT-BUDGET", "warn",
          "an entrypoint is over the context budget (%d estimated tokens) - what costs a reader "
          "is tokens, not lines; push one-way-only detail into references/" % 5000),
]
CHECK_CODES = [c.code for c in CHECKS]


# ---------- reporting -----------------------------------------------------

Finding = namedtuple("Finding", "level check where message")


class Report(object):
    """Collects findings, dropping anything outside `only` so --only is a real filter."""

    def __init__(self, only=None):
        self.only = set(only) if only else None
        self.findings = []
        self.summary = ""

    def _add(self, level, code, where, msg):
        if self.only and code not in self.only:
            return
        self.findings.append(Finding(level, code, where, msg))

    def err(self, code, where, msg):
        self._add("ERROR", code, where, msg)

    def warn(self, code, where, msg):
        self._add("WARN", code, where, msg)

    @property
    def errors(self):
        return [f for f in self.findings if f.level == "ERROR"]

    @property
    def warnings(self):
        return [f for f in self.findings if f.level == "WARN"]


def _fmt(f):
    pad = "ERROR" if f.level == "ERROR" else "WARN "
    return "%s [%s] %s: %s" % (pad, f.check, f.where, f.message)


# ---------- the repository under check ------------------------------------

class Repo(object):
    """Everything the checks read, loaded once: paths, the two contracts, the file lists."""

    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.profile = os.path.join(self.root, "templates", "campaign-profile.md")
        self.princ = os.path.join(self.root, "docs", "PRINCIPLES.md")
        self.skills = os.path.join(self.root, "skills")
        self.bundled_profile = os.path.join(
            self.skills, SETUP_SKILL, "references", "campaign-profile.md")
        self.check_links = os.path.join(self.root, "scripts", "check_links.py")
        self.bundled_check_links = os.path.join(
            self.skills, SETUP_SKILL, "references", "check_links.py")

        for required in (self.profile, self.princ):
            if not os.path.isfile(required):
                sys.exit("fatal: missing %s" % self.rel(required))

        self.profile_src = self.read(self.profile)
        self.defined_slots, self.setup_only_slots = self._slots()
        self.principles = set(re.findall(r"^###\s+(P\d{1,2})\b", self.read(self.princ), re.M))
        self.highest_principle = max((int(p[1:]) for p in self.principles), default=0)

        self.skill_dirs = sorted(
            d for d in os.listdir(self.skills)
            if os.path.isdir(os.path.join(self.skills, d))) if os.path.isdir(self.skills) else []

        self.skill_md = []
        for base, _dirs, names in os.walk(self.skills):
            for n in sorted(names):
                if n.endswith(".md"):
                    self.skill_md.append(os.path.join(base, n))
        self.skill_md.sort()
        # The bundled schema DEFINES slots, it does not cite them: counting it would make
        # every dead slot look alive.
        self.cite_md = [p for p in self.skill_md
                        if os.path.normcase(p) != os.path.normcase(self.bundled_profile)]
        self.cited_slots = defaultdict(list)
        self.cited_principles = set()

    # -- helpers
    def read(self, p):
        with open(p, encoding="utf-8") as fh:
            return fh.read()

    def rel(self, p):
        return os.path.relpath(p, self.root).replace("\\", "/")

    def at(self, p, i):
        return "%s:%d" % (self.rel(p), i)

    def skill_entrypoints(self):
        for d in self.skill_dirs:
            p = os.path.join(self.skills, d, "SKILL.md")
            if os.path.isfile(p):
                yield d, p

    def _slots(self):
        # A slot is DEFINED by a bullet:  - **`A.resource`** - ...
        # (also handles two slots on one bullet: `A.resource_loss` / `A.resource_gain`).
        # A slot annotated *(setup-only)* is recorded for the humans and for the interview;
        # no skill branches on it, so it is exempt from DEAD-SLOT. Parsed from the schema,
        # never hardcoded, and its count is printed so the exemption stays visible.
        slot_re = re.compile(r"`([A-E]\.[a-z_]+)`")
        defined, setup_only = set(), set()
        for line in self.profile_src.splitlines():
            if re.match(r"^\s*-\s+\*\*", line):
                found = slot_re.findall(line)
                defined.update(found)
                if "*(setup-only)*" in line:
                    setup_only.update(found)
        return defined, setup_only

    def shipped(self):
        """What a clone hands to an agent: every skill folder, the schema they read, and the
        principles bundled into all nine. AGENTS.md, README.md and docs/AUTHORING.md are meta -
        AUTHORING has to be able to quote a bad example in order to forbid it."""
        files = list(self.skill_md)
        for base, _dirs, names in os.walk(os.path.join(self.root, "templates")):
            files += [os.path.join(base, n) for n in sorted(names) if n.endswith(".md")]
        files.append(self.princ)
        # The nine bundled copies are byte-identical: scan the content once, so one defect is
        # one message instead of ten and the reported count means what it says.
        seen, deduped = set(), []
        for p in files:
            key = (os.path.basename(p) if os.path.basename(p) == "PRINCIPLES.md"
                   else os.path.normcase(p))
            if key in seen:
                continue
            seen.add(key)
            deduped.append(p)
        return deduped

    def all_markdown(self):
        out, seen = [], set()
        for base, dirs, names in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
            for n in sorted(names):
                p = os.path.join(base, n)
                if n.endswith(".md") and os.path.normcase(p) not in seen:
                    seen.add(os.path.normcase(p))
                    out.append(p)
        return out


# ---------- 1 + 2 + 5: citations, read in one pass ------------------------

CITE = re.compile(r"(?<![A-Za-z0-9.])([A-E]\.[a-z_]{2,})")
LEGACY = re.compile(SECTION + r"\s*\d")
PN = re.compile(r"(?<![A-Za-z0-9])P(\d{1,2})(?![0-9A-Za-z])")


def check_citations(repo, rep):
    if not repo.defined_slots:
        rep.err("SLOT-RESOLVES", repo.rel(repo.profile),
                "no slot definitions found (expected bullets like - **`A.resource`**)")
    if not repo.principles:
        rep.err("PRINCIPLE-RESOLVES", repo.rel(repo.princ),
                "no '### Pn' principle headings found")

    for f in repo.cite_md:
        rf = repo.rel(f)
        skill = rf.split("/")[1] if rf.startswith("skills/") else "?"
        src = repo.read(f)
        for i, line in enumerate(src.splitlines(), 1):
            for m in CITE.finditer(line):
                slot = m.group(1)
                if slot in repo.defined_slots:
                    repo.cited_slots[slot].append(skill)
                else:
                    rep.err("SLOT-RESOLVES", repo.at(f, i),
                            "`%s` is not a slot defined in templates/campaign-profile.md" % slot)
            legacy = LEGACY.search(line)
            if legacy:
                rep.err("NO-LEGACY-SLOTS", repo.at(f, i),
                        "legacy numeric profile citation %r - schema 2 sections are named "
                        "(A-E) and slots are cited as `B.distance`" % legacy.group(0))
            for m in PN.finditer(line):
                if "P" + m.group(1) not in repo.principles:
                    rep.err("PRINCIPLE-RESOLVES", repo.at(f, i),
                            "P%s does not resolve to any principle in docs/PRINCIPLES.md"
                            % m.group(1))
        # Count citations from the skills themselves only: the bundled PRINCIPLES copies
        # define every tag, so counting them would make every principle look cited.
        if os.path.basename(f) != "PRINCIPLES.md":
            repo.cited_principles.update("P" + m for m in PN.findall(src))

    for p in sorted(repo.principles, key=lambda t: int(t[1:])):
        if p not in repo.cited_principles:
            rep.warn("PRINCIPLE-RESOLVES", repo.rel(repo.princ),
                     "%s is defined but cited by no skill" % p)


def check_dead_slot(repo, rep):
    for slot in sorted(repo.defined_slots - repo.setup_only_slots):
        consumers = {s for s in repo.cited_slots.get(slot, ()) if s != SETUP_SKILL}
        if consumers:
            continue
        only_setup = bool(repo.cited_slots.get(slot))
        rep.err("DEAD-SLOT", repo.rel(repo.profile),
                "`%s` is defined in the schema but read by no consumer skill%s - the "
                "interview collects it and nothing ever uses it"
                % (slot, " (only %s cites it, and it collects every slot by construction)"
                   % SETUP_SKILL if only_setup else ""))


# ---------- 3: bundled copies are copies, not forks -----------------------

def check_bundles(repo, rep):
    if not os.path.isfile(repo.bundled_profile):
        rep.err("BUNDLE-IDENTICAL", repo.rel(repo.bundled_profile),
                "missing - %s drives its interview from this bundled copy" % SETUP_SKILL)
    else:
        with open(repo.profile, "rb") as a, open(repo.bundled_profile, "rb") as b:
            src, dst = a.read(), b.read()
        if src != dst:
            rep.err("BUNDLE-IDENTICAL", repo.rel(repo.bundled_profile),
                    "has drifted from templates/campaign-profile.md (%d vs %d bytes) - it is a "
                    "bundled copy, not a fork; run scripts/sync_bundles.py" % (len(dst), len(src)))

    # Same rule for the principles bundled into every skill: CHECKED-IN content, not
    # install-time output, so a clone is a valid package and an agent pointed at the repo can
    # resolve the tags it is told to cite.
    with open(repo.princ, "rb") as f:
        princ_src = f.read()
    for d in repo.skill_dirs:
        bundled = os.path.join(repo.skills, d, "references", "PRINCIPLES.md")
        where = "skills/%s/references/PRINCIPLES.md" % d
        if not os.path.isfile(bundled):
            rep.err("BUNDLE-IDENTICAL", where,
                    "missing - every skill preamble links it, and installation copies the "
                    "folder alone; it must exist in the repo, not be generated by the "
                    "installer (run scripts/sync_bundles.py)")
        elif open(bundled, "rb").read() != princ_src:
            rep.err("BUNDLE-IDENTICAL", where,
                    "has drifted from docs/PRINCIPLES.md - it is a bundled copy, not a fork; "
                    "run scripts/sync_bundles.py")

    # Same rule for scripts/check_links.py, bundled into setup so an installed copy (which
    # never receives scripts/) can still offer it as C.verify.
    if not os.path.isfile(repo.check_links):
        rep.err("BUNDLE-IDENTICAL", repo.rel(repo.check_links),
                "missing - it is the canonical source bundled into %s/references/"
                % SETUP_SKILL)
    elif not os.path.isfile(repo.bundled_check_links):
        rep.err("BUNDLE-IDENTICAL", repo.rel(repo.bundled_check_links),
                "missing - %s proposes it as C.verify and installation copies the folder "
                "alone; run scripts/sync_bundles.py" % SETUP_SKILL)
    elif open(repo.check_links, "rb").read() != open(repo.bundled_check_links, "rb").read():
        rep.err("BUNDLE-IDENTICAL", repo.rel(repo.bundled_check_links),
                "has drifted from scripts/check_links.py - it is a bundled copy, not a fork; "
                "run scripts/sync_bundles.py")


# ---------- 6: advertised principle range vs cited ------------------------

ADV = re.compile(r"`?P1`?\s*(?:\u2026|\.{2,3})\s*`?P(\d{1,2})`?")


def check_principle_range(repo, rep):
    for _d, p in repo.skill_entrypoints():
        src = repo.read(p)
        cited = {int(x) for x in PN.findall(src)}
        m = ADV.search(src)
        if not m:
            rep.warn("PRINCIPLE-RANGE", repo.rel(p), "preamble advertises no principle range")
            continue
        top = int(m.group(1))
        if top != repo.highest_principle:
            rep.err("PRINCIPLE-RANGE", repo.rel(p),
                    "preamble advertises P1...P%d but docs/PRINCIPLES.md defines up to P%d"
                    % (top, repo.highest_principle))
        over = sorted(n for n in cited if n > top)
        if over:
            rep.err("PRINCIPLE-RANGE", repo.rel(p),
                    "cites %s but its preamble advertises only up to P%d"
                    % (", ".join("P%d" % n for n in over), top))


# ---------- 7 + 8: links, once the folder is installed alone --------------

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BACKTICK_REF = re.compile(r"`(references/[A-Za-z0-9._/-]+\.[a-z]+)`")
OUTSIDE_HINT = ("docs/", "templates/", "scripts/", "assets/")


def check_links(repo, rep):
    for d in repo.skill_dirs:
        sdir = os.path.join(repo.skills, d)
        for base, _dirs, names in os.walk(sdir):
            for n in sorted(names):
                if not n.endswith(".md"):
                    continue
                p = os.path.join(base, n)
                for i, line in enumerate(repo.read(p).splitlines(), 1):
                    # markdown links resolve against the containing file; a backtick-quoted
                    # references/foo.md in prose names a path from the skill folder root.
                    targets = [(m.group(1), "link", base) for m in LINK.finditer(line)]
                    targets += [(m.group(1), "backtick reference", sdir)
                                for m in BACKTICK_REF.finditer(line)]
                    for raw, kind, anchor in targets:
                        t = raw.split("#")[0].strip()
                        if not t or re.match(r"^[a-z][a-z0-9+.-]*:", t):
                            continue                        # anchor or external URL
                        if t.startswith("/") or t.startswith("..") or "/../" in t:
                            rep.err("LINK-ESCAPES", repo.at(p, i),
                                    "%s leaves the skill folder: %s - installation copies the "
                                    "folder alone, so this is dead on the installed copy"
                                    % (kind, t))
                            continue
                        inside = os.path.relpath(
                            os.path.normpath(os.path.join(anchor, t)), sdir).replace("\\", "/")
                        if inside.startswith(".."):
                            rep.err("LINK-ESCAPES", repo.at(p, i),
                                    "%s leaves the skill folder: %s" % (kind, t))
                            continue
                        if inside in INSTALL_MATERIALISED:
                            continue
                        if not os.path.exists(os.path.join(sdir, inside)):
                            hint = ""
                            if t.startswith(OUTSIDE_HINT):
                                hint = (" - that path exists in the repo but not inside the "
                                        "installed skill folder; bundle the file or drop the link")
                            rep.err("LINK-BROKEN", repo.at(p, i),
                                    "%s points at %s, which does not exist in the skill folder%s"
                                    % (kind, t, hint))


# ---------- 9: frontmatter ------------------------------------------------

def check_frontmatter(repo, rep):
    known_skills = set(repo.skill_dirs)
    for d in repo.skill_dirs:
        p = os.path.join(repo.skills, d, "SKILL.md")
        if not os.path.isfile(p):
            rep.err("FRONTMATTER", "skills/" + d, "no SKILL.md")
            continue
        txt = repo.read(p)
        if "\ufffd" in txt:
            rep.err("FRONTMATTER", repo.rel(p),
                    "contains U+FFFD replacement character (encoding damage)")
        m = re.match(r"^---\r?\n(.*?)\r?\n---\s*$", txt, re.S | re.M)
        if not m:
            rep.err("FRONTMATTER", repo.rel(p), "missing or unterminated YAML frontmatter")
            continue
        fm = m.group(1)
        if re.search(r"^\t", fm, re.M):
            rep.err("FRONTMATTER", repo.rel(p),
                    "frontmatter contains a tab (invalid YAML indentation)")
        # The published skill format accepts only these top-level keys; anything else is
        # dropped or rejected by the loader, so a typo here silently loses a field.
        keys = set(re.findall(r"^([A-Za-z_][A-Za-z0-9_-]*):", fm, re.M))
        unexpected = sorted(keys - {"name", "description", "license", "allowed-tools",
                                    "compatibility", "metadata"})
        if unexpected:
            rep.err("FRONTMATTER", repo.rel(p),
                    "unexpected frontmatter key(s): %s - allowed: name, description, license, "
                    "allowed-tools, compatibility, metadata" % ", ".join(unexpected))
        nm = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
        if not nm:
            rep.err("FRONTMATTER", repo.rel(p), "frontmatter has no 'name'")
        else:
            name = nm.group(1).strip("\"'")
            if name != d:
                rep.err("FRONTMATTER", repo.rel(p),
                        "frontmatter name '%s' != folder '%s' (the router resolves by folder)"
                        % (name, d))
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
                rep.err("FRONTMATTER", repo.rel(p),
                        "name '%s' is not hyphen-case (lowercase, digits, single hyphens, no "
                        "leading/trailing hyphen)" % name)
            if len(name) > NAME_MAX:
                rep.err("FRONTMATTER", repo.rel(p),
                        "name is %d chars, over the %d budget" % (len(name), NAME_MAX))
        ds = re.search(r"^description:\s*(.*?)(?=\n[A-Za-z_][A-Za-z0-9_-]*:|\Z)",
                       fm, re.M | re.S)
        if not ds:
            rep.err("FRONTMATTER", repo.rel(p), "frontmatter has no 'description'")
            continue
        desc = " ".join(ds.group(1).split()).strip("\"'")
        if not desc:
            rep.err("FRONTMATTER", repo.rel(p), "'description' is empty")
            continue
        if len(desc) > DESC_MAX:
            rep.err("FRONTMATTER", repo.rel(p),
                    "description is %d chars, over the %d budget" % (len(desc), DESC_MAX))
        if "<" in desc or ">" in desc:
            rep.err("FRONTMATTER", repo.rel(p),
                    "description contains an angle bracket - the skill format forbids < and >")
        if "Use when" not in desc:
            rep.err("FRONTMATTER", repo.rel(p),
                    "description has no explicit 'Use when ...' trigger - the router sees "
                    "nothing else")
        # Unfinished scaffolding: a [TODO: ...] left in the frontmatter or in the body
        # outside a fenced block. Inside a fence it is example text, not a hole.
        if "[TODO:" in fm:
            rep.err("FRONTMATTER", repo.rel(p), "frontmatter contains an unfinished [TODO: ...]")
        fence = None
        for line in txt[m.end():].splitlines():
            f = re.match(r"^[ \t]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$", line)
            if f:
                if fence is None:
                    fence = f.group(1)[0]
                elif f.group(1)[0] == fence and not f.group(2).strip():
                    fence = None
                continue
            if fence is None and re.fullmatch(r"[ ]{0,3}\[TODO:[^\n]*\][ \t]*", line):
                rep.err("FRONTMATTER", repo.rel(p),
                        "body contains an unfinished [TODO: ...] placeholder")
        siblings = {s for s in re.findall(r"\bttrpg-[a-z][a-z-]+\b", desc)
                    if s != d and s != "ttrpg-campaign-skills"}
        unknown = sorted(s for s in siblings if s not in known_skills)
        if unknown:
            rep.err("FRONTMATTER", repo.rel(p),
                    "description names skills that do not exist: %s" % ", ".join(unknown))
        if not (siblings - set(unknown)):
            rep.err("FRONTMATTER", repo.rel(p),
                    "description declares no sibling-skill boundary ('Does not ..., see "
                    "ttrpg-<skill>') - adjacent skills collide in the router without it")


# ---------- 10: one domain section, one owner -----------------------------

TAGS = re.compile(r"\s*\((?:(?:P\d{1,2}|[A-E]\.[a-z_]+|" + SECTION + r"?[A-E])[,;\s]*)+\)\s*$")


def check_section_ownership(repo, rep):
    heads = defaultdict(list)
    for d, p in repo.skill_entrypoints():
        fenced = False
        for i, line in enumerate(repo.read(p).splitlines(), 1):
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
                heads[key].append((d, repo.at(p, i)))
    for key, locs in sorted(heads.items()):
        if key in BOILERPLATE:
            continue
        owners = sorted({d for d, _ in locs})
        if len(owners) > 1:
            rep.err("SECTION-OWNERSHIP", "skills/",
                    'section "%s" is defined by %d skills (%s) - two skills claim the same '
                    "artifact" % (key, len(owners), ", ".join(loc for _, loc in locs)))


# ---------- 11 + 12: agnosticism, mechanically ----------------------------

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


def check_agnosticism(repo, rep):
    for f in repo.shipped():
        for i, line in enumerate(repo.read(f).splitlines(), 1):
            m = SYSTEM_NAMES.search(line)
            if m:
                rep.err("NO-SYSTEM-NAMES", repo.at(f, i),
                        "names a game system (%r) - a base skill never does; the system is "
                        "`A.ruleset`, which the campaign fills, and anything irreducibly "
                        "system-shaped goes in an overlay" % m.group(0))
            for mm in (MECH_ACRONYMS.search(line), MECH_PHRASES.search(line)):
                if mm:
                    rep.warn("MECHANICS-LEAK", repo.at(f, i),
                             "uses the vocabulary of one system family (%r) - say it neutrally "
                             "(a difficulty value, a cost, the opposition is depleted) or read "
                             "the term from `A.ruleset`" % mm.group(0))


# ---------- 13: encoding, everywhere --------------------------------------

BAD_ESCAPE = re.compile(r"\\u[0-9a-fA-F]{4}")


def check_encoding(repo, rep):
    # Not limited to shipped files: no markdown in this repo has a reason to carry U+FFFD or a
    # literal escape, AGENTS.md included - it is the first file an agent reads.
    for f in repo.all_markdown():
        for i, line in enumerate(repo.read(f).splitlines(), 1):
            if "\ufffd" in line:
                rep.err("ENCODING", repo.at(f, i),
                        "contains U+FFFD replacement character (encoding damage)")
            e = BAD_ESCAPE.search(line)
            if e:
                rep.err("ENCODING", repo.at(f, i),
                        "contains the literal escape %r - it renders as six characters, not as "
                        "the intended glyph; write the character itself" % e.group(0))


# ---------- 14: the override mechanism is mapped, not mentioned -----------

BRANCH = re.compile(r"\*\*`E\.overrides`\s+branch\s+\u2014\s+mandatory\.\*\*")


def check_override_mapped(repo, rep):
    # Citing `E.overrides` in a Phase 0 table row is not implementing it. The branch is what
    # tells a reader WHICH of that skill's requirements each override switches off.
    for d, p in repo.skill_entrypoints():
        src = repo.read(p)
        if not BRANCH.search(src):
            rep.err("OVERRIDE-MAPPED", repo.rel(p),
                    "has no '**`E.overrides` branch \u2014 mandatory.**' block - the slot must be "
                    "mapped to what stops being required in THIS skill, not merely listed in "
                    "Phase 0")
        elif d == SETUP_SKILL:
            # The interviewer FILLS the slot instead of obeying it, so its branch belongs to
            # the interview phase, not to Phase 0. Stated rather than silently tolerated.
            pass
        elif "E.overrides" not in src.split("## Phase 1")[0]:
            rep.err("OVERRIDE-MAPPED", repo.rel(p),
                    "maps `E.overrides` outside Phase 0 - it is read before anything is produced")


# ---------- 15: the artifact type contract --------------------------------

def check_artifact_contract(repo, rep):
    artifact_types = defaultdict(list)
    for d, p in repo.skill_entrypoints():
        fence = None
        needs, found = [], []
        for i, line in enumerate(repo.read(p).splitlines(), 1):
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
            rep.err("ARTIFACT-CONTRACT", repo.at(p, needs[0]),
                    "skeleton shows a frontmatter placeholder but declares no fixed `type:` key - "
                    "without it no other skill can find this artifact once the campaign names it")
        for i, val in found:
            artifact_types[val].append((d, repo.at(p, i)))
    for val, locs in sorted(artifact_types.items()):
        owners = sorted({d for d, _ in locs})
        if len(owners) > 1:
            rep.err("ARTIFACT-CONTRACT", "skills/",
                    "`type: %s` is claimed by %d skills (%s) - one artifact type, one owner"
                    % (val, len(owners), ", ".join(loc for _, loc in locs)))
        if val == "campaign-profile":
            rep.err("ARTIFACT-CONTRACT", locs[0][1],
                    "`type: campaign-profile` belongs to the schema, not to a skill's skeleton")


# ---------- 16: the Phase 0 protocol is present and ordered ---------------

# The Phase 0 marker: a skill DECLARES which elements of the shared spine it carries, and each
# declaration is then verified against the text. Recognising a phase by a literal sentence made
# the checks hostage to a rewording - the marker is the anchor, the anchors below are the proof.
MARKER = re.compile(r"<!--\s*phase0:\s*([a-z0-9 ,._-]+?)\s*-->", re.I)
ELEMENT_ANCHORS = {
    # element          what counts as implementing it (any one of these)
    "find-profile": [re.compile(r"Find it before declaring it missing"),
                     re.compile(r"search by frontmatter", re.I)],
    "d-shape": [re.compile(r"\*\*`D\.shape`\s+(branch|gate)")],
    "overrides": [BRANCH],
    "search-protocol": [re.compile(r"Search before you conclude")],
}
REQUIRED_ELEMENTS = {
    "consumer": {"find-profile", "d-shape", "overrides"},
    # The finder skill fills the profile instead of reading one: its Phase 0 owns the search
    # protocol every other skill's find-it rule delegates to, and its `E.overrides` branch sits
    # in the interview phase, where OVERRIDE-MAPPED checks it - a marker about Phase 0 would be
    # claiming it twice, in the wrong place.
    SETUP_SKILL: {"search-protocol"},
}


def check_phase0_protocol(repo, rep):
    for d, p in repo.skill_entrypoints():
        src = repo.read(p)
        cut = src.find("\n## Phase 1")
        head = src[:cut] if cut != -1 else src
        required = REQUIRED_ELEMENTS.get(d, REQUIRED_ELEMENTS["consumer"])
        m = MARKER.search(head)
        if not m:
            rep.err("PHASE0-PROTOCOL", repo.rel(p),
                    "Phase 0 carries no `<!-- phase0: %s -->` marker before Phase 1 - the marker "
                    "is what makes the shared spine mechanical instead of a sentence a rewrite "
                    "can lose" % ", ".join(sorted(required)))
            continue
        declared = {t.strip().lower() for t in m.group(1).split(",") if t.strip()}
        unknown = sorted(declared - set(ELEMENT_ANCHORS))
        if unknown:
            rep.err("PHASE0-PROTOCOL", repo.at(p, head[:m.start()].count("\n") + 1),
                    "phase0 marker declares unknown element(s): %s - known: %s"
                    % (", ".join(unknown), ", ".join(sorted(ELEMENT_ANCHORS))))
        for missing in sorted(required - declared):
            rep.err("PHASE0-PROTOCOL", repo.rel(p),
                    "phase0 marker does not declare `%s`, which this skill's role requires - a "
                    "profile that exists but is not found re-interviews a GM who already "
                    "answered, and a shape a skill cannot serve must be refused before anything "
                    "is produced" % missing)
        for element in sorted(declared & set(ELEMENT_ANCHORS)):
            if not any(a.search(head) for a in ELEMENT_ANCHORS[element]):
                rep.err("PHASE0-PROTOCOL", repo.rel(p),
                        "phase0 marker declares `%s` but Phase 0 does not implement it - a "
                        "declaration is not an implementation" % element)


# ---------- 17: the context budget of an entrypoint -------------------------

# A skill's cost to a reader is tokens, not lines: a table-dense skill is cheaper per line than
# a prose one, and the 200-250 line band in AUTHORING is a shape guideline, not a measurement.
# The estimate is chars/4 - crude, stable, and enough to catch an entrypoint that doubled.
TOKEN_BUDGET = 5000


def estimate_tokens(text):
    return int(len(text) / 4.0)


def check_entrypoint_budget(repo, rep):
    for _d, p in repo.skill_entrypoints():
        tokens = estimate_tokens(repo.read(p))
        if tokens > TOKEN_BUDGET:
            rep.warn("ENTRYPOINT-BUDGET", repo.rel(p),
                     "~%d estimated tokens, over the %d budget - the entrypoint keeps what is "
                     "needed EVERY time; what is needed one way only belongs in references/"
                     % (tokens, TOKEN_BUDGET))


# The order below is the order findings are produced in; the report sorts anyway.
PASSES = [
    check_citations,
    check_dead_slot,
    check_bundles,
    check_principle_range,
    check_links,
    check_frontmatter,
    check_section_ownership,
    check_agnosticism,
    check_encoding,
    check_override_mapped,
    check_artifact_contract,
    check_phase0_protocol,
    check_entrypoint_budget,
]


def run(root, only=None):
    repo = Repo(root)
    rep = Report(only)
    for a_pass in PASSES:
        a_pass(repo, rep)
    entry_tokens = {d: estimate_tokens(repo.read(p)) for d, p in repo.skill_entrypoints()}
    worst = max(entry_tokens.items(), key=lambda kv: kv[1]) if entry_tokens else ("-", 0)
    rep.summary = (
        "%d slots defined (%d setup-only, exempt from DEAD-SLOT), %d cited | "
        "%d principles defined, %d cited | %d skills, %d markdown files | "
        "%d shipped files scanned for system leaks\n"
        "  entrypoints ~%d tokens total, worst %s ~%d of %d budget"
        % (len(repo.defined_slots), len(repo.setup_only_slots), len(repo.cited_slots),
           len(repo.principles), len(repo.cited_principles & repo.principles),
           len(repo.skill_dirs), len(repo.skill_md), len(repo.shipped()),
           sum(entry_tokens.values()), worst[0], worst[1], TOKEN_BUDGET))
    return repo, rep


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="check_contract.py",
        description="Mechanical contract checker for ttrpg-campaign-skills.")
    ap.add_argument("root", nargs="?", default=".", help="repo root (default: .)")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 on warnings too (what CI runs)")
    ap.add_argument("--only", action="append", metavar="CODE",
                    help="report only these checks (repeatable, or comma-separated)")
    ap.add_argument("--format", choices=("text", "json"), default="text",
                    help="text for humans, json for tooling")
    ap.add_argument("--list", action="store_true",
                    help="list every check and what it fails on, then exit")
    args = ap.parse_args(argv)
    utf8_stdout()

    if args.list:
        width = max(len(c.code) for c in CHECKS)
        for c in CHECKS:
            print("%-*s  %-5s  %s" % (width, c.code, c.level, c.fails_when))
        return 0

    only = None
    if args.only:
        only = [code.strip().upper()
                for item in args.only for code in item.split(",") if code.strip()]
        unknown = sorted(set(only) - set(CHECK_CODES))
        if unknown:
            ap.error("unknown check(s): %s (see --list)" % ", ".join(unknown))

    repo, rep = run(args.root, only)
    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))

    if args.format == "json":
        print(json.dumps({
            "root": repo.root,
            "summary": rep.summary,
            "strict": args.strict,
            "findings": [f._asdict() for f in
                         sorted(rep.findings, key=lambda f: (f.level, f.check, f.where))],
            "counts": {"errors": len(rep.errors), "warnings": len(rep.warnings)},
            "ok": not failed,
        }, indent=2, sort_keys=False))
        return 1 if failed else 0

    print("contract check - %s" % repo.root)
    print("  %s" % rep.summary)
    print("")
    for f in sorted(_fmt(f) for f in rep.errors):
        print(f)
    if rep.errors and rep.warnings:
        print("")
    for f in sorted(_fmt(f) for f in rep.warnings):
        print(f)
    print("\n%d error(s), %d warning(s)." % (len(rep.errors), len(rep.warnings)))
    if args.strict and rep.warnings and not rep.errors:
        print("--strict: warnings are failures here.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
