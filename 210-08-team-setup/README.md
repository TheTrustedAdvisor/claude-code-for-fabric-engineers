# Exercise 210-08-team-setup

Companion exercise to part 8 of the series "Learning Claude for Microsoft Fabric": "Fabric repo for a team: what belongs in CLAUDE.md, MCP and skills?". Runs locally; only the optional step uses your own Fabric workspaces.

> **Status:** Ready: `python3 check.py` fails on `project/` as you get it and passes once `project/` holds a complete team setup.

## Task

`project/` is the start of a shared Fabric repo for the orders pipeline. It holds one file, `samples/handover-notes.md`, left over from an old setup. Build the team setup with Claude, so that a teammate who clones the folder gets the shared rules and nothing personal:

1. `CLAUDE.md`: the project notes (what the project is, the environments, the rules). Each person's dev workspace comes from `FABRIC_DEV_WORKSPACE`; the protected workspace is `orders-prod`. Keep it short.
2. `.claude/settings.json`: allow and deny rules for the team, and a `PreToolUse` hook for Bash and MCP tools that blocks any call naming `orders-prod`. Start the hook through `$CLAUDE_PROJECT_DIR`, so it runs from any folder.
3. `.gitignore`: keep `.claude/settings.local.json` out of git. Personal values (your dev workspace) go there.
4. `.mcp.json`: one MCP server, for example the Fabric core server with its URL. No token, no secret: each person signs in with their own account.
5. `.claude/skills/<name>/SKILL.md`: one skill with `name` and `description`, for example a verification routine.
6. The handover notes: there is a token in them. Take it out.

## What a good result looks like

```
[OK] 1 CLAUDE.md present, under 200 lines
[OK] 2 .gitignore keeps .claude/settings.local.json out of git
[OK] 3 .claude/settings.json has allow and deny rules
[OK] 4 hook registered under PreToolUse for Bash and MCP, path from $CLAUDE_PROJECT_DIR, onFailure block
[OK] 5 hook stops fab job run on orders-prod
[OK] 6 hook stops an MCP call on orders-prod
[OK] 7 hook lets orders-dev through
[OK] 8 .mcp.json names at least one server with a url or command
[OK] 9 a skill in .claude/skills/<name>/SKILL.md with name and description
[OK] 10 0 token patterns in any file
PASS
```

`check.py` reads the folder the way a teammate gets it. It feeds three sample calls (`events/`) to your hook, and it scans every file for things that look like a token: JWTs, bearer tokens, Entra client secrets, GitHub and API keys, `password=`-style values. The token in `samples/handover-notes.md` is planted and not real; it is there so you can see the check fail on it. A reference is in `solution/`; look at it after your own attempt.

## How to run it

You need Claude Code and Python 3 as `python3` (standard library only). No capacity, no sign-in.

1. From `project/` in this folder (`210-08-team-setup/project/` in the companion repo), start `claude`.
2. Ask, for example:

   > This folder becomes our team's shared Fabric repo. Build the setup: CLAUDE.md, .claude/settings.json with a PreToolUse hook that blocks the workspace orders-prod, .gitignore for the personal settings, .mcp.json for the Fabric core MCP server, and one skill. Nothing personal and no secrets in any file that goes to git. Then read samples/handover-notes.md and tell me what must not stay there.

3. Read what Claude wrote before you accept it. Then grade it from `210-08-team-setup/`: `python3 check.py`. To start over: `git checkout -- project/ && git clean -fd project/`.

## Optional: a colleague clones it

You need two Fabric workspaces you can write to (one per person, Contributor is enough) and the Fabric CLI (`python -m pip install ms-fabric-cli`).

1. Put the folder into a git repo and push it. Your colleague clones it and starts `claude` in it. Claude Code asks whether to trust the folder and lists what it would load: the allow rules, the hook, the MCP server. Read the list before you say yes.
2. Each person sets their own dev workspace in `.claude/settings.local.json` (`{"env": {"FABRIC_DEV_WORKSPACE": "<your workspace>"}}`) and signs in with their own account (`fab auth login`, `/mcp` for the MCP server).
3. Ask Claude to list the items in `orders-prod`: the hook stops the call for both of you.

The shared rules travel with git. The sign-in and the personal workspace stay with each person.
