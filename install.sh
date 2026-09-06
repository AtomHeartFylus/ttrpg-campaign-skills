#!/usr/bin/env sh
# Install (copy) the skills into an agent skills directory.
#
#   ./install.sh ~/.agents/skills
#   ./install.sh ~/.agents/skills --dry-run     # say what would happen, touch nothing
#   ./install.sh ~/.agents/skills --uninstall   # remove exactly what this package installed
#   ./install.sh ~/.agents/skills --force       # also replace folders this install doesn't own
#
# The repo is the canonical copy: installing REPLACES each target folder wholesale, so local
# edits to an installed skill are lost. That is intended, and it surprises people once - which
# is why --dry-run exists and why a manifest is written next to the skills.
#
# Ownership is tracked by the manifest (`skill: <name>` lines). A folder this installer did not
# create - an unmanaged name collision - is left untouched and the run exits non-zero, unless
# --force is given. --uninstall refuses to run against a missing or legacy (no `skill:` lines)
# manifest rather than guess which folders are ours, and only ever removes manifest-listed ones.
set -eu

TARGET=""
MODE="install"
FORCE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run)   MODE="dry-run" ;;
    --uninstall) MODE="uninstall" ;;
    --force)     FORCE=1 ;;
    -h|--help)
      sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
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

# A manifest `skill:` value is trusted enough to be rm -rf'd, so it must be a bare basename
# that names an actual skill folder in THIS package's skills/ - never a path (no `/`, no `\`,
# no `.`/`..`) and never an unknown name. Checked by exact match against the real directory
# listing, not by testing path existence (which a `..`-laden name could satisfy by accident).
is_valid_skill_name() {
  _n="$1"
  case "$_n" in
    ''|.|..|*/*|*\\*) return 1 ;;
  esac
  for _d in "$SRC"/*/; do
    [ "$(basename "$_d")" = "$_n" ] && return 0
  done
  return 1
}

if [ "$MODE" = "uninstall" ]; then
  if [ ! -f "$MANIFEST" ]; then
    echo "refusing to uninstall: no manifest at $MANIFEST - cannot tell which folders in" \
         "$TARGET are ours" >&2
    exit 1
  fi
  managed="$(grep '^skill: ' "$MANIFEST" 2>/dev/null | sed 's/^skill: //')"
  if [ -z "$managed" ]; then
    echo "refusing to uninstall: $MANIFEST has no 'skill:' entries (legacy manifest, or one" \
         "hand-edited) - cannot tell which folders in $TARGET are ours" >&2
    exit 1
  fi
  invalid=""
  for name in $managed; do
    is_valid_skill_name "$name" || invalid="$invalid '$name'"
  done
  if [ -n "$invalid" ]; then
    echo "refusing to uninstall: $MANIFEST lists invalid or unknown skill: entr(y/ies)" \
         "($invalid ) - it may be hand-edited or corrupted; touching nothing" >&2
    exit 1
  fi
  removed=0
  for name in $managed; do
    if [ -d "$TARGET/$name" ]; then
      rm -rf "$TARGET/$name"
      echo "removed $TARGET/$name"
      removed=$((removed + 1))
    fi
  done
  rm -f "$MANIFEST"
  echo "uninstalled $removed skill folder(s) from $TARGET"
  exit 0
fi

# Ownership established by a prior install of THIS package: only these names may be replaced
# wholesale without --force.
existing_managed=""
if [ -f "$MANIFEST" ]; then
  for _m in $(grep '^skill: ' "$MANIFEST" 2>/dev/null | sed 's/^skill: //'); do
    # A hand-edited entry that is not a plain, known skill basename never confers ownership.
    is_valid_skill_name "$_m" && existing_managed="$existing_managed $_m"
  done
fi

is_managed() {
  _name="$1"
  for _m in $existing_managed; do
    [ "$_m" = "$_name" ] && return 0
  done
  return 1
}

[ "$MODE" = "install" ] && mkdir -p "$TARGET"

count=0
skipped=0
installed_names=""
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  collision=0
  [ -d "$TARGET/$name" ] && collision=1
  owned=0
  if [ "$collision" -eq 1 ] && is_managed "$name"; then
    owned=1
  fi

  if [ "$MODE" = "dry-run" ]; then
    if [ "$collision" -eq 0 ]; then
      echo "would install $name -> $TARGET/$name"
    elif [ "$FORCE" -eq 1 ] || [ "$owned" -eq 1 ]; then
      echo "would REPLACE $TARGET/$name (existing folder is deleted first)"
    else
      echo "would REFUSE $TARGET/$name (unmanaged folder in the way; rerun with --force to replace it)"
    fi
    count=$((count + 1))
    continue
  fi

  if [ "$collision" -eq 1 ] && [ "$FORCE" -eq 0 ] && [ "$owned" -eq 0 ]; then
    echo "refusing to replace unmanaged folder: $TARGET/$name (not owned by a prior install of" \
         "this package; use --force to override)" >&2
    skipped=$((skipped + 1))
    continue
  fi

  rm -rf "$TARGET/$name"
  cp -R "$d" "$TARGET/$name"
  echo "installed $name -> $TARGET/$name"
  installed_names="$installed_names $name"
  count=$((count + 1))
done

if [ "$MODE" = "dry-run" ]; then
  echo "dry run: $count skill folder(s) considered for $TARGET"
  exit 0
fi

# A manifest, so a machine can answer "which version of the package is this, from where, and
# which folders it owns" without guessing - and so `python scripts/check_install.py TARGET` and
# `--uninstall` can act on it instead of the whole directory.
version="$(cat "$REPO/VERSION" 2>/dev/null || echo unknown)"
commit="$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo unknown)"
{
  echo "package: ttrpg-campaign-skills"
  echo "version: $version"
  echo "commit: $commit"
  echo "source: $REPO"
  echo "installed: $(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo unknown)"
  installed_count=0
  for n in $installed_names; do installed_count=$((installed_count + 1)); done
  echo "skills: $installed_count"
  for n in $installed_names; do
    echo "skill: $n"
  done
} > "$MANIFEST"

installed_count=0
for n in $installed_names; do installed_count=$((installed_count + 1)); done
echo "$installed_count skill folder(s) installed into $TARGET (version $version, commit $commit)"
echo "edit the repo, never the installed copy: the next install replaces these folders whole."
if [ "$skipped" -gt 0 ]; then
  echo "$skipped folder(s) refused (unmanaged collision) - use --force to replace them" >&2
  exit 1
fi
