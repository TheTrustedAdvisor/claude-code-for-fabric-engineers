# Claude Code for Fabric Engineers: exercises

Companion repo to the YouTube series "Claude Code for Fabric Engineers" by Matthias Falland. Each video ends with an exercise you can run on your own laptop, with a description of what a good result looks like, so you can check yourself.

The exercises run locally with fake deploy scripts. You need no Fabric capacity; only an optional last step uses real workspaces.

## Exercises

| Folder | Video | What you do |
|---|---|---|
| [05-rules/](05-rules/) | 5: CLAUDE.md vs deny rules: what stops a Fabric prod deploy? | Write checkable rules in `CLAUDE.md`, ask for the opposite, set deny rules, try a PreToolUse hook, and find where each layer stops |

More exercises follow with the next videos.

## What you need

- Claude Code, installed and signed in
- Bash and Python 3 as `python3` (on Windows: Git Bash, details in each exercise)

Start in the exercise's `README.md`. Each one has a setup script that creates a fresh project outside this repo, so you can start over at any time.

## License

MIT, see [LICENSE](LICENSE).
