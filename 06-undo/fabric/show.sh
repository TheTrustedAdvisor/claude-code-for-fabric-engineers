#!/usr/bin/env bash
# Read the notebook back from the dev workspace and print its markdown heading.
#   ./show.sh
set -euo pipefail
ws=${FABRIC_DEV_WORKSPACE:?set FABRIC_DEV_WORKSPACE to the name of the dev workspace}
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
if ! out=$("${FAB:-fab}" export "$ws.Workspace/daily_counts.Notebook" -o "$tmp" --format .py --force 2>&1); then
  echo "$out" >&2
  echo "show: fab export failed (signed in? workspace name right?)" >&2
  exit 1
fi
file=$(find "$tmp" -name 'notebook-content.py' | head -1)
[ -n "$file" ] || { echo "no notebook daily_counts in $ws" >&2; exit 1; }
echo "in workspace $ws: $(grep -m1 '^# # ' "$file" | sed 's/^# # //')"
