# Step 9: the same tools against real Fabric workspaces

Optional. You need a Fabric capacity, two workspaces you may change (dev and prod) and a second identity with **Contributor** in dev and **Viewer** in prod. Don't use your own account for this step.

## What you install

- Python 3.12 with `ms-fabric-cli` (the `fab` command) and `fabric-cicd` in a virtual environment. Python 3.12 is the version these two packages were tested with together; on newer versions pip may not find a combination of both.
- The Azure CLI (`az`).

```
python3.12 -m venv /var/tmp/05-venv
/var/tmp/05-venv/bin/pip install ms-fabric-cli fabric-cicd azure-identity
```

This step is written for macOS, Linux and WSL. On native Windows a virtual environment has `python.exe` but no `python3.exe`, so `python3` would not pick up the packages; do step 9 in WSL.

## Sign in as the second identity, in its own config folder

The Azure CLI keeps its sign-in in the folder named by `AZURE_CONFIG_DIR`. A folder of its own keeps the second identity apart from your normal sign-in, which stays untouched.

```
export AZURE_CONFIG_DIR=/var/tmp/05-azure
az login --allow-no-subscriptions
```

Sign in as the second identity in the browser. `az account show --query user.name -o tsv` must print that identity, not you.

Both tools sign in through this folder: `deploy.py` with `AzureCliCredential` from `azure-identity`, `deploy.sh` through `fab.sh`, which hands `fab` tokens from the same sign-in (`FAB_TOKEN`, `FAB_TOKEN_ONELAKE`, `FAB_TENANT_ID`) and gives `fab` its own state folder (`FAB_HOME`, default `$AZURE_CONFIG_DIR/fab-home`).

## Start Claude Code

In the same terminal, so Claude Code and the tools see these variables:

```
export FABRIC_DEV_WORKSPACE='<name of your dev workspace>'
export FABRIC_PROD_WORKSPACE='<name of your prod workspace>'
export PATH="/var/tmp/05-venv/bin:$PATH"
cd /var/tmp/05-rules-fabric
python3 deploy.py --help
claude
```

Use workspace names without spaces or dots; `fab` addresses them as `<name>.Workspace`. `python3 deploy.py --help` must run without an import error; then `python3` is the one from the virtual environment. Tokens from `az account get-access-token` expire after about an hour; if a deploy fails with an authentication error, run it again.

## Afterwards

- In the Fabric portal, check that the prod workspace has no `hello` notebook. If one is there, the identity can write to prod: fix the role before you trust this boundary.
- Sign the second identity out: `az logout`, then delete `/var/tmp/05-azure`.
