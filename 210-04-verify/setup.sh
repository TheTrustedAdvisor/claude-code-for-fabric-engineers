#!/usr/bin/env bash
# Prepare or switch the working copy for exercise 210-04.
#
#   ./setup.sh <state> [folder]      state: empty | canceled | done; folder defaults to /var/tmp/210-04
#
# First call: copies project/ into the folder. Every call: refreshes lab/fake (the fake fab), copies the chosen
# state to lab/current, and writes env.sh, which puts the fake fab on the PATH and sets VERIFY_STATE.
# Your files (CLAUDE.md, checks/) are never overwritten.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
state="${1:-}"
folder="${2:-/var/tmp/210-04}"
case "$state" in
  empty|canceled|done) ;;
  *) echo "usage: ./setup.sh empty|canceled|done [folder]   (folder defaults to /var/tmp/210-04)" >&2; exit 2 ;;
esac
command -v python3 >/dev/null 2>&1 || { echo "setup: python3 not found. Install Python 3 so that \`python3 --version\` works." >&2; exit 2; }

mkdir -p "$folder"
folder="$(cd "$folder" && pwd)"
if git -C "$folder" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "setup: $folder is inside a Git repository. Pick a folder outside, for example /var/tmp/210-04." >&2; exit 2
fi
dir="$(dirname "$folder")"
while [ "$dir" != "/" ] && [ -n "$dir" ]; do
  if [ -f "$dir/CLAUDE.md" ]; then
    echo "setup: $dir/CLAUDE.md is above $folder; Claude Code would load it too. Pick another folder." >&2; exit 2
  fi
  dir="$(dirname "$dir")"
done

if [ ! -f "$folder/CLAUDE.md" ]; then
  cp -R "$here/project/." "$folder/"
  mkdir -p "$folder/checks"
  echo "created project in $folder"
fi
rm -rf "$folder/lab/fake" "$folder/lab/current"
mkdir -p "$folder/lab"
cp -R "$here/fake" "$folder/lab/fake"
chmod +x "$folder/lab/fake/fab"
cp -R "$here/states/$state" "$folder/lab/current"
cat > "$folder/env.sh" <<EOF
# Written by setup.sh: the fake fab on the PATH, the current state for the fake and for your check.
export PATH="$folder/lab/fake:\$PATH"
export VERIFY_STATE="$folder/lab/current"
EOF
echo "state: $state"
echo
echo "Next:"
echo "  cd $folder && source env.sh"
echo "  fab job run-list tta210-lab.Workspace/nb_kurs.Notebook     # try the fake"
echo "  claude                                                     # start Claude Code from this shell"
echo "Switch state later: $here/setup.sh <state> $folder   (VERIFY_STATE stays the same, no restart needed)"
