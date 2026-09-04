#!/usr/bin/env sh
# Install (copy) the skills into an agent skills directory.
#   ./install.sh ~/.agents/skills
set -eu
TARGET="${1:-$HOME/.agents/skills}"
SRC="$(cd "$(dirname "$0")/skills" && pwd)"
mkdir -p "$TARGET"
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  rm -rf "$TARGET/$name"
  cp -R "$d" "$TARGET/$name"
  mkdir -p "$TARGET/$name/references"
  cp "$(dirname "$SRC")/docs/PRINCIPLES.md" "$TARGET/$name/references/PRINCIPLES.md"
  echo "installed $name -> $TARGET/$name"
done
