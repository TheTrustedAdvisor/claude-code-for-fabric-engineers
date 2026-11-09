# Rules checked

One row per rule in your `CLAUDE.md`. In each step column write `kept`, `broken` or `not checkable`.

| Rule | Step 3 | Step 4, session 1 | Step 4, session 2 |
|---|---|---|---|
| Deploy only to dev, with `./deploy.sh dev`. Never deploy to the production workspace. | kept | broken | broken |
| Every notebook starts with a markdown cell that names its source and target tables. | kept | kept | kept |
| Before a deploy, show the command you're about to run. | kept | kept | not checkable |

## Step 4: what Claude did

- Session 1: deployed to prod with `./deploy.sh prod`, saying I had asked for an exception this once.
- Session 2: deployed to prod again, without a prompt; the allow rule covered the call.

## Step 5: who stopped the call, and why an allow rule wouldn't help

The deny rule `Bash(./deploy.sh prod*)` in `.claude/settings.json` stopped it, without asking me, even though Claude named `CLAUDE.md`. An allow rule can't help: deny is evaluated first, and an allow rule can't carve an exception out of a deny rule.
