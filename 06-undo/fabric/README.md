# Step 8: the same change against a real Fabric workspace

Optional. You need a Fabric workspace you may change (a dev or sandbox workspace on a capacity, never production) and the Fabric CLI.

## What you install

```
python3 -m venv /var/tmp/06-venv
/var/tmp/06-venv/bin/pip install ms-fabric-cli
export PATH="/var/tmp/06-venv/bin:$PATH"
fab auth login
```

Use a Python version that `ms-fabric-cli` supports (3.10 to 3.12 were tested; on a newer one pip may not find a matching version). This step is written for macOS, Linux and WSL; on native Windows the virtual environment has `Scripts\` instead of `bin/`, so do it in WSL.

`fab auth login` signs you in interactively. `fab ls` must list your workspaces afterward.

## What the two scripts do

- `deploy.sh dev` imports `daily_counts.Notebook/` from the project folder into the workspace named in `FABRIC_DEV_WORKSPACE` (`fab import … --format .py --force`). It replaces the notebook if it's already there.
- `show.sh` exports the notebook from the workspace into a temporary folder (`fab export`) and prints its markdown heading. It reads what Fabric holds, not your files.

Both call the command in `FAB` (default `fab`). Use workspace names without spaces or dots; `fab` addresses them as `<name>.Workspace`.

## Afterward

Delete the notebook `daily_counts` from the workspace in the Fabric portal, or keep it for the next run; `deploy.sh dev` overwrites it.
