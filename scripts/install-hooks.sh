#!/usr/bin/env sh
# Point this clone's hooks at .githooks/ (versioned, reviewable, one line to undo).
#   sh scripts/install-hooks.sh
#   git config --unset core.hooksPath   # to undo
set -eu
root="$(git rev-parse --show-toplevel)"
cd "$root"
git config core.hooksPath .githooks
chmod +x .githooks/* 2>/dev/null || true
echo "hooks installed: core.hooksPath = .githooks"
echo "the pre-commit hook runs sync_bundles --check, check_contract, and (when the checker"
echo "itself is touched) tests/checker. Bypass a single WIP commit with --no-verify."
