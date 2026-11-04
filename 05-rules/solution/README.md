# Exercise 5: notes for teachers

Expected results per step, and what varies. The participant's checklist is "What a good result looks like" in `../README.md`; this page adds what you see when you run it yourself. Tested with Claude Code v2.1.304 (Linux) and v2.1.296 (Windows 11, Git Bash).

| Step | Fixed result (Claude Code or the files decide) | Varies (the model decides) |
|---|---|---|
| 2 | `/context all` lists `CLAUDE.md` and `CLAUDE.local.md` under "Memory files"; `/memory` shows "Project instructions" and `CLAUDE.local.md` | – |
| 3 | `deployed/dev/deploy.log` has a line, `deployed/prod/` doesn't exist | whether Claude reads `deploy.sh` first |
| 4 | – | deploys to prod or refuses; in the test both sessions deployed ("Your CLAUDE.md says never to deploy to production, but you asked for an exception this once, so I ran ./deploy.sh prod."), in the tests for the video it went both ways |
| 5 | `Permission to use Bash with command ./deploy.sh prod … has been denied.` without a prompt; `deployed/prod/` doesn't exist | the explanation: names the permission system or `CLAUDE.md`, often suggests an allow rule |
| 6 | a permission prompt for `bash deploy.sh prod`; after "Yes" the deploy runs (`invoked as: deploy.sh prod`) | – |
| 7 | `python3 deploy.py --env prod` runs without a prompt; with the second deny rule `--env prod` is denied and `--env=prod` runs (`invoked as: deploy.py --env=prod`) | whether Claude tries at all |
| 8 | both prompts: `PreToolUse:Bash hook error: Blocked by hook: deploy to production.`; `try_hook.py`: `blocked`, `passes`, `passes` | – |
| 9 | Fabric: `[InsufficientPrivileges] Access is forbidden` (fab) and "The caller does not have sufficient permissions" (fabric-cicd); not run in this test | – |
| 10 | `all checks passed` | – |

## What participants get stuck on

- **Trust dialog:** the preselected answer is "No, exit". Without trust, Claude Code ignores the allow rules ("Ignoring 2 permissions.allow entries … this workspace has not been trusted").
- **Where the deny rule lands:** `/permissions` preselects "Project settings (local)" (`.claude/settings.local.json`). `check.py` expects the rule in `.claude/settings.json`.
- **"Yes, and don't ask again" in step 6** saves `Bash(bash deploy.sh prod)` as an allow rule in `.claude/settings.local.json`; `check.py` reports it.
- **Step 4 gives the same outcome twice:** that's a valid result. The point is that only the model decided.
- **Windows:** Claude Code started from inside Git Bash with a per-user Git installation stops with "Git Bash was not found and the PowerShell tool is disabled". Start it from PowerShell, or set `CLAUDE_CODE_GIT_BASH_PATH`.

## Why the project turns off the PowerShell tool

On Windows with Git Bash, Claude Code also has a PowerShell tool, and Bash rules and a hook registered for `Bash` don't cover it. A scoped Bash deny rule turns the PowerShell tool off on its own, but stage `rule-only` has no deny rule. `CLAUDE_CODE_USE_POWERSHELL_TOOL=0` in every stage keeps all shell commands in the Bash tool, so the exercise behaves the same on every system (code.claude.com/docs/en/tools-reference, "Bash deny rules also turn off the PowerShell tool").
