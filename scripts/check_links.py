#!/usr/bin/env python3
r"""Check that every wikilink and every relative markdown link in a campaign vault resolves.

    python3 scripts/check_links.py <campaign-root>
    python3 scripts/check_links.py <campaign-root> --format json

This is what `C.verify` names once a campaign has one (`ttrpg-campaign-setup` Phase 3.4): the
profile has asked nine skills to close their Verify phase on a link/reference checker since the
schema existed, and until now the package did not ship one. It checks exactly two things:

- Obsidian-style `[[wikilinks]]` - `[[target|alias]]` and `[[target#heading]]` tolerated (the
  heading is not itself verified, only the file) - resolved by matching a file's own name
  (without extension) anywhere under the root, the way Obsidian resolves an unambiguous link. A
  same-file heading reference (`[[#Heading]]`, empty target) has nothing across files to resolve
  and is not checked.
- Markdown links `[text](relative/path.md)`, relative to the folder of the file that contains
  them (`![...]` image embeds are not links and are skipped).

Fenced code blocks (```` ``` ```` or `~~~`) are blanked out before scanning: a link inside an
example is not a claim about this vault, and NO seeded defect in `tests/fixture-campaign/` lives
inside one.

Stdlib only, Python 3.9+. Exit 0 when nothing is broken, 1 when at least one link is. This script
only reports; it never edits a vault, and it does not resolve ambiguity (two files sharing a name
both count as "resolved" - that is a `C.naming` problem, not a broken-link one).
"""
import argparse
import json
import os
import re
import sys

WIKILINK = re.compile(r"\[\[([^\]|#]*)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
# Not an image embed (no leading "!"); target must end .md, optionally with a #heading.
MDLINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+\.md(?:#[^)\s]*)?)\)")
FENCE = re.compile(r"^\s*(```+|~~~+)")
INLINE_CODE = re.compile(r"`[^`\n]+`")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
SKIP_DIRS = {".git", ".obsidian", "__pycache__"}


def iter_md_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def strip_fences(lines):
    """Blank fenced code block bodies, and inline `code spans` on the surviving lines: a
    span is how this very package's own docs show wikilink/link syntax as text, never as a
    real link, and keeps line count and numbers stable either way."""
    out = []
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line))
    return out


def build_index(root):
    """basename-without-extension -> [file paths] for every .md file under root."""
    index = {}
    files = []
    for path in iter_md_files(root):
        files.append(path)
        stem = os.path.splitext(os.path.basename(path))[0]
        index.setdefault(stem, []).append(path)
    return index, files


def resolve_wikilink(target, root, index):
    target = target.strip()
    if not target:
        return True  # same-file heading reference, nothing across files to check
    if target.lower().endswith(".md"):
        target = target[:-3]
    if "/" in target or "\\" in target:
        candidate = os.path.join(root, target.replace("\\", "/") + ".md")
        return os.path.isfile(candidate)
    return target in index


def resolve_mdlink(target, file_path):
    target = target.split("#", 1)[0]
    if SCHEME.match(target):
        return True  # a URL that happens to end in .md is not a vault link
    candidate = os.path.normpath(os.path.join(os.path.dirname(file_path), target))
    return os.path.isfile(candidate)


def scan(root):
    """-> (files_scanned, links_checked, [broken dicts])"""
    index, files = build_index(root)
    broken = []
    total_links = 0
    for path in files:
        with open(path, encoding="utf-8", errors="replace") as fh:
            raw_lines = fh.read().splitlines()
        lines = strip_fences(raw_lines)
        rel = os.path.relpath(path, root).replace("\\", "/")
        for lineno, line in enumerate(lines, start=1):
            for m in WIKILINK.finditer(line):
                total_links += 1
                target = m.group(1)
                if not resolve_wikilink(target, root, index):
                    broken.append({"file": rel, "line": lineno, "target": target,
                                   "kind": "wikilink"})
            for m in MDLINK.finditer(line):
                total_links += 1
                target = m.group(1)
                if not resolve_mdlink(target, path):
                    broken.append({"file": rel, "line": lineno, "target": target,
                                   "kind": "mdlink"})
    return len(files), total_links, broken


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="check_links.py", description=__doc__.splitlines()[0])
    ap.add_argument("root", help="campaign root to scan")
    ap.add_argument("--format", choices=("text", "json"), default="text")
    args = ap.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.exit("fatal: not a directory: %s" % args.root)

    files, links, broken = scan(root)

    if args.format == "json":
        print(json.dumps({"root": root, "files": files, "links": links,
                          "broken_count": len(broken), "broken": broken}, indent=2))
    else:
        print("link check - %s" % root)
        print("  %d file(s), %d link(s), %d broken" % (files, links, len(broken)))
        for b in broken:
            print("  %s:%d -> %s [%s]" % (b["file"], b["line"], b["target"], b["kind"]))

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
