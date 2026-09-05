#!/usr/bin/env python3
r"""Release hygiene: the steps of AUTHORING §7 that a diff can prove.

    python3 scripts/check_release.py                    # against the merge-base with main
    python3 scripts/check_release.py --base origin/main
    python3 scripts/check_release.py --list

Four of the change-procedure steps are mechanical the moment you look at a diff instead of at a
file, and each of them is a rule that has been forgotten before:

  * a skill that changed and did not bump its own `metadata.version` ships as its predecessor
    on every machine that installed it;
  * a schema change without a **Migration** note leaves every fork to rediscover it;
  * a changed skeleton with an untouched worked example leaves the strongest teaching signal
    contradicting the rules;
  * a behavioural change with an untouched eval rubric is a change nobody will ever grade.

The first two are errors. The last two are warnings: only a reader can tell a wording fix from a
behavioural one, and a checker that cries wolf gets bypassed with `--no-verify`.

Stdlib only; shells out to git, which is already required to have a diff at all.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import namedtuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_contract import Report, _fmt, utf8_stdout  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

Rule = namedtuple("Rule", "code level fails_when")

RULES = [
    Rule("SKILL-VERSION", "error",
         "a skill folder changed without bumping `metadata.version` in its SKILL.md - an "
         "installed copy then reports a version it is not"),
    Rule("SCHEMA-MIGRATION", "error",
         "templates/campaign-profile.md changed without a **Migration:** note added to "
         "CHANGELOG.md in the same diff"),
    Rule("VERSION-CHANGELOG", "error",
         "the VERSION file changed without a matching `## <version>` section in CHANGELOG.md"),
    Rule("CHANGELOG-ENTRY", "warn",
         "a visible change (a skill, the schema, a check) with no CHANGELOG.md edit - forks "
         "learn what moved upstream from that file and nowhere else"),
    Rule("EXAMPLE-DRIFT", "warn",
         "a skill changed while its worked example did not - if a skeleton or a required "
         "element moved, the example now contradicts the skill"),
    Rule("EVAL-RECHECK", "warn",
         "a skill changed while its eval rubric did not - fine for a wording fix, not for a "
         "phase, a required element or a branch"),
]
RULE_CODES = [r.code for r in RULES]

EVAL_BY_SKILL = {
    "ttrpg-campaign-arc": "tests/evals/campaign-arc.md",
    "ttrpg-campaign-setup": "tests/evals/campaign-setup.md",
    "ttrpg-continuity-audit": "tests/evals/continuity-audit.md",
    "ttrpg-entity-note": "tests/evals/entity-note.md",
    "ttrpg-session-audio": "tests/evals/session-audio.md",
    "ttrpg-session-log": "tests/evals/session-log.md",
    "ttrpg-session-prep": "tests/evals/session-prep.md",
    "ttrpg-table-dossier": "tests/evals/table-dossier.md",
    "ttrpg-table-recap": "tests/evals/table-recap.md",
}


def git(*args):
    proc = subprocess.run(["git"] + list(args), cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def resolve_base(base):
    if base:
        merge = git("merge-base", "HEAD", base)
        return merge.strip() if merge else base
    for candidate in ("origin/main", "origin/master", "main", "master"):
        merge = git("merge-base", "HEAD", candidate)
        if merge:
            return merge.strip()
    return None


def changed_files(base):
    out = git("diff", "--name-only", "%s...HEAD" % base) if base else git("diff", "--name-only")
    return [ln.strip() for ln in (out or "").splitlines() if ln.strip()]


def added_lines(base, path):
    out = git("diff", "%s...HEAD" % base, "--", path) if base else git("diff", "--", path)
    return [ln[1:] for ln in (out or "").splitlines()
            if ln.startswith("+") and not ln.startswith("+++")]


def check(base, rep):
    files = changed_files(base)
    if not files:
        return files
    changed = set(files)

    touched_skills = {}
    for f in files:
        m = re.match(r"^skills/([^/]+)/", f)
        if m and not f.endswith("references/PRINCIPLES.md"):
            touched_skills.setdefault(m.group(1), []).append(f)

    for skill, paths in sorted(touched_skills.items()):
        entry = "skills/%s/SKILL.md" % skill
        bumped = any(re.match(r"^\s*version:", ln) for ln in added_lines(base, entry))
        if not bumped:
            rep.err("SKILL-VERSION", entry,
                    "%s changed (%s) but `metadata.version` was not bumped - AUTHORING §7 step 4"
                    % (skill, ", ".join(sorted(os.path.basename(p) for p in paths))))
        examples = [p for p in paths if "/references/example-" in p]
        has_example = any(
            n.startswith("example-")
            for n in (os.listdir(os.path.join(ROOT, "skills", skill, "references"))
                      if os.path.isdir(os.path.join(ROOT, "skills", skill, "references")) else []))
        if entry in changed and has_example and not examples:
            rep.warn("EXAMPLE-DRIFT", entry,
                     "%s changed but its worked example did not - if a skeleton or a required "
                     "element moved, update references/example-*.md in this commit (AUTHORING "
                     "§7 step 6)" % skill)
        eval_file = EVAL_BY_SKILL.get(skill)
        if entry in changed and eval_file and eval_file not in changed:
            rep.warn("EVAL-RECHECK", entry,
                     "%s changed but %s did not - a behavioural change re-runs that eval or "
                     "updates its rubric in the same commit (AUTHORING §9)" % (skill, eval_file))

    schema_changed = "templates/campaign-profile.md" in changed
    if schema_changed:
        migration = any("Migration" in ln for ln in added_lines(base, "CHANGELOG.md"))
        if not migration:
            rep.err("SCHEMA-MIGRATION", "templates/campaign-profile.md",
                    "the schema changed with no **Migration:** note added to CHANGELOG.md - a "
                    "fork with a filled profile has to be told what to do")

    if "VERSION" in changed:
        version = ""
        vpath = os.path.join(ROOT, "VERSION")
        if os.path.isfile(vpath):
            with open(vpath, encoding="utf-8") as fh:
                version = fh.read().strip()
        changelog = ""
        cpath = os.path.join(ROOT, "CHANGELOG.md")
        if os.path.isfile(cpath):
            with open(cpath, encoding="utf-8") as fh:
                changelog = fh.read()
        if version and not re.search(r"^##\s+%s\b" % re.escape(version), changelog, re.M):
            rep.err("VERSION-CHANGELOG", "VERSION",
                    "VERSION says %s but CHANGELOG.md has no `## %s` section - a version with "
                    "no notes is a number" % (version, version))

    visible = bool(touched_skills) or schema_changed \
        or "scripts/check_contract.py" in changed or "docs/PRINCIPLES.md" in changed
    if visible and "CHANGELOG.md" not in changed:
        rep.warn("CHANGELOG-ENTRY", "CHANGELOG.md",
                 "a visible change landed with no CHANGELOG entry - wording fixes stay out of "
                 "it, everything else does not (AUTHORING §7 step 4)")
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(prog="check_release.py",
                                description="Release hygiene checks over a git diff.")
    ap.add_argument("--base", help="compare against this ref (default: merge-base with main)")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    ap.add_argument("--only", action="append", metavar="CODE")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)
    utf8_stdout()

    if args.list:
        width = max(len(r.code) for r in RULES)
        for r in RULES:
            print("%-*s  %-5s  %s" % (width, r.code, r.level, r.fails_when))
        return 0

    only = None
    if args.only:
        only = [c.strip().upper() for item in args.only for c in item.split(",") if c.strip()]
        unknown = sorted(set(only) - set(RULE_CODES))
        if unknown:
            ap.error("unknown rule(s): %s (see --list)" % ", ".join(unknown))

    if git("rev-parse", "--git-dir") is None:
        sys.exit("fatal: not a git repository - this check reads a diff")
    base = resolve_base(args.base)
    rep = Report(only)
    files = check(base, rep)
    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))

    if args.format == "json":
        print(json.dumps({
            "base": base,
            "changed": files,
            "findings": [f._asdict() for f in
                         sorted(rep.findings, key=lambda f: (f.level, f.check, f.where))],
            "counts": {"errors": len(rep.errors), "warnings": len(rep.warnings)},
            "ok": not failed,
        }, indent=2, sort_keys=False))
        return 1 if failed else 0

    print("release hygiene - %d file(s) changed against %s"
          % (len(files), base[:12] if base else "the working tree"))
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
