#!/usr/bin/env bash
# Deploy the notebook to the dev or prod workspace.
#   ./deploy.sh dev | ./deploy.sh prod
set -euo pipefail
env=${1:?usage: deploy.sh dev|prod}
case "$env" in dev|prod) ;; *) echo "unknown environment: $env" >&2; exit 2 ;; esac
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$here/deployed/$env"
echo "hello.Notebook deployed to $env at $(date -u +%Y-%m-%dT%H:%M:%SZ) by deploy.sh (invoked as: $0 $*)" >> "$here/deployed/$env/deploy.log"
echo "deployed hello.Notebook to the $env workspace"
