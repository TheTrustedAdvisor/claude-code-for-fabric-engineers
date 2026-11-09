# Claude Code for Fabric Engineers: exercises

Companion repo to the YouTube series "Claude Code for Fabric Engineers" by Matthias Falland. Each video ends with an exercise you can run on your own laptop, with a description of what a good result looks like, so you can check yourself.

The exercises run locally with fake deploy scripts. You need no Fabric capacity; only an optional last step uses real workspaces.

## Exercises

| Folder | Video | What you do |
|---|---|---|
| [05-rules/](05-rules/) | 5: CLAUDE.md vs deny rules: what stops a Fabric prod deploy? | Write checkable rules in `CLAUDE.md`, ask for the opposite, set deny rules, try a PreToolUse hook, and find where each layer stops |

More exercises follow with the next videos.

### Series "Learning Claude for Microsoft Fabric" (TTA-210)

| Folder | Video | Status |
|---|---|---|
| [210-01-ways-in/](210-01-ways-in/) | Learning Claude for Microsoft Fabric, part 1: Fabric CLI, REST API or MCP server: which should Claude Code use? | in preparation |
| [210-02-identity/](210-02-identity/) | Learning Claude for Microsoft Fabric, part 2: Fabric identity for Claude Code: your account or a service principal? | in preparation |
| [210-03-guardrails/](210-03-guardrails/) | Learning Claude for Microsoft Fabric, part 3: Fabric guardrails for Claude Code: block a workspace, not a command | ready |
| [210-04-verify/](210-04-verify/) | Learning Claude for Microsoft Fabric, part 4: Fabric job Completed: did Claude Code really update the table? | ready |
| [210-05-notebook/](210-05-notebook/) | Learning Claude for Microsoft Fabric, part 5: Fabric notebook toolkit: can Claude Code debug a live Spark session? | in preparation |
| [210-06-git-deploy/](210-06-git-deploy/) | Learning Claude for Microsoft Fabric, part 6: Fabric Git integration: should Claude Code edit repo or workspace? | in preparation |
| [210-07-tmdl/](210-07-tmdl/) | Learning Claude for Microsoft Fabric, part 7: Fabric semantic models in TMDL: can you trust Claude Code's edits? | in preparation |
| [210-08-team-setup/](210-08-team-setup/) | Learning Claude for Microsoft Fabric, part 8: Fabric repo for a team: what belongs in CLAUDE.md, MCP and skills? | in preparation |

## What you need

- Claude Code, installed and signed in
- Bash and Python 3 as `python3` (on Windows: Git Bash, details in each exercise)

Start in the exercise's `README.md`. Each one has a setup script that creates a fresh project outside this repo, so you can start over at any time.

## License

MIT, see [LICENSE](LICENSE).
