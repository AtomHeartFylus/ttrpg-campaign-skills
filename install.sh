#!/usr/bin/env sh
# Install (copy) the skills into an agent skills directory.
#
#   ./install.sh ~/.agents/skills
#   ./install.sh ~/.agents/skills --dry-run     # say what would happen, touch nothing
#   ./install.sh ~/.agents/skills --uninstall   # remove exactly what this package installed
#
# The repo is the canonical copy: installing REPLACES each target folder wholesale, so local
# edits to an installed skill are lost. That is intended, and it surprises people once - which
# is why --dry-run exists and why a manifest is written next to the skills.
set -eu

TARGET=""
MODE="install"
for arg in "$@"; do
  case "$arg" in
    --dry-run)   MODE="dry-run" ;;
    --uninstall) MODE="uninstall" ;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    -*)
      echo "unknown option: $arg (try --help)" >&2
      exit 2 ;;
    *)  TARGET="$arg" ;;
  esac
done
TARGET="${TARGET:-$HOME/.agents/skills}"

SRC="$(cd "$(dirname "$0")/skills" && pwd)"
REPO="$(cd "$(dirname "$0")" && pwd)"
MANIFEST="$TARGET/.ttrpg-skills-manifest"

if [ "$MODE" = "uninstall" ]; then
  removed=0
  for d in "$SRC"/*/; do
    name="$(basename "$d")"
    if [ -d "$TARGET/$name" ]; then
      rm -rf "$TARGET/$name"
      echo "removed $TARGET/$name"
      removed=$((removed + 1))
    fi
  done
  [ -f "$MANIFEST" ] && rm -f "$MANIFEST"
  echo "uninstalled $removed skill folder(s) from $TARGET"
  exit 0
fi

[ "$MODE" = "install" ] && mkdir -p "$TARGET"

count=0
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  if [ "$MODE" = "dry-run" ]; then
    if [ -d "$TARGET/$name" ]; then
      echo "would REPLACE $TARGET/$name (existing folder is deleted first)"
    else
      echo "would install $name -> $TARGET/$name"
    fi
  else
    rm -rf "$TARGET/$name"
    cp -R "$d" "$TARGET/$name"
    echo "installed $name -> $TARGET/$name"
  fi
  count=$((count + 1))
done

if [ "$MODE" = "dry-run" ]; then
  echo "dry run: $count skill folder(s) would be installed into $TARGET"
  exit 0
fi

# A manifest, so a machine can answer "which version of the package is this, and from where"
# without guessing - and so `python scripts/check_install.py TARGET` can report drift.
version="$(cat "$REPO/VERSION" 2>/dev/null || echo unknown)"
commit="$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo unknown)"
{
  echo "package: ttrpg-campaign-skills"
  echo "version: $version"
  echo "commit: $commit"
  echo "source: $REPO"
  echo "installed: $(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo unknown)"
  echo "skills: $count"
} > "$MANIFEST"

echo "$count skill folder(s) installed into $TARGET (version $version, commit $commit)"
echo "edit the repo, never the installed copy: the next install replaces these folders whole."
