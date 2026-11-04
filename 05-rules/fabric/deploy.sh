#!/usr/bin/env bash
# Deploy the notebook to the dev or prod workspace with the Fabric CLI (fab import).
#   ./deploy.sh dev | ./deploy.sh prod
set -euo pipefail
env=${1:?usage: deploy.sh dev|prod}
case "$env" in
  dev)  ws=${FABRIC_DEV_WORKSPACE:?set FABRIC_DEV_WORKSPACE to the name of the dev workspace} ;;
  prod) ws=${FABRIC_PROD_WORKSPACE:?set FABRIC_PROD_WORKSPACE to the name of the prod workspace} ;;
  *)    echo "unknown environment: $env" >&2; exit 2 ;;
esac
here=$(cd "$(dirname "$0")" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/hello.Notebook"
cp "$here/workspace/hello.Notebook/.platform" "$tmp/hello.Notebook/"
sed "s/hello-01/hello-$env-via-fab-cli/" "$here/workspace/hello.Notebook/notebook-content.py" > "$tmp/hello.Notebook/notebook-content.py"
"$here/fab.sh" import "$ws.Workspace/hello.Notebook" -i "$tmp/hello.Notebook" --format .py --force
echo "deployed hello.Notebook to $ws"
