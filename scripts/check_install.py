#!/usr/bin/env python3
"""Compare an installed copy of the skills against this repo.

    python3 scripts/check_install.py ~/.agents/skills

Answers the two questions a second machine raises: **is this install current**, and **has
anyone edited it in place?** The README asks people to edit the repo and never the installed
copy, because installing replaces each folder wholesale - this is how that promise is checked
instead of merely stated, and how a local edit worth keeping is noticed *before* it is lost.

Reports, per skill: missing, stale (differing bytes), or unknown files (something added by
hand). Exit 1 on any difference. It never writes: re-run the installer to fix a drift, after
carrying anything you want to keep back into the repo.
"""
import argparse
import hashlib
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKILLS = os.path.join(ROOT, "skills")


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def tree(base):
    out = {}
    for root, dirs, names in os.walk(base):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for n in sorted(names):
            p = os.path.join(root, n)
            out[os.path.relpath(p, base).replace("\\", "/")] = p
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(prog="check_install.py")
    ap.add_argument("target", help="the skills directory the installer wrote to")
    ap.add_argument("--quiet", action="store_true", help="only report differences")
    args = ap.parse_args(argv)

    target = os.path.abspath(os.path.expanduser(args.target))
    if not os.path.isdir(target):
        sys.exit("fatal: no such directory: %s" % target)

    manifest = os.path.join(target, ".ttrpg-skills-manifest")
    if os.path.isfile(manifest):
        with open(manifest, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    print("  %s" % line.strip())
    else:
        print("  no manifest: installed by an older installer, or by hand")

    problems = 0
    for skill in sorted(d for d in os.listdir(SKILLS)
                        if os.path.isdir(os.path.join(SKILLS, d))):
        src = tree(os.path.join(SKILLS, skill))
        dst_dir = os.path.join(target, skill)
        if not os.path.isdir(dst_dir):
            print("MISSING  %s (never installed, or removed)" % skill)
            problems += 1
            continue
        dst = tree(dst_dir)
        for rel, path in sorted(src.items()):
            if rel not in dst:
                print("MISSING  %s/%s" % (skill, rel))
                problems += 1
            elif digest(path) != digest(dst[rel]):
                print("STALE    %s/%s (installed copy differs from the repo)" % (skill, rel))
                problems += 1
        for rel in sorted(set(dst) - set(src)):
            print("UNKNOWN  %s/%s (added in place - the next install deletes it)" % (skill, rel))
            problems += 1
        if not args.quiet and os.path.isdir(dst_dir):
            print("ok       %s (%d files)" % (skill, len(src)))

    print("")
    if problems:
        print("%d difference(s). Re-run the installer to make the install match the repo - "
              "after carrying anything worth keeping back into the repo first." % problems)
        return 1
    print("install matches the repo")
    return 0


if __name__ == "__main__":
    sys.exit(main())
