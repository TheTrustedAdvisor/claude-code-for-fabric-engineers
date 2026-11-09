#!/usr/bin/env bash
# Deploy the notebook in daily_counts.Notebook/ to the dev workspace with the Fabric CLI (fab import).
#   ./deploy.sh dev
set -euo pipefail
env=${1:?usage: deploy.sh dev}
[ "$env" = dev ] || { echo "unknown environment: $env (this project deploys to dev only)" >&2; exit 2; }
ws=${FABRIC_DEV_WORKSPACE:?set FABRIC_DEV_WORKSPACE to the name of the dev workspace}
here=$(cd "$(dirname "$0")" && pwd)
"${FAB:-fab}" import "$ws.Workspace/daily_counts.Notebook" -i "$here/daily_counts.Notebook" --format .py --force
echo "deployed daily_counts to $ws"
