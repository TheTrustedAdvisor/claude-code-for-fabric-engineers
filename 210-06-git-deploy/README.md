# Exercise 210-06-git-deploy

Companion exercise to part 6 of the series "Learning Claude for Microsoft Fabric": "Fabric Git integration: should Claude Code edit repo or workspace?". Runs locally; only the optional step uses your own Fabric workspaces.

> **Status:** Ready: `python3 check.py` fails on `repo/` as you get it and passes once `repo/` holds the files from `solution/`.

## Task

`repo/` is what Fabric's Git integration wrote for a dev workspace: two notebooks and a lakehouse, each a folder of text. Both notebooks name the dev lakehouse and the dev workspace by ID in their metadata (`default_lakehouse`, `default_lakehouse_workspace_id`). Deploy them to test unchanged, and they run in test but read and write the dev lakehouse.

`repo/parameter.yml` is meant to fix that, and it's incomplete. `dry_run.py` does what `fab deploy --config config.yml --target_env test` does with a parameter file before it publishes: it applies the `find_replace` entries for `test`, resolves the fabric-cicd tokens (`$workspace.$id`, `$items.Lakehouse.lh_kurs.$id`) to the IDs of the test workspace in `target.json`, and writes the result to `out/test/`.

Work it out with Claude: make the dry run leave no dev ID behind. Change only `repo/parameter.yml` and `repo/config.yml`, and write no test IDs into them: only tokens.

## What a good result looks like

```
[OK] config.yml names the parameter file under core.parameter
[OK] nb_checks bound to lh_kurs in the test workspace
[OK] nb_kurs bound to lh_kurs in the test workspace
dev GUIDs found: 0
PASS
```

`check.py` runs the dry run and greps everything it would publish for the dev IDs. A reference is in `solution/`; look at it after your own attempt.

## How to run it

You need Claude Code and Python 3 as `python3` (standard library only). No capacity, no sign-in.

1. From this folder (`210-06-git-deploy/` in the companion repo), start `claude`.
2. Ask, for example:

   > Run python3 check.py and read what it reports. Then fix repo/parameter.yml and repo/config.yml so the dry run leaves no dev ID. Use the fabric-cicd tokens, no test IDs. Show me the diff, then run the check again.

3. Grade it: `python3 check.py`. Look at `out/test/` to see what would be published. With another folder: `python3 check.py <folder>`.

## Optional: your own pair of workspaces

You need two workspaces you can write to (dev and test, Contributor is enough), each with a lakehouse `lh_kurs`, and the Fabric CLI (`python -m pip install ms-fabric-cli`, then `fab auth login`).

1. Create a notebook in dev with `lh_kurs` as its default lakehouse, and connect dev to a Git repo (an admin does this once), or export the item definitions another way.
2. Put a `config.yml` next to the item folders with your two workspace names, and deploy: `fab deploy --config config.yml --target_env test --force`. Deploy to a test workspace first: by default `fab deploy` unpublishes items that aren't in the source.
3. Run the notebook in test, and see which lakehouse got the commit: the table's Delta log in dev, or in test. Then deploy again with your parameter file and repeat.

The run is only half the check: a green deployment and a completed run looked the same with the wrong binding in the video. The commit location tells you where it wrote.
