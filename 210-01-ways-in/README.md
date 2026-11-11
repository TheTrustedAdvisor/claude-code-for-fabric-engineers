# Exercise 210-01-ways-in

Companion exercise to part 1 of the series "Learning Claude for Microsoft Fabric": "Fabric CLI, REST API or MCP server: which should Claude Code use?". Runs locally; only the optional step uses your own Fabric workspace.

> **Status:** Ready: `python3 check.py project` fails before you start and passes on `solution/`.

## Task

`tasks.md` lists five Fabric tasks. For each one, pick one way in and write it into `project/ways.yaml`:

| Way | What it is |
|---|---|
| `fab` | The Fabric command line, through Claude Code's Bash tool |
| `fab api` | A REST call through `fab api`, with the session `fab` already has |
| `core mcp` | The Fabric Core MCP server, registered as `fabric-core`; its tools are named `mcp__fabric-core__<tool>` |

Then write the allow list in `project/.claude/settings.json`: one rule per task, for the way you chose, and nothing else. The rule of thumb from the video: `fab` for work and scripts, `fab api` when there's no command, Core MCP for overview and management with a rule on each exact tool.

## What a good result looks like

`python3 check.py project` prints one `ok` line per task and two for the allow list, then PASS:

- Every task has a way that can do the job. The Core MCP server has no tool that runs a job, and it needs a browser sign-in, so it can't do tasks 1 and 2. `fab` has no command for task 5.
- Exactly one allow rule covers each task, written for that way.
- No rule is broader than a task: not `Bash(fab *)`, not `Bash(fab api *)`, not `mcp__fabric-core` or `mcp__fabric-core__*`. Task 4 allows granting a role; a rule that also allows removing one fails.

Task 4 has two right answers (`add_workspace_role` on the server, or `fab acl set`). A reference is in `solution/`; look at it after your own attempt.

## How to run it

You need Python 3 as `python3` (standard library only). Claude Code is optional for the check itself.

1. Read `tasks.md`, fill in `project/ways.yaml`, and add the rules to `project/.claude/settings.json`.
2. `python3 check.py project`. Fix what it reports, until it prints PASS.
3. With Claude Code: start `claude` in `project/`, choose "Yes, I trust this folder", and run `/permissions` to see the rules as Claude Code reads them. Claude Code skips an MCP rule that has parentheses and warns about a rule with a `*` before the subcommand.

## Optional

In your own workspace: list the items with `fab ls <workspace>.Workspace`, with `fab api workspaces/<id>/items`, and, if you've registered the Fabric Core MCP server, through `list_items`. Compare all three with the item list in the portal.

- Fabric CLI: https://learn.microsoft.com/rest/api/fabric/articles/fabric-command-line-interface
- Core MCP tools: https://learn.microsoft.com/rest/api/fabric/articles/mcp-servers/core-remote/tools-core-mcp-server
- Permission rules: https://code.claude.com/docs/en/permissions
