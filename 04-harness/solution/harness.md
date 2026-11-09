# Harness

## When did notebooks/CLAUDE.md load?

| When | Under "Memory files"? | Claude names the time zone rule? |
|---|---|---|
| before the first prompt (step 2) | no | - |
| after step 3 | no | no |
| after reading the notebook (step 4) | no | yes |
| after /clear (step 4) | no | no |
| after the import (step 5) | yes | yes |

The rule came in when Claude read the notebook with the Read tool: right below "Read 1 file" the line "Loaded notebooks/CLAUDE.md" appeared.

## The parts besides the model

| Part | Comes from | Where I saw it |
|---|---|---|
| System prompt | Claude Code | /context all, only its size |
| Tools | Claude Code, MCP tools from my profile | /context all: System tools, MCP tools |
| CLAUDE.md | the project | /context all, Memory files; /memory |
| notebooks/CLAUDE.md | the project | the Loaded line; after the import in /context all |
| Agent definition | the project | /context all, Custom agents; .claude/agents/reviewer.md |
| Permissions | the project, .claude/settings.json | /permissions, Deny tab |
| Approval | me | the permission prompt for fab ls |

## What I check before the first prompt, and why

Before the first prompt I run /context all and look at Memory files, because a rule in a subfolder only counts once it is in the context.
