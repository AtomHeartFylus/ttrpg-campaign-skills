#!/usr/bin/env python3
r"""Check that every wikilink, embed and relative markdown link in a campaign vault resolves.

    python3 scripts/check_links.py <campaign-root>
    python3 scripts/check_links.py <campaign-root> --format json

This is what `C.verify` names once a campaign has one (`ttrpg-campaign-setup` Phase 3.4): the
profile has asked nine skills to close their Verify phase on a link/reference checker since the
schema existed, and until now the package did not ship one. It checks:

- Wiki-style `[[wikilinks]]` - `[[target|alias]]` and `[[target#heading]]` tolerated (the heading
  is not itself verified, only the file) - resolved the way an unambiguous wiki link resolves:
  a bare target (`[[Note Name]]`) matches a markdown file's own name anywhere under the root; a
  target that already carries an extension (`[[map.png]]`, `![[Session 1.m4a]]`, an *embed*, `!`
  or not) matches any file of that exact name anywhere under the root. A same-file heading
  reference (`[[#Heading]]`, empty target) has nothing across files to resolve and is not checked.
- Markdown links `[text](relative/path.md)` and `[text](<relative/path with spaces.md>)`,
  relative to the folder of the file that contains them (`![...]` image embeds are not links and
  are skipped - wikilink embeds are handled above instead).

Matching is **case-insensitive** (a vault moves between Windows/macOS and a case-sensitive Linux
CI without warning): a target that resolves only by a different case is reported as its own
`case-mismatch` finding, separate from `broken`, since it works today and breaks the day the vault
moves to a case-sensitive filesystem. `%xx` URL-escapes in markdown link targets are decoded
before resolving, and both the target text and the filesystem names are compared under Unicode
NFC (`os.walk` yields NFD-decomposed names on macOS; link text typed elsewhere is normally NFC).

Fenced code blocks (```` ``` ```` or `~~~`), 4-space/tab-indented code blocks, and inline
`code spans` are blanked out before scanning: a link inside an example is not a claim about this
vault, and no seeded defect in `tests/fixture-campaign/` lives inside one.

Stdlib only, Python 3.9+. Exit 0 when nothing is broken (case mismatches alone do not fail the
exit code, but are printed and counted), 1 when at least one link is broken. This script only
reports; it never edits a vault, and it does not resolve ambiguity (two files sharing a name both
count as resolved - that is a `C.naming` problem, not a broken-link one).
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.parse

WIKILINK = re.compile(r"\[\[([^\]|#]*)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
# Not an image embed (no leading "!"); target must end .md, optionally with a #heading, bare or
# wrapped in <...> (the CommonMark escape for a path containing spaces or parentheses).
MDLINK = re.compile(
    r"(?<!!)\[[^\]]*\]\(\s*<([^<>]+?\.md(?:#[^<>]*)?)>\s*\)"
    r"|(?<!!)\[[^\]]*\]\(\s*([^<>()\s]+\.md(?:#[^()\s]*)?|[^<>()]+?\.md(?:#[^()]*)?)\s*\)"
)
FENCE = re.compile(r"^\s*(```+|~~~+)")
INLINE_CODE = re.compile(r"`[^`\n]+`")
INDENTED_CODE = re.compile(r"^(?: {4,}|\t)\S")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
EXT_RE = re.compile(r"\.[A-Za-z0-9]{1,8}$")
SKIP_DIRS = {"__pycache__"}  # any dot-directory (version control, note-tool metadata, ...) is
                              # already skipped by the leading-"." rule below


def nfc(s):
    return unicodedata.normalize("NFC", s)


def iter_all_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for name in filenames:
            yield os.path.join(dirpath, name)


def strip_noncontent(lines):
    """Blank fenced code blocks, indented code blocks, and inline `code spans`: none of them
    are a claim about this vault. Line count and numbers stay stable either way."""
    out = []
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        if in_fence or INDENTED_CODE.match(line):
            out.append("")
            continue
        out.append(INLINE_CODE.sub(lambda m: " " * len(m.group(0)), line))
    return out


def build_indexes(root):
    """(by_stem, by_name, files) - by_stem covers markdown files only (bare wikilinks are note
    references), by_name covers every file (wikilink embeds and extensioned targets). Both map
    a casefolded NFC key to a list of (original_stem_or_name, path) pairs, so a resolution can
    still report an exact-case match versus a same-file-different-case one."""
    by_stem, by_name, files = {}, {}, []
    for path in iter_all_files(root):
        name = nfc(os.path.basename(path))
        stem = os.path.splitext(name)[0]
        by_name.setdefault(name.casefold(), []).append((name, path))
        if name.lower().endswith(".md"):
            files.append(path)
            by_stem.setdefault(stem.casefold(), []).append((stem, path))
    return by_stem, by_name, files


def _lookup(index, key):
    """-> (exists, exact_case) - exists is True on any casefolded match; exact_case is True
    only if at least one match shares the query's exact case."""
    key_cf = key.casefold()
    matches = index.get(key_cf)
    if not matches:
        return False, False
    exact = any(orig == key for orig, _p in matches)
    return True, exact


def resolve_wikilink(target, root, by_stem, by_name):
    """-> None (fine), 'case-mismatch', or 'broken'."""
    target = nfc(target.strip())
    if not target:
        return None  # same-file heading reference, nothing across files to check
    if "/" in target or "\\" in target:
        rel = target.replace("\\", "/")
        if not EXT_RE.search(rel):
            rel += ".md"
        candidate = os.path.join(root, rel)
        return None if os.path.isfile(candidate) else "broken"
    if EXT_RE.search(target):
        exists, exact = _lookup(by_name, target)
    else:
        exists, exact = _lookup(by_stem, target)
    if not exists:
        return "broken"
    return None if exact else "case-mismatch"


def resolve_mdlink(target, file_path):
    """-> None (fine), 'case-mismatch', or 'broken'. Walks the target component by component -
    a case mismatch in a DIRECTORY name is exactly as fragile on a case-sensitive filesystem as
    one in the final file name, and checking only the basename missed it."""
    target = urllib.parse.unquote(target.split("#", 1)[0])
    if SCHEME.match(target):
        return None  # a URL that happens to end in .md is not a vault link
    target = nfc(target)
    directory = os.path.normpath(os.path.dirname(file_path))
    rel = os.path.normpath(os.path.join(directory, target))
    try:
        rel_from_dir = os.path.relpath(rel, directory)
    except ValueError:
        rel_from_dir = rel
    parts = [p for p in rel_from_dir.replace("\\", "/").split("/") if p not in ("", ".")]
    cursor = directory
    saw_mismatch = False
    for part in parts:
        if part == "..":
            cursor = os.path.dirname(cursor)
            continue
        try:
            entries = os.listdir(cursor)
        except OSError:
            return "broken"
        names = {nfc(e) for e in entries}
        want = nfc(part)
        if want in names:
            cursor = os.path.join(cursor, want)
            continue
        casefold_matches = [n for n in names if n.casefold() == want.casefold()]
        if not casefold_matches:
            return "broken"
        saw_mismatch = True
        cursor = os.path.join(cursor, casefold_matches[0])
    return "case-mismatch" if saw_mismatch else None


def scan(root):
    """-> (files_scanned, links_checked, [broken dicts], [case_mismatch dicts])"""
    by_stem, by_name, files = build_indexes(root)
    broken, mismatches = [], []
    total_links = 0
    for path in files:
        with open(path, encoding="utf-8", errors="replace") as fh:
            raw_lines = fh.read().splitlines()
        lines = strip_noncontent(raw_lines)
        rel = os.path.relpath(path, root).replace("\\", "/")
        for lineno, line in enumerate(lines, start=1):
            for m in WIKILINK.finditer(line):
                total_links += 1
                target = m.group(1)
                verdict = resolve_wikilink(target, root, by_stem, by_name)
                if verdict:
                    entry = {"file": rel, "line": lineno, "target": target, "kind": "wikilink"}
                    (broken if verdict == "broken" else mismatches).append(entry)
            for m in MDLINK.finditer(line):
                total_links += 1
                target = m.group(1) or m.group(2)
                verdict = resolve_mdlink(target, path)
                if verdict:
                    entry = {"file": rel, "line": lineno, "target": target, "kind": "mdlink"}
                    (broken if verdict == "broken" else mismatches).append(entry)
    return len(files), total_links, broken, mismatches


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

    files, links, broken, mismatches = scan(root)

    if args.format == "json":
        print(json.dumps({"root": root, "files": files, "links": links,
                          "broken_count": len(broken), "broken": broken,
                          "case_mismatch_count": len(mismatches),
                          "case_mismatches": mismatches}, indent=2))
    else:
        print("link check - %s" % root)
        print("  %d file(s), %d link(s), %d broken, %d case-only mismatch(es)"
              % (files, links, len(broken), len(mismatches)))
        for b in broken:
            print("  %s:%d -> %s [%s]" % (b["file"], b["line"], b["target"], b["kind"]))
        for m in mismatches:
            print("  %s:%d -> %s [%s] resolves here, breaks on a case-sensitive filesystem"
                  % (m["file"], m["line"], m["target"], m["kind"]))

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
