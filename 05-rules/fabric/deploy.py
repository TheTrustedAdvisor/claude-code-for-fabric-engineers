"""Publish the notebook to the dev or prod workspace with fabric-cicd.

    python3 deploy.py --env dev
    python3 deploy.py --env prod

Signs in with the Azure CLI identity in AZURE_CONFIG_DIR. Publishes only, never unpublishes.
"""
import argparse
import os
import pathlib
import sys

from azure.identity import AzureCliCredential
from fabric_cicd import FabricWorkspace, publish_all_items

HERE = pathlib.Path(__file__).resolve().parent
WORKSPACES = {"dev": "FABRIC_DEV_WORKSPACE", "prod": "FABRIC_PROD_WORKSPACE"}


def default_env():
    try:
        lines = (HERE / ".env").read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in lines:
        key, _, value = line.strip().partition("=")
        if key.strip() == "DEPLOY_ENV":
            return value.strip().strip("\"'") or None
    return None


parser = argparse.ArgumentParser()
parser.add_argument("--env", choices=["dev", "prod"], default=default_env())
env = parser.parse_args().env
if env not in WORKSPACES:
    sys.exit("usage: deploy.py --env dev|prod (or DEPLOY_ENV=dev|prod in .env)")
name = os.environ.get(WORKSPACES[env]) or sys.exit(f"set {WORKSPACES[env]} to the name of the {env} workspace")
if not os.environ.get("AZURE_CONFIG_DIR"):
    sys.exit("set AZURE_CONFIG_DIR to the folder the second identity signed in to (see fabric/README.md)")

workspace = FabricWorkspace(
    workspace_name=name,
    environment=env,
    repository_directory=str(HERE / "workspace"),
    item_type_in_scope=["Notebook"],
    token_credential=AzureCliCredential(),
    parameter_file_path=str(HERE / "parameter.yml"),
)
publish_all_items(workspace)
print(f"deployed hello.Notebook to {name}")
