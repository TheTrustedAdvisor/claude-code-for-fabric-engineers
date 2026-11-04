#!/usr/bin/env bash
# Run the Fabric CLI (fab) as the identity signed in to the Azure CLI in AZURE_CONFIG_DIR.
# fab gets its tokens as FAB_TOKEN, FAB_TOKEN_ONELAKE and FAB_TENANT_ID and keeps its state in FAB_HOME.
set -euo pipefail
: "${AZURE_CONFIG_DIR:?set AZURE_CONFIG_DIR to the folder the second identity signed in to (see fabric/README.md)}"
FAB_HOME=${FAB_HOME:-$AZURE_CONFIG_DIR/fab-home}
mkdir -p "$FAB_HOME"
token() { az account get-access-token --resource "$1" --query "$2" -o tsv; }
FAB_TOKEN=$(token https://analysis.windows.net/powerbi/api accessToken)
FAB_TOKEN_ONELAKE=$(token https://storage.azure.com accessToken)
FAB_TENANT_ID=$(token https://storage.azure.com tenant)
export FAB_TOKEN FAB_TOKEN_ONELAKE FAB_TENANT_ID
exec env HOME="$FAB_HOME" USERPROFILE="$FAB_HOME" fab "$@"
