#!/usr/bin/env python3
"""Rewrite the bundled copies from their canonical sources.

    python3 scripts/sync_bundles.py            # write the copies, report what changed
    python3 scripts/sync_bundles.py --check    # exit 1 if anything is out of date, write nothing

Eleven files in this package are byte-identical copies of three canonical ones:

    docs/PRINCIPLES.md            -> skills/*/references/PRINCIPLES.md      (one per skill)
    templates/campaign-profile.md -> skills/ttrpg-campaign-setup/references/campaign-profile.md
    scripts/check_links.py        -> skills/ttrpg-campaign-setup/references/check_links.py

They are **checked-in content, not installer output** (installation copies a skill folder
alone, so a clone with a dangling link is not a package) - but a copy maintained by hand is a
copy that drifts, and BUNDLE-IDENTICAL then fails after the fact. This script is the writer;
the checker stays the auditor.

Stdlib only, and deliberately dumb: it never edits a canonical file, only overwrites copies.
"""
import argparse
import os
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SETUP_SKILL = "ttrpg-campaign-setup"


def targets(root):
    """[(canonical, copy)] - the whole bundle contract, derived from what exists."""
    princ = os.path.join(root, "docs", "PRINCIPLES.md")
    profile = os.path.join(root, "templates", "campaign-profile.md")
    skills = os.path.join(root, "skills")
    pairs = []
    for d in sorted(os.listdir(skills)):
        if os.path.isdir(os.path.join(skills, d)):
            pairs.append((princ, os.path.join(skills, d, "references", "PRINCIPLES.md")))
    pairs.append((profile, os.path.join(skills, SETUP_SKILL, "references",
                                        "campaign-profile.md")))
    check_links = os.path.join(root, "scripts", "check_links.py")
    pairs.append((check_links, os.path.join(skills, SETUP_SKILL, "references",
                                            "check_links.py")))
    return pairs


def read_bytes(p):
    with open(p, "rb") as fh:
        return fh.read()


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sync_bundles.py", description=__doc__.splitlines()[0])
    ap.add_argument("root", nargs="?", default=ROOT, help="repo root (default: this repo)")
    ap.add_argument("--check", action="store_true",
                    help="report drift and exit 1, without writing")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)

    stale = []
    for canonical, copy in targets(root):
        if not os.path.isfile(canonical):
            sys.exit("fatal: missing canonical source %s"
                     % os.path.relpath(canonical, root).replace("\\", "/"))
        rel = os.path.relpath(copy, root).replace("\\", "/")
        if not os.path.isfile(copy) or read_bytes(copy) != read_bytes(canonical):
            stale.append((canonical, copy, rel))

    if not stale:
        print("bundles in sync (%d copies)" % len(targets(root)))
        return 0
    if args.check:
        for _c, _t, rel in stale:
            print("stale: %s" % rel)
        print("\n%d copy/copies out of date - run scripts/sync_bundles.py" % len(stale))
        return 1
    for canonical, copy, rel in stale:
        parent = os.path.dirname(copy)
        if not os.path.isdir(parent):
            os.makedirs(parent)
        shutil.copyfile(canonical, copy)
        print("synced: %s" % rel)
    print("\n%d copy/copies rewritten - commit them: they are content, not build output"
          % len(stale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
