# Exercise 6: notes for teachers

Expected results per step, and what varies. The participant's checklist is "What a good result looks like" in `../README.md`; this page adds what you see when you run it yourself. Tested with Claude Code v2.1.318 on Linux in manual mode; the auto mode results come from v2.1.319: steps 2 and 4 from video 6 take a3 (Opus) and an independent run with Haiku, step 8 from take af1 (Opus).

| Step | Fixed result (Claude Code or Git decides) | Varies (the model decides) |
|---|---|---|
| 1 | `git status`: only `notes.md` untracked; `git log --oneline`: one commit, `baseline` | – |
| 2 | auto mode: tool calls `Bash(…)` for `cp` and `sed`, one `Update(…)` for the notebook, no prompt; manual mode: prompts "Bash command" for `cp` and `sed`, one "Edit file" (read-only calls such as `git status` may run without one), and the transcript only shows "Ran 1 shell command"; `git status --short`: ` M clean_counts.py`, ` M daily_counts.Notebook/notebook-content.py`, `?? clean_counts.bak.py`, `?? notes.md` | whether Claude chains `ls` or `grep` into the `cp` call; whether it mentions that the notebook's code cell still uses the old column names (it did in all test runs) |
| 4 | list: `notebook-content.py +2 -2` (with the participant's own line; `+1 -1` without); confirmation "The code will be restored +2 -2 in notebook-content.py." and "⚠ Restored files go back whole, losing later changes by anyone. Bash changes to other files are not undone."; after "Restore code": ` M clean_counts.py`, `?? clean_counts.bak.py`, `?? notes.md`, own line gone | – |
| 5 | – | Claude's reason: in all local test runs (Opus and Haiku) it said something outside the session reverted the notebook ("a Fabric sync", "an editor reload"); in the Fabric runs it named the restore correctly |
| 6 | `git clean -n` lists `clean_counts.bak.py` and `notes.md`; at the end `git status --short` shows only `?? notes.md` | – |
| 8 | under the deploy prompt the rewind list says "No code changes"; after "Restore code" on the first prompt, `git status` is clean and `show.sh` still prints "Daily bike counts, Zurich"; after `./deploy.sh dev`, "Bike counts per day" | whether Claude runs `show.sh` on its own after the deploy; why two prompts: with edit and deploy in one prompt, the allowed deploy started while the edit prompt was still open (manual mode, takes f1 and f3) |
| 9 | `all checks passed` | – |

## What participants get stuck on

- **Trust dialog:** the preselected answer is "No, exit".
- **Grayed-out suggestion in the input:** after each answer, Claude Code may suggest a next prompt (seen: "redo the heading edit", "commit these changes"). Enter would send it, and a commit breaks the check. Type the next prompt over it.
- **The editor writes the file again:** if the editor still has the notebook open, it may save its own copy after the rewind, and the heading or the own line seems to come back. Close the editor before `/rewind`.
- **Claude can't find the notebook** (seen once with Haiku and an earlier prompt that didn't name the path: it searched for `*.ipynb` and proposed `find /`), **or uses Edit for `clean_counts.py`:** the point is lost. Start over with a fresh folder. The prompt now names the path.
- **macOS `sed`:** BSD `sed` needs `-i ''` and doesn't know `\b`; Opus wrote `\b` in several runs. If `clean_counts.py` isn't ` M` after step 2, the participant runs the `sed` from the README. Not tested on a Mac.
- **`git clean -f` without a file name:** deletes `notes.md` too. `check.py` reports it; write the note again.
- **Own line in `clean_counts.py` instead of the notebook:** then it stays after the rewind, because Claude never edited that file with its file tools. A good counter-example to discuss.
- **Windows:** start Claude Code from PowerShell; the project turns off the PowerShell tool so `cp` and `sed` run in Git Bash.

## Why the own line goes

The checkpoint holds the whole file as it was before the prompt. Once Claude has edited a file with its file tools, `/rewind` puts that file back whole, so every later change to it goes too: a `sed` from Claude, or a line from the participant (code.claude.com/docs/en/checkpointing, "Bash command changes not tracked", "External changes not tracked"). Older versions of Claude Code warned "Rewinding does not affect files edited manually or via bash"; v2.1.318 says "Restored files go back whole, losing later changes by anyone."

## Check the solution yourself

The files in this folder are one finished run: the filled-in `notes.md`; the files themselves are back at the baseline, which is what a fresh setup gives you. Put them into a fresh project and `check.py` prints "all checks passed"; on a fresh project without them, it fails. From the exercise folder, in Bash or Git Bash:

```
./setup.sh /var/tmp/06-solved
cp solution/notes.md /var/tmp/06-solved/
python3 check.py --project /var/tmp/06-solved
```

Use new folders each time; setup refuses a folder that already exists.
