#!/usr/bin/env bash
# Create a fresh project for exercise 4. Same as: python3 setup.py <folder> --notes <folder>
set -euo pipefail
command -v python3 >/dev/null 2>&1 || { echo "setup: python3 not found. Install Python 3 so that \`python3 --version\` works." >&2; exit 2; }
exec python3 "$(cd "$(dirname "$0")" && pwd)/setup.py" "$@"
