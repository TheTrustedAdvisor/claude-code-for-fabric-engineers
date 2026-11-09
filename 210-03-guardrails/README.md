# Exercise 210-03-guardrails

Companion exercise to part 3 of the series "Learning Claude for Microsoft Fabric": "Fabric guardrails for Claude Code: block a workspace, not a command". Runs locally; only the optional step uses your own Fabric workspaces.

> **Status:** Ready: `python3 check.py <your project>` fails before you start and passes on `solution/`.

## Task

Write a PreToolUse hook with Claude that blocks any call naming a protected workspace (name or ID), whichever tool makes it. Four sample events in events/, a fifth to think about.

## What a good result looks like

BLOCK, BLOCK, BLOCK, ALLOW (exit codes 2, 2, 2, 0), registered for Bash and MCP tools with onFailure block.

## Optional

Try it on your own dev/prod workspace pair.

## How to run it

1. Copy `project/` to a folder outside any Git repository and outside any folder with a `CLAUDE.md` above it, for example `/var/tmp/210-03`.
2. Start Claude Code there and ask it to write `.claude/hooks/block_protected.py`: read the PreToolUse event from stdin, exit 2 with the matching workspace on stderr if `tool_input` names a workspace from `.claude/protected-workspaces.json`, else exit 0. Then register it in `.claude/settings.json` under `PreToolUse` with the matcher `^(Bash|mcp__.*)$` and `"onFailure": "block"`.
3. In a second terminal: `python3 check.py /var/tmp/210-03`.

A hook registered during a session takes effect in the next session. If your hook script can't be found, `python3` itself exits with code 2, and Claude Code blocks the call even without `onFailure`; a missing executable (exit 127) only blocks with `"onFailure": "block"`.

Event 5 (`python3 scripts/run_from_config.py`) passes the hook: the workspace stands in a config file, not in the call. That is the hook's limit; the workspace role is the boundary Fabric enforces.
