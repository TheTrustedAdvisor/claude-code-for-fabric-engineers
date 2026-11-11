# Claude Code for Fabric Engineers: exercises

Companion repo to the YouTube series "Claude Code for Fabric Engineers" by Matthias Falland: Claude Code for people who build on Microsoft Fabric, one habit per part. Each part ends with an exercise you can run on your own laptop, with a description of what a good result looks like, so you can check yourself.

**Playlist:** [Claude Code for Fabric Engineers](https://www.youtube.com/playlist?list=PLe1Z-rZtBDSo)

The exercises run locally, with fake deploy scripts where a deploy is involved. You need no Fabric capacity; an optional step in each exercise uses a real workspace or model if you have one.

## Exercises

| Part | Video | Folder | What you do |
|---|---|---|---|
| 0 | Claude Code for Microsoft Fabric: setup, Desktop vs Code, the series | this repo | Clone it, ask Claude a question about it, change this README, and read the diff (see [Part 0](#part-0-a-first-real-task)) |
| 1 | Claude Code prompts: why two runs give two numbers | [01-variance/](01-variance/) | Ask the same question about open bike count data twice, find what Claude decided on its own, and write the decisions into the prompt until the number comes out the same every time |
| 2 | Reference documents: review a Fabric model by your team's rules | [02-reference/](02-reference/) | Review a semantic model in TMDL without and with your team's modeling guidelines, then change one rule and watch one finding change |
| 3 | Fabric reviews with Claude Code: who checks a reviewer subagent? | [03-reviewer/](03-reviewer/) | Judge a colleague's review yourself, run a read-only reviewer subagent after a conversation and fresh, and check one finding at the source |
| 4 | Claude Code harness: what runs besides the model? | [04-harness/](04-harness/) | Find out when a `CLAUDE.md` in a subfolder loads, load it from the start with an import, and name every part that runs besides the model |
| 5 | CLAUDE.md vs deny rules: what stops a Fabric prod deploy? | [05-rules/](05-rules/) | Write checkable rules in `CLAUDE.md`, ask for the opposite, set deny rules, try a PreToolUse hook, and find where each layer stops |
| 6 | Fabric undo with Claude Code: /rewind, Git and what neither covers | [06-undo/](06-undo/) | Let Claude change a Fabric notebook project three ways, rewind, and undo the rest with Git |
| 7 | Fabric handoff notes with Claude Code: continue without today's chat | [07-handoff/](07-handoff/) | Write a handoff note for a pipeline migration, test it with a fresh session, and continue the next morning from the note alone |

## Part 0: a first real task

Part 0 uses this repo for your first task with Claude Code:

1. Clone the repo, go into the folder and start Claude Code:

   ```
   git clone https://github.com/TheTrustedAdvisor/claude-code-for-fabric-engineers.git
   cd claude-code-for-fabric-engineers
   claude
   ```

   Claude Code asks whether you trust the folder; choose "Yes, I trust this folder".
2. Ask a question about the repo, without attaching a file:

   ```
   Which exercises in this repo need a Fabric workspace, and which run on my laptop alone? Answer with the folder names.
   ```

3. Ask for a small change:

   ```
   Add a column "Time" to the exercises table in README.md with the time each exercise takes, from each exercise's README.
   ```

4. Type `/diff` and read the change like a colleague's. Keep it with `git commit`, or throw it away with `git restore README.md`. Part 6 is all about undo.

## What you need

- Claude Code, installed and signed in (Part 0 shows how)
- Git, Bash and Python 3 as `python3` (on Windows: Git Bash, details in each exercise)

Start in the exercise's `README.md`. Each one has a setup script that creates a fresh project outside this repo, so you can start over at any time. `check.py` checks your result without Fabric, and `solution/` holds one finished run.

## License

MIT, see [LICENSE](LICENSE).
