#!/usr/bin/env bash
# First build of the packwiz modpack from mods.txt. Requires: packwiz and python3 in PATH.
# After the first build, manage mods in a launcher and sync with import_mrpack.py.
set -u
PACK_NAME="${PACK_NAME:-suze modpack}"
PACK_AUTHOR="${PACK_AUTHOR:-gwendalos}"
PACK_VERSION="${PACK_VERSION:-1.0.0}"

if [ ! -f pack.toml ]; then
  ./packwiz init --name "$PACK_NAME" --author "$PACK_AUTHOR" --version "$PACK_VERSION" \
    --mc-version 26.2 --modloader fabric --fabric-latest || exit 1
fi

: > failed.txt
grep -v '^\s*#' mods.txt | sed 's/#.*//' | while read -r slug side version; do
  [ -z "${slug:-}" ] && continue
  if [ -n "${version:-}" ]; then
    echo "==> $slug (pinned $version)"
    if ./packwiz -y modrinth add "https://modrinth.com/mod/$slug/version/$version" < /dev/null; then
      ./packwiz pin "$slug" < /dev/null || echo "$slug (added but not pinned)" >> failed.txt
    else
      echo "$slug $version (version not found: copy the exact version number from its Modrinth page)" >> failed.txt
    fi
  else
    echo "==> $slug"
    ./packwiz -y modrinth add "$slug" < /dev/null || echo "$slug" >> failed.txt
  fi
done

python3 apply_sides.py
./packwiz refresh
[ -s failed.txt ] && { echo; echo "Needs attention:"; cat failed.txt; }
